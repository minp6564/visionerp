import streamlit as st
import datetime
from openai import OpenAI
from data import dummy_data_management as dummy

# 현재 사용자
current_user = "이사원"

# 직원 정보 불러오기
employees_df = dummy.employees_df

# ✅ GPT 봇 후보로 등록 (이사원은 제외)
gpt_bots_df = employees_df[employees_df["name"] != current_user]

# 봇 이름 목록
gpt_bots = gpt_bots_df["name"].tolist()

# GPT system prompt 자동 생성
# system_prompt 생성 시 employees_df 전체를 추가
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

# ✅ API 키 확인
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.error("❌ 먼저 홈 화면에서 OpenAI API 키를 입력해주세요.")
    st.stop()

# ✅ 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_bot" not in st.session_state:
    st.session_state.selected_bot = gpt_bots[0]

# ✅ GPT 응답 함수
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

# ✅ UI
st.set_page_config(page_title="GPT 채팅", layout="wide")
st.title("💬 사내 GPT 채팅")

selected_bot = st.selectbox("🤖 대화할 GPT 직원 선택", gpt_bots)
st.session_state.selected_bot = selected_bot

st.divider()
st.subheader(f"🗨️ {selected_bot} 님과의 대화")

# 대화 내용
for chat in st.session_state.chat_history:
    with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
        st.markdown(f"**{chat['sender']}**: {chat['message']}")
        st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

# 입력창
with st.container():
    st.markdown("---")

user_input = st.chat_input("💬 메시지를 입력하세요")

if user_input and user_input.strip():
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
