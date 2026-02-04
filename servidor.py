import socket
import threading
from gestor import GestorProcesos

HOST = '0.0.0.0'  # Escucha en todo el mundo (necesario para Podman)
PORT = 5000

def manejar_cliente(conn, addr):
    print(f"[CONECTADO] {addr}")
    gestor = GestorProcesos()
    
    try:
        while True:
            datos = conn.recv(1024).decode('utf-8')
            if not datos: break
            
            # Protocolo simple: "COMANDO argumento"
            partes = datos.split(" ", 1)
            cmd = partes[0].upper()
            arg = partes[1] if len(partes) > 1 else ""
            
            resp = "Comando desconocido"
            
            if cmd == "LISTAR":
                # Convertimos la lista a string
                lista = gestor.listar_procesos()
                resp = "\n".join([f"{p['pid']} - {p['name']}" for p in lista])
            elif cmd == "MONITOREAR":
                resp = str(gestor.monitorear_recursos())
            elif cmd == "INICIAR":
                resp = gestor.iniciar_proceso(arg) if arg else "Falta argumento"
            elif cmd == "DETENER":
                resp = gestor.detener_proceso(arg) if arg.isdigit() else "PID debe ser numero"
                
            conn.send(resp.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def iniciar():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVIDOR] Escuchando en {PORT}...")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    iniciar()
