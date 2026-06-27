import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================

st.set_page_config(
    page_title="Dashboard Grupo 8",
    page_icon="📊",
    layout="wide"
)

# ============================================
# CARGA DE DATOS
# ============================================

df = pd.read_csv(
    "Sample - Superstore.csv",
    encoding="latin1"
)

# ============================================
# FILTRO
# ============================================

st.sidebar.title("Filtros")

region = st.sidebar.selectbox(
    "Seleccione una región",
    ["Todas"] + list(df["Region"].unique())
)

if region != "Todas":
    df = df[df["Region"] == region]

# ============================================
# TÍTULO
# ============================================

st.title("Dashboard Ejecutivo - Grupo 8")
st.markdown("Análisis Empresarial mediante Minería de Datos")

st.markdown("---")

# ============================================
# KPIs
# ============================================

producto_top = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .idxmax()
)

cliente_top = (
    df.groupby("Customer Name")["Sales"]
      .sum()
      .idxmax()
)

ventas_cliente_top = (
    df.groupby("Customer Name")["Sales"]
      .sum()
      .max()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Ventas",
        f"${df['Sales'].sum():,.2f}"
    )

with col2:
    st.metric(
        "Clientes",
        df["Customer ID"].nunique()
    )

with col3:
    st.metric(
        "Promedio Venta",
        f"${df['Sales'].mean():,.2f}"
    )

with col4:
    st.metric(
        "Mejor Cliente",
        cliente_top
    )

# ============================================
# PRODUCTO MÁS VENDIDO
# ============================================

colA, colB = st.columns(2)

with colA:
    st.markdown("Producto más vendido")
    st.success(producto_top)

with colB:
    st.markdown("Compras del mejor cliente")
    st.success(f"${ventas_cliente_top:,.2f}")

st.markdown("---")

# ============================================
# VENTAS POR REGIÓN
# ============================================

ventas_region = df.groupby("Region")["Sales"].sum()

st.subheader("Ventas por Región")

fig, ax = plt.subplots(figsize=(8,4))

ventas_region.plot(
    kind="bar",
    color="#6C63FF",
    ax=ax
)

ax.set_ylabel("Ventas")
ax.set_xlabel("Región")

plt.xticks(rotation=0)

st.pyplot(fig)

# ============================================
# PARTICIPACIÓN POR REGIÓN
# ============================================

st.subheader("Participación de Ventas por Región")

fig, ax = plt.subplots(figsize=(6,6))

df.groupby("Region")["Sales"].sum().plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90,
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

# ============================================
# VENTAS POR CATEGORÍA
# ============================================

ventas_categoria = df.groupby("Category")["Sales"].sum()

st.subheader("Ventas por Categoría")

fig, ax = plt.subplots(figsize=(8,4))

ventas_categoria.plot(
    kind="bar",
    color="#00C49A",
    ax=ax
)

ax.set_ylabel("Ventas")
ax.set_xlabel("Categoría")

plt.xticks(rotation=0)

st.pyplot(fig)

# ============================================
# RENTABILIDAD POR CATEGORÍA
# ============================================

rentabilidad = df.groupby("Category")["Profit"].sum()

st.subheader("Rentabilidad por Categoría")

fig, ax = plt.subplots(figsize=(8,4))

rentabilidad.plot(
    kind="bar",
    color="#FF8C42",
    ax=ax
)

ax.set_ylabel("Ganancia")
ax.set_xlabel("Categoría")

plt.xticks(rotation=0)

st.pyplot(fig)

# ============================================
# TENDENCIA DE VENTAS
# ============================================

df["Order Date"] = pd.to_datetime(df["Order Date"])

ventas_tiempo = df.groupby("Order Date")["Sales"].sum()

st.subheader("Tendencia de Ventas")

st.line_chart(ventas_tiempo)
