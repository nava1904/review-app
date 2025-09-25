import streamlit as st
import requests


API_URL = st.secrets["API_URL"]
API_KEY = st.secrets["API_KEY"]

}


st.title("Inbox")

# Filters & pagination inputs
location = st.text_input("Filter by Location")
sentiment = st.selectbox("Filter by Sentiment", options=["", "POSITIVE", "NEGATIVE", "NEUTRAL"])
search_text = st.text_input("Search Reviews")
page = st.number_input("Page", min_value=1, value=1)
page_size = st.selectbox("Page Size", [5, 10, 20], index=1)

params = {
    "location": location or None,
    "sentiment": sentiment or None,
    "q": search_text or None,
    "page": page,
    "page_size": page_size
}

try:
    with st.spinner("Loading reviews..."):
        resp = requests.get(f"{API_URL}/reviews", params=params, headers=HEADERS)
        if resp.status_code != 200:
            st.error(f"Error loading reviews: {resp.status_code} {resp.text}")
            st.stop()
        reviews = resp.json()
        if not reviews:
            st.info("No reviews found.")
            st.stop()

    st.write("## Reviews")
    for review in reviews:
        st.markdown(f"**Review #{review['id']}** - {review['location']} - Rating: {review['rating']}")
        st.write(review['text'])
        st.caption(f"Sentiment: {review.get('sentiment', '--')} | Topic: {review.get('topic', '--')}")
        st.markdown("---")

except Exception as e:
    st.error(f"Failed to fetch reviews: {e}")
