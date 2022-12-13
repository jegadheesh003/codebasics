import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
import plotly.express as px


def percentage_text_finder(btxt,atxt):
    if(btxt>atxt):
        percentage = abs(round(((atxt-btxt)/btxt)*100,1))
        original_title = '<p style="color:Red; font-size: 50px; ">'+"↓ "+str(percentage)+" %"+'</p>'
    elif(atxt>btxt):
        percentage = round(((atxt-btxt)/btxt)*100,1)
        original_title = '<p style="color:Green; font-size: 50px;">'+"↑ "+str(percentage)+" %"+'</p>'
    return original_title

def percentage_text_finder_small(btxt,atxt):
    if(btxt>atxt):
        percentage = abs(round(((atxt-btxt)/btxt)*100,1))
        original_title = '<p style="color:Red; font-size: 25px; ">'+"↓ "+str(percentage)+" %"+'</p>'
    elif(atxt>btxt):
        percentage = round(((atxt-btxt)/btxt)*100,1)
        original_title = '<p style="color:Green; font-size: 25px;">'+"↑ "+str(percentage)+" %"+'</p>'
    return original_title


def user_impact(before_df,after_df):
    
    st.subheader("Changes in Key Metric - City")
    bdf=pd.DataFrame(before_df.groupby(["city_name"])["atliqo_revenue_crores"].mean()).reset_index()
    adf=pd.DataFrame(after_df.groupby(["city_name"])["atliqo_revenue_crores"].mean()).reset_index()
    metric_df = bdf.merge(adf,on="city_name",how="left")
    metric_df["Revenue"] = ((metric_df["atliqo_revenue_crores_y"] - metric_df["atliqo_revenue_crores_x"])/metric_df["atliqo_revenue_crores_x"])*100
    metric_df.drop(columns=["atliqo_revenue_crores_x","atliqo_revenue_crores_y"],inplace=True)

    bdf=pd.DataFrame(before_df.groupby(["city_name"])["arpu"].mean()).reset_index()
    adf=pd.DataFrame(after_df.groupby(["city_name"])["arpu"].mean()).reset_index()
    arpu_df = bdf.merge(adf,on="city_name",how="left")
    arpu_df["ARPU"] = ((arpu_df["arpu_y"] - arpu_df["arpu_x"])/arpu_df["arpu_x"])*100
    arpu_df.drop(columns=["arpu_x","arpu_y"],inplace=True)

    metric_df = metric_df.merge(arpu_df,on="city_name",how="left")

    bdf=pd.DataFrame(before_df.groupby(["city_name"])["active_users_lakhs"].mean()).reset_index()
    adf=pd.DataFrame(after_df.groupby(["city_name"])["active_users_lakhs"].mean()).reset_index()
    arpu_df = bdf.merge(adf,on="city_name",how="left")
    arpu_df["Active Users"] = ((arpu_df["active_users_lakhs_y"] - arpu_df["active_users_lakhs_x"])/arpu_df["active_users_lakhs_x"])*100
    arpu_df.drop(columns=["active_users_lakhs_x","active_users_lakhs_y"],inplace=True)

    metric_df = metric_df.merge(arpu_df,on="city_name",how="left")

    bdf=pd.DataFrame(before_df.groupby(["city_name"])["unsubscribed_users_lakhs"].mean()).reset_index()
    adf=pd.DataFrame(after_df.groupby(["city_name"])["unsubscribed_users_lakhs"].mean()).reset_index()
    arpu_df = bdf.merge(adf,on="city_name",how="left")
    arpu_df["Inactive Users"] = ((arpu_df["unsubscribed_users_lakhs_y"] - arpu_df["unsubscribed_users_lakhs_x"])/arpu_df["unsubscribed_users_lakhs_x"])*100
    arpu_df.drop(columns=["unsubscribed_users_lakhs_x","unsubscribed_users_lakhs_y"],inplace=True)

    metric_df = metric_df.merge(arpu_df,on="city_name",how="left")
    metric_df.rename(columns={"city_name":"City Name"},inplace=True)
    st.dataframe(metric_df.style.background_gradient(cmap="Greens",axis=0),height=565,use_container_width=True)

