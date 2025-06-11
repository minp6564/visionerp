import pandas as pd
from datetime import datetime, timedelta

employees_df = pd.DataFrame([
    {"id": 1, "name": "홍길동", 
     "position": "사원", 
     "department": "전산", 
     "join_date": "2023-01-10", 
     "email": "hong@company.com"},
  
    {"id": 2, "name": "이영희", 
     "position": "대리", 
     "department": "인사", "join_date": 
     "2022-06-15", "email": "lee@company.com"},
  
    {"id": 3, "name": "김철수", 
     "position": "과장", 
     "department": "마케팅", 
     "join_date": "2021-03-01", 
     "email": "kim@company.com"},
])

base_date = datetime(2025, 6, 10)

attendance_logs_df = pd.DataFrame([
    # 홍길동
    {"employee_id": 1, 
     "date": base_date.date().isoformat(), 
     "clock_in": (base_date + timedelta(hours=9, minutes=5)).isoformat(), 
     "clock_out": (base_date + timedelta(hours=18)).isoformat(), 
     "location": "본사"},
  
    {"employee_id": 1, 
     "date": (base_date + timedelta(days=1)).date().isoformat(), 
     "clock_in": (base_date + timedelta(days=1, hours=9, minutes=1)).isoformat(), 
     "clock_out": (base_date + timedelta(days=1, hours=17, minutes=55)).isoformat(), 
     "location": "본사"},
    
    # 이영희
    {"employee_id": 2, 
     "date": base_date.date().isoformat(), 
     "clock_in": (base_date + timedelta(hours=9, minutes=15)).isoformat(), 
     "clock_out": (base_date + timedelta(hours=18, minutes=10)).isoformat(), 
     "location": "재택"},
    
    # 김철수
    {"employee_id": 3, 
     "date": (base_date + timedelta(days=1)).date().isoformat(), 
     "clock_in": (base_date + timedelta(days=1, hours=8, minutes=55)).isoformat(), 
     "clock_out": (base_date + timedelta(days=1, hours=17, minutes=45)).isoformat(), 
     "location": "본사"},
])

