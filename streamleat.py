import streamlit as st
from pydantic import BaseModel
from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
from config import google_api_key, GROQ_API_KEY

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
llm = ChatGroq(model="openai/gpt-oss-120b", groq_api_key=GROQ_API_KEY)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            '''
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools.
            Always include a "Sources:" section (with URLs, one per line, starting with "-") and a "Tools used:" section (with tool names, one per line, starting with "-").
            Respond ONLY with the important content, no code blocks, no JSON, no YAML, just clear and concise text.
            '''
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

st.title("Deep Research Agent")

if "history" not in st.session_state:
    st.session_state.history = []

# Use a form for input and submit, and clear input after each submission
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

with st.form(key="qa_form", clear_on_submit=True):
    user_input = st.text_input("What can I help you research?", value=st.session_state.current_input, key="input_box")
    submitted = st.form_submit_button("Submit")


# Simple memory: if user asks for previous answer, show last answer from history
def is_previous_answer_query(text):
    text = text.lower()
    return (
        "previous answer" in text
        or "repeat last answer" in text
        or "last answer" in text
        or "previous response" in text
        or "repeat previous" in text
    )

if submitted and user_input:
    if user_input.strip().lower() == "exit":
        st.success("Session ended. Refresh to start a new session.")
        st.stop()
    elif is_previous_answer_query(user_input):
        if st.session_state.history:
            entry = st.session_state.history[-1]
            st.info("Repeating previous answer:")
        else:
            st.warning("No previous answer found.")
            entry = None
    else:
        with st.spinner("Researching..."):
            raw_response = None
            entry = None
            try:
                raw_response = agent_executor.invoke({"query": user_input})
                output_str = raw_response.get("output").strip()
                # Simple extraction for sources and tools_used
                sources = []
                tools_used = []
                answer_lines = []
                in_sources = False
                in_tools = False
                for line in output_str.splitlines():
                    l = line.strip()
                    if l.lower().startswith("sources:"):
                        in_sources = True
                        in_tools = False
                        continue
                    if l.lower().startswith("tools used:"):
                        in_tools = True
                        in_sources = False
                        continue
                    if in_sources:
                        if l.startswith("-"):
                            sources.append(l[1:].strip())
                        elif l:
                            sources.append(l)
                        else:
                            in_sources = False
                    elif in_tools:
                        if l.startswith("-"):
                            tools_used.append(l[1:].strip())
                        elif l:
                            tools_used.append(l)
                        else:
                            in_tools = False
                    else:
                        answer_lines.append(line)
                answer = "\n".join(answer_lines).strip()
                entry = {
                    "question": user_input,
                    "answer": answer,
                    "sources": sources,
                    "tools_used": tools_used
                }
                st.session_state.history.append(entry)
                st.session_state.current_input = ""
            except Exception as e:
                st.error(f"Error: {e}\nRaw Response: {raw_response}")
    # Show only the latest answer (from memory or new)
    if st.session_state.history and (entry is not None):
        st.markdown(f"**Q:** {entry['question']}")
        st.write(entry['answer'])
        if entry.get("sources"):
            st.markdown("**Sources:**")
            for src in entry["sources"]:
                st.markdown(f"- {src}")
        if entry.get("tools_used"):
            st.markdown("**Tools used:** " + ", ".join(entry["tools_used"]))
        st.markdown("---")
# streamlit run streamleat.py   