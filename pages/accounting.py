import streamlit as st
import pandas as pd
from datetime import datetime

# 스타일링을 위한 HTML/CSS 코드 추가
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

# 데이터 저장을 위한 변수 설정 (SQLite 대신 메모리 사용)
if 'transactions' not in st.session_state:
    st.session_state.transactions = []  # 거래 내역을 저장
    st.session_state.income = 0  # 수익 저장
    st.session_state.expense = 0  # 비용 저장
    st.session_state.assets = {}  # 자산 항목을 저장
    st.session_state.liabilities = {}  # 부채 항목을 저장
    st.session_state.equity = {}  # 자본 항목을 저장

# 거래 추가 함수 (입금, 출금으로 단순화)
def add_transaction(_
