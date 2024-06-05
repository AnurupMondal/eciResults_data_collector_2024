import streamlit as st
import pandas as pd
import requests
import re
import plotly.express as px

def fetch_election_data():
    response = requests.get('http://backend:8000/fetch_election_data')
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from backend.")
        return {}

def format_votes(votes):
    match = re.match(r"^(\d+)\s*\(\s*([+-]\s*\d+)\)$", votes)
    if match:
        main_votes = match.group(1)
        change = match.group(2).replace(" ", "")
        color = "green" if change.startswith('+') else "red"
        return f"{main_votes} (<span style='color:{color}'>{change}</span>)"
    return votes

# Set Streamlit page configuration
st.set_page_config(page_title="2024 Lok Sabha Elections", page_icon="📊", layout="wide")

# Apply custom CSS for table styling
st.markdown(
    """
    <style>
    .dataframe {
        width: 100%;
        text-align: center;
    }
    .dataframe th, .dataframe td {
        text-align: center;
        padding: 8px;
    }
    .centered-title {
        text-align: center;
        font-size: 2em;
        margin-top: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fetch election data
with st.spinner("Loading data..."):
    data_response = fetch_election_data()

election_data = data_response.get("data", {})
timestamp = data_response.get("timestamp", "N/A")

# Display the timestamp in the top left corner
st.markdown(f"**Last Fetched: {timestamp}**", unsafe_allow_html=True)

# Display the title in the center
st.markdown("<h3 class='centered-title'>Election Data for 2024 Lok Sabha Elections</h3>", unsafe_allow_html=True)

if election_data:
    col1, col2 = st.columns(2)

    with col1:
        selected_state = st.selectbox('Select a State/Union Territory', list(election_data.keys()))
    with col2:
        if selected_state:
            selected_constituency = st.selectbox('Select a Constituency', list(election_data[selected_state].keys()))

    if selected_state and selected_constituency:
        st.write(f"Election data:")
        
        election_data_for_constituency = election_data[selected_state][selected_constituency]
        table_data = []
        vote_data = []
        for candidate, party_info in election_data_for_constituency.items():
            for party, votes in party_info.items():
                formatted_votes = format_votes(votes)
                table_data.append({"Candidate": candidate, "Party": party, "Votes": formatted_votes})
                vote_data.append({"Party": party, "Votes": int(votes.split()[0].replace(",", ""))})

        df = pd.DataFrame(table_data)
        df.index = df.index + 1  # Start index from 1

        # Use st.markdown with unsafe_allow_html to display formatted votes
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

        # Plotting the data with Plotly
        vote_df = pd.DataFrame(vote_data)

        fig = px.pie(vote_df, names='Party', values='Votes', hole=0.4, title="Vote Distribution")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            width=800,  # Adjust the width as needed
            height=600  # Adjust the height as needed
        )
        
        st.plotly_chart(fig, use_container_width=True)
