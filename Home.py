import random
#import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import plost
import altair as alt
from datetime import timedelta
import datetime as dt
import numpy as np


#######################################
# PAGE SETUP
#######################################

st.set_page_config(page_title="FK Dashboard", page_icon=":bar_chart:", layout="wide")

alt.themes.enable("dark")

st.subheader("FK investment")
st.markdown("_v0.0.1_")

#graphs will use css
theme_plotly = None

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

list_actions=[
             'ABJC','BICC','BNBC','BOAB','BOABF','BOAC','BOAM','BOAN','BOAS','CABC','CBIBF','CFAC','CIEC','ECOC',
             'ETIT','FTSC','NEIC','NSBC','NTLC','ONTBF','ORAC','ORGT','PALC','PRSC','SAFC','SCRC','SDCC','SDSC','SEMC',
             'SGBC','SHEC','SIBC','SICC','SIVC','SLBC','SMBC','SNTS','SOGC','SPHC','STAC','STBC','SVOC','TTLC',
             'TTLS','UNLC','UNXC']

nv_indice = ['Conso. de Base','Conso discrétionnaire','Energie','Industriels','services Fin.',
             'Serv. Publics','Télécommunication']
anc_indice = ['Agriculture','Distribution','Finance','Industrie','Serv. Publics','Transport','Autres']
sel_indice = ['Nouveau','Ancien']
all_period = ["Année","Semestre","Trimestre","Mois", "2 semaines", "Hebdomadaire"]

with st.sidebar:
     
    sel_tickers = st.multiselect('Selectionner Actions', placeholder="Search tickers", options=list_actions,
                                 default=['BNBC','ABJC'])

    # Date selector
    # cols = st.columns(2)
    start_date = st.date_input('Start Date', value=dt.datetime(2018,1,2), format='YYYY-MM-DD')
    # print(str(start_date) )
    end_date = st.date_input('End Date', value=dt.datetime(2024,3,11), format='YYYY-MM-DD')

    v_periode = st.selectbox('Périodes', all_period)

    v_indices = st.selectbox('Indices', sel_indice)

df = pd.read_excel('C:/Users/ckoupoh/Documents/FK_TRADE/Bul_All_2024_VF.xlsx')
orig_data= df.set_index(['Seance'])  
orig_data = orig_data.sort_index()  

df_idx = pd.read_excel('C:/Users/ckoupoh/Documents/FK_TRADE/All_indices_2024.xlsx')
orig_idx= df_idx.set_index(['Séance'])  
#######################################
# Analyse Indice
#######################################
def plot_metric(label, value, delta, df_val, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode = "number+delta",
            value= value ,
            delta = {"reference": delta, "valueformat": ".2%", "relative":True, 'position' : "bottom"},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 35,
                
            },
            title={
                "text": label,
                "font": {"size": 15},
                 
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=df_val,
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)

prem_val = 0
dern_val = 0
deb_indice =dt.datetime(2023,1,2) 
if deb_indice.date() < start_date:
    prem_val = dt.datetime(2023,1,2)
elif deb_indice.date() < end_date:
    dern_val = dt.datetime(2024,1,2)

VF_idx = orig_idx["BRVM_C"].loc[str(start_date): str(end_date)]
tx_croiss_BRVMC = round(((VF_idx.iloc[-1] / VF_idx.iloc[0])-1)*100,2)

VF_30 = orig_idx["BRVM_30"].loc[str(start_date): str(end_date)]
tx_croiss_BRVM30 = round(((VF_30.iloc[-1] / VF_30.iloc[0])-1)*100,2)

VF_pres = orig_idx["BRVM_PRES"].loc[str(start_date): str(end_date)]
tx_croiss_BRVM_Pres = round(((VF_pres.iloc[-1] / VF_pres.iloc[0])-1)*100,2)

# Allure BRVM Compo, 30, Prest
res = end_date - timedelta(weeks=6)
# print(res)
df_brvmC = orig_idx["BRVM_C"].loc[str(res): str(end_date)]
df_brvm30 = orig_idx["BRVM_30"].loc[str(res): str(end_date)]
df_pres = orig_idx["BRVM_PRES"].loc[str(res): str(end_date)]

st.markdown('#### Analyse Indices du Marché')
st.info('Valeurs des indices au : ' + str(end_date))
total1, total2, total3 = st.columns(3, gap='small')
# print(VF_idx.iloc[0])
with total1:
    plot_metric("BRVM Composite",value=VF_idx.iloc[-1], delta = VF_idx.iloc[0], 
                df_val= VF_idx, prefix="", suffix="", show_graph=True, color_graph="rgba(0, 104, 201, 0.2)")
    
    # st.metric(label="BRVM Composite", value=f"{VF_idx.iloc[-1]: ,.2f}", delta=tx_croiss_BRVMC)

with total2:
    plot_metric("BRVM 30",value=VF_30.iloc[-1], delta = VF_30.iloc[0], 
                df_val= VF_30, prefix="", suffix="", show_graph=True, color_graph="rgba(58, 104, 201, 0.2)")
    # st.metric(label="BRVM 30", value=f"{VF_30.iloc[-1]: ,.2f}", delta=tx_croiss_BRVM30)

with total3:
    plot_metric("BRVM Prestige",value=VF_pres.iloc[-1], delta = VF_pres.iloc[0], 
                df_val= VF_pres, prefix="", suffix="", show_graph=True, color_graph="rgba(58, 104, 201, 0.2)")
    # st.metric(label="BRVM Prestige", value=f"{VF_pres.iloc[-1]: ,.2f}", delta=tx_croiss_BRVM_Pres)

