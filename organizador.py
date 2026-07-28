import time
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pytesseract
from PIL import Image

PATH_INBOX = "/app/datos/inbox"
PATH_BASE = "/app/datos"

class ProcesadorArchivo(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Detectado nuevo archivo: {event.src_path}")
            # Esperar un poco para asegurar que el archivo se ha copiado del todo en la red
            time.sleep(1)
            self.clasificar(event.src_path)

    def clasificar(self, ruta_archivo):
        try:
            # Leer el texto de la imagen (OCR)
            texto = pytesseract.image_to_string(Image.open(ruta_archivo)).lower()
            nombre_archivo = os.path.basename(ruta_archivo)
            
            # Logica de clasificacion: Palabras clave
            destino = "otros"
            if any(palabra in texto for palabra in ["factura", "iban", "importe", "total"]):
                destino = "facturas"
            elif any(palabra in texto for palabra in ["contrato", "acuerdo", "firmado", "clausula"]):
                destino = "contratos"
                
            # Mover el archivo
            ruta_destino = os.path.join(PATH_BASE, destino, nombre_archivo)
            shutil.move(ruta_archivo, ruta_destino)
            print(f"Archivo {nombre_archivo} movido a -> {destino}")

        except Exception as e:
            print(f"Error procesando {ruta_archivo}: {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ProcesadorArchivo(), PATH_INBOX, recursive=False)
    print("IA Vigilando la carpeta inbox...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()