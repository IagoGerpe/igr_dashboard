"""Ejecuta consultas SQL sobre una base de datos SQLite desde la terminal.

Uso:
    python consulta.py "SELECT * FROM stores_uuid LIMIT 5"   # una consulta
    python consulta.py                                        # modo interactivo
    python consulta.py --db otra.db "SELECT ..."              # otra base de datos
    python consulta.py --web                                  # abrir en el navegador
"""

import argparse
import sqlite3
import sys
from pathlib import Path

# test.db está en la raíz del proyecto (dos carpetas por encima de este archivo)
DB_POR_DEFECTO = Path(__file__).resolve().parents[2] / "test.db"


def mostrar(cursor: sqlite3.Cursor) -> None:
    """Imprime el resultado de la consulta como una tabla."""
    if cursor.description is None:  # INSERT, UPDATE, CREATE...
        print(f"OK ({cursor.rowcount} filas afectadas)")
        return

    columnas = [c[0] for c in cursor.description]
    filas = [["NULL" if v is None else str(v) for v in fila] for fila in cursor.fetchall()]
    anchos = [max(len(x) for x in col) for col in zip(columnas, *filas)]

    def linea(valores):
        return " | ".join(v.ljust(a) for v, a in zip(valores, anchos))

    print(linea(columnas))
    print("-+-".join("-" * a for a in anchos))
    for fila in filas:
        print(linea(fila))
    print(f"\n({len(filas)} filas)")


def ejecutar(conexion: sqlite3.Connection, sql: str) -> None:
    try:
        mostrar(conexion.execute(sql))
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")


def abrir_web(db: Path) -> None:
    """Lanza la versión Streamlit (consulta_web.py) y la abre en el navegador."""
    from streamlit.web import cli as stcli

    script = Path(__file__).with_name("consulta_web.py")
    sys.argv = ["streamlit", "run", str(script), "--", str(db)]
    sys.exit(stcli.main())


def main() -> None:
    parser = argparse.ArgumentParser(description="Consultas SQLite desde la terminal")
    parser.add_argument("sql", nargs="?", help="consulta SQL (si se omite, modo interactivo)")
    parser.add_argument("--db", default=DB_POR_DEFECTO, help="ruta de la base de datos")
    parser.add_argument("--web", action="store_true", help="abrir la versión en el navegador")
    args = parser.parse_args()

    if not Path(args.db).exists():
        parser.error(f"no existe la base de datos: {args.db}")

    if args.web:
        abrir_web(Path(args.db).resolve())
        return

    with sqlite3.connect(args.db) as conexion:
        if args.sql:
            ejecutar(conexion, args.sql)
            return

        print(f"Conectado a {args.db}")
        print("Escribe una consulta terminada en ';'. 'tablas' lista las tablas, 'salir' termina.")
        buffer = ""
        while True:
            try:
                linea = input("sql> " if not buffer else "...> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break
            comando = linea.strip().lower()
            if not buffer and comando in ("salir", "exit", "quit"):
                break
            if not buffer and comando == "tablas":
                ejecutar(conexion, "SELECT name, type FROM sqlite_master "
                                   "WHERE type IN ('table', 'view') ORDER BY name")
                continue
            buffer += linea + "\n"
            if sqlite3.complete_statement(buffer):
                ejecutar(conexion, buffer)
                buffer = ""


if __name__ == "__main__":
    main()
