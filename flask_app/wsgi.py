from app import app

# Punto de entrada para Gunicorn
# Gunicorn busca el objeto 'application' en este archivo
application = app

if __name__ == "__main__":
    app.run()
