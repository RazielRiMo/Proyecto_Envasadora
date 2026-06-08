import uasyncio as asyncio #type: ignore
#lo que vendria siendo el freeRTOS
import bluetooth #type: ignore
from micropython import const #type: ignore 
import ujson as json #type: ignore
import uos #type: ignore
from machine import UART, I2C, Pin, RTC, PWM #type: ignore
import ssd1306
import network #type: ignore
import usocket #type: ignore
import utime #type: ignore

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

ble = bluetooth.BLE()
ble.active(True)
ble.config(gap_name="Puto el que se conecte")

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE,)
_UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY,)
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX,),)

services = (_UART_SERVICE,)
((tx, rx,),) = ble.gatts_register_services(services)
#tamaño del buffer de recepcion
ble.gatts_set_buffer(rx, 100)
#definir la interrupcion del bluetooth
while not ble.active():
    utime.sleep(1)
    print("Activando Bluetooth...")

def bt_irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        print("Central connected")
    elif event == _IRQ_CENTRAL_DISCONNECT:
        print("Central disconnected")
    if event == _IRQ_GATTS_WRITE:
        buffer = ble.gatts_read(rx).decode("utf-8").strip()
        print("Received:", buffer)

ble.irq(bt_irq)

def anunciar():
    payload = bytearray([2,1,6, len("puto el que se conecte") + 1, 9]) + "puto el que se conecte".encode("utf-8")
    ble.gap_advertise(100, payload)
    print("Anunciando Bluetooth...")
    

anunciar()

def enviar_alerta(alerta):
    men= "\n"
    mensaje = alerta
    if mensaje:
        mensaje = men + mensaje
        ble.gatts_notify(0, tx, mensaje.encode("utf-8"))


pin = 2
pwm = PWM(pin, freq=50, duty_u16=0)
wf = network.WLAN(network.STA_IF)
wf.active(True)
wf.connect("MigAn","Raziel-2707")
while not wf.isconnected():
    print("[Wifi] conectando")
    utime.sleep(1)
print("\nconectado:\n")
print(wf.ifconfig()[0])

SERVER_IP = "10.162.40.150"
SERVER_PORT = 2707
TP_ID = 1
s = None
socket_buf = bytearray()
uart_tx_queue = None

def connect_server():
    global s
    if s is not None:
        return True
    try:
        s = usocket.socket() #type: ignore
        s.connect((SERVER_IP, SERVER_PORT))
        s.setblocking(False)
        print(f"Conectado al servidor {SERVER_IP}:{SERVER_PORT}")
        return True
    except Exception as e:
        print("Error al conectar con el servidor:", e)
        try:
            s.close() #type: ignore
        except Exception:
            pass
        s = None
        return False

def procesar_linea_socket(linea):
    print("[TCP RX]", linea)
    try:
        obj = json.loads(linea)
        print("[TCP JSON]", obj)
        return obj
    except Exception:
        pass

async def enviar_socket_a_uart():
    global uart_tx_queue
    while True:
        if uart_tx_queue:
            linea = uart_tx_queue
            try:
                uart.write((linea + "\n").encode("utf-8"))
                print("[UART TX]", linea)
            except Exception as e:
                print("[UART] error enviando:", e)

        await asyncio.sleep_ms(10)

async def leer_socket():
    global s, socket_buf, uart_tx_queue
    while True:
        if s is None:
            connect_server()
            await asyncio.sleep_ms(1000)
            continue

        try:
            data = s.recv(128)
            if data:
                socket_buf.extend(data)
                while b"\n" in socket_buf:
                    idx = socket_buf.index(b"\n")
                    linea = bytes(socket_buf[:idx]).decode("utf-8", "ignore").strip()
                    socket_buf = socket_buf[idx + 1:]
                    if linea:
                        obj = procesar_linea_socket(linea)
                        if obj["niv"] == 1: #type: ignore
                            enviar_alerta("Nivel de agua bajo!")
                        uart_tx_queue = json.dumps(obj)
                        await enviar_socket_a_uart()
            elif data == b"":
                print("[TCP] servidor desconectado")
                try:
                    s.close()
                except Exception:
                    pass
                s = None
        except OSError:
            pass
        except Exception as e:
            print("[TCP] error leyendo:", e)
            try:
                s.close()
            except Exception:
                pass
            s = None

        await asyncio.sleep_ms(20)
    
#comunicacion UART
UART_ID = 2
UART_RX = 16
UART_TX = 17
UART_BAUD = 115200

#I2C del la pantalla
SCL = 22
SDA = 21
Wi = 128
H = 64

LOG = "/datalog.csv"

docj = {
    "dis": 0.0,
    "niv": 0,
    "aut": False,
    "tan": 0,
    "pas": 0,
    "crc": 0,
    "crcok": False,
    "ts": "---",
    "err": 0,
}

#iniciar hardware
uart = UART(UART_ID, baudrate=UART_BAUD, tx=Pin(UART_TX), rx=Pin(UART_RX))
i2c = I2C(0, scl=Pin(SCL), sda=Pin(SDA), freq=100_000)
oled = ssd1306.SSD1306_I2C(Wi, H, i2c)
rtc = RTC()

def calcular_crc32(cadena):
    crc = 0xFFFFFFFF

    for caracter in cadena:
        byte = ord(caracter)
        crc ^= byte

        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1

    return crc ^ 0xFFFFFFFF

