import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="startup analysis")

df=pd.read_csv("startup_clean.csv")
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_overall_analysis():
    st.title("overall analysis")
    #Total Invested Amount
    total = round(df['amount'].sum())

    #Maximum Amount infused in startup
    maximum_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    #Average
    Average = round(df.groupby('startup')['amount'].sum().mean())

    #Total funded startups
    num_startup=df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Amount", str(total) + " CR")

    with col2:
        st.metric("maximum_funding", str(maximum_funding) + " CR")

    with col3:
        st.metric("Average_funding", str(Average) + " CR")

    with col4:
        st.metric("Total Startups", str(num_startup) )

    st.header("MOM grapg")
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x-axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype('str')
    temp_df[['amount', 'x-axis']]
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x-axis'], temp_df['amount'])
    st.pyplot(fig5)


def load_investor_details(investors):
    st.title(investors)
    #load recent five investments
    last5_df=df[df['investor'].str.contains(investors)].head()[['date', 'startup', 'vertical', 'round', 'amount']]
    st.subheader('most recent investor')
    st.dataframe(last5_df)

    clo1,col2 = st.columns(2)
    #biggest investments
    with clo1:
        big_series = df[df['investor'].str.contains(investors)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investor'].str.contains(investors)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%1.1f%%')
        st.pyplot(fig1)
    clo3, col4 = st.columns(2)

    with clo3:
        round=df[df['investor'].str.contains(investors)].groupby('round')['amount'].sum()
        st.subheader('Rounds invested')
        fig2, ax2 = plt.subplots()
        ax2.pie(round, labels=round.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    with col4:
        city=df[df['investor'].str.contains(investors)].groupby('city')['amount'].sum()
        st.subheader('Cities invested')
        fig3, ax3 = plt.subplots()
        ax3.pie(city, labels=city.index, autopct='%1.1f%%')
        st.pyplot(fig3)

    df['year']=df['date'].dt.year
    year_series=df[df['investor'].str.contains('IDG Ventures')].groupby('year')['amount'].sum()
    st.subheader('YOY Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)




st.sidebar.title("Startup Funding Analysis")

option=st.sidebar.selectbox("Select one",["overall Analysis", "startup","Investor"])

if option=="overall Analysis":
    load_overall_analysis()
elif option=="startup":
    # Changed from title to selectbox
    st.sidebar.selectbox("Select startup",sorted(df["startup"].unique().tolist()))
    btn1=st.sidebar.button("find startup details")
    st.title("startup analysis")
else:
    # Changed from title to selectbox
    selected_investor=st.sidebar.selectbox("Select Investor",sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button("find investors details")
    if btn2:
        load_investor_details(selected_investor)
