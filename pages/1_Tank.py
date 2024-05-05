import streamlit as st
import pandas as pd
import altair as alt

# Caching the Data
@st.cache_data
def load_data():
    OW2_Data = pd.read_csv('OW2_Statistics.csv')
    return OW2_Data

# Load the data
OW2_Data = load_data()

st.header('Hello! Welcome to the :blue[Tank] Role!')
st.subheader(":blue[Tank] heroes soak up damage and shatter fortified positions, like closely grouped enemies and narrow chokepoints. If you’re a :blue[tank], you lead the charge.")
st.write('**Note:** There is 1 :blue[tank] hero per team!')

st.image("Images/Tank.png", caption="All Tank Heros", use_column_width=True)

rank_options = OW2_Data['Rank'].unique()
selected_rank = st.sidebar.selectbox("Please choose a rank:", rank_options)

OW2_Filtered = OW2_Data[OW2_Data['Rank'] == selected_rank]

tank_heroes = OW2_Filtered[OW2_Filtered['Role'] == 'Tank']
tank_heroes_2 = OW2_Filtered[OW2_Filtered['Role'] == 'Tank'] # Made a 2nd one for my text table and scatterplot because Im sorting the first one for my bar chart

# Stacked Bar Chart Code
# Sort tank heroes data by eliminations for bar chart
tank_heroes = tank_heroes[['Hero', 'Eliminations_per_10min', 'Objective_Elims_per_10min']]
tank_heroes = tank_heroes.sort_values(by='Eliminations_per_10min', ascending=False)

# Melting the dataframe
melted_data = tank_heroes.melt(id_vars='Hero', var_name='Metric', value_name='Value')

melted_data['Metric'] = melted_data.apply(lambda row: row['Metric'].replace('_per_10min', ''), axis=1)

elimination_chart_description = f"One of the main jobs of a :blue[Tank] Hero is to hold the objective and eliminate enemies that are trying to stop it. *(See Terminology)* This chart displays the :blue[**Tank's**] **Average Eliminations & Objective Eliminations** per 10 minutes in the :blue[***{selected_rank}***] rank."
st.markdown(elimination_chart_description)

# Elimination Chart
bar_chart = alt.Chart(melted_data).mark_bar().encode(
    x=alt.X('Hero:N', title='Hero', sort='-y'),
    y=alt.Y('Value:Q', title='Eliminations', scale=alt.Scale(zero=False)),
    color=alt.Color('Metric:N', scale=alt.Scale(domain=['Eliminations', 'Objective_Elims'], range=['#1f77b4', '#1fb4a7']), legend=alt.Legend(title='Metric')),
    tooltip=['Hero:N', 'Value:Q', 'Metric:N']  # Define tooltip with hero name, value, and metric
).properties(
    width=alt.Step(80),
    height=400,
    title=f'Comparison of Eliminations for Tank Heroes'
)

# Displaying the chart
st.altair_chart(bar_chart, use_container_width=True)

# Creating the Text Table for Support Hero KDA Ratio
tank_heroes_sorted = tank_heroes_2.sort_values(by='KDA_Ratio', ascending=False).reset_index(drop=True)
tank_heroes_sorted.rename(columns={'Damage_per_10min': 'Damage / 10 Mins'}, inplace=True)
tank_heroes_sorted.rename(columns={'KDA_Ratio': 'KDA Ratio'}, inplace=True)

# Pick & Win Rate of Support Heroes - Scatterplot
pick_win_rate = alt.Chart(tank_heroes_2).mark_point().encode(
    x=alt.X('Pick_Rate_Percentage', axis=alt.Axis(title='Pick Rates (Percentage)')),
    y=alt.Y('Win_Rate_Percentage', axis=alt.Axis(title="Win Rates (Percentage)")),
    color='Hero',
    size=alt.Size(value=100),
    tooltip=['Hero', 'Pick_Rate_Percentage', 'Win_Rate_Percentage']
).properties(
    width=450,
    height=340,
    title=f"Pick Rate & Win Rates of Each Tank Hero"
)

col1, col2 = st.columns(2)
with col1:
    st.write(f"This table shows the **Average Damage and KDA** per :blue[**Tank Hero**] in the :blue[***{selected_rank}***] rank!")
    st.write(tank_heroes_sorted[['Hero', 'Damage / 10 Mins', 'KDA Ratio']])

with col2:
    pick_win_description = f"The scatterplot shows the **Pick and Win Rates** per :blue[**Tank**] Hero in the :blue[***{selected_rank}***] rank!"
    st.markdown(pick_win_description)

    st.altair_chart(pick_win_rate)

st.markdown('---')

st.subheader("Terminology:")
st.markdown(":blue[**Elimininations**]: Secure kills to give your team an advantage.")
st.markdown(":blue[**KDA Ratio**]: KDA = (kills + assists)/ deaths , for your kill-deaths/assists ratio. That means, if a player has 10 kills and 5 deaths, their KD ratio is equal to 2. A KD ratio of 1 means that the player got killed exactly as many times as they successfully eliminated his opponents.")
st.markdown(':blue[**Objective**]: This varies on the game mode.It could be the "Payload", where teams need to transport a vehicle from Point A to Point B, or it could be a "Control Point", where players try to claim a territory for a given period of time.')
st.markdown(":blue[**Objective Eliminations**]: Taking out enemies where it matters most. If enemies are on the objective, no progress will be made towards the goal.")
st.markdown(":blue[**Pick Rate**]: Shows how popular a hero is chosen, usually for a good reason.")
st.markdown(":blue[**Win Rate**]: Shows that the hero can help secure wins for the team if/when played correctly.")
