import streamlit as st
import pandas as pd
import requests

def fetch_election_data():
    response = requests.get('http://backend:8000/fetch_election_data')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from backend.")
        return {}

# Streamlit UI
st.title('Election Data Viewer')

election_data = fetch_election_data()

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
                    table_data.append({"Candidate": candidate, "Party": party, "Votes": votes})

            df = pd.DataFrame(table_data)
            df.index = df.index + 1  # Start index from 1
            st.table(df)
