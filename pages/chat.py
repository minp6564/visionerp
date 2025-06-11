import streamlit as st
import datetime
import os
import uuid
import random

# 폴더 생성
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 설정
current_user = "이사원"
gpt_bots = ["박과장", "김대리", "정부장"]
group_room = "GPT 단체방"

# GPT 성격 프롬프트 (내부 참고용)
bot_prompts = {
    "박과장": "전략적인 사고와 명확한 지시를 중시하는, 경험 있는 과장답게 응답하시오.",
    "김대리": "상사의 지시를 이해하고 실무적으로 응답하는 대리답게 응답하시오. 공손하면서도 실질적인 대화로 이어가시오.",
    "정부장": "업무 전반을 관리하는 부장답게 책임감 있고 신중하며 권위 있는 말투로 응답하시오.",
}

# GPT 답변 예시
bot_replies = {
    "박과장": [
        "좋습니다. 일단 그 방향으로 추진해보죠.",
        "이번 건은 일정이 중요하니, 계획대로 밀고 가도록 하세요.",
        "성과를 낼 수 있도록 팀원들과 조율 바랍니다.",
    ],
    "김대리": [
        "네, 곧 처리해서 보고드리겠습니다!",
        "방금 말씀하신 내용은 확인 후 바로 공유드릴게요.",
        "최대한 꼼꼼히 준비하겠습니다.",
    ],
    "정부장": [
        "그 사안은 조직 전체에 영향을 줄 수 있으니 신중히 접근해야 합니다.",
        "관련 부서와 협의 후 최종 결정하겠습니다.",
        "리스크를 감안하여 대안을 마련해 두는 것이 좋겠습니다.",
    ],
}

# GPT 응답 생성
def generate_gpt_reply(bot_name, user_input):
    return random.choice(bot_replies.get(bot_name, ["네, 확인했습니다."]))

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("💬 GPT 단체방 채팅")

# 채팅 이력 표시
st.subheader(f"📢 [{group_room}] 대화방")

for chat in st.session_state.chat_history:
    if chat.get("room") == group_room:
        with st.chat_message("user" if chat["sender"] == current_user else "assistant"):
            st.markdown(f"**{chat['sender']}**: {chat['message']}")
            st.caption(chat["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

# 입력창
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("메시지를 입력하세요", key="message_input")
with col2:
    if st.button("전송"):
        if user_input.strip():
            now = datetime.datetime.now()

            # 사용자 메시지 저장
            st.session_state.chat_history.append({
                "sender": current_user,
                "message": user_input.strip(),
                "timestamp": now,
                "room": group_room,
            })

            # 각 GPT 멤버가 순차적으로 응답
            for bot in gpt_bots:
                gpt_msg = generate_gpt_reply(bot, user_input)
                st.session_state.chat_history.append({
                    "sender": bot,
                    "message": gpt_msg,
                    "timestamp": datetime.datetime.now(),
                    "room": group_room,
                })

            st.rerun()
        else:
            st.warning("메시지를 입력하세요.")