#######################################
# Analyse Indices sectoriels
#######################################
All_idx = orig_idx.loc[str(start_date): str(end_date)]
rent = ((All_idx.iloc[-1]/All_idx.iloc[0])-1)*100
data = {"Indices":rent.index, "Tx Croiss %":rent.values,
       "Nbr sociétés":[46, 30, 10, 37, 11,5, 15,2, 5,7,2]}

df_rk = pd.DataFrame(data)


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/coffee-flavors.csv')

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.subheader('Analyse Indices sectoriels', divider='red')
    m_tab = df_rk.sort_values(by= "Tx Croiss %", ascending = False).reset_index().drop(columns='index')
    st.dataframe(m_tab) 

with col2:
    st.subheader('Perf. Actions', divider='blue')
    fig = go.Figure(go.Sunburst(
    labels=[
        "Serv. publics", "Finances", "Transport","Industrie","Agri.","Distribution","Autres",  # secteurs
        "SNTS", "SDCI","CIEC","ONTBF" ,           # Entreprise SP
        "BICC","BOAB","BOABF","BOAC", "BOAM","BOAN","BOAS","CBIBF","ECOC","ETIT","NSBC","ORGT","SAFC","SGBC","SIBC",  # Entreprise Finance
        "SVOC", "SDSC",                   # Sté Transport
        "CABC","FTSC","NEIC", "NTLC", "SEMC","SLBC","SMBC","STBC", "SVOC","UNLC","UNXC",
        "PALC","SCRC","SICC","SOGC","SPHC",
        "ABJC","BNBC","CFAC","PRSC","SHEC","TTLC","TTLS",
        "STAC","LNBB",
    ],
    parents=[
        "", "", "", "", "" , "", ""  ,                       # Racine (continents n'ont pas de parent)
        "Serv. publics", "Serv. publics","Serv. publics", "Serv. publics", # Afrique → Pays
        "Finances", "Finances","Finances","Finances", "Finances","Finances","Finances", "Finances","Finances","Finances", "Finances","Finances",
        "Finances", "Finances","Finances",# Asie → Pays
        "Transport", "Transport",                      # Sté → Transport,
        "Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie",
        "Agri.","Agri.","Agri.","Agri.","Agri.",
        "Distribution","Distribution","Distribution","Distribution","Distribution","Distribution","Distribution",
        "Autres","Autres",
        
    ],
    values=[100, 100, 120, 100, 100, 100,70,
            40, 20,30, 10,
            5,5,5, 5,1,3, 3,11,14, 11,5,4, 0,18,10,
            50, 70, 
            1, 3,2,26,3,22,14,19,0,9,1,
           39,4,1,29,27,
           4,2,31,5,12,28,17,
           45,25, #info à vérifier
           ],  # Taille/poids de chaque élément 
    branchvalues="total"  # "total" = somme des enfants = parent
))
    fig = go.Figure(go.Sunburst(
    labels=[
        "Serv. publics", "Finances", "Transport","Industrie","Agri.","Distribution","Autres",  # secteurs
        "SNTS", "SDCI","CIEC","ONTBF" ,           # Entreprise SP
        "BICC","BOAB","BOABF","BOAC", "BOAM","BOAN","BOAS","CBIBF","ECOC","ETIT","NSBC","ORGT","SAFC","SGBC","SIBC",  # Entreprise Finance
        "SVOC", "SDSC",                   # Sté Transport
        "CABC","FTSC","NEIC", "NTLC", "SEMC","SLBC","SMBC","STBC", "SVOC","UNLC","UNXC",
        "PALC","SCRC","SICC","SOGC","SPHC",
        "ABJC","BNBC","CFAC","PRSC","SHEC","TTLC","TTLS",
        "STAC","LNBB",
    ],
    parents=[
        "", "", "", "", "" , "", ""  ,                       # Racine (continents n'ont pas de parent)
        "Serv. publics", "Serv. publics","Serv. publics", "Serv. publics", # Afrique → Pays
        "Finances", "Finances","Finances","Finances", "Finances","Finances","Finances", "Finances","Finances","Finances", "Finances","Finances",
        "Finances", "Finances","Finances",# Asie → Pays
        "Transport", "Transport",                      # Sté → Transport,
        "Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie","Industrie",
        "Agri.","Agri.","Agri.","Agri.","Agri.",
        "Distribution","Distribution","Distribution","Distribution","Distribution","Distribution","Distribution",
        "Autres","Autres",
        
    ],
    values=[100, 100, 120, 100, 100, 100,70,
            40, 20,30, 10,
            5,5,5, 5,1,3, 3,11,14, 11,5,4, 0,18,10,
            50, 70, 
            1, 3,2,26,3,22,14,19,0,9,1,
           39,4,1,29,27,
           4,2,31,5,12,28,17,
           45,25, #info à vérifier
           ],  # Taille/poids de chaque élément 
    branchvalues="total"  # "total" = somme des enfants = parent
))
    fig.update_layout(margin = dict(t=10, l=10, r=10, b=10))
    fig.update_traces(textinfo='label+percent entry')

    st.plotly_chart(fig, use_container_width=True)
#######################################
# Analyse Cours Action
#######################################
tab1, tab2, tab3 = st.tabs(['Trade', 'Calculator', 'Portefolio'])

with tab1:
    st.subheader('All Stocks')
    orig_data = orig_data.loc[str(start_date): str(end_date)]
    fig = px.line(orig_data, x=orig_data.index, y=sel_tickers, markers=False)
    fig.add_hline(y=0, line_dash="dash", line_color="white") 
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    # fig.update_yaxes(tickformat=',.0%') 
    st.plotly_chart(fig, use_container_width=True)