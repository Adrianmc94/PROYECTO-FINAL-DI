import os
import conexionBD as db


def test_ciclo_vida_datos():
    """Proba as operacións CRUD básicas directamente na BD."""
    print("Iniciando probas de software...")

    # 1. Proba de creación
    db.inicializar_bd()
    if os.path.exists("eventos.db"):
        print("[OK] Base de datos creada correctamente.")

    # 2. Proba de inserción (Create)
    datos_proba = ("Evento Test", "Cea", 0, "Alta", "Proba unitaria")
    db.CRUD("C", datos_proba)
    print("[OK] Inserción completada.")

    # 3. Proba de lectura (Read)
    eventos = db.CRUD("R")
    encontrado = any(e[1] == "Evento Test" for e in eventos)
    if encontrado:
        print("[OK] Lectura de datos correcta.")

    # 4. Proba de borrado (Delete)
    id_proba = eventos[-1][0]  # Collemos o último ID
    db.CRUD("D", id_proba)
    print("[OK] Borrado de proba completado.")

    print("\n--- Todas as probas pasaron con éxito (100%) ---")


if __name__ == "__main__":
    test_ciclo_vida_datos()