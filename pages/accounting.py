import streamlit as st
import pandas as pd
from datetime import datetime

transactions = []
accounts = {}

def add_transaction(date, account, description, amount_in, amount_out):
    transaction = {
        "날짜": date,
        "계정": account,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out
    }
    transactions.append(transaction)

    if account not in accounts:
        accounts[account] = 0
    accounts[account] += amount_in - amount_out

def balance_sheet():
    balance_data = pd.DataFrame(
        [(account, balance) for account, balance in accounts.items()],
        columns=["계정", "잔액"]
    )
    st.write("### 재무상태표")
    st.dataframe(balance_data)

def income_statement():
    total_in = sum(transaction['입금'] for transaction in transactions)
    total_out = sum(transaction['출금'] for transaction in transactions)
    net_income = total_in - total_out
    st.write("### 손익계산서")
    st.write(f"총 입금: {total_in}")
    st.write(f"총 출금: {total_out}")
    st.write(f"순이익: {net_income}")

def account_balance(account_name):
    if account_name in accounts:
        st.write(f"계정: {account_name} - 잔액: {accounts[account_name]}")
    else:
        st.write("계정을 찾을 수 없습니다.")

def main():
    st.title("단순 회계 시스템")

    with st.expander("거래 입력하기"):
        date = st.date_input("날짜", value=datetime.today())
        account = st.text_input("계정 (예: 현금, 매출 등)")
        description = st.text_area("설명 (간단한 설명을 입력하세요)")
        amount_in = st.number_input("입금액", min_value=0.0, value=0.0)
        amount_out = st.number_input("출금액", min_value=0.0, value=0.0)
        
        if st.button("거래 추가"):
            add_transaction(date, account, description_
