import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')
df = pd.read_csv("C:/Users/aa231/OneDrive/Desktop/streamlit/startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'], errors="coerce")
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_investor_detail(investor):
    st.title(investor)
    # Load the recent 5 investments of the investor
    last5_df = df[df["investors"].str.contains(investor)].head()[
        ["date", "startup", "vertical", "city", "round", "amount"]
    ]
    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()

    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    st.subheader('Biggest Investments')
    st.dataframe(big_series)

    
    

    col1, col2 = st.columns(2)
    with col1:
        fig1,ax1 = plt.subplots()
        ax1.bar(big_series.index, big_series.values)
        st.pyplot(fig1)
    
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        fig2,ax2 = plt.subplots()
        ax2.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f")
        st.pyplot(fig2)

    col3, col4 = st.columns(2)
    with col3:
        stage_pie = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        fig3,ax3 = plt.subplots()
        ax3.bar(stage_pie.index, stage_pie.values)
        st.pyplot(fig3)
    
    with col4:
        city_pie = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        fig4,ax4 = plt.subplots()
        ax4.pie(city_pie, labels=city_pie.index, autopct="%0.01f")
        st.pyplot(fig4)
    
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig5,ax5 = plt.subplots()
    ax5.plot(year_series.index, year_series.values)
    st.pyplot(fig5)


    ##### FIND SIMILAR INVESTORS


# load_investor_detail(' IDG Ventures')

def load_overall_analysis():
    st.title('Overall Analysis')

    total = df['amount'].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        
        st.metric('Total', str(round(total)) + ' cr.')

    with col2:
        #max amount infused in a startup
        max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max', str(round(max_funding)) + ' cr.')
    
    with col3:
        #max amount infused in a startup
        avg_funding = df.groupby('startup')['amount'].mean().values[0]
        st.metric('Avg', str(round(avg_funding)) + ' cr.')

    with col4:
        # Total funded startups
        num_startups = df['startup'].nunique()
        st.metric('Funded Startups', num_startups)
    
    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    else:
        temp_df = df.groupby(['year','month'])['amount'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig6,ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig6)


st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Select One", ["Overall Analysis", "Startup", "Investor"])

if option == "Overall Analysis":

    btn1 = st.sidebar.button("Show Overall Analysis")
    # if btn1:
    load_overall_analysis()

elif option == "Startup":
    st.sidebar.selectbox("Select Startup", sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button("Find startup details")
    st.title("Startup Analysis")
elif option == "Investor":
    selected_investor = st.sidebar.selectbox(
        "Select Investor", sorted(set(df["investors"].str.split(",").sum()))
    )
    btn2 = st.sidebar.button("Find Investor details")
    if btn2:
        load_investor_detail(selected_investor)
