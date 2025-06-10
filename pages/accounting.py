import streamlit as st
import pandas as pd
from datetime import datetime

st.markdown("""
    <style>
        .title {
            color: #2F4F4F;
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        .sub-title {
            color: #5F6368;
            font-size: 30px;
            text-align: center;
        }
        .section-header {
            color: #00796B;
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #00796B;
        }
        .card {
            background-color: #E0F2F1;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

if 'transactions' not in st.session_state:
    st.session_state.transactions = []  
    st.session_state.accounts = {} 

def add_transaction(date, account, description, amount_in, amount_out, transaction_type):
    transaction = {
        "날짜": date,
        "항목": account,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out,
        "유형": transaction_type
    }
    st.session_state.transactions.append(transaction)

    if account not in st.session_state.accounts:
        st.session_state.accounts[account] = 0
    st.session_state.accounts[account] += amount_in - amount_out

def balance_sheet():
    balance_data = pd.DataFrame(
        [(account, balance) for account, balance in st.session_state.accounts.items()],
        columns=["항목", "잔액"]
    )
    st.write("### 계좌 현황")
    st.dataframe(balance_data)

def income_statement():
    total_income = sum(entry['입금'] for entry in st.session_state.transactions if entry['유형'] == '수익')
    total_expense = sum(entry['출금'] for entry in st.session_state.transactions if entry['유형'] == '비용')
    net_income = total_income - total_expense
    st.write("### 수익과 비용")
    st.write(f"총 수익: {total_income} 💰")
    st.write(f"총 비용: {total_expense} 💳")
    st.write(f"순이익: {net_income} 💵")

def main():
    st.markdown('<div class="title">회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">거래 내역을 추가하고 계좌 현황과 수익을 확인하세요!</div>', unsafe_allow_html=True)

    with st.expander("거래 입력하기"):
        st.markdown('<div class="section-header">거래 입력</div>', unsafe_allow_html=True)
        date = st.date_input("날짜 📅", value=datetime.today())
        account = st.text_input("항목 (예: 현금, 매출 등) 💵")
        description = st.text_area("설명 (거래에 대한 간단한 설명 📝)")
        amount_in = st.number_input("입금액 💰", min_value=0.0, value=0.0)  # 입금
        amount_out = st.number_input("출금액 💳", min_value=0.0, value=0.0)  # 출금
        
        transaction_type = st.selectbox("거래 유형", ["수익 🔼", "비용 🔽"])
        
        if st.button("거래 추가 ✅"):
            add_transaction(date, account, description, amount_in, amount_out, transaction_type)
            st.success("거래가 성공적으로 추가되었습니다!")

    if len(st.session_state.transactions) > 0:
        st.markdown('<div class="section-header">추가된 거래 목록</div>', unsafe_allow_html=True)
        transactions_df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(transactions_df)

    if st.button("계좌 현황 조회 💼"):
        balance_sheet()

    if st.button("수익과 비용 조회 📊"):
        income_statement()

    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