def validar(raw: str):
    raw = raw.strip()
    try:
        obj = json.loads(raw)
        jsonstr = {"dis":obj.get("dis"), "niv": obj.get("niv"), "aut": obj.get("aut"), "niv": obj.get("niv"), "pas": obj.get("pas")}
        jsonstr = json.dumps(jsonstr)
        jsonstr = json.loads(jsonstr)
    except Exception:
        return None
    if "dis" not in obj or "niv" not in obj or "crc" not in obj:
        return None
    crcrecivido = obj["crc"]
    try:
        
        crccalculado = calcular_crc32(json.dumps(jsonstr))
        
    except Exception:
        return None
    if crccalculado != crcrecivido:
        return None  # CORRECCIÓN 1: Si el CRC falla, debe retornar None, no el objeto corrupto
    return obj

def gettimestamp() -> str:
    dt = rtc.datetime()
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[4], dt[5], dt[6])

def init_log():
    try:
        uos.stat(LOG)
        print("[LOG] ahi esta:", LOG)
    except OSError:
        with open(LOG, 'w') as f:
            f.write("dis,niv,aut,tan,pas,crc,tp\n")
        print("[LOG] creado:", LOG)

def guardarlog(dis: float, niv: int, aut: bool, tan: int, pas: int, crc:int, tp:str):
    try:
        with open(LOG, 'a') as f:
            f.write("{:.2},{},{},{},{},{},{}\n".format(dis,niv,aut,tan,pas,crc,tp)) # CORRECCIÓN 2: Se añadió \n para que el CSV no quede en una sola línea
    except Exception as e:
        print("error al guardar [LOG]:", e)
        
async def enviardato():
    global s
    if s is None:
        if not connect_server():
            return
    envio = {"tp": gettimestamp(), "dis": docj["dis"], "niv": docj["niv"], "aut": docj["aut"], "tan": docj["tan"], "pas": docj["pas"],  "crc": docj["crc"]}
    
    # CORRECCIÓN 3: Se cambió '>\\n' por '>\n' para que el servidor de PC reconozca el final de trama
    stringtosend = json.dumps(envio) + '\n' 
    
    try:
        s.send(stringtosend.encode('utf-8'))#type: ignore
    except Exception as e:
        print('Error enviando dato al servidor:', e)
        try:
            s.close()#type: ignore
        except Exception:
            pass
        s = None
    await asyncio.sleep_ms(50)

async def uartread():
    buf = bytearray()
    print("uart esperando al stm32")
    while(True):
        n = uart.any()
        if n:
            chunk = uart.read(n)
            if chunk:
                buf.extend(chunk)
                while b"\n" in buf:
                    idx = buf.index(b"\n")
                    linea = bytes(buf[:idx]).decode('ascii', 'ignore').strip()
                    buf = buf[idx+1:]
                    if not linea:
                        continue
                    obj = validar(linea)
                    
                    if obj is not None:
                        ts = gettimestamp()
                        docj["dis"] = obj["dis"]
                        docj["niv"] = obj["niv"]
                        docj["aut"] = obj["aut"]
                        docj["tan"] = obj["tan"]
                        docj["pas"] = obj["pas"]
                        docj["crc"] = obj["crc"]
                        docj["crcok"] = True # CORRECCIÓN 4: Restablecer estado OK para que la OLED no se quede en error
                        
                        guardarlog(obj["dis"], obj["niv"], obj["aut"], obj["tan"], obj["pas"],  obj["crc"], ts)
                        print("[OK] {} | dis={:.2f} niv={} aut={} tan={} pas={} crc={}, ts=".format(obj["dis"], obj["niv"], obj["aut"], obj["tan"], obj["pas"],  obj["crc"], ts))
                        await enviardato()
                    else:
                        docj["crcok"] = False
                        docj["err"] += 1
                        print("[ERR] linea corrupta #{}: {}".format(docj["err"], linea))
        await asyncio.sleep_ms(10)
    
async def oledrefres():
    while (True):
        try:
            oled.fill(0)
            oled.text("Envasadora",0 ,0)
            for x in range(128):
                oled.pixel(x, 10, 1)
            oled.text("dis:{:.1f}".format(docj["dis"]),0,14)
            
            oled.text("niv:{:.1f}".format(docj["niv"]),0,36)
            
            estado = "CRCOK" if docj["crcok"] else "CRCER"
            oled.text(estado, 0, 50)
            oled.text("Err:{}".format(docj["err"]), 72, 50)
            oled.show()
        except Exception as e:
            print("[OLED] error:", e)
            
        await asyncio.sleep_ms(250)
        
def pantalla_inicio():
    oled.fill(0)
    oled.text("Pr. Envasadora", 0, 0)
    oled.text("UD Fco. Caldas", 0, 12)
    for x in range(128):
        oled.pixel(x, 23, 1)
    oled.text("Pr. Finlar", 16, 28)
    oled.text("uasyncio v3", 20, 40)
    oled.text("Iniciando...", 24, 54)
    oled.show()
    
async def main():
    init_log()
    pantalla_inicio()
    await asyncio.sleep_ms(2000)
    
    await asyncio.gather(uartread(), oledrefres(), leer_socket())
    
asyncio.run(main())
