"""Versión en navegador de consulta.py (Streamlit).

Se abre con:  uv run consulta --web
"""

import sqlite3
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

DB_POR_DEFECTO = Path(__file__).resolve().parents[2] / "test.db"


def app() -> None:
    st.set_page_config(page_title="Consultas SQLite", page_icon="🗄️", layout="wide")
    db = Path(sys.argv[1]) if len(sys.argv) > 1 else DB_POR_DEFECTO

    st.title("🗄️ Consultas SQLite")
    st.caption(f"Base de datos: `{db}`")

    if not db.exists():
        st.error(f"No existe la base de datos: {db}")
        st.stop()

    conexion = sqlite3.connect(db)

    # Barra lateral: tablas y sus columnas
    with st.sidebar:
        st.header("Tablas")
        tablas = conexion.execute(
            "SELECT name, type FROM sqlite_master "
            "WHERE type IN ('table', 'view') ORDER BY name"
        ).fetchall()
        for nombre, tipo in tablas:
            with st.expander(f"{nombre} ({tipo})"):
                columnas = conexion.execute(f'PRAGMA table_info("{nombre}")').fetchall()
                for col in columnas:
                    st.write(f"- `{col[1]}` {col[2]}")

    sql = st.text_area(
        "Consulta SQL",
        value="SELECT * FROM sales_uuid LIMIT 10",
        height=150,
    )

    if st.button("Ejecutar", type="primary"):
        try:
            cursor = conexion.execute(sql)
            if cursor.description is None:  # INSERT, UPDATE, CREATE...
                conexion.commit()
                st.success(f"OK ({cursor.rowcount} filas afectadas)")
            else:
                columnas = [c[0] for c in cursor.description]
                df = pd.DataFrame(cursor.fetchall(), columns=columnas)
                st.write(f"**{len(df)} filas**")
                st.dataframe(df, width="stretch")
                st.download_button(
                    "Descargar CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name="resultado.csv",
                    mime="text/csv",
                )
        except sqlite3.Error as e:
            st.error(f"Error: {e}")

    conexion.close()


if __name__ == "__main__":
    app()
