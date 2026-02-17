import streamlit as st
import pandas as pd
from datetime import date
from database.db import fetch_meals, fetch_participant_totals
from utils.calculations import week_range

st.title("🏠 Hostel Meal Expense Dashboard")

start_week, end_week = week_range()

today_meals = fetch_meals(date.today().isoformat(), date.today().isoformat())
week_meals = fetch_meals(start_week, end_week)

today_total = sum(m[4] for m in today_meals)
week_total = sum(m[4] for m in week_meals)

st.metric("Today's Spending", f"{today_total:.2f}")
st.metric("This Week Spending", f"{week_total:.2f}")

totals = fetch_participant_totals()
df_totals = pd.DataFrame(totals, columns=["Person", "Total"])

st.subheader("Per Person Totals")
st.dataframe(df_totals, use_container_width=True)

st.subheader("Recent Meals")
df_meals = pd.DataFrame(week_meals, columns=["ID","Date","Type","Desc","Cost","Created"])
st.dataframe(df_meals.tail(10), use_container_width=True)

if not df_meals.empty:
    st.subheader("Spending Trend")
    trend = df_meals.groupby("Date")["Cost"].sum()
    st.line_chart(trend)
