import streamlit as st
import pdfplumber
from openai import OpenAI

# Configure Ollama API
OLLAMA_API = "http://localhost:11434/api/chat"
MODEL = "llama3.2"
ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text if text else "Error extracting text from PDF"

# Summarize resume content
def summarize_resume(text):
    prompt = f"Summarize the following resume in a structured format:\n\n{text}"
    response = ollama_via_openai.completions.create(model=MODEL, prompt=prompt)
    return response.choices[0].text.strip()

# Generate initial question
def get_initial_question(resume_summary):
    prompt = f"Generate a relevant opening interview question based on this resume summary:\n\n{resume_summary}"
    response = ollama_via_openai.completions.create(model=MODEL, prompt=prompt)
    return response.choices[0].text.strip()

# Evaluate answer with metrics
def evaluate_answer(question, answer):
    prompt = f"""
    Evaluate the candidate's answer based on these criteria:
    - **Relevance (0-10)**: How well does the answer match the question?
    - **Grammar (0-10)**: Is the grammar correct?
    - **Clarity & Coherence (0-10)**: Is the answer clear and logically structured?
    - **Conciseness (0-10)**: Is the answer precise and to the point?
    - **Overall Score (0-10)**: Weighted average score.

    Question: {question}
    Answer: {answer}

    Return the response in this format:
    Relevance: X/10
    Grammar: X/10
    Clarity: X/10
    Conciseness: X/10
    Overall Score: X/10
    Feedback: [Short feedback]
    """
    response = ollama_via_openai.completions.create(model=MODEL, prompt=prompt)
    return response.choices[0].text.strip()

# Generate follow-up question dynamically
def get_followup_question(conversation_history):
    prompt = f"""
    Based on this conversation history, generate the next logical follow-up question:

    {conversation_history}

    Ensure the question is relevant to previous responses.
    """
    response = ollama_via_openai.completions.create(model=MODEL, prompt=prompt)
    return response.choices[0].text.strip()

# Generate final performance review
def generate_performance_review(conversation_history):
    prompt = f"""
    Provide an overall feedback report for this candidate based on the interview conversation history:

    {conversation_history}

    The feedback should include:
    - Strengths
    - Areas for improvement
    - Final scores for Relevance, Grammar, Clarity, Conciseness, and Overall Performance.
    - Overall rating out of 10.
    """
    response = ollama_via_openai.completions.create(model=MODEL, prompt=prompt)
    return response.choices[0].text.strip()

# Streamlit UI
st.title("📄 AI Resume Chatbot")
st.sidebar.header("Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_summary = summarize_resume(resume_text)

    st.subheader("📌 Resume Summary")
    st.write(resume_summary)

    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "questions_asked" not in st.session_state:
        st.session_state.questions_asked = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = get_initial_question(resume_summary)
        st.session_state.conversation_history.append(f"🤖 AI: {st.session_state.current_question}")

    st.subheader("💬 AI Interactive Interview")

    # Display chat history
    for chat in st.session_state.conversation_history:
        st.write(chat)

    # User input for answering questions
    user_input = st.text_input("Your Answer:")

    if st.button("Submit"):
        if user_input:
            # Store user's response
            st.session_state.conversation_history.append(f"**You:** {user_input}")
            st.session_state.questions_asked += 1

            # Evaluate answer
            evaluation_result = evaluate_answer(st.session_state.current_question, user_input)
            st.write(f"📊 Evaluation:\n{evaluation_result}")

            # Ask next question if <5 questions asked
            if st.session_state.questions_asked < 5:
                next_question = get_followup_question("\n".join(st.session_state.conversation_history))
                st.session_state.current_question = next_question
                st.session_state.conversation_history.append(f"🤖 AI: {next_question}")
            else:
                # Generate final performance review after 5 questions
                performance_review = generate_performance_review("\n".join(st.session_state.conversation_history))
                st.session_state.conversation_history.append(f"🏆 Final Performance Review:\n\n{performance_review}")
                st.session_state.current_question = "Interview Completed 🎉"

            st.rerun()
