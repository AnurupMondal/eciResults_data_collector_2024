import requests
from bs4 import BeautifulSoup

def get_state_names():
    url = 'https://results.eci.gov.in/PcResultGenJune2024/index.htm'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    states = {}
    select_element = soup.find('select', {'id': 'ctl00_ContentPlaceHolder1_Result1_ddlState'})
    if select_element is not None:
        for option in select_element.find_all('option'):
            if option['value']:
                states[option['value']] = option.text
    else:
        print("Failed to fetch states.")
    return states

def get_constituency_names(state_value):
    url = f'https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_value}.htm'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    constituency = {}
    select_element = soup.find('select', {'id': 'ctl00_ContentPlaceHolder1_Result1_ddlState'})
    if select_element is not None:
        for option in select_element.find_all('option'):
            if option['value']:
                cleaned_value = option['value'].replace(state_value, '')
                constituency[cleaned_value] = option.text
    else:
        print("Failed to fetch constituency.")
    return constituency

def get_candidate_names(state_value, constituency_value):
    url = f'https://results.eci.gov.in/PcResultGenJune2024/candidateswise-{state_value}{constituency_value}.htm'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    candidate_info = {}
    cards = soup.find('div', {'class': 'row'}).find_all('div', {'class': 'cand-box'})
    if cards:
        for card in cards:
            try:
                name = card.find('div', {'class': 'nme-prty'}).find('h5').text.strip()
                party = card.find('div', {'class': 'nme-prty'}).find('h6').text.strip()
                votes = card.find('div', {'class': 'status'}).find_all('div')[1].text.strip()
                candidate_info[name] = {"party": party, "votes": votes}
            except AttributeError:
                print("Skipping a card due to missing data.")
                continue
    else:
        print("Failed to fetch candidate data.")
    return candidate_info

def scrape_election_data():
    states = get_state_names()
    election_data = {}

    for state_value, state_name in states.items():
        constituencies = get_constituency_names(state_value)
        for constituency_value, constituency_name in constituencies.items():
            candidate_info = get_candidate_names(state_value, constituency_value)
            for candidate_name, details in candidate_info.items():
                if state_name not in election_data:
                    election_data[state_name] = {}
                if constituency_name not in election_data[state_name]:
                    election_data[state_name][constituency_name] = {}
                if candidate_name not in election_data[state_name][constituency_name]:
                    election_data[state_name][constituency_name][candidate_name] = {}
                election_data[state_name][constituency_name][candidate_name][details['party']] = details['votes']
    return election_data