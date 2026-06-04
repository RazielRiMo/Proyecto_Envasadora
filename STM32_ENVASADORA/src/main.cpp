//LIBRERIAS

#include <Arduino.h>
#include <ArduinoJson.h>//para los paquetes
#include <STM32FreeRTOS.h>
#include <task.h>
#include <semphr.h>
#include <HardwareSerial.h>
#include <timeLib.h>

//definiciones de pines

#define TRIGGER_PIN 6 //trigger del ultrasonido
#define ECHO_PIN 7 //echo del ultrasonido

#define NIV1 8 //nivel alto o lleno el tanque
#define NIV2 9 //nivel medio o seguro para sequir
#define NIV3 10 //nivel bajo o critico


//definicion de variables

#define muestrasprox 10 //tamaño de muestras de distancia

//declaracion de Comunicacion UART

HardwareSerial hserial(PA3, PA2);//PA3 RX, PA2 TX -----> para comunicacion con la esp

//tareas

void comunicacion(void *pvParameters); //comunica a la esp los datos actuales
void motor_cinta(void *pvParameters); //controla la velocidad del motor en la cinta

//tareas sensor de proximidad

void run_trigger(void *pvParameters); //dispara el trigger
void readUltrasonic(void *pvParameters); //calcula distancia y la envia a la cola
void run_timer(void *pvParameters); //empieza a contar para calcular distancia
void procesarprox(void *pvParameters); //recoge el dato de la cola y lo promedia

//interrupciones sensor de proximidad

void isr_echo(void);

//interrupciones sensor de nivel

void isr_sen(void);

//objetos

int crcal(String str);

//declaracion de estructura

struct sendata
{
  float dis;
  int velmot;
  int nivel;
};

//creacion del Json

JsonDocument datos;

//string que acompaña al json

String Jsonstr;

//declaracion de listas

QueueHandle_t senprox; //cola para promedio proximidad
QueueHandle_t proxref; //cola para proximidad refinada
QueueHandle_t nivref;  //cola para nivel refinado

//semaforos

SemaphoreHandle_t sem1, sem2, niv;

//variables proximidad

long timer, dis2;
bool echo_received = false, ena = false, arranque = false;
int dis = 0;

void setup() {

  //inicio del comunicacion UART

  hserial.begin(115200);

  //inicio De comunicacion PC

  Serial.begin(115200);

  //definicion de pines ultrasonido

  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  //definicion de pines nivel

  pinMode(NIV1, INPUT);
  pinMode(NIV2, INPUT);
  pinMode(NIV3, INPUT);

  //Wire.begin(); //descomentar si hay sensor i2c

  //inicializo el json

  datos["niv"] = 3;
  datos["prox"] = 0.0f;
  datos["vel"] = 0.0f;
  datos["pos"] = 0;
  datos["crc"] = 0;

  //configurar listas

  senprox = xQueueCreate(10, sizeof(long));
  proxref = xQueueCreate(1, sizeof(float));
  nivref = xQueueCreate(1, sizeof(float));

  //verificar la creacion de las listas

  configASSERT(senprox !=NULL);
  configASSERT(proxref !=NULL);
  configASSERT(nivref !=NULL);

  //definicion de semaforos ultrasonido

  sem1 = xSemaphoreCreateBinary();
  sem2 = xSemaphoreCreateBinary();

  //definicion de semaforos nivel

  niv = xSemaphoreCreateBinary();

  //se definen interrupciones ultrasonido

  attachInterrupt(digitalPinToInterrupt(ECHO_PIN), isr_echo, CHANGE);

  //definicion de interrupciones nivel cualquiera que cambie activa la interrupcion

  attachInterrupt(digitalPinToInterrupt(NIV1), isr_sen, CHANGE);
  attachInterrupt(digitalPinToInterrupt(NIV2), isr_sen, CHANGE);
  attachInterrupt(digitalPinToInterrupt(NIV3), isr_sen, CHANGE);

  //se definen las tareas

  //tareas sensor de proximidad

  xTaskCreate(run_trigger, "Trigger Task", 128, NULL, 4, NULL);
  xTaskCreate(readUltrasonic, "Read Ultrasonic Task", 128, NULL, 3, NULL);
  xTaskCreate(run_timer, "Run Timer", 128, NULL, 3, NULL);
  xTaskCreate(procesarprox, "proceso de proximidad", 128, NULL, 3, NULL);

  xTaskCreate(comunicacion, "comunicacion_UART", 256, NULL, 1, NULL);
  xTaskCreate(motor_cinta, "velocidad_cinta", 256, NULL, 4, NULL);
  
  //empezar tareas

  vTaskStartScheduler();
}

