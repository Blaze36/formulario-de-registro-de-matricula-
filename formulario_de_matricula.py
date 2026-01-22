import streamlit as st
import pandas as pd
from datetime import datetime
import os


st.set_page_config(
    page_title="Registro de Asignaturas",
    layout="wide",
    initial_sidebar_state="expanded"
)


ARCHIVO_CSV = "asignaturas_matriculadas.csv"


def cargar_datos():
    if os.path.exists(ARCHIVO_CSV):
        return pd.read_csv(ARCHIVO_CSV)
    return pd.DataFrame(columns=[
        "Nombre", "Código", "Campus", "Aula", "Maestro", 
        "Fecha", "Hora Inicio", "Hora Final"
    ])


def guardar_datos(df):
    df.to_csv(ARCHIVO_CSV, index=False)


st.title("📚 Sistema de Registro de Asignaturas Matriculadas")


with st.sidebar:
    st.header("Opciones")
    opcion = st.radio(
        "Seleccione una opción:",
        ["Registrar Asignatura", "Ver Reporte", "Reporte por Campus", "Exportar Datos"]
    )


df = cargar_datos()

if opcion == "Registrar Asignatura":
    st.header("📝 Registro de Nueva Asignatura")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre de la Asignatura")
        codigo = st.text_input("Código de la Asignatura")
        campus = st.selectbox(
            "Campus",
            ["Campus San Pedro Sula ", "Campus Tegucigalpa", "Campus La Ceiba", 
             "Campus Villanueva ", "Campus Choloma", "Campus Virtual"]
        )
        aula = st.text_input("Aula")
    
    with col2:
        maestro = st.text_input("Maestro/Profesor")
        fecha = st.date_input("Fecha de Registro", datetime.now())
        hora_inicio = st.time_input("Hora de Inicio")
        hora_final = st.time_input("Hora Final")
    
    if st.button("✅ Guardar Asignatura", use_container_width=True):
        if nombre and codigo and campus and aula and maestro:
            nuevo_registro = pd.DataFrame({
                "Nombre": [nombre],
                "Código": [codigo],
                "Campus": [campus],
                "Aula": [aula],
                "Maestro": [maestro],
                "Fecha": [fecha.strftime("%Y-%m-%d")],
                "Hora Inicio": [hora_inicio.strftime("%H:%M")],
                "Hora Final": [hora_final.strftime("%H:%M")]
            })
            
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            guardar_datos(df)
            st.success("✨ Asignatura registrada correctamente")
        else:
            st.error(" Por favor complete todos los campos")

elif opcion == "Ver Reporte":
    st.header(" Reporte de Asignaturas Matriculadas")
    
    if len(df) > 0:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Asignaturas", len(df))
        with col2:
            st.metric("Total de Campus", df["Campus"].nunique())
        with col3:
            st.metric("Total de Maestros", df["Maestro"].nunique())
        
        
        st.subheader("Gestionar Asignaturas")
        idx_eliminar = st.number_input(
            "Número de fila a eliminar (0 para la primera)",
            min_value=0,
            max_value=len(df)-1 if len(df) > 0 else 0,
            step=1
        )
        
        if st.button("🗑️ Eliminar Asignatura", use_container_width=True):
            df = df.drop(idx_eliminar).reset_index(drop=True)
            guardar_datos(df)
            st.success("Asignatura eliminada correctamente")
            st.rerun()
    else:
        st.info("📭 No hay asignaturas registradas aún")

elif opcion == "Reporte por Campus":
    st.header("🏢 Reporte por Campus")
    
    if len(df) > 0:
        campus_lista = sorted(df["Campus"].unique())
        
        for campus in campus_lista:
            with st.expander(f"**{campus}** ({len(df[df['Campus'] == campus])} asignaturas)"):
                df_campus = df[df["Campus"] == campus][
                    ["Nombre", "Código", "Aula", "Maestro", "Fecha", "Hora Inicio", "Hora Final"]
                ]
                st.dataframe(df_campus, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No hay asignaturas registradas aún")

elif opcion == "Exportar Datos":
    st.header("💾 Exportar Datos")
    
    if len(df) > 0:
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar como CSV",
            data=csv,
            file_name="asignaturas_matriculadas.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Exportar a Excel
        try:
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Asignaturas', index=False)
            
            excel_data = output.getvalue()
            st.download_button(
                label="📊 Descargar como Excel",
                data=excel_data,
                file_name="asignaturas_matriculadas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except:
            st.warning("Instale openpyxl para exportar a Excel: pip install openpyxl")
        
       
        st.subheader("Resumen por Campus")
        resumen = df.groupby("Campus").size().reset_index(name="Cantidad")
        st.dataframe(resumen, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No hay datos para exportar")
