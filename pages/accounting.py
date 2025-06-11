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
    st.session_state.assets = {'현금': 0, '매출채권': 0, '건물': 0, '기계': 0}  # 자산 항목
    st.session_state.liabilities = {'매입채무': 0, '단기부채': 0, '장기부채': 0}  # 부채 항목
    st.session_state.equity = {'자본금': 0, '이익잉여금': 0}  # 자본 항목

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

    # 자산, 부채, 자본 갱신
    if transaction_type == '자산':
        st.session_state.assets['현금'] += amount_in
    elif transaction_type == '부채':
        st.session_state.liabilities['매입채무'] += amount_out
    elif transaction_type == '자본':
        st.session_state.equity['자본금'] += amount_in

# 자산, 부채, 자본 항목 입력 함수
def add_balance_sheet_item():
    st.markdown('<div class="section-header">재무상태표 항목 입력</div>', unsafe_allow_html=True)
    
    # 자산 입력
    cash_amount = st.number_input("현금 💰", min_value=0.0, value=0.0)
    receivables_amount = st.number_input("매출채권 💳", min_value=0.0, value=0.0)
    building_amount = st.number_input("건물 🏢", min_value=0.0, value=0.0)
    machinery_amount = st.number_input("기계 🛠️", min_value=0.0, value=0.0)
    if cash_amount > 0:
        st.session_state.assets['현금'] += cash_amount
    if receivables_amount > 0:
        st.session_state.assets['매출채권'] += receivables_amount
    if building_amount > 0:
        st.session_state.assets['건물'] += building_amount
    if machinery_amount > 0:
        st.session_state.assets['기계'] += machinery_amount

    # 부채 입력
    accounts_payable_amount = st.number_input("매입채무 💵", min_value=0.0, value=0.0)
    short_term_debt_amount = st.number_input("단기부채 💳", min_value=0.0, value=0.0)
    long_term_debt_amount = st.number_input("장기부채 💳", min_value=0.0, value=0.0)
    if accounts_payable_amount > 0:
        st.session_state.liabilities['매입채무'] += accounts_payable_amount
    if short_term_debt_amount > 0:
        st.session_state.liabilities['단기부채'] += short_term_debt_amount
    if long_term_debt_amount > 0:
        st.session_state.liabilities['장기부채'] += long_term_debt_amount

    # 자본 입력
    capital_amount = st.number_input("자본금 💰", min_value=0.0, value=0.0)
    retained_earnings_amount = st.number_input("이익잉여금 💵", min_value=0.0, value=0.0)
    if capital_amount > 0:
        st.session_state.equity['자본금'] += capital_amount
    if retained_earnings_amount > 0:
        st.session_state.equity['이익잉여금'] += retained_earnings_amount

# 재무상태표 출력 함수 (자동 계산)
def balance_sheet():
    st.write("### 재무상태표 (Balance Sheet)")

    # 자산, 부채, 자본 출력
    total_assets = sum(st.session_state.assets.values())
    total_liabilities = sum(st.session_state.liabilities.values())
    total_equity = sum(st.session_state.equity.values())
    net_assets = total_assets - total_liabilities  # 순자산 계산
    
    # 금액을 보기 쉽게 포맷팅 (쉼표와 원 단위)
    formatted_assets = f"{total_assets:,.0f} 원"
    formatted_liabilities = f"{total_liabilities:,.0f} 원"
    formatted_equity = f"{total_equity:,.0f} 원"
    formatted_net_assets = f"{net_assets:,.0f} 원"
    
    st.write(f"### 자산 (Assets)")
    st.write(f"현금: {st.session_state.assets['현금']:,.0f} 원")
    st.write(f"매출채권: {st.session_state.assets['매출채권']:,.0f} 원")
    st.write(f"건물: {st.session_state.assets['건물']:,.0f} 원")
    st.write(f"기계: {st.session_state.assets['기계']:,.0f} 원")
    st.write(f"**총 자산**: {formatted_assets} 💰")

    st.write(f"### 부채 (Liabilities)")
    st.write(f"매입채무: {st.session_state.liabilities['매입채무']:,.0f} 원")
    st.write(f"단기부채: {st.session_state.liabilities['단기부채']:,.0f} 원")
    st.write(f"장기부채: {st.session_state.liabilities['장기부채']:,.0f} 원")
    st.write(f"**총 부채**: {formatted_liabilities} 💳")

    st.write(f"### 자본 (Equity)")
    st.write(f"자본금: {st.session_state.equity['자본금']:,.0f} 원")
    st.write(f"이익잉여금: {st.session_state.equity['이익잉여금']:,.0f} 원")
    st.write(f"**총 자본**: {formatted_equity} 💵")

    st.write(f"### 순자산 (Net Assets)")
    st.write(f"**순자산**: {formatted_net_assets} 💸")

# Streamlit UI 구성
def main():
    st.markdown('<div class="title">회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">거래 내역을 추가하고 재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    # 거래 입력 섹션
    with st.expander("거래 입력하기"):
        st.markdown('<div class="section-header">거래 입력</div>', unsafe_allow_html=True)
        date = st.date_input("날짜 📅", value=datetime.today())
        description = st.text_area("설명 (거래에 대한 간단한 설명 📝)")
        amount_in = st.number_input("입금액 💰", min_value=0.0, value=0.0)  # 입금
        amount_out = st.number_input("출금액 💳", min_value=0.0, value=0.0)  # 출금
        
        # 자산, 부채, 자본을 구분하는 입력
        transaction_type = st.selectbox("거래 유형", ["자산", "부채", "자본"])
        
        if st.button("거래 추가 ✅"):
            add_transaction(date, description, amount_in, amount_out, transaction_type)
            st.success("거래가 성공적으로 추가되었습니다!")

    # 추가된 거래 목록 표시
    if len(st.session_state.transactions) > 0:
        st.markdown('<div class="section-header">추가된 거래 목록</div>', unsafe_allow_html=True)
        transactions_df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(transactions_df)

    # 재무상태표 조회
    if st.button("재무상태표 조회 📊"):
        balance_sheet()

    # 페이지 하단에 푸터 추가
    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
