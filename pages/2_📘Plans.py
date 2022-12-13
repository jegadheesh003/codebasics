import streamlit as st
import json
import requests
import pandas as pd
import overview_addons.plan_overview as plano
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Plans",
    page_icon="📘"
)

@st.experimental_memo
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

planlt = load_lottie("https://assets6.lottiefiles.com/packages/lf20_en58bxwg.json")

col1, col2 = st.columns([1,5])

with col1:
    st_lottie(planlt,key="logo",height=80)
with col2:
    st.header("Plans Analytics")

st.markdown("""---""")

df = pd.read_csv("./plans_revenue.csv")

plano.plan_revenue(df)

st.markdown("""---""")
plano.plan_trends(df)

st.markdown("""---""")
plano.city_plan(df)
#ends here
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)