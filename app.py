import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("US Airlines Rating Analysis")
st.header("Sample Dashboard to perform Sentiment Analysis on US Domestic Airlines based on Tweets")

st.sidebar.header("US Airlines Rating Analysis")

API_URL = ('Tweets.csv')

def load_data():
    data = pd.read_csv(API_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.subheader('***Generate Random Tweets***')
random_tweet = st.radio('Sentiment Type',('positive','negative','neutral')) #--> Widget 1
st.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(1).iat[0,0])


st.sidebar.markdown('***Number of Tweets by Sentiment***')
select = st.sidebar.selectbox('Type of Visualization',['Histogram','Pie Chart'], key=1)
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})


#Number of Tweets By Sentiment
if not st.sidebar.checkbox("Hide",True):
    st.markdown("### Number of Tweets By Sentiment")
    if select == "Histogram":
        fig  = px.bar(sentiment_count, x='Sentiment',y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig  = px.pie(sentiment_count, values='Tweets', names="Sentiment")
        st.plotly_chart(fig)

#Where the users are tweeting from
st.sidebar.markdown('***Where the users are tweeting from***')
hour = st.sidebar.slider("Hour of the day",0,23)

modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key=1):
    st.markdown("### ***Tweet Locations based on the  time of the day***")
    st.markdown("%i tweets between ***%i:00*** and ***%i:00*** hours" % (len(modified_data),hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)


st.sidebar.subheader("Total number of tweets for each airline")
each_airline = st.sidebar.selectbox("Visualization Type", ['Bar plot','Pie Chart'], key='2')
airline_sentiment_count = data.groupby('airline')['airline_sentiment'].count().sort_values(ascending=False)
airline_sentiment_count = pd.DataFrame({'Airline':airline_sentiment_count.index, 'Tweets':airline_sentiment_count.values.flatten()})
if not st.sidebar.checkbox("Close", True, key='2'):
    if each_airline =="Bar plot":
        st.subheader("Total number of tweets for each Airline")
        fig_1 = px.bar(airline_sentiment_count, x='Airline', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig_1)
    if each_airline =="Pie Chart":
        st.subheader("Total number of tweets for each Airline")
        fig_2 = px.pie(airline_sentiment_count, values='Tweets', names='Airline')
        st.plotly_chart(fig_2)
