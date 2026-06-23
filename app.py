import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "Sample - Superstore.csv",
    encoding="latin1"
)

region = st.sidebar.selectbox(
    "Seleccione una región",
    ["Todas"] + list(df["Region"].unique())
)

if region != "Todas":
    df = df[df["Region"] == region]

st.title("Dashboard Ejecutivo")

st.metric("Total Ventas", round(df['Sales'].sum(),2))
st.metric("Clientes", df['Customer ID'].nunique())
st.metric("Promedio Venta", round(df['Sales'].mean(),2))

ventas_region = df.groupby('Region')['Sales'].sum()

st.subheader("Ventas por Región")
st.bar_chart(ventas_region)
ventas_region = df.groupby('Region')['Sales'].sum()

st.subheader("Participación de Ventas por Región (%)")

fig, ax = plt.subplots()

df.groupby('Region')['Sales'].sum().plot(
    kind='pie',
    autopct='%1.1f%%',
    ax=ax
)

st.pyplot(fig)

producto_top = df.groupby('Product Name')['Sales'].sum().idxmax()

st.metric("Producto más vendido", producto_top)

ventas_categoria = df.groupby('Category')['Sales'].sum()

st.subheader("Ventas por Categoría")
st.bar_chart(ventas_categoria)

df['Order Date'] = pd.to_datetime(df['Order Date'])

ventas_tiempo = df.groupby('Order Date')['Sales'].sum()

st.subheader("Tendencia de Ventas")
st.line_chart(ventas_tiempo)