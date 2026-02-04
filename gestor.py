import psutil
import subprocess
import time

class GestorProcesos:
    """
    Clase central que interactúa con el Kernel del Sistema Operativo.
    Encapsula las funciones de administración de tareas.
    """

    def listar_procesos(self):
        """Retorna los primeros 15 procesos activos."""
        lista = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                lista.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return lista[:15]

    def monitorear_recursos(self):
        """Consulta CPU y RAM."""
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return {"cpu": cpu, "ram": ram}

    def iniciar_proceso(self, comando):
        try:
            proc = subprocess.Popen(comando, shell=True)
            return f"Exito: Proceso lanzado con PID {proc.pid}"
        except Exception as e:
            return f"Error al iniciar: {str(e)}"

    def detener_proceso(self, pid):
        try:
            proceso = psutil.Process(int(pid))
            proceso.terminate()
            proceso.wait(timeout=3)
            return f"Exito: Proceso {pid} terminado."
        except Exception as e:
            return f"Error: {e}"
