import streamlit as st
import datetime
from openai import OpenAI
from data import dummy_data_management as dummy

# 현재 사용자
current_user = "이사원"

# 직원 정보 불러오기
employees_df = dummy.employees_df

gpt_bots_df = employees_df[employees_df["name"] != current_user]
gpt_bots = gpt_bots_df["name"].tolist()

# system prompt 생성 함수
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

# 세션 상태 초기화
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}  # {bot_name: [...messages]}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

if "unread_counts" not in st.session_state:
    st.session_state.unread_counts = {name: 0 for name in gpt_bots}

# GPT 응답 함수
def generate_gpt_reply(bot_name, user_input):
    try:
        prompt = bot_prompts.get(bot_name, "당신은 회사 직원입니다.")
        client = OpenAI(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(GPT 오류: {e})"

# --- UI ---
st.set_page_config(page_title="GPT 채팅", layout="wide")

# 1️⃣ 대화방 목록
if st.session_state.active_chat is None:
    st.title("💬 GPT 직원 목록")
    st.markdown("대화하고 싶은 GPT 직원을 선택하세요:")

    # 최근 대화 정렬
    recent_sorted = sorted(
        gpt_bots,
        key=lambda name: (
            st.session_state.chat_histories.get(name, [])[-1]["timestamp"] if st.session_state.chat_histories.get(name) else datetime.datetime.min
        ),
        reverse=True
    )

    for name in recent_sorted:
        label = f"{name} 님과 대화하기"
        unread = st.session_state.unread_counts.get(name, 0)
        if unread:
            label += f" 🔴 {unread}"
        if st.button(label):
            st.session_state.active_chat = name
            if name not in st.session_state.chat_histories:
                st.session_state.chat_histories[name] = []
            st.session_state.unread_counts[name] = 0
            st.rerun()
    st.stop()

# 2️⃣ 선택된 GPT와의 대화방
selected_bot = st.session_state.active_chat
st.title(f"🗨️ {selected_bot} 님과의 대화")

if st.button("⬅️ 대화방 나가기"):
    st.session_state.active_chat = None
    st.rerun()

chat_history = st.session_state.chat_histories[selected_bot]

# 대화 출력
for chat in chat_history:
    with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
        st.markdown(f"**{chat['sender']}**: {chat['message']}")
        st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

# 입력창
user_input = st.chat_input("💬 메시지를 입력하세요")

if user_input and user_input.strip():
    now = datetime.datetime.now()
    chat_history.append({
        "sender": current_user,
        "message": user_input.strip(),
        "timestamp": now
    })

    reply = generate_gpt_reply(selected_bot, user_input.strip())
    chat_history.append({
        "sender": selected_bot,
        "message": reply,
        "timestamp": datetime.datetime.now()
    })

    # 읽지 않은 메시지 카운트 증가 (다른 채팅방에만 적용)
    for name in gpt_bots:
        if name != selected_bot:
            st.session_state.unread_counts[name] = st.session_state.unread_counts.get(name, 0) + 1

    st.rerun()
