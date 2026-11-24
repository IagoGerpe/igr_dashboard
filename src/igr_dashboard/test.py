
import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Prueba Streamlit", page_icon="🚀")

st.title("🚀 Mi primera aplicación Streamlit")
st.write("¡Bienvenido! Esta es una aplicación de prueba.")

# Entrada de texto
nombre = st.text_input("¿Cómo te llamas?")

if st.button("Saludar"):
    if nombre:
        st.success(f"¡Hola, {nombre}!")
    else:
        st.warning("Introduce tu nombre primero.")

# Slider interactivo
numero = st.slider("Selecciona un número", 1, 100, 50)
st.write(f"Has seleccionado: **{numero}**")

# Gráfica
st.subheader("Gráfica de prueba")

datos = pd.DataFrame({
    "Valores": np.random.randn(20).cumsum()
})

st.line_chart(datos)

st.info("¡Streamlit funciona correctamente!")
