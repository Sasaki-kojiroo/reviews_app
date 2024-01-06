import streamlit as st
import altair as alt
import pandas as pd
from datetime import time, datetime, timedelta


df = pd.read_csv("sentiment.csv")

df.FECHA = pd.to_datetime(df.FECHA)

Fecha_minima = df.FECHA.min()
Fecha_maxima = df.FECHA.max()

# Obtener el año, mes y día mínimo
a_min = Fecha_minima.year
m_min = Fecha_minima.month
d_min = Fecha_minima.day

# Obtener el año, mes y día máximo
a_max = Fecha_maxima.year
m_max = Fecha_maxima.month
d_max = Fecha_maxima.day



#_________________________________________________
# Sidebar
st.sidebar.title("Filtros")



# FILTERS
# FECHA
#start_time = st.sidebar.slider(
#     "When do you start?",
 #    min_value=FECHAtime(a_min, m_min, d_min),
     #max_value=FECHAtime(a_max, m_max, d_max),
    # value=(FECHAtime(a_min, m_min, d_min), FECHAtime(a_max, m_max, d_max)),
   #  format="DD/MM/YY")

#YEAR
anno = 0
if a_min == a_max:
    anno=1
    st.sidebar.write(f"El año elegido es {a_min}")
    selected_year = (a_min,a_max)
else:
    selected_year = st.sidebar.slider(
        "Selecciona un año:",
        min_value=a_min,
        max_value=a_max,
        value=(a_min, a_max))



