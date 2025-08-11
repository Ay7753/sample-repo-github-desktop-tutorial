import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

2
st.title("🤖rizo")
st.write("Ask a question, and chatbot  will reason step by step!")


user_question = st.text_area("Enter your question:", placeholder="Example: A train travels 60 km in 1 hour, then 90 km in 2 hours. What's the average speed?")

if st.button("Generate Answer"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            # Function with fallback
            def generate_answer(question, model_name="gemini-2.0-flash"):
                prompt = f"Question: {question}\nLet's think step by step."
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    return response.text
                except ResourceExhausted:
                    if model_name != "gemini-1.5-flash":
                        st.info("Quota reached for PRO model. Switching to FLASH...")
                        return generate_answer(question, model_name="gemini-1.5-flash")
                    else:
                        return "All quota exhausted. Try again later."

            answer = generate_answer(user_question)
            st.subheader("Chain of Thought Response:")
            st.write(answer)
