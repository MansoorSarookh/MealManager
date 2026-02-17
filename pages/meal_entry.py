import streamlit as st
from datetime import date
from database.db import insert_meal
from utils.calculations import calculate_share

st.title("🍽️ Add Meal")

DEFAULT_USERS = ["Fezan", "Ahmed", "Taro", "Mansoor"]

with st.form("meal_form", clear_on_submit=True):
    meal_date = st.date_input("Date", value=date.today())
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Other"])
    participants = st.multiselect("Participants", DEFAULT_USERS)
    description = st.text_input("Description")
    total_cost = st.number_input("Total Cost", min_value=0.0, step=1.0)

    submitted = st.form_submit_button("Add Meal")

    if submitted:
        if not participants:
            st.error("Select at least one participant.")
        elif total_cost <= 0:
            st.error("Cost must be greater than zero.")
        else:
            share = calculate_share(total_cost, participants)
            insert_meal(meal_date.isoformat(), meal_type, description, total_cost, participants, share)
            st.success(f"Meal added. Share per person: {share}")
