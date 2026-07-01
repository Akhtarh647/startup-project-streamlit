import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Page setup
st.set_page_config(layout="wide", page_title="startup analysis")

# Data loading & preprocessing
df = pd.read_csv("startup_clean.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


def load_overall_analysis():
    st.title("Overall Analysis")

    # KPIs calculation
    total = round(df['amount'].sum())
    maximum_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    Average = round(df.groupby('startup')['amount'].sum().mean())
    num_startup = df['startup'].nunique()

    # Display Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Amount", f"{total} CR")
    with col2:
        st.metric("Maximum Funding", f"{maximum_funding} CR")
    with col3:
        st.metric("Average Funding", f"{Average} CR")
    with col4:
        st.metric("Total Startups", str(num_startup))

    # MOM Chart Section
    st.header("MOM Graph")
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    # Uses .size() for Count to capture all records even if 'amount' is NaN
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index(name='value')
    else:
        temp_df = df.groupby(['year', 'month']).size().reset_index(name='value')

    # FIX: Create a real datetime object for the timeline rather than an overcrowded string
    temp_df['date_period'] = pd.to_datetime(temp_df['year'].astype(str) + '-' + temp_df['month'].astype(str) + '-01')
    temp_df = temp_df.sort_values('date_period')

    # Plotting layout
    fig5, ax5 = plt.subplots(figsize=(12, 5))
    ax5.plot(temp_df['date_period'], temp_df['value'], marker='o', color='b' if selected_option == 'Total' else 'g')

    # FIX: Automatically control x-axis intervals so labels don't bunch up
    ax5.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.xticks(rotation=45)
    ax5.set_ylabel('Total Amount (CR)' if selected_option == 'Total' else 'Number of Investments')
    ax5.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    st.pyplot(fig5)


def load_investor_details(investors):
    st.title(investors)

    # Filter dataset for specific investor up front
    investor_mask = df['investor'].str.contains(investors, case=False, na=False)

    # Recent five investments
    last5_df = df[investor_mask].head()[['date', 'startup', 'vertical', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    # First row layout: Biggest Investments and Sector Breakdown
    col1, col2 = st.columns(2)
    with col1:
        big_series = df[investor_mask].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        vertical_series = df[investor_mask].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    # Second row layout: Rounds and Cities
    col3, col4 = st.columns(2)
    with col3:
        round_series = df[investor_mask].groupby('round')['amount'].sum()
        st.subheader('Rounds Invested')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    with col4:
        city_series = df[investor_mask].groupby('city')['amount'].sum()
        st.subheader('Cities Invested')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%1.1f%%')
        st.pyplot(fig3)

    # YOY Investment Block
    st.subheader('YOY Investment')
    year_series = df[investor_mask].groupby('year')['amount'].sum()
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values, marker='o', color='orange')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Total Amount (CR)')
    ax4.grid(True, linestyle='--', alpha=0.5)

    # Formats the X-axis to keep years displayed cleanly as integers
    import matplotlib.ticker as ticker
    ax4.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    st.pyplot(fig4)


# Sidebar layout controls
st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select one", ["Overall Analysis", "Startup", "Investor"])

if option == "Overall Analysis":
    load_overall_analysis()

elif option == "Startup":
    st.sidebar.selectbox("Select Startup", sorted(df["startup"].dropna().unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    st.title("Startup Analysis")

else:
    # Safely unpack and clean comma-separated investor names
    clean_investors = df['investor'].dropna().str.split(',').sum()
    unique_investors = sorted(set([i.strip() for i in clean_investors if i.strip()]))

    selected_investor = st.sidebar.selectbox("Select Investor", unique_investors)
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)