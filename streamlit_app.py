import streamlit as st
import pandas as pd
import re

st.title("📦 Validador de archivos logísticos")

uploaded_file = st.file_uploader("Subí el archivo Excel", type=["xls", "xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=None).fillna('')
    df.columns = range(df.shape[1])

    campos_clave = {
        "Cantidad de SKU": ["cantidad de sku"],
        "Dimensiones": ["dimensiones", "bulto", "pallet"],
        "Peso": ["peso", "unidad"],
        "Frecuencia ingreso": ["frecuencia de ingreso", "frecuencia recepción"],
        "Pedidos por día": ["pedidos por día", "pedidos diarios"],
        "Volumen por día": ["volumen por día"],
        "Posiciones pallet": ["posiciones de pallet", "cantidad de posiciones"],
        "Estantería o m2": ["estantería", "m2", "metros cuadrados"],
        "Frecuencia distribución": ["frecuencia de distribución", "distribución"]
    }

    def buscar_valor(claves):
        for i, row in df.iterrows():
            texto = str(row[1]).lower()
            for clave in claves:
                if clave in texto:
                    for j in [2, 3]:
                        if j < len(row):
                            val = str(row[j]).strip()
                            if val and val.lower() not in ["nan", ""]:
                                return val
        return None

    faltantes = []
    valores_encontrados = {}

    for campo, claves in campos_clave.items():
        valor = buscar_valor(claves)
        valores_encontrados[campo] = valor
        if not valor:
            faltantes.append(campo)

    observaciones = []
    try:
        vol_diario = float(re.findall(r"\d+", valores_encontrados["Volumen por día"])[0])
        frecuencia = float(re.findall(r"\d+", valores_encontrados["Frecuencia distribución"])[0])
        estimado = vol_diario * frecuencia

        if valores_encontrados["Posiciones pallet"]:
            posiciones = float(re.findall(r"\d+", valores_encontrados["Posiciones pallet"])[0])
            if abs(posiciones - estimado) > 0.3 * estimado:
                observaciones.append("⚠️ Incongruencia entre volumen diario y posiciones estimadas.")
    except:
        observaciones.append("No se pudo evaluar congruencia de volumen.")

    st.subheader("📋 Valores encontrados:")
    st.write(valores_encontrados)

    if faltantes:
        st.subheader("❌ Campos faltantes:")
        st.write(faltantes)
    else:
        st.success("✅ Todos los campos clave fueron identificados.")

    if observaciones:
        st.subheader("⚠️ Observaciones:")
        for obs in observaciones:
            st.warning(obs)
    else:
        st.success("✅ No se detectaron incongruencias.")
