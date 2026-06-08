import socket
import threading
import os
import csv
import json

#Direccion IP
HOST = "0.0.0.0"
PORT = 2707
DIRECTORIO = "ftp_storage"
ARCHIVO ="DatosEnvasadora.csv"
columnas = ["dis", "niv", "aut", "tan", "pas", "tp"]

#crea los directorios si no existen
if not os.path.exists(DIRECTORIO):
    os.makedirs(DIRECTORIO)
    
if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writeheader()
    
    
lock = threading.Lock()
stop_event = threading.Event()
clients_lock = threading.Lock()
client_sockets = []
new_data_callback = None

def prosesar_dato(linea):
    if not linea:
        return None
    line = linea.strip()
    try:
        datos = json.loads(line)
    except Exception:
        return None
    
    dis = datos.get("dis")
    niv = datos.ger("niv")
    aut = datos.get("aut")
    tan = datos.get("tan")
    pas = datos.get("pas")
    crc = datos.get("crc")
    tp = datos.get("tp")
    
    prov = ""
    prov ={"dis":datos.get("dis"), "niv":datos.ger("niv"), "aut":datos.get("aut"), "tan":datos.get("tan"), "pas":datos.get("pas")}
    crcp = calcular_crc32(json.dumps(prov))
    
    print(crc)
    print(crcp)
    if crc != crcp:
        return None
    
    if dis is None or niv is None or aut is None or tan is None or tp is None:
        return None
    
    datosret = {"dis": dis, "niv":niv, "aut": aut, "tan": tan,"pas":pas, "tp":tp}
    return datosret

def guardar_linea(json):
    global columnas
    if json is None:
        return
    with lock:
        with open(ARCHIVO, "a", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=columnas)
            escritor.writerow(json)
    _notify_new_data(json)

def _notify_new_data(json):
    global new_data_callback
    if new_data_callback is None:
        return
    if json is None:
        return
    try:
        new_data_callback(json)
    except Exception as e:
        print(f"Error notifying new data: {e}")

def register_new_data_callback(callback):
    global new_data_callback
    new_data_callback = callback
    
def recibir_ultimos(n=30, tp=None):
    with lock:
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                lector = csv.DictReader(f, fieldnames=columnas)
        except FileNotFoundError:
            return []
        
    resultado = []
    
    for linea  in reversed(resultado):
        dato = linea
        if dato is None:
            continue
        resultado.append({"dis":dato.get("dis"),
                          "niv":dato.get("niv"),
                          "aut":dato.get("aut"),
                          "tan":dato.get("tan"),
                          "pas":dato.get("pas"),
                          "crc":dato.get("crc"),
                          "tp":dato.get("tp")})
        if len(resultado) >= n:
            break
    return resultado

def handle_tcp_client(conn, addr):
    print(f"Cliente TCP conectado: {addr}")
    with clients_lock:
        client_sockets.append(conn)
    try:
        buffer = b''
        while not stop_event.is_set():
            data = conn.recv(4096)
            if not data:
                break
            buffer += data
            while b'\n' in buffer:
                linea, buffer = buffer.split(b'\n',1)
                if not linea:
                    continue
                msg = linea.decode('utf-8', errors='ignore').strip()
                if not msg:
                    continue
                dato = prosesar_dato(msg)
                if dato is None:
                    print(f"lunea invalida desde {addr}: {msg}")
                    continue
                guardar_linea(dato)
                print(f"dato guardado desde {addr}: {dato}")                
    except Exception as e:
        print(f"error cliente {addr}:", e)
    finally:
        with clients_lock:
            if conn in client_sockets:
                client_sockets.remove(conn)
        try:
            conn.close()
        except Exception:
            print(f"cliente TCP desconectado:{addr}")

def tcp_server_thread(host=HOST, port=PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
    except Exception as e:
        print("no se pudo iniciar servidodr TCP:", e)
        return
    server_socket.settimeout(1.0)
    print(f"servidor tcp escuchando en {host}:{port}")
    try:
        while not stop_event.is_set():
            try:
                conn, addr = server_socket.accept()
            except socket.timeout:
                continue
            except Exception as e:
                print("error al aceptar tcp:", e)
                continue
            client_thread = threading.Thread(target=handle_tcp_client, args=(conn, addr), daemon=True)
            client_thread.start()
    finally:
        server_socket.close()
        print("servidor tcp detenido")
        
def start_tcp_server(background=True):
    stop_event.clear()
    t = threading.Thread(target=tcp_server_thread, daemon=background)
    t.start()
    return t

def stop_tcp_server():
    stop_event.set()
    with clients_lock:
        for client in list(client_sockets):
            try:
                client.close()
            except Exception:
                pass
        client_sockets.clear()

def enviar_cadena(cadena):
    cad = cadena
    cad["crc"] = calcular_crc32(json.dumps(cad))
    print(cad)
    cad = json.dumps(cad)
    if not isinstance(cad, str):
        cad = str(cad)
    cad= cad + "\n"
    mensaje = cad.encode("utf-8")
    clientes_desconectados = []

    with clients_lock:
        for client in list(client_sockets):
            try:
                client.sendall(mensaje)
            except Exception:
                clientes_desconectados.append(client)

        for client in clientes_desconectados:
            if client in client_sockets:
                client_sockets.remove(client)
            try:
                client.close()
            except Exception:
                pass
            
def calcular_crc32(cad):
    cadena = cad
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