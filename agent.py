from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

# Faster settings
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.7,
    num_ctx=4096,      # smaller context = faster
    num_predict=1024   # limit output length
)

class AgentState(TypedDict):
    topic: str
    subject: str
    grade_level: str
    student_profile: str
    content: str
    critique: str
    revision_count: int

def generate_content(state: AgentState):
    prompt = f"""Expert {state['subject']} teacher. Create engaging personalized content.

Topic: {state['topic']}
Grade: {state['grade_level']}
Student: {state['student_profile']}

Provide: Explanation + Example + 2 Questions + Key Takeaways."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"content": response.content, "revision_count": state.get("revision_count", 0) + 1}

def critique_content(state: AgentState):
    prompt = f"""Quick critique of this content. Be concise. List 2-3 main improvements needed.

Content: {state['content'][:1500]}"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"critique": response.content}

def should_continue(state: AgentState):
    if state.get("revision_count", 0) >= 2:   # Reduced from 3 → faster
        return "end"
    return "revise"

# Simplified Graph
workflow = StateGraph(AgentState)
workflow.add_node("generate", generate_content)
workflow.add_node("critique", critique_content)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "critique")
workflow.add_conditional_edges("critique", should_continue, {"revise": "generate", "end": END})

app = workflow.compile()

def generate_improved_lesson(topic: str, subject: str = "History", grade: str = "8th Grade", profile: str = "visual learner"):
    result = app.invoke({
        "topic": topic,
        "subject": subject,
        "grade_level": grade,
        "student_profile": profile,
        "revision_count": 0
    })
    print(f"✅ Done! ({result.get('revision_count')} steps)")
    return result["content"]