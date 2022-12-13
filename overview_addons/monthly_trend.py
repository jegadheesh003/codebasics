import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
import plotly.express as px

def avg_revenue_trend(df):
    ardf=pd.DataFrame(df.groupby("month")["atliqo_revenue_crores"].sum()).reset_index()
    #CHART_REV=avg_rev_trend(ardf,"month","atliqo_revenue_crores")
    #html(CHART_REV, width=650, height=370)
    
    ardf["atliqo_revenue_crores"] = round(ardf["atliqo_revenue_crores"],2)
    fig = px.line(ardf, x="month", y="atliqo_revenue_crores",text="atliqo_revenue_crores",height=300)
    fig.update_traces(textposition="top right",line_color="green")
    fig.update_traces(mode="markers+lines", hovertemplate = 'Revenue: %{y:.2f} Crores<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10),
    hovermode="x"
    )
    st.plotly_chart(fig, use_container_width=True,config={"displayModeBar": False})

def avg_arpu_trend(df):
    arpudf=pd.DataFrame(df.groupby("month")["arpu"].mean()).reset_index()
    arpudf["arpu"] = round(arpudf["arpu"],2)
    fig = px.line(arpudf, x="month", y="arpu",text="arpu",height=300)
    fig.update_traces(textposition="top right",line_color="green")
    fig.update_traces(mode="markers+lines", hovertemplate = 'ARPU: %{y:.2f} Rupees<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10),
    hovermode="x"
    )
    
    st.plotly_chart(fig, use_container_width=True,config={"displayModeBar": False})
    

def avg_active_trend(df):
    actdf=pd.DataFrame(df.groupby("month")["active_users_lakhs"].sum()).reset_index()
    #st.line_chart(actdf)
    actdf["active_users_lakhs"] = round(actdf["active_users_lakhs"],2)
    fig = px.line(actdf, x="month", y="active_users_lakhs",text="active_users_lakhs",height=300)
    fig.update_traces(textposition="top right",line_color="purple")
    fig.update_traces(mode="markers+lines", hovertemplate = 'Users: %{y:.2f} Lakhs<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10),
    hovermode="x"
    )
    
    st.plotly_chart(fig, use_container_width=True,config={"displayModeBar": False})

def avg_unsub_trend(df):
    unsubdf=pd.DataFrame(df.groupby("month")["unsubscribed_users_lakhs"].sum()).reset_index()
    #st.line_chart(unsubdf)
    unsubdf["unsubscribed_users_lakhs"] = round(unsubdf["unsubscribed_users_lakhs"],2)
    fig = px.line(unsubdf, x="month", y="unsubscribed_users_lakhs",text="unsubscribed_users_lakhs",height=300)
    fig.update_traces(textposition="top right",line_color="purple")
    fig.update_traces(mode="markers+lines", hovertemplate = 'Inactive: %{y:.2f} Lakhs<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10),
    hovermode="x"
    )
    st.plotly_chart(fig, use_container_width=True,config={"displayModeBar": False})

"""
def avg_rev_trend(df,x_col,y_col):
    chart = Chart(width="640px", height="360px", display=DisplayTarget.MANUAL)
    data_pd = Data()
    df = df.reset_index()
    data_pd.add_data_frame(df)
    chart.animate(data_pd)
    chart.animate(Config({"y": y_col, "x": x_col, "label": y_col,"geometry": "circle"}))

    #chart.animate(Config({"geometry": "circle"}))
    chart.animate(Config({"geometry": "line"}))
    chart.animate(
    Style({"plot": {"marker": {"colorPalette": "#9355e8FF #123456FF #BDAF10FF"}}})
    )
    return chart._repr_html_()
"""    


def cities(df):
    df["unsub%"] = round((df["unsubscribed_users_lakhs"]/(df["active_users_lakhs"]+df["unsubscribed_users_lakhs"]))*100,2)
    cdf = pd.DataFrame(df.groupby(["city_name"]).agg({"atliqo_revenue_crores":"mean","arpu":"mean","active_users_lakhs":"mean","unsubscribed_users_lakhs":"mean","unsub%":"mean"}))
    cdf.rename(columns={"atliqo_revenue_crores":"Revenue in Crores",
                        "arpu":"ARPU","active_users_lakhs":"Active Users in Lakhs",
                        "unsubscribed_users_lakhs":"Inactive Users in Lakhs","unsub%":"Inactive %"},inplace=True)
    st.dataframe(data=cdf.style.background_gradient(cmap="Greens",axis=0),height=565,use_container_width=True)