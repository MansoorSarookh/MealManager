import streamlit as st
from database.db import init_db

st.set_page_config(page_title="Hostel Meal Expense Manager", layout="wide")

init_db()

st.sidebar.title("Navigation")
st.sidebar.info("Use the sidebar to switch pages.")

st.title("🍽️ Hostel Meal Expense Manager")
st.subtitle("Developed by Faizan Friend 😅")
st.write("Track shared meals, split costs, and generate reports.")