#MONTH
# Crear un select_slider para seleccionar un rango de meses
st.sidebar.subheader("Mes")
selected_months = st.sidebar.select_slider('Selecciona un rango de meses', options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'], value=('Enero', 'Diciembre'))

months_dic = {
    "Enero":1,
    "Febrero":2,
    "Marzo":3,
    "Abril":4,
    "Mayo":5,
    "Junio":6,
    "Julio":7,
    "Agosto":8,
    "Septiembre":9,
    "Octubre":10,
    "Noviembre":11,
    "Diciembre":12
}
selected_months = (months_dic[selected_months[0]],months_dic[selected_months[1]])

#DAYS
st.sidebar.subheader("Días")

selected_day = st.sidebar.select_slider(
    "Selecciona rango de días del mes:",
        options=range(1,32),
        value=(1, 31)
        )


# TIME
st.sidebar.subheader("Hora")
selected_time = st.sidebar.select_slider(
    "Selecciona rango de horas:",
        options=range(0,24),
        value=(00, 23)
        )

# Sentimiento
genre = st.sidebar.radio(
    "Elige el sentimiento",
    ["Todos","Positivo 	:blush:", "Neutro", "Negativo :angry:"])


#_________________________________________________
# TITLE
st.title('Hospital Los Ángeles')
st.header("Ciudad Juárez")

#______________________________________________________________________________________________
# FILTROS
st.subheader('Filtros')

# Mostrar el rango de meses seleccionado

if anno ==1:
    st.write(f"Año: {a_min}")
else:
    st.write(f"Años selecionados: {selected_year[0]}-{selected_year[1]}")

st.write(f"Días seleccionados: {selected_day[0]}-{selected_day[1]}")
st.write(f'Meses seleccionados: {selected_months[0]} - {selected_months[1]}')

st.write(f'Horas seleccionadas: {selected_time[0]} - {selected_time[1]}')

#_________________________________________________
# DATAFRAME with filters

# Adjust the initial and final date according to the selected year, month, and day
int_date = datetime(selected_year[0] if anno == 0 else a_min, selected_months[0], selected_day[0])
fin_date = datetime(selected_year[1] if anno == 0 else a_max, selected_months[1], selected_day[1], 23, 59, 59)

# Filter the DataFrame
df_filtered = df[(df['FECHA'] >= int_date) & (df['FECHA'] <= fin_date)]

# Year, Month, Days, Time
df_filtered = df_filtered[df_filtered['FECHA'].dt.year.between(selected_year[0], selected_year[1])]
df_filtered = df_filtered[df_filtered['FECHA'].dt.month.between(selected_months[0], selected_months[1])]
df_filtered = df_filtered[df_filtered['FECHA'].dt.day.between(selected_day[0], selected_day[1])]
df_filtered = df_filtered[df_filtered['FECHA'].dt.hour.between(selected_time[0], selected_time[1])]

if genre == "Neutro":
    df_filtered = df_filtered[df_filtered['SENTIMENT']== "Neutro"]
elif genre == "Positivo 	:blush:":
    df_filtered = df_filtered[df_filtered['SENTIMENT']== "Positivo"]
elif genre == "Negativo :angry:":
    df_filtered = df_filtered[df_filtered['SENTIMENT']== "Negativo"]
#_________________________________________________

#_________________________________________________
# BODY Graphs
###############

###########################################################################
# Ultimas reseñas
###########################################################################
    
# Función para aplicar formato condicional
def highlight_sentiment(val):
    if val == "Neutro":
        return 'background-color: yellow'
    elif val == "Positivo":
        return 'background-color: green'
    elif val == "Negativo":
        return 'background-color: red'
    else:
        return ''

st.header("Últimas reseñas")
df_latest = df_filtered[["REVIEW", "SENTIMENT", "GRUPO", "FECHA"]]
df_latest = df_latest.sort_values("FECHA", ascending=False)
df_latest = df_latest.head(5)

# Aplicar formato condicional a la columna "SENTIMENT"
df_latest_styled = df_latest.head(1).style.applymap(highlight_sentiment, subset=["SENTIMENT"])
df_latest_styledd = df_latest.style.applymap(highlight_sentiment, subset=["SENTIMENT"])

# Mostrar DataFrame con formato condicional
st.subheader("Última reseña")
st.dataframe(
    df_latest_styled,
    column_config={
        "FECHA": "Fecha",
        "REVIEW": "Reseña",
        "SENTIMENT": "Sentimiento",
        "GRUPO": "Grupo",
    },
    hide_index=True,
)

st.subheader("Últimas 5 reseñas")


with st.expander('Da un "Click" para ver'):

    st.dataframe(
        df_latest_styledd,
        column_config={
            "FECHA":"Fecha",
            "REVIEW":"Reseña",
            "GRUPO":"Grupo",
        },
        hide_index=True,
    )



###########################################################################
st.header("Gráficos")
###########################################################################
# POR HORA
###############

# Group by hour and sentiment
df_filtered['HOUR'] = df_filtered['FECHA'].dt.hour
hourly_sentiment = df_filtered.groupby(['HOUR', 'SENTIMENT']).size().reset_index(name='counts')

# Pivot the grouped data to get sentiments as separate columns
hourly_sentiment_pivot = hourly_sentiment.pivot(index='HOUR', columns='SENTIMENT', values='counts').fillna(0).reset_index()

# Melt the pivoted DataFrame to long-form for Altair
df_melted = hourly_sentiment_pivot.melt('HOUR', var_name='Sentiment', value_name='Count')


st.subheader('Por Hora')
# Create the bar chart using the melted DataFrame
hourly_chart = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X('HOUR:N', title='Hora del día'),
    y=alt.Y('Count:Q', title='Cantidad de menciones'),
    color=alt.Color('Sentiment:N', scale=alt.Scale(domain=['Positivo', 'Neutro', 'Negativo'], range=['royalblue', 'skyblue', 'red'])),
    tooltip=['HOUR', 'Sentiment', 'Count']
).properties(
    width=600,
    height=300
)

# Use Streamlit to render the chart
st.altair_chart(hourly_chart, use_container_width=True)

#_________________________________________________

###############
# POR FECHA
###############
st.subheader('Por Fecha')
fecha_chart = alt.Chart(df_filtered).mark_circle().encode(
    x='FECHA',
    y='SENTIMENT',
    color=alt.Color('SENTIMENT:N', scale=alt.Scale(domain=['Positivo', 'Neutro', 'Negativo'], range=['royalblue', 'skyblue', 'red'])),
    tooltip=['FECHA', 'SENTIMENT']
)
st.altair_chart(fecha_chart, use_container_width=True)
#_________________________________________________
###############
# POR DIA DE SEMANA
###############
# Para el primer gráfico, agrupa por día de la semana y el criterio de clasificación
df_day_sentiment = df_filtered.groupby([df_filtered['FECHA'].dt.day_name(), 'SENTIMENT']).size().reset_index(name='counts')

