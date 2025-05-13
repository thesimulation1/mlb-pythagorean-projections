import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pybaseball import schedule_and_record
import time

st.set_page_config(page_title="Pythagorean by Team", page_icon="📈", layout="wide")


team_list = ['CLE', 'LAA', 'CHC', 'COL', 'MIL', 'STL', 'PHI', 'TOR', 'OAK',
       'HOU', 'TEX', 'DET', 'BOS', 'ATL', 'PIT', 'NYY', 'SDP', 'MIA',
       'CHW', 'BAL', 'WSN', 'TBR', 'SFG', 'MIN', 'ARI', 'KCR', 'NYM',
       'CIN', 'LAD', 'SEA']


def generate_projections_2024():
    df = pd.read_excel('MLB_Projections_2024.xlsx')
    df_2024_projections = df.copy()
    df_2024_projections['Expected_Win_Percentage'] = 0
    for i in range(len(df_2024_projections)):
        df_2024_projections['Expected_Win_Percentage'].iloc[i] = (df_2024_projections['DC\nRS'].iloc[i])**(1.83)/((df_2024_projections['DC\nRA'].iloc[i])**(1.83) + (df_2024_projections['DC\nRS'].iloc[i])**(1.83))
    df_2024_projections['Expected_Wins'] = df_2024_projections['Expected_Win_Percentage']*162
    df_2024_projections['Expected_Losses'] = 162-df_2024_projections['Expected_Wins']
    df_2024_projections['Year'] = 2024
    df_2024_projections.rename(index={0: "NYY", 1: "TOR", 2: "TBR",3: "BAL", 4: "BOS", 5: "MIN",6: "CLE", 7: "DET", 8: "KCR", 9: "CHW", 10: "HOU", 11: "TEX",
                        12: "SEA", 13: "LAA", 14: "OAK",15: "ATL", 16: "PHI", 17: "NYM", 18: "MIA", 19: "WSN", 20: "STL", 21: "CHC", 22: "MIL", 23: "CIN",
                        24: "PIT", 25: "LAD", 26: "ARI", 27: "SFG", 28: "SDP", 29: "COL"})
    return df_2024_projections

@st.cache_data(show_spinner="Fetching data from API...")
def generate_pythagorean_chart(data):

    fig = px.line(data, x = 'Date', y=['Win_Percentage','SMA10','Expected_Win_Percentage'], title=team,
              # template = 'plotly_dark',
              width=1000, height=600)
    fig.add_hline(y=df_2024.loc[team]['Expected_Win_Percentage'])
        
    fig.update_traces(mode='markers+lines')

    fig.update_yaxes(range=[0, 1])
    return fig

@st.cache_data(show_spinner="Fetching data from API...")
def generate_pythagorean_team(team):
    data = schedule_and_record(2024, team)
    data["Win_Count"]= data["W/L"].str.count('W')
    data["Loss_Count"]= data["W/L"].str.count('L')
    data['Cum_Win_Count'] = data['Win_Count'].cumsum()
    data['Cum_Loss_Count'] = data['Loss_Count'].cumsum()
    data['Cum_Run'] = data['R'].cumsum()
    data['Cum_Run_Allowed'] = data['RA'].cumsum()
    data['Expected_Win_Percentage'] = (data['Cum_Run'])**(1.83)/((data['Cum_Run_Allowed'])**(1.83) + (data['Cum_Run'])**(1.83))
    data['Win_Percentage'] = data['Cum_Win_Count']/(data['Cum_Win_Count']+data['Cum_Loss_Count'])
    data['SMA10'] = data['Win_Percentage'].rolling(10).mean()
    data['CMA30'] = data['Win_Percentage'].expanding(10).mean()
    data['EWM30'] = data['Win_Percentage'].ewm(span=10).mean()
    data['RUNSMA10'] = data['R'].rolling(10).mean()
    data['RUNCMA30'] = data['R'].expanding(10).mean()
    data['RUNEWM30'] = data['R'].ewm(span=10).mean()
    data['Performance'] = data['Win_Percentage'] - data['Expected_Win_Percentage']
    data = data[['Date', 'Tm', 'Home_Away', 'Opp', 'W/L', 'R', 'RA', 'W-L',
     'Win', 'Loss', 'Save', 'Streak', 
       'Expected_Win_Percentage', 'Win_Percentage', 'Performance', 'SMA10', 'CMA30', 'EWM30','RUNSMA10','RUNCMA30','RUNEWM30']]
    return data

