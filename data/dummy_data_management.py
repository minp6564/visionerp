import pandas as pd
from datetime import datetime, timedelta

employees_df = pd.DataFrame([
    {"id": 1, "name": "김승현", "position": "사원", "department": "전산팀", "join_date": "2023-01-10", "email": "kimseung@company.com"},
    {"id": 2, "name": "민승기", "position": "대리", "department": "인사팀", "join_date": "2022-06-15", "email": "mean@company.com"},
    {"id": 3, "name": "정하람", "position": "과장", "department": "물류팀", "join_date": "2021-03-01", "email": "haram@company.com"},
    {"id": 4, "name": "정유현", "position": "차장", "department": "영업팀", "join_date": "2020-09-01", "email": "jung@company.com"},
    {"id": 5, "name": "한나영", "position": "사원", "department": "경영팀", "join_date": "2024-02-20", "email": "han@company.com"},
])

base_date = datetime(2025, 6, 10)

attendance_logs_df = pd.DataFrame([
    # 김승현
    {"employee_id": 1, "date": base_date.date().isoformat(), "clock_in": (base_date + timedelta(hours=9, minutes=5)).isoformat(), "clock_out": (base_date + timedelta(hours=18)).isoformat(), "location": "본사"},
    {"employee_id": 1, "date": (base_date + timedelta(days=1)).date().isoformat(), "clock_in": (base_date + timedelta(days=1, hours=9, minutes=1)).isoformat(), "clock_out": (base_date + timedelta(days=1, hours=17, minutes=55)).isoformat(), "location": "본사"},

    # 민승기
    {"employee_id": 2, "date": base_date.date().isoformat(), "clock_in": (base_date + timedelta(hours=9, minutes=15)).isoformat(), "clock_out": (base_date + timedelta(hours=18, minutes=10)).isoformat(), "location": "재택"},

    # 정하람
    {"employee_id": 3, "date": (base_date + timedelta(days=1)).date().isoformat(), "clock_in": (base_date + timedelta(days=1, hours=8, minutes=55)).isoformat(), "clock_out": (base_date + timedelta(days=1, hours=17, minutes=45)).isoformat(), "location": "본사"},

    # 정유현
    {"employee_id": 4, "date": base_date.date().isoformat(), "clock_in": (base_date + timedelta(hours=9, minutes=10)).isoformat(), "clock_out": (base_date + timedelta(hours=18, minutes=5)).isoformat(), "location": "본사"},

    # 한나영
    {"employee_id": 5, "date": (base_date + timedelta(days=1)).date().isoformat(), "clock_in": (base_date + timedelta(days=1, hours=9)).isoformat(), "clock_out": (base_date + timedelta(days=1, hours=18)).isoformat(), "location": "재택"},
])
