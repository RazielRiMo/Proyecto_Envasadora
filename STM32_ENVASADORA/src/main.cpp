//LIBRERIAS
#include <Arduino.h>
#include <ArduinoJson.h>
#include <STM32FreeRTOS.h>
#include <task.h>
#include <semphr.h>
#include <HardwareSerial.h>

//declaracion de Comunicacion UART

HardwareSerial hserial(PA3, PA2);//PA3 RX, PA2 TX

//tareas
void sensor_prox(void *pvParameters);
void sensor_nivel(void *pvParameters);
void comunicacion(void *pvParameters);
void motor_cinta(void *pvParameters);

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
QueueHandle_t senniv;  //cola para promedio nivel
QueueHandle_t proxref; //cola para proximidad refinada
QueueHandle_t nivref;  //cola para nivel refinado


void setup() {

  //inicio del comunicacion UART

  hserial.begin(115200);

  //inicio De comunicacion PC

  Serial.begin(115200);

  //Wire.begin(); //descomentar si hay sensor i2c

  //inicializo el json

  datos["niv"] = 0.0f;
  datos["prox"] = 0.0f;
  datos["vel"] = 0.0f;
  datos["pos"] = 0;
  datos["crc"] = 0;

  //configurar listas

  senprox = xQueueCreate(10, sizeof(float));
  senniv = xQueueCreate(10, sizeof(float));
  proxref = xQueueCreate(1, sizeof(float));
  nivref = xQueueCreate(1, sizeof(float));

  //verificar la creacion de las listas

  configASSERT(senprox !=NULL);
  configASSERT(senniv !=NULL);
  configASSERT(proxref !=NULL);
  configASSERT(nivref !=NULL);

  //se definen las tareas

  xTaskCreate(sensor_prox,"posicion-botella", 256, NULL, 3, NULL);
  xTaskCreate(sensor_nivel, "comprobacion-nivel", 256, NULL, 2,NULL);
  xTaskCreate(comunicacion, "comunicacion_UART", 256, NULL, 1, NULL);
  xTaskCreate(motor_cinta, "velocidad_cinta", 256, NULL, 4, NULL);
  vTaskStartScheduler();
}

void loop() {
  // put your main code here, to run repeatedly:
}
