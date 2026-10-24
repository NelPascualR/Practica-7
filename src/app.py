
import os
import time

import mysql.connector
from flask import Flask

app = Flask(__name__)


def conectar_mysql():
    for intento in range(30):
        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER", "appuser"),
                password=os.getenv("DB_PASSWORD", "app123"),
                database=os.getenv("DB_NAME", "holamundo"),
                port=3306
            )

            return conexion

        except mysql.connector.Error as error:
            print(f"Esperando a MySQL: {error}")
            time.sleep(2)

    return None


@app.route("/")
def inicio():
    conexion = conectar_mysql()

    if conexion is None:
        return """
        <h1>Hola Mundo</h1>
        <p>No se pudo conectar con MySQL.</p>
        """, 503

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]

        cursor.close()

        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Práctica 7 - Hola Mundo</title>
        </head>
        <body>
            <h1>¡Hola Mundo!</h1>
            <p>Aplicación web ejecutada correctamente con Docker.</p>
            <p>Conexión a MySQL: exitosa.</p>
            <p>Versión de MySQL: {version}</p>
        </body>
        </html>
        """

    finally:
        conexion.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
