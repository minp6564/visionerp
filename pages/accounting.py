import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 제목 및 스타일 설정
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

# 세션에 필요한 값들 초기화
if 'transactions' not in st.session_state:
    st.session_state.transactions = []  # 거래 내역
    st.session_state.money = 0  # 돈 (자산)
    st.session_state.debt = 0  # 빚 (부채)

# 거래 내역 추가 함수
def add_transaction(date, description, amount_in, amount_out, transaction_type):
    transaction = {
        "날짜": date,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out,
        "유형": transaction_type
    }
    st.session_state.transactions.append(transaction)

    # 돈과 빚 갱신
    if transaction_type == '돈':
        st.session_state.money += amount_in
    elif transaction_type == '빚':
        st.session_state.debt += amount_out

# 대차대조표 항목 입력 함수
def add_balance_sheet_item():
    st.markdown('<div class="section-header">대차대조표 입력</div>', unsafe_allow_html=True)

    # 돈 (자산) 입력
    money_amount = st.number_input("돈 (자산) 금액 💰", min_value=0.0, value=0.0)
    if money_amount > 0:
        st.session_state.money += money_amount

    # 빚 (부채) 입력
    debt_amount = st.number_input("빚 (부채) 금액 💳", min_value=0.0, value=0.0)
    if debt_amount > 0:
        st.session_state.debt += debt_amount

# 대차대조표 출력 함수
def balance_sheet():
    st.write("### 대차대조표 (Balance Sheet)")
    
    # 돈 (자산)과 빚 (부채) 출력
    st.write(f"돈 (자산): {st.session_state.money} 💰")
    st.write(f"빚 (부채): {st.session_state.debt} 💳")
    st.write(f"순자산 (돈 - 빚): {st.session_state.money - st.session_state.debt} 💵")

# Streamlit UI 구성
def main():
    st.markdown('<div class="title">간단한 회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">거래 내역을 추가하고 대차대조표를 확인하세요!</div>', unsafe_allow_html=True)

    # 거래 입력 섹션
    with st.expander("거래 입력하기"):
        st.markdown('<div class="section-header">거래 입력</div>', unsafe_allow_html=True)
        date = st.date_input("날짜 📅", value=datetime.today())
        description = st.text_area("설명 (거래에 대한 간단한 설명 📝)")
        amount_in = st.number_input("입금액 💰", min_value=0.0, value=0.0)  # 입금
        amount_out = st.number_input("출금액 💳", min_value=0.0, value=0.0)  # 출금
        
        # 돈과 빚을 구분하는 입력
        transaction_type = st.selectbox("거래 유형", ["돈", "빚"])
        
        if st.button("거래 추가 ✅"):
            add_transaction(date, description, amount_in, amount_out, transaction_type)
            st.success("거래가 성공적으로 추가되었습니다!")

    # 추가된 거래 목록 표시
    if len(st.session_state.transactions) > 0:
        st.markdown('<div class="section-header">추가된 거래 목록</div>', unsafe_allow_html=True)
        transactions_df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(transactions_df)

    # 돈과 빚 입력
    add_balance_sheet_item()

    # 대차대조표 조회
    if st.button("대차대조표 조회 📊"):
        balance_sheet()

    # 페이지 하단에 푸터 추가
    st.markdown('<div class="footer">간단한 회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
