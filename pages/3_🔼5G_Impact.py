import streamlit as st
import requests
import pandas as pd
from streamlit_lottie import st_lottie
import overview_addons.metric5g as metric5g
import overview_addons.market5g as market5g
st.set_page_config(
    page_title="5G Impact",
    page_icon="🔼"
)

@st.experimental_memo
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

fivelt = load_lottie("https://assets8.lottiefiles.com/packages/lf20_8RLUIE.json")

col1, col2 = st.columns([1,5])

with col1:
    st_lottie(fivelt,key="logo",height=80)
with col2:
    st.header("Impact of 5G")


tab1,tab2 = st.tabs(["Revenue & Users","Market Share"])

overdf = pd.read_csv("./atliqo_report.csv")
marketdf=pd.read_csv("./market_share.csv")

with tab1:
    metric5g.display_metric(overdf)
with tab2:
    market5g.display_market(marketdf)

#ends here
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)