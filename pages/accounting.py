import streamlit as st
import pandas as pd
from datetime import datetime

transactions = []  # 거래 내역을 저장
accounts = {}  # 각 항목의 잔액을 저장

def add_transaction(date, account, description, amount_in, amount_out, transaction_type):
    """
    거래 추가
    - transaction_type: '수익' 또는 '비용'으로 거래의 유형을 구분
    """
    transaction = {
        "날짜": date,
        "항목": account,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out,
        "유형": transaction_type  # '수익' 또는 '비용'
    }
    transactions.append(transaction)

    if account not in accounts:
        accounts[account] = 0
    accounts[account] += amount_in - amount_out

def balance_sheet():
    balance_data = pd.DataFrame(
        [(account, balance) for account, balance in accounts.items()],
        columns=["항목", "잔액"]
    )
    st.write("### 계좌 현황")
    st.dataframe(balance_data)

def income_statement():
    total_inc_
