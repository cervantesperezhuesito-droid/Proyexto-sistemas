import socket

HOST = '127.0.0.1'  # IP local (localhost)
PORT = 5000         # El mismo puerto del servidor

def iniciar_cliente():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        print(f"[CONECTADO] Servidor en {HOST}:{PORT}")
        print("Comandos disponibles: LISTAR, MONITOREAR, INICIAR <cmd>, DETENER <pid>, SALIR")

        while True:
            mensaje = input("\nTu comando >> ")
            
            if mensaje.upper() == "SALIR":
                break
            
            # Enviar datos
            cliente.send(mensaje.encode('utf-8'))

            # Recibir respuesta (hasta 4096 bytes)
            respuesta = cliente.recv(4096).decode('utf-8')
            print(f"--- Respuesta ---\n{respuesta}")

    except ConnectionRefusedError:
        print("❌ Error: No se pudo conectar. ¿El servidor está encendido?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    iniciar_cliente()
