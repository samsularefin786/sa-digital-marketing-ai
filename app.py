import streamlit as st
from google import genai
from datetime import datetime

st.set_page_config(
    page_title="SA Digital Marketing AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #10131c;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #171c29;
}
.stButton button {
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("SA Marketing AI")
st.sidebar.caption("Your Private AI Workspace")

agent = st.sidebar.selectbox(
    "Select Agent",
    [
        "Main Marketing Agent",
        "SEO Specialist",
        "Content Writer",
        "On-Page SEO",
        "Technical SEO",
        "Competitor Analyst",
        "SMM Specialist"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("Workspace")
st.sidebar.write("Dashboard")
st.sidebar.write("Task History")
st.sidebar.write("Reports")
st.sidebar.write("Settings")

# Main Dashboard
st.title("SA Digital Marketing AI")
st.caption("Your AI-powered Digital Marketing Workspace")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Status", "IDLE")

with col2:
    st.metric("Active Tasks", "0")

with col3:
    st.metric("Mode", "On Demand")

st.divider()

st.subheader("AI Workspace")

task = st.text_area(
    "What would you like me to do?",
    placeholder="Example: Analyze this website and create an SEO strategy...",
    height=150
)

start = st.button(
    "START TASK",
    type="primary",
    use_container_width=True
)

if "history" not in st.session_state:
    st.session_state.history = []

if start:

    if not task.strip():
        st.warning("Please enter a task first.")

    else:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]

            client = genai.Client(api_key=api_key)

            instructions = f"""
You are SA Digital Marketing AI,
a professional digital marketing assistant.

Selected Agent: {agent}

Your responsibilities:
- SEO
- Keyword Research
- Content Writing
- On-Page SEO
- Technical SEO
- Competitor Analysis
- Social Media Marketing
- Digital Marketing Strategy

Rules:
1. Follow the user's exact instructions.
2. Never claim to have accessed a website unless you actually did.
3. Clearly separate verified facts from assumptions.
4. Provide practical and actionable recommendations.
5. Do not perform any task without user instruction.
6. Do not initiate background tasks.
7. Answer in the language used by the user.

User Task:
{task}
"""

            with st.status("Working on your task...", expanded=True):
                response = client.models.generate_content(
                   model="gemini-3.1-flash-lite",
                    contents=instructions
                )

            st.success("Task Completed")

            st.markdown("### Result")
            st.markdown(response.text)

            st.session_state.history.append({
                "agent": agent,
                "task": task,
                "result": response.text,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            client.close()

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()

st.subheader("Recent Task History")

for item in reversed(st.session_state.history):
    with st.expander(
        f"{item['agent']} | {item['time']}"
    ):
        st.write(item["task"])
        st.markdown(item["result"])

st.caption("SA Digital Marketing AI | On-Demand Workspace")
