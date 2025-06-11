import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_versioned_filename(directory, filename):
    name, ext = os.path.splitext(filename)
    pattern = re.compile(re.escape(name) + r'_v(\d+)' + re.escape(ext))
    existing_versions = []
    for f in os.listdir(directory):
        m = pattern.fullmatch(f)
        if m:
            existing_versions.append(int(m.group(1)))
        elif f == filename:
            existing_versions.append(0)
    if not existing_versions:
        return filename
    else:
        new_version = max(existing_versions) + 1
        return f"{name}_v{new_version}{ext}"

if 'documents' not in st.session_state:
    st.session_state.documents = pd.DataFrame(columns=["제목", "파일명", "업로더", "등록일"])

if 'delete_confirm' not in st.session_state:
    st.session_state.delete_confirm = None  # 삭제 확인 대상 idx 저장

st.title("📚 문서 등록 및 공유 페이지")

with st.form("upload_form"):
    st.subheader("📤 문서 업로드")
    uploaded_file = st.file_uploader("문서 파일 업로드", type=["pdf", "docx", "xlsx", "png", "jpg", "txt"])
    title = st.text_input("문서 제목", value=uploaded_file.name if uploaded_file else "")
    uploader = st.text_input("담당자 명")
    submitted = st.form_submit_button("업로드")

    if submitted:
        if not title or not uploader or not uploaded_file:
            st.warning("모든 항목을 입력하고 파일을 업로드해주세요.")
        else:
            versioned_filename = get_versioned_filename(UPLOAD_DIR, uploaded_file.name)
            file_path = os.path.join(UPLOAD_DIR, versioned_filename)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            now_kst = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

            new_doc = pd.DataFrame([{
                "제목": title,
                "파일명": versioned_filename,
                "업로더": uploader,
                "등록일": now_kst
            }])
            st.session_state.documents = pd.concat([st.session_state.documents, new_doc], ignore_index=True)
            st.success(f"✅ 문서가 업로드되었습니다. 저장된 파일명: {versioned_filename}")

st.subheader("🔍 문서 목록 및 다운로드 / 삭제")

col1, col2 = st.columns(2)
with col1:
    search = st.text_input("문서 제목 또는 담당자 이름 검색")
with col2:
    ext_filter = st.selectbox("확장자 필터", ["전체", "pdf", "docx", "xlsx", "png", "jpg", "txt"])

sort_by = st.selectbox("정렬 기준", ["등록일", "제목", "업로더"])
sort_order = st.radio("정렬 순서", ["내림차순", "오름차순"], horizontal=True)

filtered = st.session_state.documents.copy()

if search:
    filtered = filtered[filtered.apply(lambda r: search.lower() in r["제목"].lower() or search.lower() in r["업로더"].lower(), axis=1)]

if ext_filter != "전체":
    filtered = filtered[filtered["파일명"].str.lower().str.endswith(ext_filter)]

ascending = sort_order == "오름차순"
filtered = filtered.sort_values(by=sort_by, ascending=ascending).reset_index(drop=True)

st.markdown(f"**총 문서 수: {len(filtered)}개**")

if filtered.empty:
    st.info("등록된 문서가 없습니다.")
else:
    for idx, row in filtered.iterrows():
        file_path = os.path.join(UPLOAD_DIR, row["파일명"])
        st.write(f"📄 **{row['제목']}**")
        st.caption(f"업로더: {row['업로더']} | 등록일: {row['등록일']}")
        size_kb = os.path.getsize(file_path) / 1024
        st.caption(f"파일 크기: {size_kb:.1f} KB")

        if row["파일명"].lower().endswith((".png", ".jpg", ".jpeg")):
            st.image(file_path, width=300)
        elif row["파일명"].lower().endswith(".pdf"):
            st.components.v1.iframe(f"{UPLOAD_DIR}/{row['파일명']}", height=400)

        col1, col2 = st.columns([3, 1])
        with col1:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️ 다운로드",
                    data=f,
                    file_name=row["파일명"],
                    mime="application/octet-stream",
                    key=f"download_{row['파일명']}"
                )
        with col2:
            if st.session_state.delete_confirm == idx:
                st.warning(f"'{row['제목']}' 문서를 삭제하시겠습니까? 삭제를 원하면 다시 삭제 버튼을 눌러주세요.")
                if st.button("🗑️ 삭제 확인", key=f"confirm_delete_{idx}"):
                    try:
                        os.remove(file_path)
                    except FileNotFoundError:
                        pass
                    st.session_state.documents = st.session_state.documents.drop(idx).reset_index(drop=True)
                    st.success(f"'{row['제목']}' 문서가 삭제되었습니다.")
                    st.session_state.delete_confirm = None
                    st.experimental_rerun()
            else:
                if st.button("🗑️ 삭제", key=f"delete_{idx}"):
                    st.session_state.delete_confirm = idx
        st.markdown("---")
