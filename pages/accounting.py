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
    </style>
    """, unsafe_allow_html=True)

if 'transactions' not in st.session_state:
    st.session_state.transactions = []  
    st.session_state.assets = 0 
    st.session_state.liabilities = 0  

def add_transaction(date, description, amount_in, amount_out, transaction_type):
    transaction = {
        "날짜": date,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out,
        "유형": transaction_type
    }
    st.session_state.transactions.append(transaction)

    if transaction_type == '자산':
        st.session_state.assets += amount_in
    elif transaction_type == '부채':
        st.session_state.liabilities += amount_out

def add_balance_sheet_item():
    st.markdown('<div class="section-header">재무상태표 입력</div>', unsafe_allow_html=True)

    asset_amount = st.number_input("자산 금액 💰", min_value=0.0, value=0.0)
    if asset_amount > 0:
        st.session_state.assets += asset_amount

    liability_amount = st.number_input("부채 금액 💳", min_value=0.0, value=0.0)
    if liability_amount > 0:
        st.session_state.liabilities += liability_amount

def balance_sheet():
    st.write("### 재무상태표 (Balance Sheet)")

    formatted_assets = f"{st.session_state.assets:,.0f} 원"
    formatted_liabilities = f"{st.session_state.liabilities:,.0f} 원"
    formatted_net_assets = f"{st.session_state.assets - st.session_state.liabilities:,.0f} 원"
    
    st.write(f"자산: {formatted_assets} 💰")
    st.write(f"부채: {formatted_liabilities} 💳")
    st.write(f"순자산 (자산 - 부채): {formatted_net_assets} 💵")

def main():
    st.markdown('<div class="title">회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">거래 내역을 추가하고 재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    with st.expander("거래 입력하기"):
        st.markdown('<div class="section-header">거래 입력</div>', unsafe_allow_html=True)
        date = st.date_input("날짜 📅", value=datetime.today())
        description = st.text_area("설명 (거래에 대한 간단한 설명 📝)")
        amount_in = st.number_input("입금액 💰", min_value=0.0, value=0.0)  
        amount_out = st.number_input("출금액 💳", min_value=0.0, value=0.0)  
        
        transaction_type = st.selectbox("거래 유형", ["자산", "부채"])
        
        if st.button("거래 추가 ✅"):
            add_transaction(date, description, amount_in, amount_out, transaction_type)
            st.success("거래가 성공적으로 추가되었습니다!")

    if len(st.session_state.transactions) > 0:
        st.markdown('<div class="section-header">추가된 거래 목록</div>', unsafe_allow_html=True)
        transactions_df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(transactions_df)

    add_balance_sheet_item()

    if st.button("재무상태표 조회 📊"):
        balance_sheet()

    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
