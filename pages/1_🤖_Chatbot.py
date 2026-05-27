import streamlit as st
from datetime import datetime
from chatbot import get_chatbot_config, get_interview_response

st.title("🤖 Patient Interview Chatbot")

# --- Initial setup of session state ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "diagnosis" not in st.session_state:
    st.session_state.diagnosis = ""
if "end_conversation" not in st.session_state:
    st.session_state.end_conversation = False
if "i" not in st.session_state:
    st.session_state.i = 0
if "responder" not in st.session_state:
    st.session_state.responder = None
if "age" not in st.session_state:
    st.session_state.age = None
if "gender" not in st.session_state:
    st.session_state.gender = None
if "submitted_basic_info" not in st.session_state:
    st.session_state.submitted_basic_info = False
if "chatbot_mode" not in st.session_state:
    st.session_state.chatbot_mode = 1  # default to mode 1
if "case_id" not in st.session_state:
    st.session_state.case_id = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()


# --- Step 0: Select chatbot configuration ---

if not st.session_state.submitted_basic_info:
    st.session_state.case_id = st.text_input("Please enter case ID", value="")
    #st.subheader("Select Chatbot Mode")
    st.session_state.chatbot_mode = st.radio(
        "Choose a chatbot configuration",
        options=[1, 2, 3, 4],
        format_func=lambda x: {
            1: "1",
            2: "2",
            3: "3",
            4: "4"
        }[x],
        horizontal=True
        
    )

    # --- Step 1: Collect basic patient information ---
    
    relationship_options = [
        "Patient themselves",
        "Parent",
        "Spouse",
        "Child",
        "Sibling",
        "Caregiver",
        "Friend",
        "Other (please specify)"
        ]
    
    responder_option = st.selectbox(
        "Who is answering this questionnaire?",
        options=relationship_options
        )

    # Placeholder for final value
    final_responder = None

    # If "Other", enforce text entry
    if responder_option == "Other (please specify)":
        other_detail = st.text_input("Please specify your relationship")
    
        if not other_detail:
            st.error("Please enter a relationship before continuing.")
        else:
            final_responder = f"Other: {other_detail}"
    else:
        final_responder = responder_option

    st.session_state['responder'] = final_responder

    st.session_state.age = st.number_input("Please provide the patient's age.", min_value=0, max_value=120, step=1)
    st.session_state.gender = st.radio("Please provide the patient's sex assigned at birth.", ["Male", "Female"])

    if st.button("Start Chat"):
        st.session_state.submitted_basic_info = True
        if len(st.session_state.conversation) == 0:
            st.session_state.conversation.append({
                "role": "assistant",
                "content": "What brings you in today? Do you have any health concerns?"
            })
        st.rerun()


else:
    # --- Step 2: Display chat history ---
    for entry in st.session_state.conversation:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

    # --- Step 3: Chat input area ---
    if not st.session_state.end_conversation:
        user_input = st.chat_input("Please tell us your health concerns here")

        if user_input:
            st.session_state.conversation.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            st.session_state.i += 1

            # --- Condition 1: Max turns reached (30 messages) ---
            if len(st.session_state.conversation) >= 30:
                st.session_state.end_conversation = True
                st.session_state.conversation.append({
                    "role": "assistant",
                    "content": "Thank you for your cooperation. Please wait here until the physician is ready to see you."
                })
                st.rerun()

            else:
                # --- Generate LLM response ---
                full_history = "\n".join(
                    [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.conversation]
                )
                detail, think = get_chatbot_config(st.session_state.chatbot_mode)
                
                ai_response = get_interview_response(
                    full_history,
                    responder=st.session_state.responder,
                    age=st.session_state.age,
                    gender=st.session_state.gender,
                    detail=detail,
                    think=think
                )

                # --- Condition 2: End-phrases from model ---
                END_PHRASES = [
                    "Please consult with the physician next",
                    "This concludes the interview",
                    "I’ll now summarize your information for the doctor"
                ]
                if any(phrase in ai_response for phrase in END_PHRASES):
                    st.session_state.end_conversation = True
                    st.session_state.conversation.append({
                        "role": "assistant",
                        "content": "Thank you for your cooperation. Please wait here until the physician is ready to see you."
                    })
                    st.rerun()
                else:
                    st.session_state.conversation.append({"role": "assistant", "content": ai_response})
                    with st.chat_message("assistant"):
                        st.markdown(ai_response)

    # --- Step 4: End interview button ---
    if st.button("End Interview"):
        st.session_state.end_conversation = True
        full_convo = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.conversation])
        st.success("The interview has ended. Thank you for your cooperation.")