# Pivotea los datos para que 'SENTIMENT' sean columnas separadas
df_day_sentiment_pivot = df_day_sentiment.pivot(index='FECHA', columns='SENTIMENT', values='counts').fillna(0).reset_index()


# Crear los gráficos con Altair
# Gráfico de barras apiladas por día de la semana
st.subheader('Por Día de la Semana')
day_chart = alt.Chart(df_day_sentiment).mark_bar().encode(
    x='FECHA:N',
    y=alt.Y('counts:Q', stack='zero'),
    color=alt.Color('SENTIMENT:N', scale=alt.Scale(domain=['Positivo', 'Neutro', 'Negativo'], range=['royalblue', 'skyblue', 'red'])),
    tooltip=['FECHA', 'SENTIMENT', 'counts']
).properties(
    width=600,
    height=300
)
st.altair_chart(day_chart, use_container_width=True)
#_________________________________________________

###############
# POR SENTIMIENTO
###############

# Para el segundo gráfico, cuenta las ocurrencias de cada clasificación
df_sentiment_counts = df_filtered['SENTIMENT'].value_counts().reset_index()
df_sentiment_counts.columns = ['SENTIMENT', 'counts']



# Gráfico de barras para positivas, neutrales y negativas
st.subheader('Positivas, Neutras y Negativas')
sentiment_chart = alt.Chart(df_sentiment_counts).mark_bar().encode(
    x='SENTIMENT:N',
    y='counts:Q',
    color=alt.Color('SENTIMENT:N', scale=alt.Scale(domain=['Positivo', 'Neutro', 'Negativo'], range=['royalblue', 'skyblue', 'red'])),
    tooltip=['SENTIMENT', 'counts']
).properties(
    width=600,
    height=300
)
st.altair_chart(sentiment_chart, use_container_width=True)

#_________________________________________________
# VISUALIZACIÓN DE RESEÑAS
st.header("TOP 10 reseñas")
df_Positivas = df_filtered[["REVIEW","FECHA","GRUPO","SCORE"]]
df_Positivas = df_Positivas.sort_values("SCORE", ascending=False)
df_Positivas =df_Positivas.head(5)

with st.expander("Reseñas más positivas"):

    st.dataframe(
        df_Positivas,
        column_config={
            "FECHA":"Fecha",
            "REVIEW":"Reseña",
            "GRUPO":"Grupo",
        },
        hide_index=True,
    )

df_Negatiavas = df_filtered[["REVIEW","FECHA","GRUPO","SCORE"]]
df_Negatiavas = df_Negatiavas.sort_values("SCORE", ascending=True)
df_Negatiavas =df_Negatiavas.head(5)

with st.expander("Reseñas más negativas"):

    st.dataframe(
        df_Negatiavas,
        column_config={
            "FECHA":"Fecha",
            "REVIEW":"Reseña",
            "GRUPO":"Grupo",
        },
        hide_index=True,
    )

#############################
# COMPARATIVA
# Sentimiento
# Calcula la fecha del mes pasado
hoy = datetime.now()
hoy = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
mes_pasado = hoy - timedelta(days=hoy.day)
mes_pasado = mes_pasado.replace(day=1)

semana_pasada = hoy - timedelta(days=hoy.weekday() + 7)
semana_presente = hoy - timedelta(days=hoy.weekday())
ayer = hoy - timedelta(days=1)
ayer = ayer.replace(hour=0, minute=0, second=0, microsecond=0)

# Filtra las reseñas del mes actual, el mes pasado, la semana pasada y ayer
reseñas_mes_actual = df[(df['FECHA'] >= hoy) & (df['FECHA'] < hoy + pd.DateOffset(months=1))]
reseñas_mes_pasado = df[(df['FECHA'] >= mes_pasado) & (df['FECHA'] < hoy)]
reseñas_semana_pasada = df[(df['FECHA'] >= semana_pasada) & (df['FECHA'] < hoy)]
reseñas_semana_presente = df[(df['FECHA'] >= semana_presente) & (df['FECHA'] < hoy)]
reseñas_ayer = df[(df['FECHA'] >= ayer) & (df['FECHA'] <= hoy)]
reseñas_hoy = df[df['FECHA'] >= hoy]


