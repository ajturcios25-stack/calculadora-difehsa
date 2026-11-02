import streamlit as st
import math

def convertir_a_pies(metros):
    return metros * 3.28084

def calcular_tablillas(largo, ancho):
    lances_a = math.ceil(ancho / 0.25)
    lances_por_tablilla_a = math.floor(5.95 / largo) if largo <= 5.95 else 1
    if lances_por_tablilla_a < 1: lances_por_tablilla_a = 1
    
    if largo > 5.95:
        lances_totales_a = lances_a * math.ceil(largo / 5.95)
        tablillas_a = lances_totales_a
        union_a, juntas_a = True, math.ceil(largo / 5.95) - 1
    else:
        tablillas_a = math.ceil(lances_a / lances_por_tablilla_a)
        union_a, juntas_a = False, 0
        
    lances_b = math.ceil(largo / 0.25)
    lances_por_tablilla_b = math.floor(5.95 / ancho) if ancho <= 5.95 else 1
    if lances_por_tablilla_b < 1: lances_por_tablilla_b = 1
    
    if ancho > 5.95:
        lances_totales_b = lances_b * math.ceil(ancho / 5.95)
        tablillas_b = lances_totales_b
        union_b, juntas_b = True, math.ceil(ancho / 5.95) - 1
    else:
        tablillas_b = math.ceil(lances_b / lances_por_tablilla_b)
        union_b, juntas_b = False, 0
        
    if tablillas_a <= tablillas_b:
        return (tablillas_a, "a lo largo", union_a, juntas_a, lances_por_tablilla_a)
    else:
        return (tablillas_b, "a lo ancho", union_b, juntas_b, lances_por_tablilla_b)

def calcular_materiales(nombre, largo, ancho):
    perimetro_m = (largo * 2) + (ancho * 2)
    perimetro_ft = convertir_a_pies(perimetro_m)
    tablillas, orientacion, usa_union_h, juntas, lances_por_tablilla = calcular_tablillas(largo, ancho)
    angulos = math.ceil(perimetro_ft / 10)
    boceles = math.ceil(perimetro_ft / 19)
    
    if orientacion == "a lo largo":
        lances_furring = math.ceil(largo / 0.5)
        medida_furring_ft = convertir_a_pies(ancho)
        lances_canaleta = math.ceil(ancho / 1)
        medida_canaleta_ft = convertir_a_pies(largo)
    else:
        lances_furring = math.ceil(ancho / 0.5)
        medida_furring_ft = convertir_a_pies(largo)
        lances_canaleta = math.ceil(largo / 1)
        medida_canaleta_ft = convertir_a_pies(ancho)
        
    furring = math.ceil((lances_furring * medida_furring_ft) / 12)
    canaleta = math.ceil((lances_canaleta * medida_canaleta_ft) / 16)
    tornillos_tablilla_bocel = 15 * (tablillas + boceles)
    clavos_angulo = 12 * angulos
    tornillos_metal = 10 * (canaleta + furring)
    
    union_h = 0
    if usa_union_h:
        union_h = juntas * math.ceil(ancho / 5.8) if orientacion == "a lo largo" else juntas * math.ceil(largo / 5.8)
        
    return {
        "nombre": nombre, "largo": largo, "ancho": ancho, "orientacion": orientacion,
        "lances_por_tablilla": lances_por_tablilla, "tablillas": tablillas, "angulos": angulos,
        "boceles": boceles, "furring": furring, "canaleta": canaleta, 
        "tornillos_tablilla_bocel": tornillos_tablilla_bocel, "clavos_angulo": clavos_angulo,
        "tornillos_metal": tornillos_metal, "union_h": union_h
    }

st.set_page_config(page_title="Calculadora DIFEHSA", layout="wide")
st.title("🏗️ Calculadora de Materiales - DIFEHSA")

num_areas = st.number_input("¿Cuántas áreas tiene la casa? (máx. 11)", min_value=1, max_value=11, value=1)
areas_data = []

cols = st.columns(3)
for i in range(num_areas):
    with cols[i % 3]:
        st.subheader(f"Área {i+1}")
        nombre = st.text_input(f"Nombre", value=f"Área {i+1}", key=f"nom_{i}")
        largo = st.number_input(f"Largo (m)", min_value=0.1, value=3.0, key=f"lar_{i}")
        ancho = st.number_input(f"Ancho (m)", min_value=0.1, value=3.0, key=f"anch_{i}")
        areas_data.append((nombre, largo, ancho))

if st.button("Calcular Materiales", type="primary"):
    resultados = [calcular_materiales(n, l, a) for n, l, a in areas_data]
    
    st.header("Resultados por Área")
    for r in resultados:
        with st.expander(f"📌 {r['nombre']} ({r['largo']}m x {r['ancho']}m)", expanded=True):
            st.write(f"**Orientación:** {r['orientacion']} | **Lances por tablilla:** {r['lances_por_tablilla']}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Tablillas", r['tablillas'])
            c1.metric("Unión H", r['union_h'])
            c2.metric("Ángulos", r['angulos'])
            c2.metric("Boceles", r['boceles'])
            c3.metric("Furring", r['furring'])
            c3.metric("Canaleta", r['canaleta'])
            c4.metric("Tornillos Tab/Bocel", r['tornillos_tablilla_bocel'])
            c4.metric("Tornillos Metal", r['tornillos_metal'])
            c4.metric("Clavos Ángulo", r['clavos_angulo'])

    st.header("📦 Total General de la Casa")
    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Total Tablillas", sum(r['tablillas'] for r in resultados))
    tc1.metric("Total Unión H", sum(r['union_h'] for r in resultados))
    tc2.metric("Total Ángulos", sum(r['angulos'] for r in resultados))
    tc2.metric("Total Boceles", sum(r['boceles'] for r in resultados))
    tc3.metric("Total Furring", sum(r['furring'] for r in resultados))
    tc3.metric("Total Canaleta", sum(r['canaleta'] for r in resultados))
    tc4.metric("Total Tornillos Tab/Boc", sum(r['tornillos_tablilla_bocel'] for r in resultados))
    tc4.metric("Total Tornillos Metal", sum(r['tornillos_metal'] for r in resultados))
    tc4.metric("Total Clavos Ángulo", sum(r['clavos_angulo'] for r in resultados))
