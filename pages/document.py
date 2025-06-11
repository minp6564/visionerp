import streamlit as st
import pandas as pd
import os
from datetime import datetime

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if 'documents' not in st.session_state:
    st.session_state.documents = pd.DataFrame(columns=["제목", "파일명", "업로더", "등록일"])

st.title("📚 문서 등록 및 공유 페이지")

with st.form("upload_form"):
    st.subheader("📤 문서 업로드")

    uploaded_file = st.file_uploader("문서 파일 업로드", type=["pdf", "docx", "xlsx", "png", "jpg", "txt"])

    # 업로드된 파일명이 있으면 문서 제목 기본값으로 자동 입력, 없으면 빈칸
    if uploaded_file is not None:
        title = st.text_input("문서 제목", value=uploaded_file.name)
    else:
        title = st.text_input("문서 제목")

    uploader = st.text_input("담당자 명")

    submitted = st.form_submit_button("업로드")

    if submitted:
        if not title or not uploader or not uploaded_file:
            st.warning("모든 항목을 입력하고 파일을 업로드해주세요.")
        else:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            new_doc = pd.DataFrame([{
                "제목": title,
                "파일명": uploaded_file.name,
                "업로더": uploader,
                "등록일": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])

            st.session_state.documents = pd.concat(
                [st.session_state.documents, new_doc], ignore_index=True
            )
            st.success("✅ 문서가 업로드되었습니다.")

st.subheader("🔍 문서 목록 및 다운로드")
search = st.text_input("문서 제목 또는 담당자 이름으로 검색")

filtered_docs = (
    st.session_state.documents[
        st.session_state.documents.apply(
            lambda row: search.lower() in row["제목"].lower() or search.lower() in row["업로더"].lower(), axis=1
        )
    ] if search else st.session_state.documents
)

if filtered_docs.empty:
    st.info("등록된 문서가 없습니다.")
else:
    for _, row in filtered_docs.iterrows():
        st.write(f"📄 **{row['제목']}**")
        st.caption(f"업로더: {row['업로더']} | 등록일: {row['등록일']}")
        file_path = os.path.join(UPLOAD_DIR, row["파일명"])
        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ 다운로드",
                data=f,
                file_name=row["파일명"],
                mime="application/octet-stream",
                key=row["파일명"]
            )
        st.markdown("---")

