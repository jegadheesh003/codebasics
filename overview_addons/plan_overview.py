import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
import plotly.express as px

def plan_revenue(df):
    ndf=pd.DataFrame(df.groupby(["plan_def"])["plan_revenue_crores"].sum()).reset_index().sort_values(by="plan_revenue_crores",ascending=False)
    ndf.rename(columns={'plan_def':'Plans','plan_revenue_crores':'Total Revenue in crores'},inplace=True)
    fig = px.bar(ndf,y="Plans",x="Total Revenue in crores",height=400,color="Plans",color_discrete_sequence=px.colors.sequential.Blugrn)
    fig.update_traces(hovertemplate = 'Revenue: %{x:.2f}<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)        
    )
    st.subheader("Total Revenue of Plans")
    st.plotly_chart(fig, use_container_width=True,config={"displayModeBar": False})

def plan_trends(df):
    mdf = pd.DataFrame(df.groupby(["month","plan_def"])["plan_revenue_crores"].mean().reset_index())
    fig = px.line(mdf, x="month", y="plan_revenue_crores",color="plan_def",height=450,color_discrete_sequence=px.colors.sequential.Blugrn,hover_name="plan_def",hover_data={"plan_revenue_crores":True,"month":False,"plan_def":False})
    fig.update_traces(textposition="top right")
    fig.update_traces(mode="markers+lines")
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="Revenue in Crores")
    fig.update_xaxes(title="Month")
    
    
    #fig.update_traces(mode="markers+lines", hovertemplate = 'Revenue: %{y:.2f}Crores<extra></extra>')
    fig.update_layout(
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)
    )
    st.subheader("Monthly Revenue Trend")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})

def city_plan(df):
    plans_list=df.plan_def.unique()
    plan = st.selectbox(
    'Select a Plan',
    plans_list)
    df=df[df.plan_def==plan]
    df["monthly_revenue"] = df["plan_revenue_crores"]
    cpdf=pd.DataFrame(df.groupby(["city"]).agg({"plan_revenue_crores":"sum","monthly_revenue":"mean"}))
    cpdf.rename(columns={"plan_revenue_crores":"Total Revenue in Crores","monthly_revenue":"Monthly Revenue"},inplace=True)
    st.dataframe(data=cpdf.style.background_gradient(cmap="YlGn",axis=0),height=565,use_container_width=True)
