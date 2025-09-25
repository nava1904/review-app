import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8003"
HEADERS = {
    "X-API-KEY": "secret123",
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
