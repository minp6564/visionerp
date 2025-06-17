import streamlit as st
import pandas as pd
from datetime import datetime

# 스타일 설정
st.markdown("""
    <style>
        .title { color: #2F4F4F; font-size: 40px; font-weight: bold; text-align: center; margin-top: 20px; }
        .sub-title { color: #5F6368; font-size: 30px; text-align: center; }
        .section-header { color: #00796B; font-size: 20px; font-weight: bold; margin-top: 20px; }
        .footer { text-align: center; margin-top: 50px; font-size: 14px; color: #00796B; }
        .positive { color: green; }
        .negative { color: red; }
    </style>
""", unsafe_allow_html=True)

# 세션 초기화
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
    st.session_state.assets = {'유동자산': 0, '비유동자산': 0}
    st.session_state.liabilities = {'유동부채': 0, '비유동부채': 0}
    st.session_state.equity = {'자본금': 0, '이익잉여금': 0}

# 거래 추가 함수
def add_transaction(date, description, amount_in, amount_out, transaction_type, category, memo):
    transaction = {
        "날짜": date, "설명": description, "입금": amount_in, "출금": amount_out,
        "유형": transaction_type, "카테고리": category, "메모": memo
    }
    st.session_state.transactions.append(transaction)

    if category in st.session_state.assets:
        st.session_state.assets[category] += amount_in
    elif category in st.session_state.liabilities:
        st.session_state.liabilities[category] += amount_out
    elif category in st.session_state.equity:
        st.session_state.equity[category] += amount_in

# 거래 유형에 따른 카테고리 매핑
def get_category_options(transaction_type):
    if transaction_type == "자산":
        return ["유동자산", "비유동자산"]
    elif transaction_type == "부채":
        return ["유동부채", "비유동부채"]
    elif transaction_type == "자본":
        return ["자본금", "이익잉여금"]
    else:
        return []

# 재무상태표 출력 함수
def balance_sheet():
    st.write("### 재무상태표")
    total_assets = sum(st.session_state.assets.values())
    total_liabilities = sum(st.session_state.liabilities.values())
    total_equity = sum(st.session_state.equity.values())
    net_assets = total_assets - total_liabilities

    st.write(f"### 자산")
    st.write(f"유동자산: {st.session_state.assets['유동자산']:,.0f} 원")
    st.write(f"비유동자산: {st.session_state.assets['비유동자산']:,.0f} 원")
    st.write(f"**총 자산**: {total_assets:,.0f} 원 💰")

    st.write(f"### 부채")
    st.write(f"유동부채: {st.session_state.liabilities['유동부채']:,.0f} 원")
    st.write(f"비유동부채: {st.session_state.liabilities['비유동부채']:,.0f} 원")
    st.write(f"**총 부채**: {total_liabilities:,.0f} 원 💳")

    st.write(f"### 자본")
    st.write(f"자본금: {st.session_state.equity['자본금']:,.0f} 원")
    st.write(f"이익잉여금: {st.session_state.equity['이익잉여금']:,.0f} 원")
    st.write(f"**총 자본**: {total_equity:,.0f} 원 💵")

    st.write(f"### 순자산")
    st.write(f"**순자산**: {net_assets:,.0f} 원 💸")

# 연도별 재무 데이터
financials_by_year = {
    "2019": {'유동자산': 1869176, '비유동자산': 1192399, '유동부채': 2151142, '비유동부채': 860221, '자본금': 12419, '이익잉여금': -3759187},
    "2018": {'유동자산': 1354558, '비유동자산': 448089, '유동부채': 1475843, '비유동부채': 365463, '자본금': 11357, '이익잉여금': -3035947},
    "2017": {'유동자산': 680666, '비유동자산': 391949, '유동부채': 986318, '비유동부채': 347364, '자본금': 10691, '이익잉여금': -1862102},
    "2016": {'유동자산': 683453, '비유동자산': 516864, '유동부채': 618527, '비유동부채': 83702, '자본금': 9916, '이익잉여금': -1208589},
    "2015": {'유동자산': 867654, '비유동자산': 207585, '유동부채': 554456, '비유동부채': 88159, '자본금': 9186, '이익잉여금': -646793},
    "2014": {'유동자산': 256468, '비유동자산': 86372, '유동부채': 276830, '비유동부채': 42306, '자본금': 5826, '이익잉여금': -160823},
}

# 재무 데이터 불러오기 함수
def load_financials(year):
    if year in financials_by_year:
        data = financials_by_year[year]
        for category, value in data.items():
            if category in st.session_state.assets:
                st.session_state.assets[category] = value
            elif category in st.session_state.liabilities:
                st.session_state.liabilities[category] = value
            elif category in st.session_state.equity:
                st.session_state.equity[category] = value
        st.success(f"{year}년 기준 재무제표 데이터를 불러왔습니다!")
    else:
        st.error(f"{year}년 데이터가 존재하지 않습니다.")

# 메인 UI 함수
def main():
    st.markdown('<div class="title">회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">거래 내역을 추가하고 재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    year = st.selectbox("불러올 연도 선택", list(financials_by_year.keys()))
    if st.button("재무제표 불러오기"):
        load_financials(year)

    with st.expander("거래 입력하기"):
        st.markdown('<div class="section-header">거래 입력</div>', unsafe_allow_html=True)
        date = st.date_input("날짜 📅", value=datetime.today())
        description = st.text_area("설명 📝")
        amount_in = st.number_input("입금액 💰", min_value=0.0, value=0.0)
        amount_out = st.number_input("출금액 💳", min_value=0.0, value=0.0)
        transaction_type = st.selectbox("거래 유형", ["자산", "부채", "자본"])

        category_options = get_category_options(transaction_type)
        category = st.selectbox("카테고리", category_options)
        memo = st.text_input("비고", "")

        if st.button("거래 추가 ✅"):
            add_transaction(date, description, amount_in, amount_out, transaction_type, category, memo)
            st.success("거래가 성공적으로 추가되었습니다!")

    if len(st.session_state.transactions) > 0:
        st.markdown('<div class="section-header">추가된 거래 목록</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.transactions))

    if st.button("재무상태표 조회 📊"):
        balance_sheet()

    st.markdown('<div class="footer">회계 시스템을 사용해 주셔서 감사합니다! ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
