import streamlit as st
import requests
import pandas as pd
from streamlit_lottie import st_lottie
from streamlit.components.v1 import html
import plotly.express as px

st.set_page_config(
    page_title="Competition",
    page_icon="💹"
)

@st.experimental_memo
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
clogo = load_lottie("https://assets5.lottiefiles.com/packages/lf20_t5xpcbcq.json")




#starts here

col1, col2 = st.columns([1,5])

with col1:
    st_lottie(clogo,key="logo",height=80)
with col2:
    st.header("Competition Analysis")

st.markdown("""---""")

#total share

df = pd.read_csv("./market_share.csv")
newdf = df

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

cities = df.city.unique()
cities_selected = [True for i in cities]
with st.sidebar:
    with st.expander("Select the cities"):
        for i in range(0,len(cities)):
            cities_selected[i] = st.checkbox(cities[i],value=True)

for i in range(0,len(cities)):
    if(cities_selected[i]==False):
        newdf  = newdf[newdf.city!=cities[i]]

with st.sidebar:
    with st.expander("Select 5G Status"):
        time_period = st.radio(
        "",
        ('All time', 'Before 5G', 'After 5G'))


if(time_period=="Before 5G"):
    newdf = newdf[newdf["5G"]=="Before 5G"]
if(time_period=="After 5G"):
    newdf = newdf[newdf["5G"]=="After 5G"]

ndf=pd.DataFrame(newdf.groupby("company")["share"].mean()).reset_index()
ndf["share"] = round(ndf["share"],2)
ndf = ndf.sort_values(by="share",ascending=False)

st.subheader("Overall - Marker Share")
st.write("")

comp_col1, comp_col2 = st.columns([3,3])

with comp_col2:
    fig = px.pie(ndf, values="share", names="company", hole=.3,height=200,color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_traces(hovertemplate = 'Share Percentage<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)        
    )
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
with comp_col1:
    fig = px.bar(ndf,x="share",y="company",height=200,color="company",color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_traces(hovertemplate = 'Share: %{x:.2f} Percentage<extra></extra>')
    fig.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)        
    )
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})

st.markdown("""---""")
st.subheader("Market Share Trend")

sdf=pd.DataFrame(newdf.groupby(["month","company"])["ms_pct"].mean()).reset_index()
sdf["share"] = round(sdf["ms_pct"],2) 

fig = px.line(sdf, x="month", y="share",color="company",height=350,color_discrete_sequence=px.colors.qualitative.Vivid)
fig.update_traces(textposition="top right")
fig.update_traces(mode="markers+lines", hovertemplate = 'Revenue: %{y:.2f} Crores<extra></extra>')
fig.update_layout(
plot_bgcolor="white",
margin=dict(t=10,l=10,b=10,r=10),
hovermode="x"
)
st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})

st.markdown("""---""")

#cities

st.subheader("Cities and Shares")

citydf=pd.DataFrame(newdf.groupby("city")["tmv_city_crores"].mean())
company_list = newdf.company.unique()
for i in range(0,len(company_list)):
    cdf  = newdf[newdf.company==company_list[i]]
    cdf = pd.DataFrame(cdf.groupby("city")["ms_pct"].mean())
    cdf.rename(columns={"ms_pct":company_list[i]},inplace=True)
    citydf=pd.merge(citydf, cdf, on = 'city')
    #st.dataframe(cdf)
citydf["tmv_city_crores"] = round(citydf["tmv_city_crores"],1)
citydf.rename(columns={"tmv_city_crores":"Market Value(in crores)"},inplace=True)

st.dataframe(data=citydf.style.background_gradient(cmap="YlGn",axis=0),height=565,use_container_width=True)

#ends here
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)