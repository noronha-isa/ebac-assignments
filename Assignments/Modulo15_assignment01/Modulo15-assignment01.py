import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import os
import sys

st.set_page_config(page_title = "Assignment M15",
                    page_icon=':cat:',
                    layout='centered')

st.title('Teste de aplicação de códigos')
st.subheader('Testando códigos aleatórios...')

with st.spinner('Carregando...'):
    time.sleep(2)
st.success('Pronto!')


st.write('----')
st.write('Por motivo nenhum, te apresento meus gatos: ')

col1, col2 = st.columns(2)

with col1:
   st.header("Tagarela")
   st.image("https://github.com/noronha-isa/EBAC_Ciencia_de_dados/blob/main/tagbox2.jpg?raw=true")

with col2:
   st.header("Dona Matilde")
   st.image("https://github.com/noronha-isa/EBAC_Ciencia_de_dados/blob/main/gatajulgando.jpg?raw=true")

# Expandir explicação
with st.expander("Quer saber mais?"):
    st.write("D. Matilde é uma gata senhora que adora uma coçadinha no pescoço. Tagarela é, digamos, mais falante, e pede muita atenção. Os dois odeiam que eu faça cursos, mas acompanham todo o processo.")

gostou = st.radio(
    "Gostou dos meus gatos? ",
    ["Prefiro cachorros", "SIMMM","Odeio animais :imp:"])

if gostou == "Prefiro cachorros":
    st.write('Ok, eu gosto de cachorros também :) :dog:')
elif gostou == "SIMMM":
    st.balloons()
    st.write(':rainbow[YEEEEEEEES]')
else:
    st.write("Não confio em você.")

st.write('----')

# Usando o dataframe pronto do Seaborn

st.subheader("Mudando de Assunto...")
df = sns.load_dataset("penguins")

st.write("Carregando o dataset de pinguins do Seaborn")
st.write(df.head())

# limpando o df

df = df.fillna(df.mode(0).iloc[-1])

st.write("Histograma de espécies")
especies = df.species.value_counts()
st.write(data=especies, x='Espécies', y='Nº de indivíduos', color='orangered')
st.bar_chart(especies)

st.write("Gráfico de distribuição")

st.scatter_chart(data=df, x='flipper_length_mm', y="body_mass_g", color='species')

