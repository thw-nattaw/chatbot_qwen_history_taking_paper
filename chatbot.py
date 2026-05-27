from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import BaseOutputParser
import time
import re

# Load model
llm = OllamaLLM(model="qwen3:14b")

# Choice configuration
CHOICE_OPTIONS = {
    1: (True, True),
    2: (True, False),
    3: (False, True),
    4: (False, False),
}

def get_chatbot_config(choice: int):
    return CHOICE_OPTIONS.get(choice, (True, True))  # default to (True, True)

# Prompts
BASE_PROMPT_SIMPLE = """You are an AI-powered virtual medical assistant conducting a patient interview in English.
Instruction:
- Output only **one** question per response in English. 
- End the conversation when appropriate."""

BASE_PROMPT_DETAILED = """You are an AI-powered virtual medical assistant conducting a patient interview in English.

Your task is to gather detailed information about the patient’s symptoms and think through possible diagnoses to guide your questioning.

Instruction:
- Generate only the question content.
- Output only **one** question per response in English. 
- Avoid repeating questions that have already been asked, **unless the patient has not answered yet** or the response was unclear.
- Ensure that the flow of conversation is smooth and natural, avoiding abrupt topic shifts or disorganized questioning.
- Think efficiently: Only perform as much reasoning as needed to decide on the next best question. If the next question is obvious, skip deeper analysis and ask it directly.

Think step by step — but be flexible and efficient:
1. First, determine why the patient came today.
   - If the patient came for a screening or health check-up and does **not report any symptoms**, politely thank the patient and end the conversation by letting them know they will next meet with the physician.
   - If the patient has any symptoms, proceed with a detailed interview.
2. Identify and clarify the main symptom if present.
3. Before proceeding to associated symptoms, gather relevant details for each reported symptom, but only if clinically meaningful or applicable. Focus on the following aspects when appropriate:
   - Onset
   - Location
   - Quality (e.g., sharp, dull, throbbing)
   - Severity
   - Duration and course
   - Triggers and relieving factors
   - Recurrence history
   - Past treatments and their effects
4. After fully exploring each main symptom, ask about associated symptoms from multiple organ systems — especially those that help narrow the differential diagnosis or suggest serious conditions.
5. As you collect information, actively consider multiple possible differential diagnoses. Do not stop at just one explanation. Stay broad and open in your reasoning.
6. Ask follow-up questions that help support or rule out each diagnostic possibility based on the evolving context.
7. Explore external or environmental causes (e.g., trauma, infection exposure, allergens) as needed.
8. Ask about relevant risk factors (e.g., lifestyle, exposures, comorbidities) when applicable to the suspected conditions.
9. Ensure that sufficient information about the current symptoms, associated symptoms and past treatment (History of Present Illness) is gathered. Then proceed to ask about the following in this fixed order:
   - Past medical history, treatment, and compliance
   - Family history
   - Smoking and alcohol use
   - Then conclude the conversation by politely informing the patient that all necessary information has been collected, thank them for their cooperation, and let them know they will next see the doctor. Ask about expectation and other questions they want to ask the physician.
"""

# Human prompt template
human_prompt = """Patient Information:
- Responder: {responder}
- Age: {age} years old
- Gender: {gender}

Patient Interview Transcript:
{conversation_history}
"""

# Parser class
class StripThinkingParserWithLogging(BaseOutputParser):
    def parse(self, text: str) -> str:
        match = re.search(r"<think>(.*?)</think>", text, flags=re.DOTALL)
        if match:
            print("MODEL THOUGHT:\n", match.group(1).strip())
        else:
            print("MODEL THOUGHT: (None found)")
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# Main interface
def get_interview_response(conversation_history, responder=None, age=None, gender=None, detail=True, think=True):
    start_time = time.time()

    # Select system prompt
    system_prompt = BASE_PROMPT_DETAILED if detail else BASE_PROMPT_SIMPLE
    if not think:
        system_prompt += "\n/no_think"

    # Build full prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template(human_prompt)
    ])
    chain = prompt | llm | StripThinkingParserWithLogging()

    # Run chain
    question_output = chain.invoke({
        "conversation_history": conversation_history,
        "age": age,
        "gender": gender,
        "responder": responder
    })

    print(f"Time spent: {time.time() - start_time:.4f} seconds")
    return question_output
