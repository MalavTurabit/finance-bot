import streamlit as st
import requests
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Finance Assistant", layout="wide")

st.title("AI Personal Finance Assistant")

st.header("Create User")

with st.form("user_form"):
    email = st.text_input("Email")
    name = st.text_input("Name")
    submitted = st.form_submit_button("Create User")

if submitted:
    res = requests.post(
        f"{API_URL}/users/",
        json={"email": email, "name": name},
    )
    st.success(res.json())
st.header("Add Expense")

with st.form("expense_form"):
    user_id = st.number_input("User ID", min_value=1)
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0)
    description = st.text_input("Description")
    add_expense = st.form_submit_button("Add")

if add_expense:
    res = requests.post(
        f"{API_URL}/expenses/",
        json={
            "user_id": user_id,
            "category": category,
            "amount": amount,
            "description": description,
        },
    )
    st.success(res.json())
st.header("Spending Chart")

chart_user_id = st.number_input("User ID for chart", min_value=1, key="chart")

if st.button("Load Expenses"):
    res = requests.get(f"{API_URL}/expenses/{chart_user_id}")
    data = res.json()

    categories = {}
    for e in data:
        categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]

    fig = plt.figure()
    plt.bar(categories.keys(), categories.values())
    plt.title("Spending by Category")

    st.pyplot(fig)
st.header("Purchase Advisor")

purchase_user = st.number_input("User ID", min_value=1, key="purchase")
product_url = st.text_input("Product URL")

if st.button("Evaluate Purchase"):
    res = requests.post(
        f"{API_URL}/purchase/",
        json={
            "user_id": purchase_user,
            "product_url": product_url,
        },
    )

    st.write(res.json())
