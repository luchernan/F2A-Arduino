# F2A - Sistema de Control de Acceso IoT con Enfoque en Ciberseguridad

![Versión](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.12-green)
![Django](https://img.shields.io/badge/Django-5.0-df3b3b)
![Arduino](https://img.shields.io/badge/Arduino-IDE-00979D)

## 📌 Descripción del Proyecto
**F2A** es un sistema integral de control de acceso que fusiona hardware (Arduino), comunicaciones seriales (Python Bridge) y desarrollo web (Django). Fue desarrollado como una práctica avanzada para explorar la interacción entre dispositivos IoT y aplicaciones web, con un fuerte énfasis en la **seguridad de la información** y la gestión de sesiones.

El sistema permite validar la identidad de un usuario mediante tarjetas RFID físicas o simuladas, procesar la autorización en un backend centralizado y reflejar el resultado instantáneamente tanto en hardware como en una interfaz web dinámica.

---

## 🏗️ Arquitectura del Sistema
El flujo de datos sigue un ciclo de 4 capas:
1.  **Capa Física (Arduino + MFRC522):** Captura el UID de la tarjeta y lo transmite por Serial.
2.  **Capa de Enlace (Python Bridge):** Actúa como middleware traduciendo datos Serial a peticiones HTTP JSON.
3.  **Capa de Lógica (Django REST API):** Valida los permisos en la base de datos y gestiona el historial de accesos.
4.  **Capa de Presentación (Web Frontend):** Interfaz futurista que reacciona en tiempo real mediante *polling* y gestión de sesiones.

---

## 🚀 Características Principales

### 🛠️ Hardware (Arduino)
- Lectura real mediante sensor **RFID-RC522**.
- Feedback visual en tiempo real con **Pantalla LCD I2C 16x2**.
- Indicadores de estado mediante **LEDs (Verde/Rojo)**.
- Comunicación bidireccional mediante protocolo Serial.

### 💻 Backend & API (Django)
- **REST API:** Endpoints especializados para validación y chequeo de estado.
- **Base de Datos:** Modelos para `CardUser` (usuarios autorizados) y `AccessLog` (auditoría).
- **Session Management:** Implementación de sesiones seguras para evitar bypass manual de URLs.

### 🌐 Frontend (Cyberpunk UI)
- Diseño responsivo con estética moderna (Dark mode, gradientes neón).
- Redirección inteligente basada en estado de sesión.
- Feedback de errores ("Acceso Denegado") integrado en la UI sin recarga de página.

---

## 🛡️ Enfoque en Ciberseguridad
Este proyecto sirve para demostrar y mitigar vulnerabilidades comunes en sistemas IoT:

- **Validación de Sesiones:** Se implementó una lógica donde el Dashboard no puede ser accedido simplemente escribiendo la URL; requiere un evento físico de validación previo vinculado a la sesión del navegador.
- **Auditoría (Logging):** Cada intento de acceso (exitoso o fallido) queda registrado con marca de tiempo y UID, esencial para análisis forense.
- **Seguridad en Comunicaciones:** Análisis de los riesgos de enviar UIDs planos por Serial y discusión sobre la implementación de Tokens (JWT) para proteger la API.
- **Aislamiento de Lógica:** La decisión de "quién entra" no se toma en el Arduino (fácil de manipular), sino en el servidor seguro.

---

## 🛠️ Instalación y Configuración

### 1. Arduino
1. Instala la librería `MFRC522` y `LiquidCrystal I2C`.
2. Carga `arduino/F2A/F2A.ino` en tu placa (Arduino Nano/Uno).
3. Conexión de pines:
   - SDA: 10, RST: 9, SCK: 13, MOSI: 11, MISO: 12.
   - LCD: SDA/SCL a pines A4/A5.

### 2. Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # O venv\Scripts\activate en Windows
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py runserver
```

### 3. Python Serial Bridge
```bash
cd serial
pip install pyserial requests
python serial_service.py
```

---

## 📖 Cómo Funciona (Paso a Paso)
1. El usuario pasa su tarjeta RFID.
2. El Arduino lee el UID y lo envía al puerto Serial.
3. El script de Python capta el UID y hace un `POST` a `/api/rfid/validate/`.
4. Django verifica el UID, guarda el log y responde `OK` o `DENY`.
5. El script de Python reenvía la respuesta al Arduino.
6. El Arduino activa el LED/LCD correspondiente.
7. Simultáneamente, la web detecta el acceso exitoso y redirige al usuario al área privada.

---

## 📝 Licencia
Este proyecto es de uso educativo para prácticas de desarrollo web y ciberseguridad.


