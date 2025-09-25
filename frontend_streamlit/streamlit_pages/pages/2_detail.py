import streamlit as st
import requests

API_URL = "http://127.0.0.1:8003"
HEADERS = {
    "X-API-KEY": "secret123",
    "Content-Type": "application/json"
}

st.title("Review Detail")

review_id = st.number_input("Enter Review ID", min_value=1, step=1)

if review_id:
    try:
        # Fetch review by ID - backend must implement this GET endpoint
        res = requests.get(f"{API_URL}/reviews/{review_id}", headers=HEADERS)
        if res.status_code != 200:
            st.error("Review not found.")
        else:
            review = res.json()
            st.write(f"### Review #{review_id}")
            st.write(review['text'])
            st.write(f"Location: {review.get('location', '--')}")
            st.write(f"Rating: {review.get('rating', '--')}")
            st.write(f"Sentiment: {review.get('sentiment', '--')}")
            st.write(f"Topic: {review.get('topic', '--')}")

            # Fetch AI reply (needs backend GET /reviews/{review_id}/reply)
            reply_resp = requests.get(f"{API_URL}/reviews/{review_id}/reply", headers=HEADERS)
            ai_reply = reply_resp.json() if reply_resp.status_code == 200 else None
            
            suggested_reply = st.text_area("Suggested AI Reply", value=ai_reply.get("reply") if ai_reply else "")

            if st.button("Refresh AI Reply"):
                # Trigger backend AI reply generation, no text sending
                post_resp = requests.post(f"{API_URL}/reviews/{review_id}/suggest-reply", headers=HEADERS)
                if post_resp.status_code == 200:
                    st.success("AI Reply refreshed.")
                    updated_reply = post_resp.json().get("reply", "")
                    st.text_area("Suggested AI Reply", value=updated_reply)
                else:
                    st.error("Failed to refresh AI Reply.")

    except Exception as ex:
        st.error(f"Error loading review detail: {ex}")
