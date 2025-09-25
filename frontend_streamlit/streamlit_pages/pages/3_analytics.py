import streamlit as st
import requests
import pandas as pd

API_URL = st.secrets["API_URL"]
API_KEY = st.secrets["API_KEY"]

HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

st.title("Analytics Dashboard")

try:
    resp = requests.get(f"{API_URL}/analytics", headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        sentiment_data = pd.DataFrame(list(data['sentiment_counts'].items()), columns=['Sentiment', 'Count'])
        topic_data = pd.DataFrame(list(data['topic_counts'].items()), columns=['Topic', 'Count'])

        st.header("Analysis by Sentiment")
        st.bar_chart(sentiment_data.set_index('Sentiment'))

        st.header("Analysis by Topic")
        st.bar_chart(topic_data.set_index('Topic'))
    else:
        st.error("Failed to load analytics data.")
except Exception as e:
    st.error(f"Error: {e}")
