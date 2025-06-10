import streamlit as st
import pandas as pd
from datetime import datetime

journal_entries = []
accounts = {}

def add_entry(date, account, description, debit, credit):
    entry = {
        "date": date,
        "account": account,
        "description": description,
        "debit": debit,
        "credit": credit
    }
    journal_entries.append(entry)

    if account not in accounts:
        accounts[account] = 0
    accounts[account] += debit - credit

def balance_sheet():
    balance_data = pd.DataFrame(
        [(account, balance) for account, balance in accounts.items()],
        columns=["Account", "Balance"]
    )
    st.write("### Balance Sheet")
    st.dataframe(balance_data)

def income_statement():
    total_debit = sum(entry['debit'] for entry in journal_entries)
    total_credit = sum(entry['credit'] for entry in journal_entries)
    net_income = total_credit - total_debit
    st.write("### Income Statement")
    st.write(f"Total Debit: {total_debit}")
    st.write(f"Total Credit: {total_credit}")
    st.write(f"Net Income: {net_income}")

def account_balance(account_name):
    if account_name in accounts:
        st.write(f"Account: {account_name} - Balance: {accounts[account_name]}")
    else:
        st.write("Account not found.")

def main():
    st.title("ERP Accounting System")

    with st.expander("Add Journal Entry"):
        date = st.date_input("Date", value=datetime.today())
        account = st.text_input("Account")
        description = st.text_area("Description")
        debit = st.number_input("Debit", min_value=0.0, value=0.0)
        credit = st.number_input("Credit", min_value=0.0, value=0.0)
        
        if st.button("Add Entry"):
            add_entry(date, account, description, debit, credit)
            st.success("Entry added successfully!")

    if st.button("View Balance Sheet"):
        balance_sheet()

    if st.button("View Income Statement"):
        income_statement()

    account_to_check = st.text_input("Check Account Balance", "")
    if account_to_check:
        account_balance(account_to_check)

if __name__ == "__main__":
    main()
