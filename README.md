# 🧠 Smart NAS con Clasificación Documental por IA (Docker & OCR)

> **Proyecto de Infraestructura Contenerizada y Automatización (ASIR)**  
> **Autor:** Adahi Sánchez Gómez  
> **Tecnologías:** Docker, Docker Compose, Linux (Ubuntu), Samba, Python, Tesseract OCR.  

---

## 📋 Descripción del Proyecto
Despliegue de un Servidor de Almacenamiento en Red (NAS) orquestado mediante contenedores Docker, integrado con un motor de Inteligencia Artificial de Reconocimiento Óptico de Caracteres (OCR). 

El sistema actúa como un *Smart Storage*: vigila un volumen de red (inbox) en tiempo real, extrae el texto de las imágenes (facturas, contratos, etc.) mediante IA, y orquesta el movimiento automatizado de los archivos hacia sus directorios correspondientes según reglas de negocio.

---

## 🚀 Arquitectura y Componentes del Sistema

El proyecto se despliega mediante `docker-compose` orquestando dos microservicios interconectados mediante volúmenes compartidos:

### 1. Servicio NAS (Samba Container)
* **Imagen:** `dperson/samba`
* **Funcionalidad:** Servidor de archivos accesible en red local (Puertos 139/445). Configurado con control de acceso por credenciales y mapeo de volúmenes persistentes (`./datos:/mnt/nas`).

### 2. Motor de Inteligencia Artificial (AI Brain Container)
* **Imagen Personalizada (Dockerfile):** Construida sobre `python:3.9-slim`.
* **Motor OCR:** Integración de Tesseract OCR a nivel de sistema operativo para el reconocimiento de texto en español.
* **Lógica de Automatización (Python):** 
  * `watchdog`: Monitorización de eventos del sistema de archivos en tiempo real.
  * `pytesseract`: Extracción de strings desde los archivos entrantes.
  * Lógica de clasificación: Búsqueda de keywords ("factura", "contrato") y enrutado automático (`shutil`).

---

## 🛠️ Despliegue y Troubleshooting Destacado
* **Gestión de Permisos (Linux/Samba):** Resolución de conflictos de acceso y variables de entorno aplicando control de propiedad (`chown`) y políticas `smbpasswd`.
* **Gestión de Red Docker:** Resolución de conflictos de puertos y nombres de contenedores mediante limpieza de stack (`docker-compose down / rm -f`).
* **Debugging en Tiempo Real:** Optimización del contenedor Python configurando la salida de logs sin búfer (`python -u`) para monitorizar los eventos del demonio `watchdog` en vivo (`docker logs -f`).

---

## 📁 Estructura del Repositorio
* `docker-compose.yml`: Archivo de orquestación de la arquitectura.
* `Dockerfile`: Receta de construcción de la imagen del motor IA.
* `organizador.py`: Código fuente del demonio de clasificación en Python.
* **Documentación PDF:** Memoria técnica completa con evidencias gráficas del funcionamiento, despliegue y resolución de problemas (troubleshooting) paso a paso.
