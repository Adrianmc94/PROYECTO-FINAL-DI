import sqlite3

def conectar():
    """Establece conexión con la base de datos SQLite."""
    return sqlite3.connect('eventos.db')

def inicializar_bd():
    """Crea la tabla con todos los campos necesarios al iniciar."""
    with conectar() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT,
            catering INTEGER,
            prioridade TEXT,
            notas TEXT)""")

def CRUD(operacion, datos=None):
    """Gestiona las operaciones Create, Read, Update y Delete."""
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
    """Calcula estadísticas para la tercera ventana de la aplicación."""
    with conectar() as con:
        cur = con.cursor()
        total = cur.execute("SELECT COUNT(*) FROM eventos").fetchone()[0]
        con_catering = cur.execute("SELECT COUNT(*) FROM eventos WHERE catering = 1").fetchone()[0]
        return total, con_catering