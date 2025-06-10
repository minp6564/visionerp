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
        columns=["계정", "잔액"]
    )
    st.write("### 재무상태표")
    st.dataframe(balance_data)

def income_statement():
    total_debit = sum(entry['debit'] for entry in journal_entries)
    total_credit = sum(entry['credit'] for entry in journal_entries)
    net_income = total_credit - total_debit
    st.write("### 손익계산서")
    st.write(f"총 차변: {total_debit}")
    st.write(f"총 대변: {total_credit}")
    st.write(f"순이익: {net_income}")

def account_balance(account_name):
    if account_name in accounts:
        st.write(f"계정: {account_name} - 잔액: {accounts[account_name]}")
    else:
        st.write("계정을 찾을 수 없습니다.")

def main():
    st.title("ERP 회계 시스템")

    with st.expander("거래 입력하기"):
        date = st.date_input("날짜", value=datetime.today())
        account = st.text_input("계정")
        description = st.text_area("설명")
        debit = st.number_input("차변", min_value=0.0, value=0.0)
        credit = st.number_input("대변", min_value=0.0, value=0.0)
        
        if st.button("거래 추가"):
            add_entry(date, account, description, debit, credit)
            st.success("거래가 성공적으로 추가되었습니다!")

    # 재무상태표 조회
    if st.button("재무상태표 조회"):
        balance_sheet()

    # 손익계산서 조회
    if st.button("손익계산서 조회"):
        income_statement()

    # 잔액 조회
    account_to_check = st.text_input("계정 잔액 조회", "")
    if account_to_check:
        account_balance(account_to_check)

if __name__ == "__main__":
    main()
