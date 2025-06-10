import streamlit as st
import pandas as pd
from datetime import datetime

journal_entries = []  
accounts = {}  

def add_entry(date, account, description, amount_in, amount_out):
    entry = {
        "날짜": date,
        "계정": account,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out
    }
    journal_entries.append(entry)

    if account not in accounts:
        accounts[account] = 0
    accounts[account] += amount_in - amount_out

def balance_sheet():
    balance_data = pd.DataFrame(
        [(account, balance) for account, balance in accounts.items()],
        columns=["계정", "잔액"]
    )
    st.write("### 계좌 현황")
    st.dataframe(balance_data)

def income_statement():
    total_in = sum(entry['입금'] for entry in journal_entries)
    total_out = sum(entry['출금'] for entry in journal_entries)
    net_income = total_in - total_out
    st.write("### 수익과 비용")
    st.write(f"총 입금: {total_in}")
    st.write(f"총 출금: {total_out}")
    st.write(f"순이익: {net_income}")

# 계정 잔액 조회 함수
def account_balance(account_name):
    if account_name in accounts:
        st.write(f"계정: {account_name} - 잔액: {accounts[account_name]}")
    else:
        st.write("계정을 찾을 수 없습니다.")

def main():
    st.title("간단한 회계 시스템")

    with st.expander("거래 입력하기"):
        date = st.date_input("날짜", value=datetime.today())
        account = st.text_input("계정 (예: 현금, 매출 등)")
        description = st.text_area("설명 (거래에 대한 간단한 설명)")
        amount_in = st.number_input("입금액", min_value=0.0, value=0.0)  # 입금
        amount_out = st.number_input("출금액", min_value=0.0, value=0.0)  # 출금
        
        if st.button("거래 추가"):
            add_entry(date, account, description, amount_in, amount_out)
            st.success("거래가 성공적으로 추가되었습니다!")

    if len(journal_entries) > 0:
        st.write("### 추가된 거래 목록")
        journal_df = pd.DataFrame(journal_entries)
        st.dataframe(journal_df)

    if st.button("계좌 현황 조회"):
        balance_sheet()

    if st.button("수익과 비용 조회"):
        income_statement()

    account_to_check = st.text_input("계정 잔액 조회", "")
    if account_to_check:
        account_balance(account_to_check)

if __name__ == "__main__":
    main()
