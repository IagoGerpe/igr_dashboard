# igr-dashboard

Herramientas en Python para consultar la base de datos SQLite `test.db`, desde la terminal o desde el navegador.

## Requisitos

- [uv](https://docs.astral.sh/uv/)
- Python 3.14 (uv lo instala si hace falta)

Instalar dependencias (solo la primera vez):

```bash
uv sync
```

Todos los comandos se ejecutan desde la carpeta `igr_dashboard`.

## Consultas en la terminal

Una sola consulta:

```bash
uv run consulta "SELECT * FROM stores_uuid LIMIT 5"
```

Modo interactivo:

```bash
uv run consulta
```

- Escribe la consulta y termínala con `;` (puede ocupar varias líneas).
- `tablas` muestra las tablas y vistas.
- `salir` o `Ctrl+D` para terminar.

## Consultas en el navegador

```bash
uv run consulta --web
```

Abre http://localhost:8501 (o el siguiente puerto libre). En la página:

- A la izquierda están las tablas; despliega una para ver sus columnas.
- Escribe la consulta y pulsa **Ejecutar**.
- Descarga el resultado con **Descargar CSV**.

Para cerrarla, pulsa `Ctrl+C` en la terminal.

## Usar otra base de datos

Por defecto se usa `test.db`. Para usar otra:

```bash
uv run consulta --db otra.db "SELECT ..."
```

```bash
uv run consulta --web --db otra.db
```

## Tablas de `test.db`

| Tabla | Columnas |
|---|---|
| `sales_uuid` | transaction_id, store_id, product_id, quantity, price, transaction_date |
| `products_uuid` | product_id, product_name, category |
| `stores_uuid` | store_id, store_name, location |
| `products_fancy` (vista) | product_id, price — ventas con price > 10 |
| `products_fancy_table` | product_id, price |

Ejemplo, ventas totales por tienda:

```bash
uv run consulta "SELECT st.store_name, ROUND(SUM(sa.quantity * sa.price), 2) AS total
FROM sales_uuid sa JOIN stores_uuid st USING (store_id)
GROUP BY st.store_name ORDER BY total DESC"
```

> **Cuidado:** `INSERT`, `UPDATE` y `DELETE` también funcionan y los cambios se guardan en `test.db`.

## App de prueba de Streamlit

```bash
uv run streamlit run src/igr_dashboard/test.py
```
