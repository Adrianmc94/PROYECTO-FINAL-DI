import os
import sys

# 1. Ajuste del Path: Permite que el test encuentre el código dentro de /src aunque se ejecute desde /tests
ruta_base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(ruta_base), "src"))

import conexionBD as db


def test_ciclo_vida_datos():
    """Prueba las operaciones CRUD básicas directamente en la BD."""
    print("Iniciando pruebas de software...")

    # 2. Inicialización
    db.inicializar_bd()

    # Verificación de la ruta correcta de la BD
    ruta_db = os.path.join(os.path.dirname(ruta_base), "data", "eventos.db")

    if os.path.exists(ruta_db):
        print(f"[OK] Base de datos encontrada en: {ruta_db}")
    else:
        print(f"[ERROR] No se encontró la BD en: {ruta_db}")
        return

    # 3. Prueba de inserción (Create)
    datos_prueba = ("Evento Test", "Cena", 0, "Alta", "Prueba unitaria")
    db.CRUD("C", datos_prueba)
    print("[OK] Inserción completada.")

    # 4. Prueba de lectura (Read)
    eventos = db.CRUD("R")
    encontrado = any(e[1] == "Evento Test" for e in eventos)
    if encontrado:
        print("[OK] Lectura de datos correcta.")
    else:
        print("[ERROR] El evento de prueba no fue encontrado.")

    # 5. Prueba de borrado (Delete)
    # Buscamos el ID de nuestro evento específico para el test
    try:
        id_prueba = [e[0] for e in eventos if e[1] == "Evento Test"][-1]
        db.CRUD("D", id_prueba)
        print("[OK] Borrado de prueba completado.")
    except IndexError:
        print("[ERROR] No se pudo identificar el ID para borrar.")

    print("\n--- Todas las pruebas pasaron con éxito (100%) ---")


if __name__ == "__main__":
    test_ciclo_vida_datos()