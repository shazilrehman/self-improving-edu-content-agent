import streamlit as st
from agent import generate_improved_lesson

st.title("🧠 LearnWith.AI - Self-Improving Educational Agent")
st.markdown("**LangGraph + Ollama** — Self-Improving Content Generator Demo")

with st.form("lesson_form"):
    topic = st.text_input("Topic", "Causes of World War II")
    subject = st.selectbox("Subject", ["History", "Science", "Biology", "Physics"])
    grade = st.selectbox("Grade Level", ["5th Grade", "8th Grade", "10th Grade", "High School"])
    profile = st.text_input("Student Profile (learning style)", "visual learner who struggles with timelines")
    
    submitted = st.form_submit_button("🚀 Generate & Self-Improve Lesson")
    
    if submitted:
        with st.spinner("🧠 Agent is working... (20-60 seconds per step, first run is slowest)"):
            content = generate_improved_lesson(topic, subject, grade, profile)
            st.success("✅ Final Improved Lesson")
            st.markdown(content)

st.caption("This agent uses LangGraph reflection loops to iteratively improve educational content — matching LearnWith.AI requirements.")