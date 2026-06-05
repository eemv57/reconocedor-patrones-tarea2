import streamlit as st

st.set_page_config(page_title="Reconocedor de Patrones 3x3", layout="wide")

st.title("Tarea 2 — Construyendo una Máquina que Reconoce Patrones")
st.markdown("""
Este sistema interactivo calcula manualmente el puntaje de similitud para mini-imágenes binarias de $3\\times3$ 
con el fin de identificar la letra **T** sin utilizar librerías de Inteligencia Artificial.
""")

# 1. DEFINICIÓN DE IMÁGENES REQUISITO MÍNIMO (3 Positivas y 3 Negativas)
imagenes = {
    "T Clásica (Positivo 1)": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    "T Gruesa (Positivo 2)": [
        [1, 1, 1],
        [1, 1, 1],
        [0, 1, 0]
    ],
    "T Alta (Positivo 3)": [
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    "Línea Horizontal (Negativo 1)": [
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0]
    ],
    "Cruz / Invertida (Negativo 2)": [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    "Cuadrado Hueco (Negativo 3)": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
}

st.sidebar.header("⚙️ Configuración de la Máquina")

# Valores iniciales recomendados en la guía de la actividad
valores_iniciales = [
    [2, 2, 2],
    [-1, 3, -1],
    [-1, 3, -1]
]

st.sidebar.subheader("Matriz de Pesos (w)")
st.sidebar.write("Ajusta los pesos para cada posición de la cuadrícula de 3x3:")

pesos = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
for i in range(3):
    cols = st.sidebar.columns(3)
    for j in range(3):
        with cols[j]:
            pesos[i][j] = st.sidebar.slider(f"w_{i}{j}", min_value=-5, max_value=5, value=valores_iniciales[i][j], key=f"w_{i}_{j}")

threshold = st.sidebar.slider("Umbral de Decisión (Threshold)", min_value=-5, max_value=15, value=4)

# INTERFAZ DE SELECCIÓN DE IMAGEN
col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.subheader("🖼️ Selección de Imagen Binaria")
    nombre_seleccionado = st.selectbox("Elige un patrón para evaluar:", list(imagenes.keys()))
    matriz_img = imagenes[nombre_seleccionado]
    
    st.write("**Visualización de la matriz (Píxeles):**")
    for fila in matriz_img:
        celdas = "".join([f"⬛" if pixel == 1 else f"⬜" for pixel in fila])
        st.markdown(f"### {celdas}")

# CÁLCULO MANUAL PASO A PASO (Requisito estricto sin librerías)
puntaje_total = 0
terminos_formula = []

for i in range(3):
    for j in range(3):
        x = matriz_img[i][j]
        w = pesos[i][j]
        producto = w * x
        puntaje_total += producto
        terminos_formula.append(f"({w} \\cdot {x})")

with col_der:
    st.subheader("🧮 Cálculo del Puntaje Total")
    st.write("Fórmula de combinación lineal: $y = \\sum (w_i \\cdot x_i)$")
    
    formula_desglosada = " + ".join(terminos_formula)
    st.latex(f"y = {formula_desglosada}")
    
    st.metric(label="Puntaje Final Calculado (y)", value=puntaje_total)
    st.metric(label="Umbral configurado", value=threshold)

st.markdown("---")
st.subheader("🎯 Resultado del Reconocimiento")

if puntaje_total >= threshold:
    st.success(f"🎉 **¡RECONOCIDA!** El puntaje ({puntaje_total}) cumple con el umbral ({threshold}). La máquina clasifica este patrón como una letra **T**.")
else:
    st.error(f"❌ **RECHAZADA:** El puntaje ({puntaje_total}) es menor que el umbral ({threshold}). La máquina determina que **NO** cumple las características.")
