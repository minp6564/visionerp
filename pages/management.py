import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from data import dummy_data_management

# ✅ 더미 데이터 사용
employees_df = dummy_data_management.employees_df
attendance_logs_df = dummy_data_management.attendance_logs_df

# DB 연결
conn = sqlite3.connect("employee.db", check_same_thread=False)
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        department TEXT,
        join_date TEXT,
        email TEXT
    )
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    date TEXT,
    clock_in TEXT,
    clock_out TEXT,
    location TEXT
)
""")
conn.commit()

if cursor.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 0:
    for _, row in employees_df.iterrows():
        cursor.execute("""
            INSERT INTO employees (id, name, position, department, join_date, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (row.id, row.name, row.position, row.department, row.join_date, row.email))

    for _, row in attendance_logs_df.iterrows():
        cursor.execute("""
            INSERT INTO attendance_logs (employee_id, date, clock_in, clock_out, location)
            VALUES (?, ?, ?, ?, ?)
        """, (row.employee_id, row.date, row.clock_in, row.clock_out, row.location))

    conn.commit()

# Streamlit UI
st.set_page_config(page_title="인사 관리 시스템", layout="wide")
st.title("🧑‍💼 인사 관리 시스템 ")

menu = st.sidebar.radio("인사 관리 시스템", ["직원 등록", "직원 목록","출근/퇴근 기록", "직원 수정", "직원 삭제"])

# 직원 등록
if menu == "직원 등록":
    st.subheader("직원 등록")

    with st.form("register_form"):
        name = st.text_input("이름")
        position = st.selectbox("직급", ["사원", "대리", "과장", "차장", "부장", "임원"])
        department = st.selectbox("부서", ["경영", "회계", "인사", "영업", "전산", "마케팅"])
        join_date = st.date_input("입사일", value=datetime.today())
        email = st.text_input("이메일")
        submitted = st.form_submit_button("등록")

        if submitted:
            cursor.execute(
                "INSERT INTO employees (name, position, department, join_date, email) VALUES (?, ?, ?, ?, ?)",
                (name, position, department, join_date.isoformat(), email)
            )
            conn.commit()
            st.success("직원이 등록되었습니다!")

# 직원 목록
elif menu == "직원 목록":
    st.subheader("📋 직원 목록")
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    st.dataframe(df, use_container_width=True)
elif menu == "출근/퇴근 기록":
    st.subheader("🕒 출근 / 퇴근 기록")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = st.selectbox("위치", ["본사", "재택"])

    df = pd.read_sql_query("SELECT * FROM employees", conn)

    if df.empty:
        st.warning("직원 정보가 없습니다. 먼저 직원을 등록해주세요.")
    else:
        employee_ids = df["id"].tolist()
        selected_id = st.selectbox("직원 선택 (ID)", ["직원 선택"] + [str(i) for i in employee_ids])

        if selected_id != "직원 선택":
            EMPLOYEE_ID = int(selected_id)

            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("출근"):
                    today = datetime.now().date().isoformat()
                    cursor.execute(
                        "INSERT INTO attendance_logs (employee_id, date, clock_in, location) VALUES (?, ?, ?, ?)",
                        (EMPLOYEE_ID, today, now, location)
                    )
                    conn.commit()
                    st.session_state.attendance = now
                    st.success(f"출근 시간 기록됨: {now}")

            with col2:
                if st.button("퇴근"):
                    today = datetime.now().date().isoformat()
                    cursor.execute(
                        "UPDATE attendance_logs SET clock_out=? WHERE employee_id=? AND date=?",
                        (now, EMPLOYEE_ID, today)
                    )
                    conn.commit()
                    st.session_state.leave = now
                    st.success(f"퇴근 시간 기록됨: {now}")
        else:
            st.info("직원을 선택해주세요.")


# 직원 수정
elif menu == "직원 수정":
    st.subheader("🛠️ 직원 정보 수정")

    df = pd.read_sql_query("SELECT * FROM employees", conn)
    selected_id = st.selectbox("직원 선택 (ID)", df["id"])

    if selected_id:
        employee = df[df["id"] == selected_id].iloc[0]

        # ✅ 실제 데이터와 맞춰 부서 목록 구성
        department_options = ["경영팀", "회계팀", "인사팀", "영업팀", "전산팀", "마케팅팀"]
        position_options = ["사원", "대리", "과장", "차장", "부장", "임원"]

        with st.form("edit_form"):
            name = st.text_input("이름", value=employee["name"])
            position = st.selectbox("직급", position_options, index=position_options.index(employee["position"]))
            department = st.selectbox("부서", department_options, index=department_options.index(employee["department"]))
            join_date = st.date_input("입사일", value=datetime.fromisoformat(employee["join_date"]))
            email = st.text_input("이메일", value=employee["email"])
            
            # ✅ 반드시 submit 버튼 필요
            updated = st.form_submit_button("수정 완료")

            if updated:
                cursor.execute("""
                    UPDATE employees
                    SET name=?, position=?, department=?, join_date=?, email=?
                    WHERE id=?
                """, (name, position, department, join_date.isoformat(), email, selected_id))
                conn.commit()
                st.success("직원 정보가 수정되었습니다!")

# 직원 삭제
elif menu == "직원 삭제":
    st.subheader("🗑️ 직원 삭제")

    df = pd.read_sql_query("SELECT * FROM employees", conn)
    selected_id = st.selectbox("삭제할 직원 선택 (ID)", df["id"])

    if st.button("삭제"):
        cursor.execute("DELETE FROM employees WHERE id=?", (selected_id,))
        conn.commit()
        st.warning("직원 정보가 삭제되었습니다.")
