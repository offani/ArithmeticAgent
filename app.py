import streamlit as st
from langchain.agents import create_agent
from langchain_groq.chat_models import ChatGroq
from langchain_core.tools import tool
import httpx
from dotenv import load_dotenv
import os

load_dotenv()


VALID_USERS = {
    "aniketh": os.getenv("PASS")
}


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.getenv("groq_api_key") or ""

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .centered-form {display:flex;justify-content:center;}
    .login-box {max-width:600px;width:100%;}
    </style>
    """, unsafe_allow_html=True)
    st.write("This application requires authentication and a Groq API key to proceed.")
    with st.container():
        with st.form("login_form", clear_on_submit=False):
            st.text_input("Username", key="_login_username")
            st.text_input("Password", type="password", key="_login_password")
            st.text_input("Groq API Key", type="password", key="_groq_input")
            cols = st.columns([1, 1])
            submitted = cols[0].form_submit_button("Login")
            cancel = cols[1].form_submit_button("Cancel")
            if submitted:
                uname = st.session_state.get("_login_username", "").strip()
                pwd = st.session_state.get("_login_password", "")
                entered_key = st.session_state.get("_groq_input", "").strip()
                # print(uname,pwd,VALID_USERS.get(uname))
                if not uname or not pwd:
                    st.error("Please enter username and password.")
                elif VALID_USERS.get(uname) != pwd:
                    st.error("Invalid username or password.")
                elif not entered_key:
                    st.error("Please enter a valid Groq API key.")
                else:
                    st.session_state.authenticated = True
                    st.session_state.groq_api_key = entered_key
                    st.rerun()
            if cancel:
                st.stop()
    st.stop()


@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@tool  
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first."""
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second. Avoid dividing by zero."""
    if b == 0:
        return "Error: Division by zero"
    return a / b


@st.cache_resource
def initialize_agent(api_key: str):
    tools = [add, subtract, multiply, divide]
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=api_key,
        http_client=httpx.Client(verify=False),
        streaming=True
    )
    
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""You are a helpful assistant specialized in basic arithmetic operations.

You have access to these tools: add, subtract, multiply, divide.

RULES:
1. For arithmetic questions: ALWAYS use the provided tools to calculate. Never do math in your head.
2. After tools execute, provide a clear, concise final answer.
3. For greetings (hello, hi, hey): Respond warmly and ask how you can help with calculations.
4. For ANY other questions (weather, facts, advice, etc): Politely decline and say: "I'm specialized in basic arithmetic operations only. Please ask me to add, subtract, multiply, or divide numbers."
5. For all the queries not related to arithmetic operations that you perform, respond with: "I'm specialized in basic arithmetic operations only. Please ask me to add, subtract, multiply, or divide numbers."

Never write function syntax like <function=...> in your responses. Just use the tools and explain the result."""
    )
    return agent

# Streamlit UI
st.set_page_config(page_title="Math Agent Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Arithmetic Agent ")
# st.markdown("Ask me to perform arithmetic calculations or just chat!")


if "messages" not in st.session_state:
    st.session_state.messages = []


for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":

            if "intermediate_steps" in msg:
                with st.expander("🔍 View Intermediate Steps", expanded=False):
                    if msg["intermediate_steps"].get("tool_calls"):
                        st.markdown("**🔧 Tool Calls:**")
                        for tool_call in msg["intermediate_steps"]["tool_calls"]:
                            st.markdown(f"- Calling `{tool_call['name']}` with args: `{tool_call['args']}`")
                    
                    if msg["intermediate_steps"].get("tool_results"):
                        st.markdown("**📊 Tool Results:**")
                        for result in msg["intermediate_steps"]["tool_results"]:
                            st.markdown(f"- `{result['name']}`: {result['content']}")
        
        st.markdown(msg["content"])


