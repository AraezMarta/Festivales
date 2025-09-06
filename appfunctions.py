# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:00:26 2024

@author: 34711
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
import os


from streamlit.components.v1 import html

from streamlit_lottie import st_lottie

#abrimos los csv

data_path = "data"

festivales_city_clean = pd.read_csv(
    os.path.join(data_path, "festivales_city_clean.csv"), sep=',').drop_duplicates()

festivales_genre_clean = pd.read_csv(
    os.path.join(data_path, "festivales_genre_clean.csv"), sep=',').drop_duplicates()

festivales_concat = pd.read_csv(
    os.path.join(data_path, "festivales_concat.csv"), sep=',').drop_duplicates()

festivales_join = pd.read_csv(
    os.path.join(data_path, "festivales_join.csv"), sep=',').drop_duplicates()


numbers_to_months = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Leer mapa.html en la misma carpeta del script
script_dir = os.path.dirname(__file__)  # Directorio donde está este archivo .py
mapa_path = os.path.join(script_dir, "mapa.html")

with open(mapa_path, "r", encoding="utf-8") as f:
    mapa_html = f.read()


#Definimos una función para aplicar los estilos

def apply_custom_styles(
    font="poppins",
    background_color="#d7effa", 
    text_color="#000000",
    primary_color="#5c9fd9", 
    button_text_color="#ffffff",
    button_active_color="#3d7aa5", 
    button_active_text_color="#ffffff",
    secondary_background_color="#c9e4f4",
    accent_color="#000000",
    link_color="#4da8d9",
):
    st.markdown(
        f"""
        <style>
        /* Definir la fuente de la página */
        @import url('https://fonts.googleapis.com/css2?family={font}&display=swap');

        body {{
            background-color: {background_color};
            color: {text_color};
            font-family: '{font}', sans-serif;
        }}

        /* Personalizar los botones */
        .stButton>button {{
            background-color: {primary_color};
            color: {button_text_color};
            border: none;
            border-radius: 5px;
            font-weight: bold;
            padding: 10px;
            transition: background-color 0.3s ease;
        }}

        /* Cambiar el color del botón cuando se hace clic o está seleccionado */
        .stButton>button:active,
        .stButton>button:focus {{
            background-color: {button_active_color};  /* Cambiar el fondo del botón al hacer clic */
            color: {button_active_text_color};  /* Cambiar el color del texto cuando el botón está activo */
        }}

        /* Personalizar el sidebar (cambia el color de fondo) */
        .css-1d391kg {{
            background-color: {secondary_background_color};  /* Cambiar fondo del sidebar */
        }}

        /* Estilo de la aplicación principal */
        .stApp {{
            background-color: {background_color};
        }}

        /* Cambiar color de los enlaces */
        a {{
            color: {link_color};  /* Azul verdoso */
        }}

        /* Cambiar el color de los campos de texto */
        .stTextInput, .stTextArea, .stMarkdown {{
            color: {accent_color};  /* Amarillo suave */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Definimos una función para crear tarjetas personalizadas

def create_event_card(event_name, event_date, event_price, event_followers):
    tarjeta_html = f"""
    <div style="border: 3px solid #5c9fd9; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: #ffe8db;">
        <h4 style="text-align: center; color: #2a5487; font-size: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{event_name}</h4>
        <p style="font-size: 16px;"><strong>Fecha:</strong> {event_date}</p>
        <p style="font-size: 16px;"><strong>Precio:</strong> {event_price}</p>
        <p style="font-size: 16px;"><strong>Seguidores en Wegow:</strong> {event_followers}</p>
    </div>
    """
    st.markdown(tarjeta_html, unsafe_allow_html=True)



# Definimos una función para abrir menus de columna

def column_menu(festivales, column):
    column_elements = festivales[column].unique()
    
    col1, col2 = st.columns([1, 1])

    with col1:
        radio_menu_option = st.radio(
            "Selecciona una opción",
            column_elements,
            label_visibility="collapsed")
    
    with col2:
        if column =='city' and len(column_elements)==11:
            st.image("images/sunsets2.jpg", use_column_width=True)
            
        if column =='genre':
            st.image("images/Concert_aesthetic.jpg",use_column_width=True)
            
        if column =='city' and len(column_elements)!=11:
            st.write("\n")
            st.write('Explora los datos por ciudad, pasando el ratón por el gráfico.')
            
        if column =='month_name':
            st.write("\n")
            st.write('Explora los datos por mes, pasando el ratón por el gráfico.')
            

    return radio_menu_option


#Definimos una función para mostrar los eventos
                        
def show_events(festivales, column, selection):
    events = festivales[festivales[column] == selection].drop_duplicates(subset=['event_names'])

    cols = st.columns(3)
    
    for idx, row in events.iterrows():
        event = row['event_names']
        
        with cols[idx % 3]:
            if st.button(f"{event}"):
                st.markdown("##### Detalles del evento:")
                
                create_event_card(
                    event_name=row['event_names'],
                    event_date=row['event_dates'],
                    event_price=row['event_prices'],
                    event_followers=row['event_followers'])


#Aplicamos el estilo

apply_custom_styles(
    font="poppins",
    background_color="#e0f5ff",
    text_color="#000000",
    primary_color="#5c9fd9",
    button_text_color="#ffffff",
    button_active_color="#3d7aa5",
    button_active_text_color="#ffffff",
    secondary_background_color="#c9e4f4",
    accent_color="#000000",
    link_color="#4da8d9",
)


#Menu de opciones lateral
side_menu_option = st.sidebar.selectbox("Elige una opción:", ["Inicio","Festivales por ciudad", "Festivales por género","Comparar precios" ,"Salir"])

if side_menu_option == "Inicio":
    st.title("¡Encuentra tu Festival Favorito!")
    
    with open("images/animation.json", "r") as f:
        animation = json.load(f)
        
    col_animation, col_animation2, col_animation3 = st.columns([1, 2, 1])  # Esto crea 3 columnas con proporciones 1:2:1

    with col_animation2:

        st_lottie(animation, width=300, height=300,speed=1, loop=True)
    
    st.write("Descubre y compara!")

    if st.button("Mostrar mapa"):
        html(mapa_html, height=600)
        
        
if side_menu_option == "Festivales por ciudad":
    st.title("Festivales por ciudad")
    st.write("Selecciona una ciudad:")
    selected_city = column_menu(festivales_concat,'city')
    show_events(festivales_concat,'city', selected_city)
    
    
if side_menu_option == "Festivales por género":
    st.title("Festivales por género")
    st.write("Selecciona un género:")
    selected_genre = column_menu(festivales_genre_clean, 'genre')
    show_events(festivales_genre_clean, 'genre', selected_genre)
    

if side_menu_option == "Comparar precios":
    st.title("Comparar precios")
    selected_option = st.selectbox("¿Cómo quieres comparar?", ['Comparar por mes','Comparar por ciudad']) 
    
    if selected_option =='Comparar por mes':
        festivales_join_sorted = festivales_join.sort_values('month')
        months = festivales_join.sort_values('month')
        festivales_join_sorted['month_name'] = festivales_join_sorted['month'].map(numbers_to_months)
        selected_month = column_menu(festivales_join_sorted, 'month_name')
        
        with open(f"graphics/grafico_{selected_month}.html", "r", encoding="utf-8") as f:
            graphic_month = f.read()
            html(graphic_month, height=600)
            
        if st.button('Ver comparación general'):
            with open("graphics/grafico_media_mes.html", "r", encoding="utf-8") as f:
                graphic_month = f.read()
                html(graphic_month, height=600)
            
    if selected_option =='Comparar por ciudad':
        festivales_concat_graf = festivales_concat[festivales_concat.event_prices != 'No se especifica']
        cities = festivales_concat_graf.city.unique()
        selected_city = column_menu(festivales_concat_graf, 'city')
        
        with open(f"graphics/grafico_{selected_city}.html", "r", encoding="utf-8") as f:
            graphic_month = f.read()
            html(graphic_month, height=600)
            
            if st.button('Ver comparación general'):
                with open("graphics/grafico_media_ciudad.html", "r", encoding="utf-8") as f:
                    graphic_month = f.read()
                    html(graphic_month, height=600)
             
                    
if  side_menu_option == "Salir":
    st.write('¡Hasta pronto!🎶')
    with open("images/disc.json", "r") as f:
        disc = json.load(f)
        st_lottie(disc,speed=1, loop=True)
        
























