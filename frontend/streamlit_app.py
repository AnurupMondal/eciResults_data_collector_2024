import streamlit as st
import pandas as pd
import requests
import re

def fetch_election_data():
    response = requests.get('http://backend:8000/fetch_election_data')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from backend.")
        return {}

def format_votes(votes):
    # Regex to match the vote pattern and change
    match = re.match(r"^(\d+)\s*\(([\+\-]\s*\d+)\)$", votes)
    if match:
        main_votes = match.group(1)
        change = match.group(2).replace(" ", "")
        color = "green" if change.startswith('+') else "red"
        return f"{main_votes} (<span style='color:{color}'>{change}</span>)"
    return votes

# Set Streamlit page configuration
st.set_page_config(page_title="Election Data Viewer", page_icon="📊", layout="wide")

# Fetch election data
data_response = fetch_election_data()
election_data = data_response.get("data", {})
timestamp = data_response.get("timestamp", "N/A")

# Display the timestamp in the top left corner
st.markdown(f"**Last Fetched: {timestamp}**", unsafe_allow_html=True)

st.title('Election Data Viewer')

if election_data:
    selected_state = st.selectbox('Select a State/Union Territory', list(election_data.keys()))
    if selected_state:
        selected_constituency = st.selectbox('Select a Constituency', list(election_data[selected_state].keys()))
        if selected_constituency:
            st.write(f"Selected State/UT: {selected_state}")
            st.write(f"Selected Constituency: {selected_constituency}")
            st.write("Election Data:")

            election_data_for_constituency = election_data[selected_state][selected_constituency]
            table_data = []
            for candidate, party_info in election_data_for_constituency.items():
                for party, votes in party_info.items():
                    formatted_votes = format_votes(votes)
                    table_data.append({"Candidate": candidate, "Party": party, "Votes": formatted_votes})

            df = pd.DataFrame(table_data)
            df.index = df.index + 1  # Start index from 1

            # Use st.markdown with unsafe_allow_html to display formatted votes
            st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
