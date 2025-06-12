import streamlit as st
import pandas as pd
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI
from data import dummy_data_management as dummy
import fitz  # PyMuPDF
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="문서 관리", layout="wide")

# ✅ API 키 확인
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.error("❌ 홈 화면에서 OpenAI API 키를 먼저 입력해 주세요.")
    st.stop()

# ✅ 문서 데이터프레임 초기화
if 'documents' not in st.session_state:
    st.session_state.documents = pd.DataFrame(columns=[
        "제목", "파일명", "업로더", "등록일", "파일데이터", "요약", "임베딩", "전체텍스트"
    ])

if 'document_knowledge' not in st.session_state:
    st.session_state.document_knowledge = []

# ✅ 버전 있는 파일명 생성

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

# ✅ GPT 요약 및 임베딩 함수
@st.cache_data(show_spinner=False)
def summarize_and_embed_with_gpt(text):
    try:
        client = OpenAI(api_key=st.session_state.api_key)
        summary_resp = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "당신은 ERP 기업 문서 요약 도우미입니다. 문서 내용을 간결하게 요약하세요."},
                {"role": "user", "content": text[:6000]}
            ],
            temperature=0.3
        )
        summary = summary_resp.choices[0].message.content.strip()
        emb_resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8191]
        )
        embedding = emb_resp.data[0].embedding
        return summary, embedding
    except Exception as e:
        return f"요약 실패: {e}", []

# ✅ PDF 텍스트 추출 함수
def extract_text_from_pdf(file_bytes):
    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in pdf)
    except Exception:
        return ""

# ✅ 타이틀
st.title("📚 문서 등록 및 공유")

# ✅ 문서 업로드 폼
with st.form("upload_form", clear_on_submit=True):
    st.subheader("📤 문서 업로드")
    uploaded_file = st.file_uploader("파일 선택", type=["pdf", "docx", "xlsx", "png", "jpg", "txt"])
    title = st.text_input("문서 제목", value=uploaded_file.name if uploaded_file else "")
    uploader = st.selectbox("담당자 선택", dummy.employees_df["name"].tolist())
    submitted = st.form_submit_button("업로드")

    if submitted and uploaded_file and title and uploader:
        filename = get_versioned_filename(uploaded_file.name)
        now_kst = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")
        file_bytes = uploaded_file.getvalue()

        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
            summary, embedding = summarize_and_embed_with_gpt(text)
        else:
            text = "(텍스트 추출 불가)"
            summary, embedding = "(요약은 PDF 문서만 지원됩니다)", []

        new_doc = pd.DataFrame([{
            "제목": title,
            "파일명": filename,
            "업로더": uploader,
            "등록일": now_kst,
            "파일데이터": file_bytes,
            "요약": summary,
            "임베딩": embedding,
            "전체텍스트": text
        }])
        st.session_state.documents = pd.concat([st.session_state.documents, new_doc], ignore_index=True)

        st.session_state.document_knowledge.append({
            "제목": title,
            "요약": summary,
            "전체텍스트": text,
            "업로더": uploader
        })

        st.success(f"✅ 문서 업로드 및 요약 완료: {filename}")
