import pymysql
from werkzeug.security import generate_password_hash
from config import DB

def main():
    conn = pymysql.connect(host=DB['host'], port=DB['port'],
                           user=DB['user'], password=DB['password'],
                           charset=DB['charset'], cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit(True)
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB['db']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cur.execute(f"USE `{DB['db']}`;")
        cur.execute("""                    CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                rol ENUM('admin','usuario') NOT NULL DEFAULT 'usuario'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        admin_email = 'admin@example.com'
        cur.execute("SELECT id FROM usuarios WHERE email=%s", (admin_email,))
        if not cur.fetchone():
            hashed = generate_password_hash('1234')
            cur.execute("INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s,%s,%s,%s)",
                        ('Admin', admin_email, hashed, 'admin'))
            print("Admin creado: email=admin@example.com pass=1234")
        else:
            print("Admin ya existe.")
    conn.close()

if __name__ == '__main__':
    main()
