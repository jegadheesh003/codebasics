import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
import plotly.express as px

def percentage_formater(p,c):
    if(p<=0):
        comp = '<p>'+c+'</p><br>'
        original_title = '<p style="color:Red; font-size: 25px; ">'+"↓ "+str(p)+" %"+'</p>'
        div = '<div style="background-image: linear-gradient(to right,rgba(255, 153, 128,0.2), rgba(255, 112, 77,0.0));padding:5px;text-align:center;border-radius:10px;">'+c+original_title+'</div>'
    elif(p>0):
        comp = '<p >'+c+'</p><br>'
        original_title = '<p style="color:Green; font-size: 25px;">'+"↑ "+str(p)+" %"+'</p>'
        div = '<div style="background-image: linear-gradient(to right,rgba(102, 255, 204,0.2), rgba(0, 204, 163,0.0));padding:5px;text-align:center;border-radius:10px;">'+c+original_title+'</div>'
    return div

def city_share(df):

    st.subheader("Total Market Value of the Cities")
    st.write("")
    bdf = pd.DataFrame(df[df["5G"]=="Before 5G"].groupby(["city"])["tmv_city_crores"].mean()).reset_index()
    bdf.rename(columns={"tmv_city_crores":"Before 5G"},inplace=True)
    adf = pd.DataFrame(df[df["5G"]=="After 5G"].groupby(["city"])["tmv_city_crores"].mean()).reset_index()
    adf.rename(columns={"tmv_city_crores":"After 5G"},inplace=True)
    tdf=bdf.merge(adf,on="city",how="left")
    tdf["Change %"] = ((tdf["After 5G"] - tdf["Before 5G"])/tdf["Before 5G"])*100
    st.dataframe(tdf.style.background_gradient(cmap="Greens",axis=0),height=565,use_container_width=True)
def market_share_change(df):

    st.subheader("Change in Market Share Value of Companies")
    st.write("")
    companies = df.company.unique()
    col=[0 for i in companies]
    before_df = [0 for i in companies]
    after_df = [0 for i in companies]
    before_share = [0 for i in companies]
    after_share = [0 for i in companies]
    col[0],col[1],col[2],col[3],col[4] = st.columns(len(companies))
    for i in range(0,len(companies)):
        cdf = df[df.company==companies[i]]
        bdf = cdf[cdf["5G"]=="Before 5G"]
        adf = cdf[cdf["5G"]=="After 5G"]
        before_df[i]=pd.DataFrame(bdf.groupby(["time_period"])["share"].sum())
        after_df[i]=pd.DataFrame(adf.groupby(["time_period"])["share"].sum())
        before_share[i] = before_df[i]["share"].mean()
        after_share[i] = after_df[i]["share"].mean()
        cng = round(((after_share[i] - before_share[i])/before_share[i])*100,2)
       
        with col[i]:
            #st.markdown("*"+companies[i]+"*")
            st.markdown(percentage_formater(cng,companies[i]),unsafe_allow_html=True)
         
    dict1 ={"Company":companies,"Revenue":before_share,"5G":"Before 5G"}
    dict2 ={"Company":companies,"Revenue":after_share,"5G":"After 5G"}
    sharedf1 = pd.DataFrame(dict1)
    sharedf2 = pd.DataFrame(dict2)
    sharedf = pd.concat([sharedf1,sharedf2])
    sharedf = sharedf.reset_index()
    sharedf.drop(columns=["index"],inplace=True)
    fig = px.bar(sharedf, y="Revenue", x="Company", color="5G", barmode="group",height=300,color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_traces(hovertemplate = 'Share: %{y:.2f}<extra></extra>')
    fig.update_layout(
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)        
    )
    st.write("")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    st.markdown("---")
    city_share(df)


def display_market(df):
    market_share_change(df)