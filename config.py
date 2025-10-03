import os

DB = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''),   # XAMPP default: ''
    'db': os.getenv('DB_NAME', 'flask_laboratorio'),
    'charset': 'utf8mb4'
}

SECRET_KEY = os.getenv('SECRET_KEY', 'cambia_esto_por_una_clave_mas_segura')
