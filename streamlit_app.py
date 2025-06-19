import streamlit as st
import pandas as pd
import openai
import os

st.set_page_config(page_title="Validador inteligente", layout="wide")
st.title("📦 Validador inteligente de formularios logísticos")

openai_api_key = st.text_input("🔑 Ingresá tu OpenAI API Key:", type="password")

uploaded_file = st.file_uploader("📄 Subí el formulario Excel", type=["xlsx", "xls"])

if uploaded_file and openai_api_key:
    df = pd.read_excel(uploaded_file, header=None).fillna('')
    st.write("📋 Vista previa del formulario:")
    st.dataframe(df)

    # Convertimos el dataframe a Markdown (texto plano legible por GPT)
    tabla_texto = df.to_markdown(index=False)

    prompt = f"""
Actuá como un analista logístico experto. Tenés el siguiente formulario (en formato tabla).
Tu tarea es:

1. Extraer los valores de estos campos si están:
   - Cantidad de SKU
   - Dimensiones
   - Peso
   - Frecuencia de ingreso
   - Pedidos por día
   - Volumen por día
   - Posiciones pallet
   - Estantería o m2
   - Frecuencia distribución

2. Decir si alguno falta o no está claro.

3. Evaluar si hay alguna incongruencia, como por ejemplo:
   - Volumen diario vs. Posiciones
   - Peso o dimensiones poco realistas
   - Datos duplicados o inconsistentes

4. Dar un resumen final en lenguaje simple para un comercial.

Tabla:
{tabla_texto}

Respondé en forma clara, ordenada y estructurada.
    """

    with st.spinner("Analizando con GPT..."):
        try:
            openai.api_key = openai_api_key
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Sos un experto en logística y validación de formularios industriales."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1200
            )

            resultado = response['choices'][0]['message']['content']
            st.success("✅ Análisis completado")
            st.markdown("### 🧠 Resultado del análisis:")
            st.markdown(resultado)

        except Exception as e:
            st.error(f"Error: {e}")

