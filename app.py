import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# CARGA DE DATOS
# ==========================

df = pd.read_csv(
    "Sample - Superstore.csv",
    encoding="latin1"
)

# ==========================
# FILTRO POR REGIÓN
# ==========================

region = st.sidebar.selectbox(
    "Seleccione una región",
    ["Todas"] + list(df["Region"].unique())
)

if region != "Todas":
    df = df[df["Region"] == region]

# ==========================
# TÍTULO
# ==========================

st.title("Dashboard Ejecutivo de Ventas")

# ==========================
# KPIs
# ==========================

st.metric(
    "Total Ventas",
    f"${df['Sales'].sum():,.2f}"
)

st.metric(
    "Total Clientes",
    df['Customer ID'].nunique()
)

st.metric(
    "Promedio de Venta",
    f"${df['Sales'].mean():,.2f}"
)

st.metric(
    "Total Registros",
    len(df)
)

producto_top = (
    df.groupby('Product Name')['Sales']
      .sum()
      .idxmax()
)

st.metric(
    "Producto más vendido",
    producto_top
)

# ==========================
# VENTAS POR REGIÓN
# ==========================

ventas_region = df.groupby('Region')['Sales'].sum()

st.subheader("Ventas por Región")
st.bar_chart(ventas_region)

# ==========================
# GRÁFICO CIRCULAR
# ==========================

st.subheader("Participación de Ventas por Región (%)")

fig, ax = plt.subplots()

df.groupby('Region')['Sales'].sum().plot(
    kind='pie',
    autopct='%1.1f%%',
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

# ==========================
# VENTAS POR CATEGORÍA
# ==========================

ventas_categoria = df.groupby('Category')['Sales'].sum()

st.subheader("Ventas por Categoría")
st.bar_chart(ventas_categoria)

# ==========================
# RENTABILIDAD POR CATEGORÍA
# ==========================

rentabilidad = df.groupby('Category')['Profit'].sum()

st.subheader("Rentabilidad por Categoría")
st.bar_chart(rentabilidad)

# ==========================
# TENDENCIA TEMPORAL
# ==========================

df['Order Date'] = pd.to_datetime(df['Order Date'])

ventas_tiempo = df.groupby('Order Date')['Sales'].sum()

st.subheader("Tendencia de Ventas")
st.line_chart(ventas_tiempo)