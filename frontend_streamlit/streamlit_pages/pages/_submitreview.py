import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8003"
HEADERS = {
    "X-API-KEY": "secret123",
    "Content-Type": "application/json"
}


st.title("Batch Submit Reviews")

st.write("Paste or type an array of review JSON objects below:")

default_example = """
[
  {
    "review": "Great product, love it!",
    "location": "New York",
    "rating": 5,
    "date": "2025-09-24",
    "topic": "quality"
  },
  {
    "review": "Poor customer service experience.",
    "location": "Chicago",
    "rating": 1,
    "date": "2025-09-23",
    "topic": "service"
  }
]
"""

batch_input = st.text_area("Review JSON Array", value=default_example, height=300)

if st.button("Submit Batch Reviews"):
    try:
        # Parse input JSON
        reviews_list = json.loads(batch_input)
        if not isinstance(reviews_list, list):
            st.error("Input must be a JSON array of review objects.")
        else:
            resp = requests.post(API_URL + "/ingest", headers=HEADERS, json=reviews_list)
            if resp.status_code == 200:
                st.success(f"Inserted {resp.json().get('inserted', 0)} reviews successfully!")
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")
    except json.JSONDecodeError:
        st.error("Invalid JSON format! Please correct and try again.")
    except Exception as ex:
        st.error(f"Submission failed: {ex}")
