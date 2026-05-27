import streamlit as st
from datetime import datetime
import random
import os
import csv

st.title("📄 Conversation Summary")



# Directory to store saved files
SAVE_DIR = "saved_conversations"
os.makedirs(SAVE_DIR, exist_ok=True)

if st.button("Save Conversation"):
    if "conversation" not in st.session_state or not st.session_state.conversation:
        st.warning("No conversation available. Please start from the Chatbot page.")
    else:
        end_time = datetime.now()
        start_time = st.session_state.get("start_time", end_time)
        duration = round((end_time - start_time).total_seconds(), 2)

        # Join the full conversation
        full_convo = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.conversation])
        st.text_area("Conversation", full_convo, height=400)

        # Generate random ID (or use UUID if preferred)
        random_id = random.randint(100000, 999999)
        txt_filename = f"{random_id}.txt"
        txt_path = os.path.join(SAVE_DIR, txt_filename)

        # Save the conversation as a .txt file
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_convo)

        st.success(f"Conversation saved")

        # Save metadata to blind_log.csv
        log_path = os.path.join(SAVE_DIR, "blind_log.csv")
        chatbot_mode = st.session_state.get("chatbot_mode", "N/A")
        case_id = st.session_state.get("case_id", "N/A")

        file_exists = os.path.isfile(log_path)
        with open(log_path, mode="a", newline="", encoding="utf-8") as log_file:
            writer = csv.writer(log_file)
            if not file_exists:
                writer.writerow(["random_id", "chatbot_mode", "case_id", "start_time", "end_time", "duration_seconds"])
            writer.writerow([random_id, chatbot_mode, case_id, start_time.isoformat(), end_time.isoformat(), duration])

        st.success("Log saved to blind_log.csv")

if st.button("🔁 Restart"):
    for key in ["conversation", "diagnosis", "end_conversation", "chatbot_mode", "case_id", "start_time", "end_time", "duration_seconds"]:
        st.session_state.pop(key, None)
    st.rerun()