def generate_pythagorean_game_filter(data, game_selected):
    data = data.loc[game_selected[0]:game_selected[1]]
    return data

def generate_animated_frames(data):
    dfi = data
    #dfi['Date'] = pd.to_datetime(dfi['Date'])
    start = game_selected[0]
    obs = game_selected[1]

    # new datastructure for animation
    df = pd.DataFrame() # container for df with new datastructure
    for i in np.arange(start,obs):
        dfa = dfi.head(i).copy()
        dfa['ix']=i
        df = pd.concat([df, dfa])
    return df
def generate_animated_plot(df):
    # plotly figure
    fig = px.line(df, x = 'Date', y=['Win_Percentage','SMA10','Expected_Win_Percentage'],
              animation_frame='ix', title=team)

    #fig.add_hline(y=expected_win[1])
    fig.update_traces(mode='markers+lines')

    fig.update_yaxes(range=[0, 1])
# attribute adjusments
    fig.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True
    return fig

df_2024 = generate_projections_2024()



with st.sidebar:
    st.write("Choose a team")
    with st.form("pythagorean_selection"):
        team = st.selectbox("Select a Team",
                            ('CLE', 'LAA', 'CHC', 'COL', 'MIL', 'STL', 'PHI', 'TOR', 'OAK','HOU', 'TEX', 'DET', 'BOS', 'ATL', 'PIT', 'NYY', 'SDP', 'MIA','CHW', 'BAL', 'WSN', 'TBR', 'SFG', 'MIN', 'ARI', 'KCR', 'NYM','CIN', 'LAD', 'SEA'),)
        st.form_submit_button("Submit my Selections")

    game_selected = st.slider("Select a range of games", 1, 162, (1, 162))
    
df_2024 = df_2024.rename(index={0: "NYY", 1: "TOR", 2: "TBR",3: "BAL", 4: "BOS", 5: "MIN",6: "CLE", 7: "DET", 8: "KCR", 9: "CHW", 10: "HOU", 11: "TEX",12: "SEA", 13: "LAA", 14: "OAK",15: "ATL", 16: "PHI", 17: "NYM", 18: "MIA", 19: "WSN", 20: "STL",21: "CHC", 22: "MIL", 23: "CIN",24: "PIT", 25: "LAD", 26: "ARI", 27: "SFG", 28: "SDP", 29: "COL"})



choice1 = generate_pythagorean_team(team)
choice2 = generate_pythagorean_game_filter(choice1, game_selected)
choice3= generate_pythagorean_chart(choice2)
choice4 = generate_animated_frames(choice2)
choice5 = generate_animated_plot(choice4)
#choice = generate_pythagorean_chart(team,game_selected)



st.header("Pythagorean Projections")
tab1, tab2 = st.tabs(["Graph", "Table"])
col1, col2 = st.columns(2, gap='small', vertical_alignment="center")

with tab1:
    st.plotly_chart(choice3, use_container_width=True)

with tab2:
        st.dataframe(choice2, use_container_width=True)

st.metric(label="Actual Winning Percentage", value=choice2['Win_Percentage'].tail(1))
st.metric(label="Expected Winning Percentage", value=choice2['Expected_Win_Percentage'].tail(1))
st.metric(label="Difference Winning Percentage", value=choice2['Win_Percentage'].tail(1) - choice2['Expected_Win_Percentage'].tail(1))
st.plotly_chart(choice5)



