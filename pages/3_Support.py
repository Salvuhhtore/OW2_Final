import streamlit as st
import pandas as pd
import altair as alt

# Cache Data
@st.cache_data
def load_data():
    OW2_Data = pd.read_csv('data/OW2_Statistics.csv')
    return OW2_Data

# Load the data
OW2_Data = load_data()

st.header('Hello! Welcome to the :green[Support] Role!')
st.subheader(":green[Support] heroes empower their allies by healing, shielding, boosting damage, and disabling foes. As a :green[support], you’re the backbone of your team’s survival.")
st.write('**Note:** There are 2 :green[support] heroes per team!')

st.image("Images/Support.png", caption="All Support Heros", use_column_width=True)

rank_options = OW2_Data['Rank'].unique()
selected_rank = st.sidebar.selectbox("Please choose a rank:", rank_options)

OW2_Filtered = OW2_Data[OW2_Data['Rank'] == selected_rank]

support_heroes = OW2_Filtered[OW2_Filtered['Role'] == 'Support']

# Healing bar chart
healing = alt.Chart(support_heroes).mark_bar(color='green').encode(
    x=alt.X('Hero', sort='-y'),
    y=alt.Y('Healing_per_10min', axis=alt.Axis(title="Healing per 10 minutes")),
    tooltip=['Hero', 'Healing_per_10min']
).properties(
    width=600,
    height=400,
    title=f"Healing per 10 minutes for Support Heroes"
)

healing_chart_description = f"One of the main jobs a :green[Support] Hero should do is heal their allies. This chart displays the average healing of each :green[**Support Hero**] per 10 mins, based on the :green[***{selected_rank}***] rank."
st.markdown(healing_chart_description)
st.altair_chart(healing, use_container_width=True)

# Creating the Text Table for Support Hero KDA Ratio
support_heroes_sorted = support_heroes.sort_values(by='KDA_Ratio', ascending=False).reset_index(drop=True)
support_heroes_sorted.rename(columns={'Damage_per_10min': 'Damage / 10 Mins'}, inplace=True)
support_heroes_sorted.rename(columns={'KDA_Ratio': 'KDA Ratio'}, inplace=True)

# Pick & Win Rate of Support Heroes - Scatterplot
pick_win_rate = alt.Chart(support_heroes).mark_point().encode(
    x=alt.X('Pick_Rate_Percentage', axis=alt.Axis(title='Pick Rates (Percentage)')),
    y=alt.Y('Win_Rate_Percentage', axis=alt.Axis(title="Win Rates (Percentage)")),
    color='Hero',
    size=alt.Size(value=100),
    tooltip=['Hero', 'Pick_Rate_Percentage', 'Win_Rate_Percentage']
).properties(
    width=450,
    height=340,
    title=f"Pick Rate & Win Rates of Each Support Hero"
)

col1, col2 = st.columns(2)
with col1:
    st.write(f"This table shows the **Average Damage and KDA** per :green[**Support Hero**] in the :green[***{selected_rank}***] rank!")
    st.write(support_heroes_sorted[['Hero', 'Damage / 10 Mins', 'KDA Ratio']])

with col2:
    pick_win_description = f"The scatterplot shows the **Pick and Win Rates** per :green[**Support**] Hero in the :green[***{selected_rank}***] rank!"
    st.markdown(pick_win_description)

    st.altair_chart(pick_win_rate)

st.markdown('---')

st.subheader("Terminology:")
st.markdown(":green[**Damage**]: Creating opportunities to eliminate enemies.")
st.markdown(":green[**Healing**]: Keeping your team alive and healthy.")
st.markdown(":green[**KDA Ratio**]: KDA = (kills + assists)/ deaths , for your kill-deaths/assists ratio. That means, if a player has 10 kills and 5 deaths, his KD ratio is equal to 2. A KD ratio of 1 means that the player got killed exactly as many times as he successfully eliminated his opponents.")
st.markdown(":green[**Pick Rate**]: Shows how popular a hero is chosen, usually for a good reason.")
st.markdown(":green[**Win Rate**]: Shows that the hero can help secure wins for the team if/when played correctly.")