if user_query := st.chat_input("Enter your query..."):

    st.session_state.messages.append({"role": "user", "content": user_query})
    

    with st.chat_message("user"):
        st.markdown(user_query)
    

    with st.chat_message("assistant"):

        agent = initialize_agent(st.session_state.groq_api_key)
        inputs = {"messages": [("user", user_query)]}
        
        #  placeholders for progressive updates
        steps_placeholder = st.empty()
        response_placeholder = st.empty()
        

        tool_calls_list = []
        tool_results_list = []
        final_response = ""
        
        try:

            for chunk in agent.stream(inputs, stream_mode="values"):
                if "messages" in chunk:
                    messages = chunk["messages"]
                    

                    current_tool_calls = []
                    current_tool_results = []
                    current_response = ""
                    

                    for msg in messages:
                        msg_type = getattr(msg, "type", None)
                        
                        # Skip human messages
                        if msg_type == "human":
                            continue
                        
                        #  tool calls from AI messages
                        if msg_type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                tool_name = tool_call.get("name", "unknown")
                                tool_args = tool_call.get("args", {})
                                tool_call_data = {"name": tool_name, "args": tool_args}
                                if tool_call_data not in current_tool_calls:
                                    current_tool_calls.append(tool_call_data)
                        
                        #  tool results
                        elif msg_type == "tool":
                            tool_name = getattr(msg, "name", "unknown")
                            tool_content = msg.content
                            tool_result_data = {"name": tool_name, "content": tool_content}
                            if tool_result_data not in current_tool_results:
                                current_tool_results.append(tool_result_data)
                        
                        #  final AI response without tool calls
                        elif msg_type == "ai" and hasattr(msg, "content") and msg.content:
                            if not (hasattr(msg, "tool_calls") and msg.tool_calls):
                                current_response = msg.content
                    
                    # Update tool calls and results lists
                    tool_calls_list = current_tool_calls
                    tool_results_list = current_tool_results
                    
                    # Update intermediate steps display
                    if tool_calls_list or tool_results_list:
                        with steps_placeholder.container():
                            with st.expander("🔍 View Intermediate Steps", expanded=False):
                                if tool_calls_list:
                                    st.markdown("**🔧 Tool Calls:**")
                                    for tool_call in tool_calls_list:
                                        st.markdown(f"- Calling `{tool_call['name']}` with args: `{tool_call['args']}`")
                                
                                if tool_results_list:
                                    st.markdown("**📊 Tool Results:**")
                                    for result in tool_results_list:
                                        st.markdown(f"- `{result['name']}`: {result['content']}")
                    
                    # Stream response 
                    if current_response and current_response != final_response:
          
                        for i in range(len(final_response), len(current_response)):
                            final_response = current_response[:i+1]
                            response_placeholder.markdown(final_response + "▌")
                            import time
                            time.sleep(0.01)  
                        final_response = current_response
            
  
            if final_response:
                response_placeholder.markdown(final_response)
            else:
                final_response = "I've processed your request."
                response_placeholder.markdown(final_response)
        
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            st.error(error_message)
            final_response = error_message
        
        #  assistant response to chat history with intermediate steps log
        message_data = {"role": "assistant", "content": final_response}
        if tool_calls_list or tool_results_list:
            message_data["intermediate_steps"] = {
                "tool_calls": tool_calls_list,
                "tool_results": tool_results_list
            }
        st.session_state.messages.append(message_data)


with st.sidebar:
    st.header("About")
    st.markdown("""
    This is your Basic Math  Assistant powered by:
    - **LangChain** for agent orchestration
    - **Groq** for LLM inference
    - **Streamlit** for the UI
    
    ### Available Tools:
    - ➕ Add
    - ➖ Subtract
    - ✖️ Multiply
    - ➗ Divide
    
    ### Example Queries:
    - "Add 10 and 10, then subtract 5 from it and multiply by 4."
    - "What is 2 + 2 * 3 - 4 / 2?"
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
