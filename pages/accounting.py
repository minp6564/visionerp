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
    st.session_state.assets = {
        '현금': 0, '매출채권': 0, '재고자산': 0,
        '선급금': 0, '선급비용': 0, '기타유동자산': 0,
        '건물': 0, '토지': 0, '기계장치': 0
    }
    st.session_state.liabilities = {
        '매입채무': 0, '미지급금': 0, '단기차입금': 0,
        '미지급비용': 0, '선수금': 0, '예수금': 0,
        '장기차입금': 0, '사채': 0, '충당부채': 0, '기타비유동부채': 0
    }
    st.session_state.equity = {
        '자본금': 0, '이익잉여금': 0, '자본잉여금': 0,
        '기타포괄손익누계액': 0, '자기주식': 0
    }

# 더미 데이터 직접 정의
dummy_data = [
    {"날짜": "2025-01-01", "설명": "초기 현금", "입금": 5000000, "출금": 0, "유형": "자산", "카테고리": "현금", "메모": "초기 자본금"},
    {"날짜": "2025-01-02", "설명": "매출 발생", "입금": 1000000, "출금": 0, "유형": "자산", "카테고리": "매출채권", "메모": "제품 판매 외상"},
    {"날짜": "2025-01-03", "설명": "상품 구매", "입금": 0, "출금": 600000, "유형": "자산", "카테고리": "재고자산", "메모": "재고 확보"},
    {"날짜": "2025-01-04", "설명": "선급금 지급", "입금": 0, "출금": 300000, "유형": "자산", "카테고리": "선급금", "메모": "거래처 계약금"},
    {"날짜": "2025-01-05", "설명": "선급비용 지급", "입금": 0, "출금": 100000, "유형": "자산", "카테고리": "선급비용", "메모": "보험료"},
    {"날짜": "2025-01-06", "설명": "건물 취득", "입금": 0, "출금": 2500000, "유형": "자산", "카테고리": "건물", "메모": "사무실 구매"},
    {"날짜": "2025-01-07", "설명": "토지 취득", "입금": 0, "출금": 3000000, "유형": "자산", "카테고리": "토지", "메모": "공장 부지 확보"},
    {"날짜": "2025-01-08", "설명": "기계장치 취득", "입금": 0, "출금": 1000000, "유형": "자산", "카테고리": "기계장치", "메모": "생산설비"},
    {"날짜": "2025-01-09", "설명": "매입채무 발생", "입금": 0, "출금": 500000, "유형": "부채", "카테고리": "매입채무", "메모": "외상구매"},
    {"날짜": "2025-01-10", "설명": "단기차입금", "입금": 0, "출금": 800000, "유형": "부채", "카테고리": "단기차입금", "메모": "운영비"},
    {"날짜": "2025-01-11", "설명": "장기차입금", "입금": 0, "출금": 2000000, "유형": "부채", "카테고리": "장기차입금", "메모": "설비 투자금"},
    {"날짜": "2025-01-12", "설명": "자본금 출자", "입금": 6000000, "출금": 0, "유형": "자본", "카테고리": "자본금", "메모": "주주 출자"},
    {"날짜": "2025-01-13", "설명": "이익잉여금 반영", "입금": 1500000, "출금": 0, "유형": "자본", "카테고리": "이익잉여금", "메모": "전기이익 반영"},
    {"날짜": "2025-02-01", "설명": "추가 설비 도입", "입금": 0, "출금": 1300000, "유형": "자산", "카테고리": "기계장치", "메모": "라인 증설"},
    {"날짜": "2025-02-15", "설명": "보험료 납부", "입금": 0, "출금": 200000, "유형": "자산", "카테고리": "선급비용", "메모": "분기 납부"},
    {"날짜": "2025-03-05", "설명": "공장 유지비", "입금": 0, "출금": 250000, "유형": "부채", "카테고리": "미지급비용", "메모": "3월분"},
    {"날짜": "2025-03-10", "설명": "선급비용 추가", "입금": 0, "출금": 150000, "유형": "자산", "카테고리": "선급비용", "메모": "보험료"},
    {"날짜": "2025-04-05", "설명": "추가 외상 매입", "입금": 0, "출금": 700000, "유형": "부채", "카테고리": "매입채무", "메모": "외상 매입금"},
    {"날짜": "2025-04-20", "설명": "미지급금 반영", "입금": 0, "출금": 300000, "유형": "부채", "카테고리": "미지급금", "메모": "설비"},
    {"날짜": "2025-05-01", "설명": "현금 추가 입금", "입금": 1200000, "출금": 0, "유형": "자산", "카테고리": "현금", "메모": "계좌 이체"},
    {"날짜": "2025-05-15", "설명": "자본잉여금 유입", "입금": 500000, "출금": 0, "유형": "자본", "카테고리": "자본잉여금", "메모": "유입금"},
    {"날짜": "2025-06-01", "설명": "기타포괄손익 반영", "입금": 400000, "출금": 0, "유형": "자본", "카테고리": "기타포괄손익누계액", "메모": "평가손익"},
    {"날짜": "2025-06-13", "설명": "자본금 증자", "입금": 2000000, "출금": 0, "유형": "자본", "카테고리": "자본금", "메모": "유상 증자"}
]

# 더미 데이터 불러오기
# dummy_data는 외부 파일에서 import됩니다
def load_dummy_data():
    if 'dummy_loaded' not in st.session_state:
        for entry in dummy_data:
            add_transaction(
                pd.to_datetime(entry["날짜"]),
                entry["설명"],
                entry["입금"],
                entry["출금"],
                entry["유형"],
                entry["카테고리"],
                entry["메모"]
            )
        st.session_state.dummy_loaded = True
        st.success("더미 데이터를 성공적으로 불러왔습니다.")

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
        return ["현금", "매출채권", "재고자산", "선급금", "선급비용", "기타유동자산", "건물", "토지", "기계장치"]
    elif transaction_type == "부채":
        return ["매입채무", "미지급금", "단기차입금", "미지급비용", "선수금", "예수금", "장기차입금", "사채", "충당부채", "기타비유동부채"]
    elif transaction_type == "자본":
        return ["자본금", "이익잉여금", "자본잉여금", "기타포괄손익누계액", "자기주식"]
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
    for name, value in st.session_state.assets.items():
        st.write(f"{name}: {value:,.0f} 원")
    st.write(f"**총 자산**: {total_assets:,.0f} 원 💰")

    st.write(f"### 부채")
    for name, value in st.session_state.liabilities.items():
        st.write(f"{name}: {value:,.0f} 원")
    st.write(f"**총 부채**: {total_liabilities:,.0f} 원 💳")

    st.write(f"### 자본")
    for name, value in st.session_state.equity.items():
        st.write(f"{name}: {value:,.0f} 원")
    st.write(f"**총 자본**: {total_equity:,.0f} 원 💵")

    st.write(f"### 순자산")
    st.write(f"**순자산**: {net_assets:,.0f} 원 💸")

# 메인 UI 함수
def main():
    st.markdown('<div class="title">회계 시스템</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">거래 내역을 추가하고 재무상태표를 확인하세요!</div>', unsafe_allow_html=True)

    if st.button("거래 더미 데이터 불러오기"):
        load_dummy_data()

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
