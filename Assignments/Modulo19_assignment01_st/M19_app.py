import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import os
import sys
from PIL import Image

custom_params = {"axes.spines.right":True, "axes.spines.top":False}
sns.set_theme(style="darkgrid", palette="flare", rc=custom_params)

@st.cache_data   
def load_data(file_data):
    return pd.read_csv(file_data, sep=';')

def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)


def main():
    st.set_page_config(page_title = "Telemarketing Analysis",
                        page_icon=':telephone_receiver:',
                        layout='wide',
                        initial_sidebar_state='expanded')

    st.title('Telemarketing Analysis')
    st.subheader('Dados dos clientes que receberam ligações de telemarketing')
    st.markdown('---')

    image = Image.open('./img/bank.png')
    st.sidebar.image(image)

    bank_raw = load_data('./data/input/bank-additional-full.csv')
    bank = bank_raw.copy()

    st.write('### Dados ANTES dos filtros')
    st.write(bank_raw.head())

    # Idades 
    with st.sidebar.form(key='my_form'):
        max_age = int(bank.age.max())
        min_age = int(bank.age.min())
        idades = st.slider(label='Idade',
                                min_value=min_age,
                                max_value=max_age,
                                value=(min_age, max_age),
                                step=1)

        st.write('Idades: ', idades)

        # Profissões
        jobs_list = bank.job.unique().tolist()
        jobs_list.append('all')
        jobs_selected = st.multiselect('Profissão', jobs_list, ['all'])

         # Estado civil
        marital_list = bank.marital.unique().tolist()
        marital_list.append('all')
        marital_selected = st.multiselect('Estado Civil', marital_list, ['all'])

         # Default
        default_list = bank.default.unique().tolist()
        default_list.append('all')
        default_selected = st.multiselect('Default', default_list, ['all'])

         # Financiamento imobiliário
        housing_list = bank.housing.unique().tolist()
        housing_list.append('all')
        housing_selected = st.multiselect('Tem financiamento imobiliário?', housing_list, ['all'])

         # Empréstimo
        loan_list = bank.job.unique().tolist()
        loan_list.append('all')
        loan_selected = st.multiselect('Tem empréstimo?', loan_list, ['all'])
         
         # Contato
        contact_list = bank.contact.unique().tolist()
        contact_list.append('all')
        contact_selected = st.multiselect('Meio de contato', contact_list, ['all'])

        # Mês
        month_list = bank.month.unique().tolist()
        month_list.append('all')
        month_selected = st.multiselect('Mês', month_list, ['all'])

        # Dia da semana
        day_of_week_list = bank.day_of_week.unique().tolist()
        day_of_week_list.append('all')
        day_of_week_selected = st.multiselect('Dia da semana', day_of_week_list, ['all'])


        bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                .pipe(multiselect_filter, 'job', jobs_selected)
                .pipe(multiselect_filter, 'marital', marital_selected)
                .pipe(multiselect_filter, 'default', default_selected)
                .pipe(multiselect_filter, 'housing', housing_selected)
                .pipe(multiselect_filter, 'loan', loan_selected)
                .pipe(multiselect_filter, 'contact', contact_selected)
                .pipe(multiselect_filter, 'month', month_selected)
                .pipe(multiselect_filter, 'day_of_week', day_of_week_selected))

        submit_button = st.form_submit_button(label='Aplicar filtros')

    st.write('### Dados DEPOIS dos filtros')
    st.write(bank.head())
    st.markdown('---')

    fig, ax = plt.subplots(1,2, figsize=(4,3))
    fig.tight_layout()

    bank_raw_target_perc = (bank_raw.y.value_counts(normalize=True)).to_frame()*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()

    bank_target_perc = (bank.y.value_counts(normalize=True)).to_frame()*100
    bank_target_perc = bank_target_perc.sort_index()

    sns.barplot(x=bank_raw_target_perc.index,
                y='proportion',
                data=bank_raw_target_perc,
                ax=ax[0],
                color='red',
                palette=['tab:red', 'tab:green'])

    ax[0].bar_label(ax[0].containers[0], fontsize=8)
    ax[0].set_title('Dados brutos',
                   fontweight='bold')
    ax[0].set_xlabel('Aceitou a ligação?', fontdict={'size': 9})
    ax[0].set_ylabel('Porcentagem', fontdict={'size': 9})
    
    sns.barplot(x=bank_target_perc.index,
               y='proportion',
               data=bank_target_perc,
                ax=ax[1],
                color='red',
                palette=['tab:red', 'tab:green'])

    ax[1].bar_label(ax[1].containers[0], fontsize=8)
    ax[1].set_title('Dados filtrados',
                   fontweight='bold')
    ax[1].set_xlabel('Aceitou a ligação?', fontdict={'size': 9})
    ax[1].set_ylabel('Porcentagem', fontdict={'size': 9})

    st.write('### Proporção de aceite da ligação')
    st.pyplot(fig)

if __name__=='__main__':
    main()