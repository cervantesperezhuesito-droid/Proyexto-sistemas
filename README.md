# Gestor de Procesos Distribuido (Sistema Operativo)

## 1. Objetivos del Proyecto
Diseñar e implementar un sistema distribuido cliente-servidor capaz de administrar procesos (listar, iniciar, detener, monitorear) en múltiples nodos remotos de forma centralizada, utilizando contenedores para simular un entorno distribuido.

## 2. Arquitectura del Sistema
El sistema sigue una arquitectura de **Middleware Centralizado**:
* **Nodos Servidores (Ubuntu/Podman):** Ejecutan el `servidor.py` que interactúa directamente con el Kernel de Linux usando `psutil`.
* **Middleware (Cliente Maestro):** Actúa como intermediario; descubre qué servidores están activos en la red y rutea los comandos del usuario.
* **Protocolo:** Comunicación vía Sockets TCP/IP crudos (Puerto 5000).
```mermaid
graph TD
    User((Usuario)) -->|Terminal| Client[Middleware / Cliente.py]
    
    subgraph Host: Fedora Linux
        Client
        
        subgraph "Red Virtual: red-sistemas (Podman)"
            S1[Contenedor: Servidor 1]
            S2[Contenedor: Servidor 2]
        end
    end
    
    Client -->|1. Descubrimiento TCP| S1
    Client -->|1. Descubrimiento TCP| S2
    
    Client -->|2. Envía Comando| S1
    Client -->|2. Envía Comando| S2
    
    S1 -->|psutil| Kernel[(Kernel Linux)]
    S2 -->|psutil| Kernel
´´´
## 3. Descripción de Módulos
* **`gestor.py`:** Clase `GestorProcesos`. Encapsula la lógica de sistema (uso de CPU, gestión de PIDs).
* **`servidor.py`:** Maneja la concurrencia con `threading` y expone las funciones del gestor a la red.
* **`middleware.py`:** Implementa el descubrimiento de servicios (Service Discovery) y la interfaz de usuario (CLI).
* **`Dockerfile`:** Define el entorno de ejecución virtualizado basado en Ubuntu.

## 4. Decisiones de Diseño
1.  **Uso de Contenedores (Podman) en lugar de Máquinas Virtuales:**
    * *Justificación:* Se eligió Podman por su arquitectura "daemonless" y la capacidad de gestionar redes ligeras sin la sobrecarga de recursos de una VM completa.
2.  **Comunicación vía Sockets TCP Crudos (en lugar de HTTP/REST):**
    * *Justificación:* Para cumplir con los requisitos de bajo nivel de la materia y tener control total sobre el flujo de bytes y el manejo de errores de conexión.

## 5. Desafíos y Soluciones
1.  **Bloqueo de archivos por SELinux en Fedora:**
    * *Problema:* Al montar el volumen con el código fuente, el contenedor arrojaba `Permission Denied` [Errno 13].
    * *Solución:* Se aplicó la etiqueta `:z` al volumen (`-v $(pwd):/app:z`) para instruir a SELinux que comparta el contexto de seguridad con el contenedor.
2.  **Descubrimiento de Servicios Dinámico:**
    * *Problema:* El cliente no sabía a qué IPs conectarse dentro de la red virtual.
    * *Solución:* Se implementó un escáner en `middleware.py` que itera sobre una lista de hostnames conocidos definidos en la red DNS interna de Podman.

## Instrucciones de Ejecución
1.  Construir imagen: `podman build -t imagen-servidor .`
2.  Crear red: `podman network create red-sistemas`
3.  Lanzar nodos: `podman run -d --network red-sistemas imagen-servidor`
4.  Ejecutar cliente: `python3 middleware.py` (dentro de la red).
