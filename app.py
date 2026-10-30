import streamlit as st
import json
import os
import pandas as pd

st.title("💸 My Expense Tracker Web App")

file_name = "Expenses_Track.json"


def load_expense():
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []


def save_expense(data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


expense = load_expense()

# ---------- Messages (rerun ke baad bhi dikhenge) ----------
if "msg" in st.session_state:
    st.success(st.session_state.pop("msg"))

# ---------- Add Expense ----------
st.sidebar.header("➕ Add a New Expense")

with st.sidebar.form("expense_form", clear_on_submit=True):
    date = st.date_input("Select Date")
    category = st.text_input("Category").strip().title()
    title = st.text_input("Expense Title").strip().title()
    amount = st.number_input("Amount", min_value=0.0)

    submit_button = st.form_submit_button("Add Expense")

    if submit_button:
        if title == "" or category == "":
            st.error("Bhai, Title aur Category khali nahi chhod sakte!")
        elif amount <= 0:
            st.error("Amount 0 se zyada hona chahiye!")
        else:
            new_expense = {
                "date": date.strftime("%d-%m-%Y"),
                "category": category,
                "title": title,
                "amount": amount,
            }
            expense.append(new_expense)
            save_expense(expense)
            st.session_state["msg"] = f"Successfully added: {title} - ₹{amount}"
            st.rerun()

# ---------- All Expenses & Budget Tracker ----------
st.write("---")
st.subheader("📊 All Expenses & Budget Tracker")

if expense:
    st.dataframe(expense, use_container_width=True)
    total = sum(item["amount"] for item in expense)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="💰 Grand Total Expenses", value=f"₹ {total:,.2f}")
        
    with col2:
        budget = st.number_input("🎯 Set Your Budget Target", min_value=0.0, value=5000.0, step=500.0)
    if budget > 0:
        if total <= budget:
            progress_pct = total / budget
            st.progress(progress_pct)
            st.success(f"✅ Awesome! Aap apne budget ke andar hain. (₹ {budget - total:,.2f} bache hain)")
        else:
            st.progress(1.0)
            st.error(f"🚨 ALERT! Budget cross ho gaya hai! (₹ {total - budget:,.2f} limit se zyada kharch hue)")
else:
    st.info("Abhi tak koi kharcha nahi joda gaya hai.")

# ---------- Quick Insights & Category Breakdown ----------
st.write("---")
st.subheader("💡 Quick Insights & Category Breakdown")

if expense:
    col1, col2, col3 = st.columns(3)
    amounts = [item["amount"] for item in expense]
    highest = max(amounts)
    average = sum(amounts) / len(amounts)
    
    highest_item = next(item["title"] for item in expense if item["amount"] == highest)

    with col1:
        st.metric("📈 Highest Expense", f"₹ {highest:,.2f}", f"For: {highest_item}")
    with col2:
        st.metric("📉 Average Expense", f"₹ {average:,.2f}")
    with col3:
        st.metric("🧾 Total Transactions", f"{len(expense)} items")

    category_summary = {}
    for item in expense:
        cat = item["category"]
        category_summary[cat] = category_summary.get(cat, 0) + item["amount"]
    
    st.write("<br>**Spending by Category (Graph):**", unsafe_allow_html=True)
    
    cat_df = pd.DataFrame(
        {"Amount Spent": list(category_summary.values())},
        index=list(category_summary.keys())
    )
    st.bar_chart(cat_df)

# ---------- Search by Category ----------
st.write("---")
st.subheader("🔍 Search by Category")
if expense:
    all_categories = []
    for item in expense:
        if item["category"] not in all_categories:
            all_categories.append(item["category"])

    search_cat = st.selectbox("Category chunein:", ["All"] + all_categories)

    if search_cat == "All":
        filtered_data = expense
    else:
        filtered_data = [item for item in expense if item["category"] == search_cat]

    st.dataframe(filtered_data, use_container_width=True)
    filtered_total = sum(item["amount"] for item in filtered_data)
    st.success(f"**Total for {search_cat}: ₹{filtered_total:,.2f}**")

# ---------- Delete Expense ----------
st.write("---")
st.subheader("❌ Delete an Expense")

if expense:
    delete_options = []
    for i, item in enumerate(expense):
        delete_options.append(
            f"{i} - {item['title']} (₹{item['amount']} on {item['date']})"
        )

    choice = st.selectbox("Kaunsa kharcha delete karna hai?", delete_options)
    if st.button("Delete Selected Expense"):
        selected_index = int(choice.split(" - ")[0])
        expense.pop(selected_index)
        save_expense(expense)
        st.session_state["msg"] = "Kharcha successfully delete ho gaya!"
        st.rerun()

# ---------- Monthly Summary ----------
st.write("---")
st.subheader("📅 Monthly Expense Summary")

if expense:
    monthly_summary = {}

    for item in expense:
        d = pd.to_datetime(item["date"], format="%d-%m-%Y")
        month_year = d.strftime("%Y-%m")  # sorting sahi rahegi
        monthly_summary[month_year] = monthly_summary.get(month_year, 0) + item["amount"]

    monthly_summary = dict(sorted(monthly_summary.items()))

    summary_list = [
        {"Month-Year": m, "Total Spent": amt} for m, amt in monthly_summary.items()
    ]
    st.dataframe(summary_list, use_container_width=True)

    st.write("**Expense Chart:**")
    chart_df = pd.DataFrame(
        {"Total Spent": list(monthly_summary.values())},
        index=list(monthly_summary.keys()),
    )
    st.bar_chart(chart_df)

# ---------- Export ----------
st.write("---")
st.subheader("📥 Export Data")

if expense:
    df = pd.DataFrame(expense)
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Expenses as CSV",
        data=csv_data,
        file_name="My_Expenses.csv",
        mime="text/csv",
    )