#POSITIVAS
#pasado
r_ayer_p = reseñas_ayer.query("SENTIMENT == 'Positivo'").shape[0]
r_semana_p = reseñas_semana_pasada.query("SENTIMENT == 'Positivo'").shape[0]
r_mes_p = reseñas_mes_pasado.query("SENTIMENT == 'Positivo'").shape[0]

#presente
r_hoy_p = reseñas_hoy.query("SENTIMENT == 'Positivo'").shape[0]
r_semanaA_p = reseñas_semana_presente.query("SENTIMENT == 'Positivo'").shape[0]
r_mesA_p = reseñas_mes_actual.query("SENTIMENT == 'Positivo'").shape[0]

# Calcula las diferencias porcentuales
dif_d_e = f"{int(((r_hoy_p - r_ayer_p) / (r_ayer_p + 1)) * 100)}%"
dif_semana_e = f"{int(((r_semanaA_p - r_semana_p) / (r_semana_p + 1)) * 100)}%"
dif_mes_e = f"{int(((r_mesA_p - r_mes_p) / (r_mes_p + 1)) * 100)}%"

# Neutras
# pasado
r_ayer_n = reseñas_ayer.query("SENTIMENT == 'Neutro'").shape[0]
r_semana_n = reseñas_semana_pasada.query("SENTIMENT == 'Neutro'").shape[0]
r_mes_n = reseñas_mes_pasado.query("SENTIMENT == 'Neutro'").shape[0]

# presente
r_hoy_n = reseñas_hoy.query("SENTIMENT == 'Neutro'").shape[0]
r_semanaA_n = reseñas_semana_presente.query("SENTIMENT == 'Neutro'").shape[0]
r_mesA_n = reseñas_mes_actual.query("SENTIMENT == 'Neutro'").shape[0]

# Calcula las diferencias porcentuales
dif_d_n = f"{int(((r_hoy_n - r_ayer_n) / (r_ayer_n + 1)) * 100)}%"
dif_semana_n = f"{int(((r_semanaA_n - r_semana_n) / (r_semana_n + 1)) * 100)}%"
dif_mes_n = f"{int(((r_mesA_n - r_mes_n) / (r_mes_n + 1)) * 100)}%"

# Negativas
# pasado
r_ayer_neg = reseñas_ayer.query("SENTIMENT == 'Negativo'").shape[0]
r_semana_neg = reseñas_semana_pasada.query("SENTIMENT == 'Negativo'").shape[0]
r_mes_neg = reseñas_mes_pasado.query("SENTIMENT == 'Negativo'").shape[0]

# presente
r_hoy_neg = reseñas_hoy.query("SENTIMENT == 'Negativo'").shape[0]
r_semanaA_neg = reseñas_semana_presente.query("SENTIMENT == 'Negativo'").shape[0]
r_mesA_neg = reseñas_mes_actual.query("SENTIMENT == 'Negativo'").shape[0]

# Calcula las diferencias porcentuales
dif_d_neg = f"{int(((r_hoy_neg - r_ayer_neg) / (r_ayer_neg + 1)) * 100)}%"
dif_semana_neg = f"{int(((r_semanaA_neg - r_semana_neg) / (r_semana_neg + 1)) * 100)}%"
dif_mes_neg = f"{int(((r_mesA_neg - r_mes_neg) / (r_mes_neg + 1)) * 100)}%"

# Llenar los espacios "VACIO" en la interfaz
st.header('Comparativa')
tab1, tab2, tab3 = st.tabs(["Mes Pasado", "Semana Pasada", "Ayer"])
with tab1:
    with st.container():
        st.subheader("Diferencia mes pasado | mes actual")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Positivas", r_mes_p, dif_mes_e)
        col2.metric("Neutrales", r_mes_n, dif_mes_n)
        col3.metric("Negativas", r_mes_neg, dif_mes_neg)

with tab2:
    with st.container():
        st.subheader("Diferencia semana pasada | semana presente")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Positivas", r_semana_p, dif_semana_e)
        col2.metric("Neutrales", r_semana_n, dif_semana_n)
        col3.metric("Negativas", r_semana_neg, dif_semana_neg)

with tab3:
    with st.container():
        st.subheader("Diferencia ayer | hoy")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Positivas", r_ayer_p, f"{dif_d_e}")
        col2.metric("Neutrales", r_ayer_n, f"{dif_d_n}")
        col3.metric("Negativas", r_ayer_neg, f"{dif_d_neg}")
