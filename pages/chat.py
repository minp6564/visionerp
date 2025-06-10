# rerun 플래그 초기화
if "trigger_rerun" not in st.session_state:
    st.session_state.trigger_rerun = False

# 전송 버튼 처리
if st.button("전송"):
    saved_file_path = None

    if uploaded_file:
        file_name = uploaded_file.name
        saved_file_path = os.path.join(UPLOAD_DIR, file_name)
        with open(saved_file_path, "wb") as f:
            f.write(uploaded_file.read())

    if message.strip() or saved_file_path:
        new_chat = {
            "sender": current_user,
            "message": message if message.strip() else None,
            "file_path": saved_file_path,
            "timestamp": datetime.datetime.now(),
        }

        if chat_mode == "1:1 채팅":
            new_chat.update({
                "mode": "private",
                "receiver": receiver
            })
        else:
            new_chat.update({
                "mode": "custom_group",
                "room": selected_room
            })

        st.session_state.chat_history.append(new_chat)

        with open(SAVE_FILE, "wb") as f:
            pickle.dump(st.session_state.chat_history, f)

        st.session_state.trigger_rerun = True  # 🔸 여기에서만 True로 설정
    else:
        st.warning("메시지나 파일을 입력해주세요.")

# 🔁 rerun은 여기서 별도로 실행
if st.session_state.get("trigger_rerun"):
    st.session_state.trigger_rerun = False
    st.experimental_rerun()
