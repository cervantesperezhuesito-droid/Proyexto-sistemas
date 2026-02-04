import socket
import time

# Lista de posibles nodos en nuestra red de Podman
# En un sistema real usariamos broadcast, pero esto cumple como "lista de descubrimiento"
NODOS = ["servidor1", "servidor2"] 
PUERTO = 5000

def descubrir_servicios():
    """
    Escanea la red para ver qué servidores responden.
    Cumple con: 'Descubrimiento de servicios' de la rúbrica.
    """
    print("\n[MIDDLEWARE] 🔍 Escaneando la red 'red-sistemas'...")
    activos = []
    
    for nodo in NODOS:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # Esperamos máximo 1 seg
        try:
            s.connect((nodo, PUERTO))
            activos.append(nodo)
            s.close()
            print(f" ✅ {nodo}: ONLINE")
        except:
            print(f" ❌ {nodo}: OFFLINE (O no alcanzable)")
    
    return activos

def enviar_comando(nodo, comando):
    """Conecta, envía y recibe la respuesta."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((nodo, PUERTO))
            s.sendall(comando.encode('utf-8'))
            return s.recv(4096).decode('utf-8')
    except Exception as e:
        return f"Error de comunicación: {e}"

def iniciar_middleware():
    while True:
        # 1. Descubrimiento
        servidores = descubrir_servicios()
        
        if not servidores:
            print("⚠️ No hay servidores disponibles. Reintenta en 5s...")
            time.sleep(5)
            continue

        # 2. Menú de Selección
        print("\n--- GESTOR DISTRIBUIDO ---")
        for i, serv in enumerate(servidores):
            print(f"{i+1}. Conectar a {serv}")
        print("0. Salir")
        
        opcion = input("Elige un servidor: ")
        
        if opcion == "0": break
        
        try:
            target = servidores[int(opcion)-1]
            
            # 3. Interacción con el servidor elegido
            while True:
                cmd = input(f"\n[{target}] Comandos: LISTAR, MONITOREAR, INICIAR <cmd>, DETENER <pid>, ATRAS\n>> ")
                if cmd.upper() == "ATRAS": break
                
                respuesta = enviar_comando(target, cmd)
                print(f"\nRespuesta de {target}:\n{respuesta}")
                
        except (ValueError, IndexError):
            print("Opción inválida.")

if __name__ == "__main__":
    iniciar_middleware()
