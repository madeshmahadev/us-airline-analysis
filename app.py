import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("US Airlines Rating Analysis")
st.header("Sample Dashboard to perform Sentiment Analysis on US Domestic Airlines based on Tweets")
st.write("Created by [Madesh Mahadev](https://madeshmahadev.space/)")
st.write("Click here to [View Code](https://github.com/madeshmahadev/us-airline-analysis)")

st.sidebar.header("US Airlines Rating Analysis")

API_URL = ('Tweets.csv')

def load_data():
    data = pd.read_csv(API_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.subheader('***Choose to Generate a Random Tweet***')
random_tweet = st.radio('Sentiment Type',('positive','negative','neutral')) #--> Widget 1
st.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(1).iat[0,0])


st.sidebar.markdown('***Number of Tweets by Sentiment***')
select = st.sidebar.selectbox('Type of Visualization',['Histogram','Pie Chart'], key=1)
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})


#Number of Tweets By Sentiment
if not st.sidebar.checkbox("Hide",False):
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



@st.cache(persist=True)
def plot_sentiment(airline):
    df = data[data['airline']==airline]
    count = df['airline_sentiment'].value_counts()
    count = pd.DataFrame({'Sentiment':count.index, 'Tweets':count.values.flatten()})
    return count


st.sidebar.subheader("Breakdown airline by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways','United','American','Southwest','Delta','Virgin America'))
if len(choice) > 0:
    st.subheader("Breakdown airline by sentiment")
    breakdown_type = st.sidebar.selectbox('Visualization type', ['Pie chart', 'Bar plot', ], key='3')
    fig_3 = make_subplots(rows=1, cols=len(choice), subplot_titles=choice)
    if breakdown_type == 'Bar plot':
        for i in range(1):
            for j in range(len(choice)):
                fig_3.add_trace(
                    go.Bar(x=plot_sentiment(choice[j]).Sentiment, y=plot_sentiment(choice[j]).Tweets, showlegend=False),
                    row=i+1, col=j+1
                )
        fig_3.update_layout(height=600, width=800)
        st.plotly_chart(fig_3)
    else:
        fig_3 = make_subplots(rows=1, cols=len(choice), specs=[[{'type':'domain'}]*len(choice)], subplot_titles=choice)
        for i in range(1):
            for j in range(len(choice)):
                fig_3.add_trace(
                    go.Pie(labels=plot_sentiment(choice[j]).Sentiment, values=plot_sentiment(choice[j]).Tweets, showlegend=True),
                    i+1, j+1
                )
        fig_3.update_layout(height=600, width=800)
        st.plotly_chart(fig_3)
st.sidebar.subheader("Breakdown airline by sentiment")
choice = st.sidebar.multiselect('Pick airlines', ('US Airways','United','American','Southwest','Delta','Virgin America'), key=0)
if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_0 = px.histogram(
                        choice_data, x='airline', y='airline_sentiment',
                         histfunc='count', color='airline_sentiment',
                         facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'},
                          height=600, width=800)
    st.plotly_chart(fig_0)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Close", True, key='3'):
    st.subheader('Word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
