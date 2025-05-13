import pandas as pd
import streamlit as st
import time
import numpy as np
import plotly.express as px


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
def filter_dataframe(df, selections):
    if selections:
        filtered_df = df[df['Teams'].isin(selections)]
    else:
        filtered_df = df
    return filtered_df

def generate_team_plot(df):
    fig = px.bar(df, x= 'Teams', y='Expected_Wins')
    return fig




st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# 2024 MLB Projections")
st.sidebar.header("Plotting Demo")
st.write(
    """This page shows the projections for the 2024 MLB season. Please select a team using the dropdown"""
)

df_2024 = generate_projections_2024()

with st.sidebar:
    st.write("Choose a team and a range of games")
    selected_options = st.multiselect("Select a Team",df_2024['Teams'].unique())

filtered_teams = filter_dataframe(df_2024, selected_options)

projection_plot = generate_team_plot(filtered_teams)


st.write(projection_plot)
st.write(filtered_teams)
