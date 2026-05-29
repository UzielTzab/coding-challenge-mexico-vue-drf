# DEPLOYMENT.md

# Despliegue oficial — ArbiBTC

Este documento define el despliegue oficial del sistema ArbiBTC.

Frontend:

```txt
AWS Amplify
```

Backend:

```txt
AWS EC2
```

Base de datos:

```txt
Neon PostgreSQL
```

---

## 1. Variables de entorno backend

Archivo:

```txt
backend/.env
```

Variables:

```env
DJANGO_SECRET_KEY=
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=
DATABASE_URL=
CORS_ALLOWED_ORIGINS=
CSRF_TRUSTED_ORIGINS=
DJANGO_SETTINGS_MODULE=config.settings
```

Para WebSocket:

```env
ASGI_APPLICATION=config.asgi.application
```

---

## 2. Variables de entorno frontend

Archivo local:

```txt
frontend/.env
```

Variables:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
```

Producción en AWS Amplify:

```env
VITE_API_BASE_URL=https://<backend-domain>/api
VITE_WS_BASE_URL=wss://<backend-domain>/ws
```

---

## 3. Base de datos Neon

La base de datos oficial es PostgreSQL en Neon.

El backend se conecta mediante `DATABASE_URL`.

Formato:

```txt
postgresql://user:password@host/dbname?sslmode=require
```

Reglas:

- No subir credenciales al repositorio.
- Usar `.env.example` sin valores sensibles.
- Ejecutar migraciones en producción después de configurar variables.

---

## 4. Backend en EC2

Servidor oficial:

```txt
Ubuntu EC2
```

Paquetes requeridos:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip nginx git -y
```

Clonar repo:

```bash
git clone <repo-url>
cd CODING_CHALLENGE_MEXICO/backend
```

Crear entorno:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Migraciones:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Seed demo:

```bash
python manage.py seed_demo
```

---

## 5. Servidor ASGI

Como el backend usa WebSockets, el servidor debe correr ASGI.

Comando recomendado:

```bash
uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

Para producción, se gestiona con `systemd`.

Archivo:

```txt
/etc/systemd/system/arbibtc.service
```

Ejemplo:

```ini
[Unit]
Description=ArbiBTC ASGI Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/CODING_CHALLENGE_MEXICO/backend
EnvironmentFile=/home/ubuntu/CODING_CHALLENGE_MEXICO/backend/.env
ExecStart=/home/ubuntu/CODING_CHALLENGE_MEXICO/backend/venv/bin/uvicorn config.asgi:application --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable arbibtc
sudo systemctl start arbibtc
sudo systemctl status arbibtc
```

---

## 6. Nginx

Archivo:

```txt
/etc/nginx/sites-available/arbibtc
```

Configuración base:

```nginx
server {
    listen 80;
    server_name <backend-domain>;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar:

```bash
sudo ln -s /etc/nginx/sites-available/arbibtc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 7. Frontend en AWS Amplify

Archivo raíz:

```txt
amplify.yml
```

Contenido oficial:

```yaml
version: 1
applications:
  - appRoot: frontend
    frontend:
      phases:
        preBuild:
          commands:
            - npm ci
        build:
          commands:
            - npm run build
      artifacts:
        baseDirectory: dist
        files:
          - '**/*'
      cache:
        paths:
          - node_modules/**/*
```

---

## 8. CORS y CSRF

Backend debe permitir el dominio de Amplify.

Ejemplo:

```env
CORS_ALLOWED_ORIGINS=https://<amplify-domain>
CSRF_TRUSTED_ORIGINS=https://<amplify-domain>
```

---

## 9. Checklist deploy backend

- Variables `.env` configuradas.
- Neon conectado.
- Migraciones ejecutadas.
- Seed demo ejecutado.
- ASGI corriendo.
- Nginx proxy funcionando.
- `/api/health/` responde.
- `/ws/dashboard/` acepta conexión.

---

## 10. Checklist deploy frontend

- Variables `VITE_API_BASE_URL` y `VITE_WS_BASE_URL` configuradas.
- Build exitoso en Amplify.
- Dashboard carga datos de API.
- WebSocket conecta en producción.
- No existen URLs hardcodeadas a localhost.

---

## 11. Criterio de entrega

La entrega se considera lista cuando:

- Existe URL pública del frontend.
- Existe backend accesible públicamente.
- El dashboard muestra datos.
- Los WebSockets funcionan.
- El README incluye instrucciones de ejecución y arquitectura.
- No hay secretos en el repositorio.
