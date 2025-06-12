import streamlit as st
import pandas as pd
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI
from data import dummy_data_management as dummy 
import fitz  # PyMuPDF


# 타이틀
st.set_page_config(page_title="문서 관리", layout="wide")
st.title("📚 문서 등록 및 공유")



# 문서 목록 초기화 및 더미 데이터 추가
if 'documents' not in st.session_state:
    st.session_state.documents = pd.DataFrame(columns=[
        "제목", "파일명", "업로더", "등록일", "파일데이터", "요약"
    ])

# API 키 입력
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
st.session_state.api_key = st.text_input("🔑 OpenAI API Key", type="password", value=st.session_state.api_key)

if not st.session_state.api_key:
    st.warning("📌 먼저 OpenAI API Key를 입력하세요.")
    st.stop()

# 버전 있는 파일명 생성 함수
def get_versioned_filename(filename):
    name, ext = re.match(r"(.+?)(\.[^.]+)?$", filename).groups()
    ext = ext or ""
    existing = st.session_state.documents["파일명"].tolist()
    pattern = re.compile(f"{re.escape(name)}(?:_v(\\d+)){re.escape(ext)}")
    versions = [int(m.group(1)) for f in existing if (m := pattern.match(f))]
    if filename in existing:
        versions.append(0)
    new_version = max(versions) + 1 if versions else None
    return filename if new_version is None else f"{name}_v{new_version}{ext}"

# GPT 요약 함수
@st.cache_data(show_spinner=False)
def summarize_text_with_gpt(text):
    try:
        client = OpenAI(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "당신은 ERP 기업 문서 요약 도우미입니다. 문서 내용을 간결하게 요약하세요."},
                {"role": "user", "content": text[:6000]}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"요약 실패: {e}"

# PDF → 텍스트 추출
def extract_text_from_pdf(file_bytes):
    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in pdf)
    except Exception as e:
        return ""


# 업로드 폼
with st.form("upload_form"):
    st.subheader("📤 문서 업로드")
    uploaded_file = st.file_uploader("파일 선택", type=["pdf", "docx", "xlsx", "png", "jpg", "txt"])
    title = st.text_input("문서 제목", value=uploaded_file.name if uploaded_file else "")
    uploader_names = dummy.employees_df["name"].tolist()
    uploader = st.selectbox("담당자 선택", uploader_names)
    submitted = st.form_submit_button("업로드")

    if submitted:
        if not title or not uploader or not uploaded_file:
            st.warning("모든 항목을 입력하고 파일을 업로드하세요.")
        else:
            filename = get_versioned_filename(uploaded_file.name)
            now_kst = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")
            file_bytes = uploaded_file.getvalue()

            if filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(file_bytes)
                summary = summarize_text_with_gpt(text)
            else:
                summary = "(요약은 PDF 문서만 지원됩니다)"

            new_doc = pd.DataFrame([{
                "제목": title,
                "파일명": filename,
                "업로더": uploader,
                "등록일": now_kst,
                "파일데이터": file_bytes,
                "요약": summary
            }])
            st.session_state.documents = pd.concat([st.session_state.documents, new_doc], ignore_index=True)
            st.success(f"✅ 문서 업로드 및 요약 완료: {filename}")

# 문서 목록 검색/정렬
st.subheader("🔍 문서 목록")
col1, col2 = st.columns(2)
with col1:
    search = st.text_input("문서 제목 또는 담당자 검색")
with col2:
    ext_filter = st.selectbox("확장자 필터", ["전체", "pdf", "docx", "xlsx", "png", "jpg", "txt"])

sort_by = st.selectbox("정렬 기준", ["등록일", "제목", "업로더"])
sort_order = st.radio("정렬 순서", ["내림차순", "오름차순"], horizontal=True)

# 필터링
docs = st.session_state.documents.copy()
if search:
    docs = docs[docs.apply(
        lambda r: search.lower() in r["제목"].lower() or search.lower() in r["업로더"].lower(),
        axis=1
    )]
if ext_filter != "전체":
    docs = docs[docs["파일명"].str.lower().str.endswith(ext_filter)]

# 정렬 적용
docs = docs.sort_values(by=sort_by, ascending=(sort_order == "오름차순")).reset_index(drop=True)

# 출력
st.markdown(f"**총 문서 수: {len(docs)}개**")
if docs.empty:
    st.info("등록된 문서가 없습니다.")
else:
    for idx, row in docs.iterrows():
        with st.expander(f"📄 {row['제목']}"):
            st.caption(f"업로더: {row['업로더']} | 등록일: {row['등록일']}")
            st.download_button(
                "⬇️ 다운로드",
                data=row["파일데이터"],
                file_name=row["파일명"],
                mime="application/octet-stream",
                key=f"download_{idx}"
            )
            if row.get("요약"):
                st.markdown("**📌 요약 내용:**")
                st.info(row["요약"])

            col1, col2 = st.columns([3, 1])
            with col1:
                delete_input = st.text_input(
                    f"'{row['제목']}' 삭제 확인용 입력",
                    key=f"delete_input_{idx}",
                    label_visibility="collapsed",
                    placeholder="삭제"
                )
            with col2:
                if st.button("🗑️ 삭제", key=f"delete_btn_{idx}"):
                    if delete_input.strip() == "삭제":
                        st.session_state.documents.drop(index=idx, inplace=True)
                        st.session_state.documents.reset_index(drop=True, inplace=True)
                        st.success(f"✅ '{row['제목']}' 문서가 삭제되었습니다.")
                        st.experimental_rerun()
                    else:
                        st.warning("❗ 삭제하려면 '삭제'라고 입력해 주세요.")
            st.markdown("---")
