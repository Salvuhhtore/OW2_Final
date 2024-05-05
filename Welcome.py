import streamlit as st
import pandas as pd
import altair as alt

st.title("Season 3 Statistics of :orange[Overwatch 2]")

st.image("Images/OW2.png", width=500)
st.markdown('---')
st.header("What is :orange[Overwatch 2?]")
st.write(":orange[**Overwatch 2**] is a hero shooter game where players choose from a diverse roster of over 30 characters, categorized into :red[**Damage**], :green[**Support**], and :blue[**Tank**] roles - each with their own purpose. Each hero has distinct active, passive, and ultimate abilities. The game focuses on player versus player combat across various modes and maps, offering both casual and ranked competitive matches.")

st.header("What is the :orange[Purpose] of This Project?")
st.write("The purpose of this project is to create visuals that highlight the performance of each hero in the game. By showcasing each hero's abilities and strengths, users can gain insights into their effectiveness across different competitive ranks, ranging from **Bronze** to **Grandmaster**. Additionally, the project can inform future updates to the game by identifying heroes that may require balancing adjustments, such as :red[nerfs] to overperforming heroes or :green[buffs] to underperforming ones.")

st.header("How Does This :orange[Work]?")
st.write("Simply go to a **hero class**, (:blue[**Tank**], :red[**Damage**], or :green[**Support**]) select the **competitive rank** you're interested in, and see the charts displayed to get information!")