void loop() {
  // put your main code here, to run repeatedly:
}

//objetos realmente nesesarios

int crcal(String str){
  uint16_t crc = 0xFFFF;
  const uint16_t polynomial = 0x1021;

  for (size_t i = 0; i < str.length(); ++i) {
    uint8_t byte = static_cast<uint8_t>(str[i]);
    crc ^= static_cast<uint16_t>(byte) << 8;
    for (uint8_t bit = 0; bit < 8; ++bit) {
      if (crc & 0x8000) {
        crc = (crc << 1) ^ polynomial;
      } else {
        crc <<= 1;
      }
    }
  }

  return static_cast<int>(crc & 0xFFFF);
}

//tareas

//correr el trigger del sensor de proximidad

void run_trigger(void *pvParameters)
{
  while(1)
  {
    //limpio semaforos para evitar que se acumulen
    digitalWrite(TRIGGER_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_PIN, LOW);
    vTaskDelay(50 / portTICK_PERIOD_MS); // Esperar 1 segundo antes de la siguiente medición
  }
}

//interrupcion de cambio del sensor de proximidad

void isr_echo(void)
{ 
  //liberar el semaforo para que la tarea de lectura pueda calcular la distancia
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  if (digitalRead(ECHO_PIN) == LOW) {
    //limpia semaforo para evitar que se acumulen
    xSemaphoreGiveFromISR(sem1, &xHigherPriorityTaskWoken);
  }
  else {
    xSemaphoreGiveFromISR(sem2, &xHigherPriorityTaskWoken);
  }
  portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

//empezar a contar

void run_timer(void *pvParameters){
  while(1)
  {
    if((xSemaphoreTake(sem2, portMAX_DELAY) == pdTRUE) && !echo_received)
    {// Detener la interrupción para evitar interferencias
      echo_received = true;
      timer = micros();
       // Guardar el tiempo en que se recibe el pulso de echo// Volver a habilitar la interrupción para detectar el final del pulso de echo
    }
  }
}

//termina de contar y calcula distancia a la botella

void readUltrasonic(void *pvParameters)
{
  while(1)
  {
    if((xSemaphoreTake(sem1, portMAX_DELAY) == pdTRUE) && echo_received)
    {
      long duration = micros() - timer;
      echo_received = false; // Calcular la duración del pulso de echo
      long distance = (duration / 2) / 29.1;
      if (distance >= 400 || distance <= 2) {
        dis = 400;
      } else {
        xQueueSend(senprox, &distance, 0);
      }
    }
  }
}

//proceso de procesamiento del sensor de proximidad

void procesarprox(void *pvParameters){
  long buf[muestrasprox] = {0.0f};//buffer para poner los datos tomados
  int index = 0;//index que indica que dato borrar y cual reemplazar
  long sum = 0.0f;//variable para guardar la suma de todos los valores
  uint8_t cuenta = 0;//cuenta que sirve para saber 
  long distance;
  while(1){
    if(xQueueReceive(senprox, &distance, portMAX_DELAY) == pdTRUE){
      sum -= buf[index];
      buf[index] = distance;
      sum += buf[index];
      index = (uint8_t)((index +1) % muestrasprox);
      if (cuenta < muestrasprox) cuenta++;
      float promedio = roundf((float)sum / (float)muestrasprox);
      float basura;
      xQueueReceive(proxref, &basura, 0);
      xQueueSend(proxref, &promedio, 0);
    }
  }
}

//interrupcion actualizacion de nivel de agua

void isr_sen(void){
  //liberar el semaforo para que la tarea de lectura pueda calcular el nivel del agua
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  ena = true;
  xSemaphoreGiveFromISR(niv, &xHigherPriorityTaskWoken);
  portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

//tarea para calcular el nivel del agua
void run_timer(void *pvParameters){
  int pos = 3;
  while(1)
  {
    if((xSemaphoreTake(niv, portMAX_DELAY) == pdTRUE) && !ena){
      if (digitalRead(NIV3) == LOW) {
        pos = 3;
      } else if (digitalRead(NIV2) == LOW) {
        pos = 2;
      } else if (digitalRead(NIV1) == LOW) {
        pos = 1;
      }
      
      int basura;
      xQueueReceive(nivref, &basura, 0);
      xQueueSend(nivref, &pos, 0);
    }
  }
}
