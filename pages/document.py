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
        "제목", "파일명", "업로더", "등록일", "파일데이터", "요약", "임베딩"
    ])

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
def summarize_and_embed_with_gpt(title, text):
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
        embedding_input = f"{title}\n\n{text[:8000]}"
        emb_resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=embedding_input
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
    uploader = st.selectbox("담당자 선택", dummy.employees_df["name"].tolist())
    submitted = st.form_submit_button("업로드")

    if submitted and uploaded_file and uploader:
        filename = get_versioned_filename(uploaded_file.name)
        title = uploaded_file.name.rsplit('.', 1)[0]  # 파일명에서 확장자 제거

        now_kst = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")
        file_bytes = uploaded_file.getvalue()

        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
            summary, embedding = summarize_and_embed_with_gpt(title, text)
        else:
            summary, embedding = "(요약은 PDF 문서만 지원됩니다)", []

        new_doc = pd.DataFrame([{
            "제목": title,
            "파일명": filename,
            "업로더": uploader,
            "등록일": now_kst,
            "파일데이터": file_bytes,
            "요약": summary,
            "임베딩": embedding
        }])
        st.session_state.documents = pd.concat([st.session_state.documents, new_doc], ignore_index=True)
        st.success(f"✅ 문서 업로드 및 요약 완료: {filename}")

# ✅ 검색 입력
col1, col2 = st.columns(2)
with col1:
    search = st.text_input("문서 제목 또는 담당자 검색")
with col2:
    gpt_query = st.text_input("💡 GPT 기반 문서 검색어 입력")

# ✅ 필터링 설정
col1, col2 = st.columns(2)
with col1:
    ext_filter = st.selectbox("확장자 필터", ["전체", "pdf", "docx", "xlsx", "png", "jpg", "txt"])
with col2:
    sort_by = st.selectbox("정렬 기준", ["등록일", "제목", "업로더"])
sort_order = st.radio("정렬 순서", ["내림차순", "오름차순"], horizontal=True)

# ✅ 문서 검색 수행
filtered_docs = st.session_state.documents.copy()

if search:
    filtered_docs = filtered_docs[filtered_docs.apply(
        lambda r: search.lower() in r["제목"].lower() or search.lower() in r["업로더"].lower(), axis=1
    )]

if gpt_query:
    try:
        client = OpenAI(api_key=st.session_state.api_key)
        query_emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=gpt_query
        ).data[0].embedding

        title_sims, content_sims = [], []
        for _, row in filtered_docs.iterrows():
            title_emb = client.embeddings.create(
                model="text-embedding-3-small",
                input=row["제목"]
            ).data[0].embedding
            title_sim = cosine_similarity([query_emb], [title_emb])[0][0] if title_emb else 0.0
            content_sim = cosine_similarity([query_emb], [row["임베딩"]])[0][0] if row["임베딩"] else 0.0
            title_sims.append(title_sim)
            content_sims.append(content_sim)

        filtered_docs["제목 유사도"] = title_sims
        filtered_docs["본문 유사도"] = content_sims

        colw1, colw2 = st.columns(2)
        with colw1:
            w_title = st.slider("제목 유사도 가중치", 0.0, 1.0, 0.3, 0.05)
        with colw2:
            st.caption(f"본문 유사도 가중치: {1 - w_title:.2f}")

        filtered_docs["종합 유사도"] = w_title * filtered_docs["제목 유사도"] + (1 - w_title) * filtered_docs["본문 유사도"]
        filtered_docs = filtered_docs.sort_values(by="종합 유사도", ascending=False)

    except Exception as e:
        st.warning(f"GPT 검색 실패: {e}")
else:
    if ext_filter != "전체":
        filtered_docs = filtered_docs[filtered_docs["파일명"].str.lower().str.endswith(ext_filter)]
    filtered_docs = filtered_docs.sort_values(by=sort_by, ascending=(sort_order == "오름차순")).reset_index(drop=True)

# ✅ 문서 목록 출력
st.markdown(f"**총 문서 수: {len(filtered_docs)}개**")
if filtered_docs.empty:
    st.info("등록된 문서가 없습니다.")
else:
    for idx, row in filtered_docs.iterrows():
        with st.expander(f"📄 {row['제목']}" + (f" (🧠 {row['종합 유사도']:.2f})" if "종합 유사도" in row else "")):
            if "제목 유사도" in row:
                st.caption(f"제목 유사도: {row['제목 유사도']:.2f} | 본문 유사도: {row['본문 유사도']:.2f}")
            st.caption(f"업로더: {row['업로더']} | 등록일: {row['등록일']}")
            st.download_button("⬇️ 다운로드", row["파일데이터"], file_name=row["파일명"], mime="application/octet-stream", key=f"down_{idx}")
            if row["요약"]:
                st.markdown("**📌 요약:**")
                st.info(row["요약"])
            if row["임베딩"]:
                if st.button("🔎 임베딩 보기", key=f"embed_btn_{idx}"):
                    st.json(row["임베딩"])
            col1, col2 = st.columns([3,1])
            with col1:
                delete_input = st.text_input("삭제하려면 '삭제' 입력", key=f"del_in_{idx}", label_visibility="collapsed", placeholder="삭제")
            with col2:
                if st.button("🗑️ 삭제", key=f"del_btn_{idx}"):
                    if delete_input.strip() == "삭제":
                        st.session_state.documents = st.session_state.documents.drop(index=idx).reset_index(drop=True)
                        st.success(f"✅ '{row['제목']}' 삭제 완료")
                        st.rerun()
                    else:
                        st.warning("❗ '삭제'라고 입력해야 삭제됩니다.")
