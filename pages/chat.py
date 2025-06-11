import streamlit as st
from openai import OpenAI
import datetime

# ✅ 현재 사용자
current_user = "이사원"

# ✅ GPT 역할 목록 및 성격
gpt_bots = ["박과장", "김대리", "정부장"]
bot_system_prompts = {
    "박과장": "당신은 전략적인 사고와 명확한 지시를 중시하는, 경험 있는 과장입니다.",
    "김대리": "당신은 상사의 지시를 이해하고 실무적으로 반응하는 예의 바른 대리입니다.",
    "정부장": "당신은 책임감 있고 권위 있는 부장입니다. 부드럽지만 단호하게 말하세요.",
}

# ✅ API 키 확인
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.error("❌ 먼저 홈 화면에서 OpenAI API 키를 입력해주세요.")
    st.stop()

# ✅ 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = gpt_bots[0]

# ✅ GPT 응답 생성 함수
def generate_gpt_reply(bot_name, user_input):
    system_prompt = bot_system_prompts.get(bot_name, "당신은 회사의 사내 직원입니다.")

    try:
        client = OpenAI(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(GPT 오류: {e})"
# ✅ UI 구성
st.set_page_config(page_title="GPT 채팅", layout="wide")
st.title("💬 사내 GPT 채팅")

# 봇 선택
selected_bot = st.selectbox("🤖 대화할 GPT 직원 선택", gpt_bots)
st.session_state.selected_bot = selected_bot
st.divider()

# ✅ 대화 출력
st.subheader(f"🗨️ {selected_bot} 님과의 대화")
for chat in st.session_state.chat_history:
    with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
        st.markdown(f"**{chat['sender']}**: {chat['message']}")
        st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

# ✅ 입력창 및 전송
user_input = st.text_input("💬 메시지를 입력하세요", key="message_input")

if st.button("✅ 전송") and user_input.strip():
    now = datetime.datetime.now()

    # 유저 메시지 저장
    st.session_state.chat_history.append({
        "sender": current_user,
        "message": user_input.strip(),
        "timestamp": now
    })

    # GPT 응답
    reply = generate_gpt_reply(selected_bot, user_input.strip())
    st.session_state.chat_history.append({
        "sender": selected_bot,
        "message": reply,
        "timestamp": datetime.datetime.now()
    })

    st.rerun()
