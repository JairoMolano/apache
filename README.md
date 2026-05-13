# Práctica Servidor Web Linux — Flask + Gunicorn + Apache + Docker

## Arquitectura

```
Tu navegador (Windows)
        │  HTTP :80
        ▼
  ┌─────────────┐
  │   Apache    │  ← Reverse Proxy (contenedor srv_apache)
  │   httpd:2.4 │
  └──────┬──────┘
         │  HTTP interno :5000
         ▼
  ┌─────────────┐
  │  Gunicorn   │  ← Servidor WSGI (contenedor srv_flask)
  │  + Flask    │
  └─────────────┘
```

**Flujo de una solicitud:**
`Browser → Apache :80 → Gunicorn :5000 → Flask app → HTML → de vuelta`

---

## Árbol del proyecto

```
practica-web/
├── docker-compose.yml          ← Orquesta los dos contenedores
├── flask_app/
│   ├── Dockerfile              ← Imagen Python + Gunicorn
│   ├── requirements.txt        ← Flask + Gunicorn
│   ├── wsgi.py                 ← Punto de entrada WSGI
│   ├── app.py                  ← Aplicación Flask
│   └── templates/
│       └── index.html          ← Página web
└── apache/
    ├── Dockerfile              ← Imagen Apache con proxy activado
    └── miaplicacion.conf       ← Virtual host (reverse proxy)
```

---

## Comandos esenciales (copiar y pegar)

### Levantar el proyecto
```bash
cd practica-web
docker compose up -d
```

### Ver que todo está corriendo
```bash
docker compose ps
```

### Ver logs en tiempo real
```bash
# Todos los servicios
docker compose logs -f

# Solo Apache
docker compose logs -f apache

# Solo Flask/Gunicorn
docker compose logs -f flask
```

### Entrar al contenedor de Flask
```bash
docker exec -it srv_flask bash
```

### Entrar al contenedor de Apache
```bash
docker exec -it srv_apache bash
```

### Reconstruir contenedores (tras cambios en Dockerfile o requirements)
```bash
docker compose down
docker compose up -d --build
```

### Reiniciar servicios (sin reconstruir)
```bash
docker compose restart
```

### Detener todo
```bash
docker compose down
```

---

## Flujo de trabajo con VS Code

1. Conectarse a la VM por SSH Remote (VS Code)
2. Abrir la carpeta `practica-web/`
3. Editar `flask_app/app.py` o `flask_app/templates/index.html`
4. El bind mount hace que los cambios lleguen al contenedor automáticamente
5. Para que Gunicorn los aplique, reiniciar solo Flask:
   ```bash
   docker compose restart flask
   ```
6. Refrescar el browser → cambios visibles

---

## Validaciones para demostrar al profesor

### ✅ 1. Apache responde desde otra máquina
```bash
# Desde Windows (PowerShell) — reemplazar IP_DE_LA_VM
curl http://IP_DE_LA_VM
# O simplemente abrir el browser en http://IP_DE_LA_VM
```

### ✅ 2. Verificar que Apache está corriendo
```bash
docker exec srv_apache apachectl -t        # Verifica sintaxis de config
docker exec srv_apache apachectl status    # Estado del servicio
```

### ✅ 3. Verificar que Gunicorn está corriendo
```bash
# Ver el proceso dentro del contenedor
docker exec srv_flask ps aux
# Debe mostrar: gunicorn master + workers
```

### ✅ 4. Verificar la configuración de Apache
```bash
docker exec srv_apache cat /usr/local/apache2/conf/extra/miaplicacion.conf
```

### ✅ 5. Probar Flask directamente (sin Apache)
```bash
# Desde dentro de la VM — Flask escucha internamente en :5000
# pero NO está expuesto al exterior (solo Apache en :80 lo está)
docker exec srv_flask curl http://localhost:5000/salud
# Respuesta esperada: {"estado": "ok", "mensaje": "Servidor Flask operativo"}
```

### ✅ 6. Ver la red interna entre contenedores
```bash
docker network ls
docker network inspect practica-web_red_practica
```

### ✅ 7. Ver los archivos de configuración
```bash
# wsgi.py
docker exec srv_flask cat /app/wsgi.py

# app.py
docker exec srv_flask cat /app/app.py

# Configuración Apache
docker exec srv_apache cat /usr/local/apache2/conf/extra/miaplicacion.conf
```

---

## Preguntas frecuentes del profesor

**¿Por qué usamos Gunicorn?**
Flask tiene un servidor de desarrollo integrado que NO es adecuado para producción (un solo hilo, sin manejo de concurrencia). Gunicorn es un servidor WSGI de producción que puede manejar múltiples solicitudes simultáneas.

**¿Por qué usamos Apache como proxy inverso?**
Apache gestiona las conexiones HTTP del exterior, aplica seguridad, puede servir archivos estáticos y delega las solicitudes dinámicas a Gunicorn. Esto separa responsabilidades.

**¿Qué es WSGI?**
Web Server Gateway Interface — es la interfaz estándar de Python entre servidores web (Apache/Nginx) y aplicaciones web (Flask/Django). Gunicorn implementa WSGI.

**¿Por qué Docker y no instalación directa?**
Docker aísla el entorno, evita conflictos de versiones, es reproducible en cualquier máquina y permite levantar/bajar servicios en segundos.
