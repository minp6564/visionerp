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
    st.session_state.assets = {'현금': 0, '매출채권': 0, '재고자산': 0, '장기투자': 0}  # 자산 항목
    st.session_state.liabilities = {'매입채무': 0, '단기부채': 0, '장기부채': 0}  # 부채 항목
    st.session_state.equity = {'자본금': 0, '이익잉여금': 0}  # 자본 항목

# 거래 내역 추가 함수
def add_transaction(date, description, amount_in, amount_out, transaction_type, category):
    transaction = {
        "날짜": date,
        "설명": description,
        "입금": amount_in,
        "출금": amount_out,
        "유형": transaction_type,
        "카테고리": category
    }
    st.session_state.transactions.append(transaction)

    # 자산, 부채, 자본 갱신
    if transaction_type == '자산':
        st.session_state.assets[category] += amount_in
    elif transaction_type == '부채':
        st.session_state.liabilities[category] += amount_out
    elif transaction_type == '자본':
        st.session_state.equity[category] += amount_in

# 재무상태표 출력 함수 (자동 계산)
def financial_statement():
    st.write("### 재무상태표")

    # 자산, 부채, 자본 출력
    total_current_assets = sum([st.session_state.assets[key] for key in ['현금', '매출채권', '재고자산']])
    total_non_current_assets = st.session_state.assets['장기투자']
    total_assets = total_current_assets + total_non_current_assets

    total_current_liabilities = sum([st.session_state.liabilities[key] for key in ['매입채무', '단기부채']])
    total_non_current_liabilities = st.session_state.liabilities['장기부채']
    total_liabilities = total_current_liabilities + total_non_current_liabilities

    total_equity = sum(st.session_state.equity.values())

    # 금액을 보기 쉽게 포맷팅 (쉼표와 원 단위)
    formatted_total_assets = f"{total_assets:,.0f} 원"
    formatted_total_liabilities = f"{total_liabilities:,.0f} 원"
    formatted_total_equity = f"{total_equity:,.0f} 원"

    # 자산 항목
    st.write(f"### 자산")
    st.write(f"**유동자산**: {total_current_assets:,.0f} 원")
    st.write(f"**비유동자산**: {total_non_current_assets:,.0f} 원")
    st.write(f"**총 자산**: {formatted_total_assets} 💰")

    # 부채 항목
    st.write(f"### 부채")
    st.write(f"**유동부채**: {total_current_liabilities:,.0f} 원")
    st.write(f"**비유동부채**: {total_non_current_liabilities:,.0f} 원")
    st.write(f"**총 부채**: {formatted_total_liabilities} 💳")

    # 자본 항목
    st.write(f"### 자본")
    st.write(f"**자본금**: {st.session_state.equity['자본금']:,.0f} 원")
    st.write(f"**이익잉여금**: {st.session_state.equity['이익잉여금']:,.0f} 원")
    st.write(f"**총 자본**: {formatted_total_equity} 💵")

# 거래 입력 섹션
def transaction_input():
    st.markdown('<div class="section-header">거래 입력하기</div>', unsafe_allow_html=True)
    date = st.date_input("날짜 📅", value=datetime.today())
    description = st.text_area("설명 (거래에 대한 간단한 설명 📝)")
    
    # 금액 입력 (입금액과 출금액을 구분)
    amount_in = st.number_input("입금액 💰", min_value=0.0, value=0.0)  # 입금
    amount_out = st.number_input("출금액 💳", min_value=0.0, value=0.0)  # 출금

    # 자산, 부채, 자본 구분 선택
    transaction_type = st.selectbox("거래 유형", ["자산", "부채", "자본"])
    category = st.text_input("카테고리(예: 현금, 매입채무 등)", "")

    # 유효성 검사: 금액이 입력되지 않으면 경고
    if amount_in == 0 and amount_out == 0:
        st.warning("입금액 또는 출금액을 하나는 반드시 입력해야 합니다.")

    if st.button("거래 추가 ✅"):
        if category == "" or (amount_in == 0 and amount_out == 0):
            st.error("카테고리 또는 금액이 올바르지 않습니다.")
        else:
            add_transaction(date, description, amount_in, amount_out, transaction_type, category)
            st.success("거래가 성공적으로 추가되었습니다!")

# 거래 목록 표시
def display_transactions():
    if len(st.session_state.transactions) > 0:
        st.markdown('<div class="section-header">추가된 거래 목록</div>', unsafe_allow_html=True)
        transactions_df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(transactions_df)

# Streamlit UI 구성
def main():
    st.markdown('<div class="title">회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">거래 내역을 추가하고 재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    # 거래 입력
    transaction_input()

    # 거래 목록 표시
    display_transactions()

    # 재무상태표 조회
    if st.button("재무상태표 조회 📊"):
        financial_statement()

    # 페이지 하단에 푸터 추가
    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
