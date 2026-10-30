import streamlit as st

st.title("My first Python web application")

st.write("Welcome! This application runs in Python.")

name = st.text_input("What is your name?")

if name:
    st.success(f"Hello, {name}! Welcome to my application.")

number = st.slider(
    "Choose a number",
    min_value=1,
    max_value=100,
    value=50
)

st.write(f"You selected: {number}")