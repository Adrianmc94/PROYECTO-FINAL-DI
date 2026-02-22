import os
import sqlite3


def conectar():
    """Establece conexión con el motor SQLite."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(base_dir), "data", "eventos.db")
    return sqlite3.connect(db_path)


def inicializar_bd():
    """
    Crea la estructura de tablas necesaria para el despliegue inicial.
    Verifica la existencia de la tabla 'eventos' y sus campos.
    """
    with conectar() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS eventos
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           nome
                           TEXT
                           NOT
                           NULL,
                           tipo
                           TEXT,
                           catering
                           INTEGER,
                           prioridade
                           TEXT,
                           notas
                           TEXT
                       )""")


def CRUD(operacion, datos=None):
    """
    Fachada para las operaciones de persistencia.

    :param operacion: Carácter 'C', 'R', 'U' o 'D' según la acción requerida.
    :param datos: Tupla de datos para operaciones de escritura/actualización.
    :return: Lista de registros en caso de operación 'R'.
    """
    with conectar() as con:
        cur = con.cursor()
        if operacion == "C":
            cur.execute("INSERT INTO eventos (nome, tipo, catering, prioridade, notas) VALUES (?,?,?,?,?)", datos)
        elif operacion == "R":
            return cur.execute("SELECT * FROM eventos").fetchall()
        elif operacion == "U":
            cur.execute("UPDATE eventos SET nome=?, tipo=?, catering=?, prioridade=?, notas=? WHERE id=?", datos)
        elif operacion == "D":
            cur.execute("DELETE FROM eventos WHERE id=?", (datos,))
        con.commit()


def obter_resumo():
    """
    Realiza consultas de agregación para el análisis de datos.

    :return: Tupla con (total, catering_count, por_tipo_list, nombres_catering, nombres_alta)
    """
    with conectar() as con:
        cur = con.cursor()
        total = cur.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
        con_catering = cur.execute("SELECT COUNT(*) FROM eventos WHERE catering = 1").fetchone()[0]
        nomes_catering = cur.execute("SELECT nome FROM eventos WHERE catering = 1").fetchall()
        nomes_alta = cur.execute("SELECT nome FROM eventos WHERE prioridade = 'Alta'").fetchall()
        por_tipo = cur.execute("SELECT tipo, COUNT(*) FROM eventos GROUP BY tipo").fetchall()

        return total, con_catering, por_tipo, nomes_catering, nomes_alta