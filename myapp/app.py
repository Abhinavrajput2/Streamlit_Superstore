import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
# import hydralit_components as hc
import streamlit_authenticator as stauth # pip install streamlit-authenticator
import mymodule
#---USER AUTHENTICATOR--------------------
from streamlit_option_menu import option_menu
from firebase_admin import credentials
from firebase_admin import auth
import json

warnings.filterwarnings('ignore')


st.set_page_config(page_title="Abhinav Superstore!!!", page_icon="chart_with_upwards_trend",layout="wide",initial_sidebar_state="auto")
st.title(" :chart_with_upwards_trend: SuperStore ")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# specify the primary menu definition
menu_data = [
        {'icon': "far fa-copy", 'label':"Left End"},
        {'id':'Copy','icon':"🐙",'label':"Copy"},
        {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
        {'icon': "far fa-address-book", 'label':"Book"},
        {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
        {'icon': "far fa-clone", 'label':"Component"},
        {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
        {'icon': "far fa-copy", 'label':"Right End"},
]
# we can override any part of the primary colors of the menu
#over_theme = {'txc_inactive': '#FFFFFF','menu_background':'red','txc_active':'yellow','option_active':'blue'}
over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(menu_definition=menu_data,home_name='Home',override_theme=over_theme)

    
#get the id of the menu item clicked
st.info(f"{menu_id=}")

tp = st.secrets.type
project_id = st.secrets.project_id
pkid = st.secrets.private_key_id
pk = st.secrets.private_key
cemail = st.secrets.client_email
cid = st.secrets.client_id
auri = st.secrets.auth_uri
turi = st.secrets.token_uri
aprovider = st.secrets.auth_provider_x509_cert_url
cert = st.secrets.client_x509_cert_url
udom = st.secrets.universe_domain

json_data = {
    "type": tp,
    "project_id": project_id,
    "private_key_id": pkid,
    "private_key": pk,
    "client_email": cemail,
    "client_id": cid,
    "auth_uri": auri,
    "token_uri": turi,
    "auth_provider_x509_cert_url": aprovider,
    "client_x509_cert_url": cert,
    "universe_domain": udom
}

json_string = json.dumps(json_data)

cred = credentials.Certificate(json_data)

# firebase_admin.initialize_app(cred,"App")

with st.sidebar:
    selected = option_menu(
        menu_title = "navbar",
        options = ["Account","sales"]
    )

if selected =="Account":
    mymodule.app()
    
   
    


if selected == "sales":


    fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding = "ISO-8859-1")
    else:
        os.chdir(r"/mount/src/streamlit_superstore/myapp/files")
        df = pd.read_csv("Superstore.csv", encoding = "ISO-8859-1")

    col1, col2 = st.columns((2))
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Getting the min and max date 
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()




    st.sidebar.header("Your filter: ")
    # Create for Region
    region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df["Region"].isin(region)]

    # Create for State
    state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2["State"].isin(state)]

    # Create for City
    city = st.sidebar.multiselect("Pick the City",df3["City"].unique())

    # Filter the data based on Region, State and City

    if not region and not state and not city:
        filtered_df = df
    elif not state and not city:
        filtered_df = df[df["Region"].isin(region)]
    elif not region and not city:
        filtered_df = df[df["State"].isin(state)]
    elif state and city:
        filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
    elif region and city:
        filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
    elif region and state:
        filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
    elif city:
        filtered_df = df3[df3["City"].isin(city)]
    else:
        filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

    category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

    with col1:
        st.subheader("Category wise Sales")
        fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)

    with col2:
        st.subheader("Region wise Sales")
        fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
        fig.update_traces(text = filtered_df["Region"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)

    cl1, cl2 = st.columns((2))
    with cl1:
        with st.expander("Category_ViewData"):
            st.write(category_df.style.background_gradient(cmap="Blues"))
            csv = category_df.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                                help = 'Click here to download the data as a CSV file')

    with cl2:
        with st.expander("Region_ViewData"):
            region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
            csv = region.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
            
    filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
    st.subheader('Time Series Analysis')

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
    fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
    st.plotly_chart(fig2,use_container_width=True)

    with st.expander("View Data of TimeSeries:"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

    # Create a treem based on Region, category, sub-Category
    st.subheader("Hierarchical view of Sales using TreeMap")
    fig3 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                    color = "Sub-Category")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3, use_container_width=True)

    chart1, chart2 = st.columns((2))
    with chart1:
        st.subheader('Segment wise Sales')
        fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with chart2:
        st.subheader('Category wise Sales')
        fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
        fig.update_traces(text = filtered_df["Category"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Sub-Category Sales Summary")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
        fig = ff.create_table(df_sample, colorscale = "Cividis")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Month wise sub-Category Table")
        filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
        sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"],columns = "month")
        st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

    # Create a scatter plot
    data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
    data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                        titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                        yaxis = dict(title = "Profit", titlefont = dict(size=19)))
    st.plotly_chart(data1,use_container_width=True)

    with st.expander("View Data"):
        st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

    # Download orginal DataSet
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")
