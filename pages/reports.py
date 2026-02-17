import streamlit as st
import pandas as pd
from datetime import date
from database.db import fetch_meals, fetch_participant_totals

st.title("📊 Reports")

tab1, tab2, tab3, tab4 = st.tabs(["Daily","Weekly","Custom","Monthly"])

with tab1:
    d = st.date_input("Select Date", date.today())
    meals = fetch_meals(d.isoformat(), d.isoformat())
    totals = fetch_participant_totals(d.isoformat(), d.isoformat())
    st.dataframe(pd.DataFrame(meals, columns=["ID","Date","Type","Desc","Cost","Created"]))
    st.dataframe(pd.DataFrame(totals, columns=["Person","Total"]))

with tab2:
    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    if start and end and start <= end:
        meals = fetch_meals(start.isoformat(), end.isoformat())
        totals = fetch_participant_totals(start.isoformat(), end.isoformat())
        st.dataframe(pd.DataFrame(meals, columns=["ID","Date","Type","Desc","Cost","Created"]))
        st.dataframe(pd.DataFrame(totals, columns=["Person","Total"]))

with tab3:
    start = st.date_input("Custom Start", key="c1")
    end = st.date_input("Custom End", key="c2")
    if start and end and start <= end:
        meals = fetch_meals(start.isoformat(), end.isoformat())
        st.dataframe(pd.DataFrame(meals, columns=["ID","Date","Type","Desc","Cost","Created"]))

with tab4:
    month = st.date_input("Select Month")
    start = month.replace(day=1)
    end = month
    meals = fetch_meals(start.isoformat(), end.isoformat())
    df = pd.DataFrame(meals, columns=["ID","Date","Type","Desc","Cost","Created"])
    if not df.empty:
        st.metric("Total", df["Cost"].sum())
        st.metric("Average", df["Cost"].mean())
        st.line_chart(df.groupby("Date")["Cost"].sum())
