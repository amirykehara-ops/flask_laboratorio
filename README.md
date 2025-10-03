# Flask Laboratorio - Proyecto listo

## Requisitos
- XAMPP: Apache y MySQL ON.
- Python 3.8+ (tú indicastes 3.13.7 — perfecto).
- Crear y activar virtualenv.

## Pasos rápidos
1. Clona o extrae este proyecto.
2. Crea y activa virtualenv:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
3. Revisa `config.py` si necesitas cambiar credenciales (DB user/password).
4. Ejecuta para crear la base de datos y el admin:
   ```bash
   python create_db.py
   ```
   Credenciales por defecto: `admin@example.com` / `1234`
5. Ejecuta la app:
   ```bash
   python app.py
   ```
6. Abre `http://127.0.0.1:5000` y accede con las credenciales del admin.

## Estructura
- app.py
- create_db.py
- config.py
- templates/
- requirements.txt
