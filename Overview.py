import streamlit as st
import requests
import pandas as pd
import overview_addons.monthly_trend as mtrend
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="Overview",
    page_icon="📡"
    )

@st.experimental_memo
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lt = load_lottie("https://assets7.lottiefiles.com/packages/lf20_55bbjdzw.json")
lt2 = load_lottie("https://assets3.lottiefiles.com/packages/lf20_jdwwew5g.json")
cal = load_lottie("https://assets6.lottiefiles.com/packages/lf20_crjmqokf.json")
loc = load_lottie("https://assets9.lottiefiles.com/private_files/lf30_ed9sjb8t.json")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

col1, col2 = st.columns([1,5])

with col1:
    st_lottie(lt2,key="logo",height=80)
with col2:
    st.header("Atliquo Telecom - Performance")

st.markdown("""---""")

df = pd.read_csv("atliqo_report.csv")

#the actual code

overall_avg_revenue = round(pd.DataFrame(df.groupby("month")["atliqo_revenue_crores"].sum())["atliqo_revenue_crores"].mean(),1)
overall_avg_arpu = round(pd.DataFrame(df.groupby("month")["arpu"].mean())["arpu"].mean(),1)
overall_avg_active = round(pd.DataFrame(df.groupby("month")["active_users_lakhs"].sum())["active_users_lakhs"].mean(),1)
overall_avg_unsub = round(pd.DataFrame(df.groupby("month")["unsubscribed_users_lakhs"].sum())["unsubscribed_users_lakhs"].mean(),1)

months_select = [True,True,True,True,True,True,True,True]
months = ["1-Jan","2-Feb","3-Mar","4-Apr","6-Jun","7-Jul","8-Aug","9-Sep"]

with st.sidebar:
    with st.expander("Select Month"):
        months_select[0] = st.checkbox('January',value=True)
        months_select[1] = st.checkbox('February',value=True)
        months_select[2] = st.checkbox('March',value=True)
        months_select[3] = st.checkbox('April',value=True)

        months_select[4] = st.checkbox('June',value=True)
        months_select[5] = st.checkbox('July',value=True)
        months_select[6] = st.checkbox('August',value=True)
        months_select[7] = st.checkbox('September',value=True)

mcol1, mcol2, mcol3, mcol4 = st.columns(4)

newdf = df

for i in range(0,8):
    if(months_select[i]==False):
        newdf = newdf[newdf.month!=months[i]]

cities = df.city_name.unique()
cities_selected = [True for i in cities]
with st.sidebar:
    with st.expander("Select the cities"):
        for i in range(0,len(cities)):
            cities_selected[i] = st.checkbox(cities[i],value=True)

for i in range(0,len(cities)):
    if(cities_selected[i]==False):
        newdf  = newdf[newdf.city_name!=cities[i]]

with st.sidebar:
    with st.expander("Select 5G Status"):
        time_period = st.radio(
        "",
        ('All time', 'Before 5G', 'After 5G'))


if(time_period=="Before 5G"):
    newdf = newdf[newdf["5G"]=="Before 5G"]
if(time_period=="After 5G"):
    newdf = newdf[newdf["5G"]=="After 5G"]

avg_revenue = round(pd.DataFrame(newdf.groupby("month")["atliqo_revenue_crores"].sum())["atliqo_revenue_crores"].mean(),1)
avg_arpu = round(pd.DataFrame(newdf.groupby("month")["arpu"].mean())["arpu"].mean(),1)
avg_active = round(pd.DataFrame(newdf.groupby("month")["active_users_lakhs"].sum())["active_users_lakhs"].mean(),1)
avg_unsub = round(pd.DataFrame(newdf.groupby("month")["unsubscribed_users_lakhs"].sum())["unsubscribed_users_lakhs"].mean(),1)

def find_delta(val,actual):
    pct = round((val/actual)*100,2)
    if(val<actual):
        pct = round(100 - pct,2)
        return str(-1*pct)+"%"
    return str(pct)+"%"

with mcol1:
    st.subheader("Avg Revenue")
    st.metric(label="Monthly (in crores)",value="₹ "+str(avg_revenue),delta=find_delta(avg_revenue,overall_avg_revenue))

with mcol2:
    st.subheader("Avg ARPU")
    st.metric(label="Monthly",value="₹ "+str(avg_arpu),delta=find_delta(avg_arpu,overall_avg_arpu))

with mcol3:
    st.subheader("Active Users")
    st.metric(label="Monthly (in lakhs)",value=str(avg_active),delta=find_delta(avg_active,overall_avg_active))

with mcol4:
    st.subheader("Unsubscribers")
    st.metric(label="Monthly (in lakhs)",value=str(avg_unsub),delta=find_delta(avg_unsub,overall_avg_unsub))
st.write("")
st.caption("*ARPU - Average Revenue Per User")

st.markdown("""---""")

#monthly trend

mcol1, mcol2 = st.columns([1,5])

with mcol1:
    st_lottie(cal,key="calender",height=50)
with mcol2:
    st.subheader("Monthly Trend of KPIs")






t1,t2,t3,t4 = st.tabs(["💵 Revenue","💹 ARPU","👤 Active Users","⚠️ Unsubscribers"])
with t1:
    mtrend.avg_revenue_trend(newdf)
with t2:
    mtrend.avg_arpu_trend(newdf)
with t3:
    mtrend.avg_active_trend(newdf)
with t4:
    mtrend.avg_unsub_trend(newdf)

st.write("")
st.markdown("""---""")
#city
ccol1, ccol2 = st.columns([1,5])

with ccol1:
    st_lottie(loc,key="location",height=50)
with ccol2:
    st.subheader("Cities and KPIs")

mtrend.cities(newdf)

#ends here
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)