def user_metric(before_df,after_df):
    bdf_act=pd.DataFrame(before_df.groupby(["time_period"])["active_users_lakhs"].sum()).reset_index()
    adf_act=pd.DataFrame(after_df.groupby(["time_period"])["active_users_lakhs"].sum()).reset_index()
    bmean_act = bdf_act["active_users_lakhs"].mean()
    amean_act = adf_act["active_users_lakhs"].mean()
    act_chg = round(((amean_act-bmean_act)/bmean_act)*100,2)
    bdf_act["5G"] = "Before 5G"
    adf_act["5G"] = "After 5G"
    act_df = bdf_act.append(adf_act)

    bdf_in=pd.DataFrame(before_df.groupby(["time_period"])["unsubscribed_users_lakhs"].sum()).reset_index()
    adf_in=pd.DataFrame(after_df.groupby(["time_period"])["unsubscribed_users_lakhs"].sum()).reset_index()
    bmean_in = bdf_in["unsubscribed_users_lakhs"].mean()
    amean_in = adf_in["unsubscribed_users_lakhs"].mean()
    in_chg = round(((amean_in-bmean_in)/bmean_in)*100,2)
    bdf_in["5G"] = "Before 5G"
    adf_in["5G"] = "After 5G"
    in_df = bdf_in.append(adf_in)
    st.subheader("Impact on users (Monthly Active and Inactive)")
    st.write("")
    col1, col2,col3 = st.columns([1,2,2])
    
    with col1:
        st.markdown("**_Avg Active users_**")
        st.markdown(percentage_text_finder_small(bmean_act,amean_act),unsafe_allow_html=True)
        st.markdown("**_Avg Inactive users_**")
        st.markdown(percentage_text_finder_small(bmean_in,amean_in),unsafe_allow_html=True)
    with col2:
        st.markdown("**_Active trend_**")
        fig = px.line(act_df, x='time_period', y='active_users_lakhs', color='5G', symbol="5G",height=200)
        fig.update_traces(textposition="top right")
        fig.update_traces(mode="markers+lines", hovertemplate = '%{y:.2f} lakhs<extra></extra>')
        fig.update_layout(
        showlegend=True,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10),
        hovermode="x"
        )
        fig.update_yaxes(title="Users")
        fig.update_xaxes(title="Month")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    with col3:
        st.markdown("**_Inactive trend_**")
        fig = px.line(in_df, x='time_period', y='unsubscribed_users_lakhs', color='5G', symbol="5G",height=200)
        fig.update_traces(textposition="top right")
        fig.update_traces(mode="markers+lines", hovertemplate = '%{y:.2f} lakhs<extra></extra>')
        fig.update_layout(
        showlegend=True,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10),
        hovermode="x"
        )
        fig.update_yaxes(title="")
        fig.update_xaxes(title="Month")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    st.markdown("---")
    user_impact(before_df,after_df)

def avg_arpu(before_df,after_df):
    rev_b=pd.DataFrame(before_df.groupby(["time_period"])["arpu"].mean())
    rev_bf = round(rev_b["arpu"].mean(),2)
    rev_a = pd.DataFrame(after_df.groupby(["time_period"])["arpu"].mean())
    rev_af = round(rev_a["arpu"].mean(),2)

    rev_a["5G"] = "After 5G"
    rev_b["5G"] = "Before 5G"

    rev_a = rev_a.reset_index()
    rev_b = rev_b.reset_index()

    total_rev_df = rev_a.append(rev_b)

    st.subheader("Avg ARPU")
    
    col1,emp,col2 = st.columns([3,1,5])
    col1.markdown(percentage_text_finder(rev_bf,rev_af), unsafe_allow_html=True)

    fig = px.bar(y=[rev_bf,rev_af],x=["Before 5G","After 5G"],text=[rev_bf,rev_af],height=200)
    fig.update_traces(hovertemplate = '%{y:.2f} <extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)        
    )
    #fig.update_layout(yaxis_range=[390,400])
    fig.update_yaxes(title=None)
    fig.update_xaxes(title="In Rupees")
    col1.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    
    with col2:
        fig = px.line(total_rev_df, x='time_period', y='arpu', color='5G', symbol="5G",height=300)
        fig.update_traces(textposition="top right")
        fig.update_traces(mode="markers+lines", hovertemplate = 'ARPU: %{y:.2f} Rupees<extra></extra>')
        fig.update_layout(
        showlegend=True,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10),
        hovermode="x"
        )
        fig.update_yaxes(title="Revenue")
        fig.update_xaxes(title="Month")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    st.markdown("---")
    user_metric(before_df,after_df)

def display_metric(df):

    before_df = df[df["5G"]=="Before 5G"]
    after_df  = df[df["5G"]=="After 5G"]

    rev_b=pd.DataFrame(before_df.groupby(["time_period"])["atliqo_revenue_crores"].sum())
    rev_bf = round(rev_b["atliqo_revenue_crores"].mean(),2)
    rev_a = pd.DataFrame(after_df.groupby(["time_period"])["atliqo_revenue_crores"].sum())
    rev_af = round(rev_a["atliqo_revenue_crores"].mean(),2)

    rev_a["5G"] = "After 5G"
    rev_b["5G"] = "Before 5G"

    rev_a = rev_a.reset_index()
    rev_b = rev_b.reset_index()

    total_rev_df = rev_a.append(rev_b)

    st.subheader("Avg Revenue")
    
    col1,emp,col2 = st.columns([3,1,5])
    col1.markdown(percentage_text_finder(rev_bf,rev_af), unsafe_allow_html=True)

    fig = px.bar(y=[rev_bf,rev_af],x=["Before 5G","After 5G"],text=[rev_bf,rev_af],height=200)
    fig.update_traces(hovertemplate = '%{y:.2f} Crores<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)        
    )
    fig.update_layout(yaxis_range=[390,400])
    fig.update_yaxes(title=None)
    fig.update_xaxes(title="In Crores")
    col1.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    
    with col2:
        fig = px.line(total_rev_df, x='time_period', y='atliqo_revenue_crores', color='5G', symbol="5G",height=300)
        fig.update_traces(textposition="top right")
        fig.update_traces(mode="markers+lines", hovertemplate = 'Revenue: %{y:.2f} Crores<extra></extra>')
        fig.update_layout(
        showlegend=True,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10),
        hovermode="x"
        )
        fig.update_yaxes(title="Revenue")
        fig.update_xaxes(title="Month")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    avg_arpu(before_df,after_df)