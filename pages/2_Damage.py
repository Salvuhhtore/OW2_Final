import streamlit as st
import pandas as pd
import altair as alt

# Cache Data
@st.cache_data
def load_data():
    OW2_Data = pd.read_csv('OW2_Statistics.csv')
    return OW2_Data

# Load the data
OW2_Data = load_data()

st.header('Hello! Welcome to the :red[Damage] Role!')
st.subheader(":red[Damage] heroes seek out, engage, and obliterate the enemy with wide-ranging tools, abilities, and play styles. Fearsome but fragile, :red[damage] heroes require backup to survive.")
st.write('**Note:** There are 2 :red[damage] heroes per team!')

st.image("Images/Damage.png", caption="All Damage Heros", use_column_width=True)

rank_options = OW2_Data['Rank'].unique()
selected_rank = st.sidebar.selectbox("Please choose a rank:", rank_options)

OW2_Filtered = OW2_Data[OW2_Data['Rank'] == selected_rank]

damage_heroes = OW2_Filtered[OW2_Filtered['Role'] == 'Damage']

# Horizontal Bar Chart Code - Damage Heroes & Eliminations
bar_chart = alt.Chart(damage_heroes).mark_bar(color='#B30707').encode(
    y=alt.Y('Hero:N', title='Hero', sort='-x'),  # Horizontal bar chart
    x=alt.X('sum(Eliminations_per_10min):Q', title='Average Eliminations'),
    tooltip=['Hero:N', alt.Tooltip('average(Eliminations_per_10min):Q', title='Eliminations / 10min')]
).properties(
    width=600,
    height=500,
    title=f'Average Eliminations for Damage Heroes'
)

# Displaying the chart & description
damage_chart_description = f"One of the main jobs of a :red[Damage] Hero is to... well, deal damage and secure eliminations for the team! This chart displays the average eliminations of each :red[**Damage Hero**] per 10 minutes, based on the :red[***{selected_rank}***] rank."
st.markdown(damage_chart_description)
st.altair_chart(bar_chart, use_container_width=True)

# Creating the Text Table for Damage Heroes - KDA Ratio & Average Damage
damage_heroes_sorted = damage_heroes.sort_values(by='KDA_Ratio', ascending=False).reset_index(drop=True)
damage_heroes_sorted.rename(columns={'Damage_per_10min': 'Damage / 10 Mins'}, inplace=True)
damage_heroes_sorted.rename(columns={'KDA_Ratio': 'KDA Ratio'}, inplace=True)

# Pick & Win Rate of Damage Heroes - Scatterplot
pick_win_rate = alt.Chart(damage_heroes).mark_point().encode(
    x=alt.X('Pick_Rate_Percentage', axis=alt.Axis(title='Pick Rates (Percentage)')),
    y=alt.Y('Win_Rate_Percentage', axis=alt.Axis(title="Win Rates (Percentage)")),
    color='Hero',
    size=alt.Size(value=100),
    tooltip=['Hero', 'Pick_Rate_Percentage', 'Win_Rate_Percentage']
).properties(
    width=550,
    height=460,
    title=f"Pick Rate & Win Rates of Each Support Hero"
)
# Putting into columns
col1, col2 = st.columns(2)
with col1:
    st.write(f"This table shows the **Average Damage and KDA** per :red[**Damage Hero**] in the :red[***{selected_rank}***] rank!")
    st.write(damage_heroes_sorted[['Hero', 'Damage / 10 Mins', 'KDA Ratio']])

with col2:
    pick_win_description = f"The scatterplot shows the **Pick and Win Rates** per :red[**Damage**] Hero in the :red[***{selected_rank}***] rank!"
    st.markdown(pick_win_description)

    st.altair_chart(pick_win_rate)

st.markdown('---')

st.subheader("Terminology:")
st.markdown(":red[**Damage**]: Creating opportunities to eliminate enemies.")
st.markdown(":red[**Elimininations**]: Secure kills to give your team an advantage.")
st.markdown(":red[**KDA Ratio**]: KDA = (kills + assists)/ deaths , for your kill-deaths/assists ratio. That means, if a player has 10 kills and 5 deaths, his KD ratio is equal to 2. A KD ratio of 1 means that the player got killed exactly as many times as he successfully eliminated his opponents.")
st.markdown(":red[**Pick Rate**]: Shows how popular a hero is chosen, usually for a good reason.")
st.markdown(":red[**Win Rate**]: Shows that the hero can help secure wins for the team if/when played correctly.")
