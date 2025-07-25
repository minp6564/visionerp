import streamlit as st
import datetime
from openai import OpenAI
from data import dummy_data_management as dummy

# 현재 사용자
current_user = "이사원"

# 직원 정보
employees_df = dummy.employees_df
gpt_bots_df = employees_df[employees_df["name"] != current_user]
gpt_bots = gpt_bots_df["name"].tolist()

# GPT system prompt 생성
def generate_prompt(row):
    employee_list = "\n".join(
        f"{r['name']} ({r['position']}, {r['department']}, {r['email']})"
        for _, r in employees_df.iterrows()
    )
    return f"""당신은 {row['department']} 부서의 {row['position']} {row['name']}입니다.
ERP 시스템에서 사용자와 대화하며 업무를 지원합니다.
다음은 전체 직원 명단입니다:
{employee_list}
답변은 직책에 맞는 말투로 하세요."""

bot_prompts = {
    row["name"]: generate_prompt(row) for _, row in gpt_bots_df.iterrows()
}

# API 키 확인
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.error("❌ 먼저 홈 화면에서 OpenAI API 키를 입력해주세요.")
    st.stop()

# 세션 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# GPT 응답 생성 함수
def generate_gpt_reply(bot_name, user_input):
    try:
        prompt = bot_prompts.get(bot_name, "당신은 회사 직원입니다.")

        # 문서 연동: 업로더가 일치하는 문서만 참조
        matched_docs = []
        if "document_knowledge" in st.session_state:
            matched_docs = [doc for doc in st.session_state.document_knowledge if doc.get("업로더") == bot_name]

        if matched_docs:
            doc_context = "\n\n".join(
                f"[{doc['제목']} 요약]: {doc['요약']}\n[본문]: {doc.get('본문', '')[:1000]}"
                for doc in matched_docs
            )
            prompt += f"\n\n다음은 {bot_name}님이 업로드한 문서입니다. 필요 시 참고하세요:\n{doc_context}"
        elif "문서" in user_input or "내용" in user_input:
            return f"그건 제가 업로드 한 문서가 아니라 잘 모르겠습니다."

        client = OpenAI(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(오류: {e})"

# 직원 목록 → 채팅 선택
if "selected_chat_target" not in st.session_state:
    st.set_page_config(page_title="GPT 채팅", layout="wide")
    st.title("💬 사내 채팅")
    st.subheader("대화할 직원 선택")

    for name in gpt_bots:
        row = gpt_bots_df[gpt_bots_df["name"] == name].iloc[0]
        last_msg = next(
            (chat["message"] for chat in reversed(st.session_state.chat_history)
             if chat["sender"] in (name, current_user) and
             (chat.get("receiver") == name or chat.get("receiver") == current_user)),
            "메시지 없음"
        )
        box = st.button(
            label=f"{name} ({row['position']}, {row['department']})\n최근: {last_msg[:50]}",
            key=f"btn_{name}",
            use_container_width=True
        )
        if box:
            st.session_state.selected_chat_target = name
            st.rerun()

# 채팅 UI
else:
    selected_bot = st.session_state.selected_chat_target
    row = gpt_bots_df[gpt_bots_df["name"] == selected_bot].iloc[0]

    st.set_page_config(page_title="GPT 채팅", layout="wide")
    st.title("💬 사내 채팅")
    st.subheader(f"🗨️ {selected_bot} ({row['position']}, {row['department']}) 님과의 대화")

    if st.button("← 직원 목록으로 돌아가기"):
        del st.session_state.selected_chat_target
        st.rerun()

    # 대화 출력
    for chat in st.session_state.chat_history:
        if {chat.get("sender"), chat.get("receiver")} == {current_user, selected_bot}:
            is_user = chat["sender"] == current_user
            align = "flex-end" if is_user else "flex-start"
            bg_color = "#DCF8C6" if is_user else "#F1F0F0"
            st.markdown(
                f"""
                <div style='display: flex; justify-content: {align}; margin-bottom: 10px;'>
                    <div style='background-color: {bg_color}; padding: 10px 15px; border-radius: 12px; max-width: 70%;'>
                        <div style='font-weight: bold;'>{chat['sender']}</div>
                        <div>{chat['message']}</div>
                        <div style='font-size: 10px; color: gray; text-align: right;'>
                            {chat['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # 입력창
    user_input = st.chat_input("메시지를 입력하세요")
    if user_input and user_input.strip():
        now = datetime.datetime.now()
        st.session_state.chat_history.append({
            "sender": current_user,
            "receiver": selected_bot,
            "message": user_input.strip(),
            "timestamp": now
        })

        reply = generate_gpt_reply(selected_bot, user_input.strip())
        st.session_state.chat_history.append({
            "sender": selected_bot,
            "receiver": current_user,
            "message": reply,
            "timestamp": datetime.datetime.now()
        })
        st.rerun()
