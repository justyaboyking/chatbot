30. Two cylindrical candles burn evenly.
    The linear relation between the length [l] in cm and the time [t] in hours
    of these two candles is graphically represented below.
    
    a. Which graph belongs to the thickest candle?
    b. Why do you think that?
    c. You light both candles at the same time.
       After how many hours is the thin candle as tall as the thicker candle?
    d. Which formula fits the thinnest candle?
    e. How long does it take to burn 10 cm of the thickest candle?
    
    31. Two taxi companies calculate their price in different ways.
    Company A uses the formula: price = € 2.50 x number of km + € 3.10.
    Company B uses the formula: price = € 2.30 x number of km + € 5.50.
    
    a. Which company is cheapest for a 7 km ride?
    b. You need to go 20 km home. Which company do you choose?
    c. At what number of kilometers driven are both companies equally expensive?
       Use ICT to find the solution.
    d. How much do you have to pay then?
    """
    
    page_content[219] = """
    Page 219 contains the following exercises:
    
    32. Gardening company VABI charges € 75 plus € 3.45 per m² for garden maintenance.
    
    a. What is the cost of maintaining a garden of 380 m²?
    b. Mrs. Lesage has a garden of 12 a 75 ca. How much will she have to pay?
    c. Mr. Vanhee had his garden fixed up. He received a bill of 2,638.35 euros.
       How big is Mr. Vanhee's garden?
    
    33. Yasin's truck consumed 45 liters of fuel after 250 km.
    
    a. How many liters of fuel does the truck consume to travel 100 km?
    b. The truck's fuel tank can hold 500 liters. How many kilometers can Yasin drive with that?
       Round to the unit.
    """
    
    return page_content

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemini-1.5-flash"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "show_presets" not in st.session_state:
    st.session_state.show_presets = True
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None
if "copied_message" not in st.session_state:
    st.session_state.copied_message = None
if "current_page" not in st.session_state:
    st.session_state.current_page = None
if "page_content_data" not in st.session_state:
    st.session_state.page_content_data = get_page_content()
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# Define direct answers prompt
formatted_answers_prompt = """# Math Answer Formatter

Your task is to provide complete answers to math exercises in a clear, structured format.

## Instructions:

1. When the student only enters a page number, automatically give ALL answers for that page in the correct format.

2. Format for answers:
   - Use clear headings like "Exercise 10" (with number)
   - Briefly mention the question
   - Give the answer directly
   - For tables, fill in all values
   - For calculations, show basic operations but no lengthy explanations

3. Example of good formatting:
   Exercise 10: The relation between quantity and cost price
   Question: Fill in the missing values in the table.

   a. 
   Quantity | 0 | 1 | 2 | 3
   Cost price (€) | 50 | 40 | 30 | 20

4. Use a consistent format for all answers with clear separation between exercises.

5. Give direct, clear answers without lengthy explanations.
"""

# Define presets
presets = {
    "math_homework": {
        "content": formatted_answers_prompt
    }
}

# Example answer format for Gemini
example_answer_format = """
Exercise 10: The relation between quantity and cost price
Question: Fill in the missing values in the table, knowing that the relation between the quantity and the cost price is linear.

We have the following table:

Quantity	0	1	2	3
Cost price (€)	50	40	30	20

Exercise 12: Complete the table using the formulas
Question 12a: p = 4 x z

The completed table for 12a is:
z	0	1	2	3	5	15
p	0	4	8	12	20	60

Question 12b: p = 10 + (2 x t)

The completed table for 12b is:
t	0	1	2	3	5	15
p	10	12	14	16	20	40

Question 12c: p = d x 3.14

The completed table for 12c is:
d	0	1	2	3	5	15
p	0	3.14	6.28	9.42	15.7	47.1
"""

# Configure Gemini API - Use environment variables for security
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"  # Fallback for testing
genai.configure(api_key=api_key)

# Sidebar with improved styling
with st.sidebar:
    # Logo and Brand
    st.markdown("""
    <div class="brand-logo">
        <div class="logo-icon">📐</div>
        <div class="logo-text">Math Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom buttons instead of standard Streamlit ones
    st.markdown("""
    <button class="sidebar-button" id="new-chat-btn" onclick="window.location.reload()">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px;">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
        </svg>
        New Chat
    </button>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Homework sections
    st.markdown("#### 📚 Homework Modules")
    
    # Math button
    if st.button("📐 Math Homework", key="math_btn"):
        st.session_state.messages = []
        st.session_state.context = presets["math_homework"]["content"]
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Which page(s) of your math workbook would you like to cover? (pages 208-221)"
        })
        st.session_state.show_presets = False
        st.session_state.active_chat = "Math Homework Helper"
        st.rerun()
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # AI Settings
    with st.expander("🤖 AI Settings", expanded=False):
        model_options = {
            "Gemini 1.5 Flash": "gemini-1.5-flash",
            "Gemini 2.0 Flash Thinking": "gemini-2.0-flash-thinking-exp-01-21",
            "Gemini 2.0 Flash-Lite": "gemini-2.0-flash-lite"
        }
        
        selected_model = st.selectbox(
            "AI Model:",
            options=list(model_options.keys()),
            index=list(model_options.values()).index(st.session_state.model_name) if st.session_state.model_name in list(model_options.values()) else 0
        )
        st.session_state.model_name = model_options[selected_model]
        
        st.session_state.temperature = st.slider(
            "Creativity:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            format="%.1f"
        )

# Main chat interface
main_container = st.container()

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Initial greeting
if st.session_state.show_presets and not st.session_state.messages:
    with main_container:
        st.session_state.messages = []
        st.session_state.context = ""
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "👋 Hello! How can I help you with your homework today? Choose a module in the menu on the left."
        })
        st.session_state.show_presets = False
        st.rerun()

# Display chat messages with modern styling
with main_container:
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Display thinking animation if needed
    if st.session_state.thinking:
        with st.chat_message("assistant"):
            st.markdown("""
            <div class="thinking-container">
                <div class="thinking-icon"></div>
                <span class="thinking-text">Thinking</span>
                <div class="thinking-dots"><span></span><span></span><span></span></div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Type your question here...")
if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.show_presets = False
    
    # Create active chat if none exists
    if not st.session_state.active_chat:
        chat_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
        st.session_state.active_chat = chat_title
    
    # Set thinking state to true
    st.session_state.thinking = True
    
    # Show user message immediately
    st.rerun()

# Handle AI response generation (after rerun with user message visible)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and st.session_state.thinking:
    user_input = st.session_state.messages[-1]["content"]
    
    try:
        # Configure the model
        model = genai.GenerativeModel(
            st.session_state.model_name,
            generation_config={"temperature": st.session_state.temperature}
        )
        
        # Check if user is requesting a specific page in Math mode
        if st.session_state.active_chat == "Math Homework Helper":
            # Direct page number input - check if it's just a number
            if user_input.isdigit() and 208 <= int(user_input) <= 221:
                st.session_state.current_page = int(user_input)
            
            # Check for page number in text input
            elif "page" in user_input.lower():
                page_nums = [int(s) for s in user_input.split() if s.isdigit() and 208 <= int(s) <= 221]
                if page_nums:
                    st.session_state.current_page = page_nums[0]
            
            # Alternative detection for "do page X" pattern
            elif "do" in user_input.lower() and "page" in user_input.lower():
                page_nums = [int(s) for s in user_input.split() if s.isdigit() and 208 <= int(s) <= 221]
                if page_nums:
                    st.session_state.current_page = page_nums[0]
        
        # Prepare prompt with context if needed
        if st.session_state.active_chat == "Math Homework Helper" and st.session_state.context:
            if st.session_state.current_page:
                page_content = st.session_state.page_content_data.get(st.session_state.current_page, f"Page {st.session_state.current_page} contains various math exercises.")
                
                # If only a page number is entered, automatically give all answers
                if user_input.isdigit() and 208 <= int(user_input) <= 221:
                    complete_prompt = f"""
                    Context information:
                    {st.session_state.context}
                    
                    Page content:
                    {page_content}
                    
                    Format example:
                    {example_answer_format}
                    
                    The student has selected page {st.session_state.current_page}. Give all answers according to the format example.
                    Important format:
                    - Use clear headings with exercise numbers: "Exercise 10"
                    - Briefly mention the question for each exercise
                    - Show all completed tables fully
                    - Use a similar format to the example
                    
                    Now give all complete answers for page {st.session_state.current_page}.
                    """
                # Otherwise, just answer the specific question
                else:
                    complete_prompt = f"""
                    Context information:
                    {st.session_state.context}
                    
                    Page content:
                    {page_content}
                    
                    Format example:
                    {example_answer_format}
                    
                    The student is working on page {st.session_state.current_page} and asks: "{user_input}"
                    
                    Answer this question according to the format example. If it concerns a specific exercise number, 
                    handle that specific number completely.
                    """
            else:
                # No page selected yet - but try to extract it from the input
                if user_input.isdigit() and 208 <= int(user_input) <= 221:
                    st.session_state.current_page = int(user_input)
                    page_content = st.session_state.page_content_data.get(st.session_state.current_page, f"Page {st.session_state.current_page} contains various math exercises.")
                    
                    complete_prompt = f"""
                    Context information:
                    {st.session_state.context}
                    
                    Page content:
                    {page_content}
                    
                    Format example:
                    {example_answer_format}
                    
                    The student has selected page {st.session_state.current_page}. Give all answers according to the format example.
                    Important format:
                    - Use clear headings with exercise numbers: "Exercise 10"
                    - Briefly mention the question for each exercise
                    - Show all completed tables fully
                    - Use a similar format to the example
                    
                    Now give all complete answers for page {st.session_state.current_page}.
                    """
                else:
                    # No page selected yet
                    complete_prompt = f"""
                    Context information:
                    {st.session_state.context}
                    
                    The student has not yet selected a specific page. Ask them to just type a page number (between 208-221).
                    """
        else:
            complete_prompt = user_input
        
        # Turn off thinking state
        st.session_state.thinking = False
        
        # Generate AI response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response with enhanced animation
            for response in model.generate_content(
                complete_prompt,
                stream=True
            ):
                if hasattr(response, 'text'):
                    chunk = response.text
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)  # Short delay to make typing visible
            
            # Final display without cursor
            message_placeholder.markdown(full_response)
                    
            # Add assistant message to chat history after streaming completes
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        # Handle errors
        st.error(f"Error: {str(e)}")
        
        # Add error message to chat
        st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})
        
        # Turn off thinking state
        st.session_state.thinking = False
    
    # Rerun to update UI with new messages
    st.rerun()
import streamlit as st 
import google.generativeai as genai
import time
import os
import re
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="Math Assistant",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with animations and professional styling
st.markdown("""
<style>
    /* === FONTS === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* === BASE STYLES === */
    body {
        color: white;
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    /* === SIDEBAR STYLING === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1c24 0%, #13151c 100%);
        border-right: 1px solid rgba(42, 45, 54, 0.5);
        box-shadow: 2px 0 10px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
        padding: 0.5rem 0;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    
    /* Sidebar dividers */
    .sidebar-divider {
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
    }
    
    /* Sidebar buttons */
    .sidebar-button {
        background: linear-gradient(90deg, #3a7bd5 0%, #2b5876 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        padding: 10px 15px;
        margin: 5px 0;
        text-align: center;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
        display: block;
        font-size: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .sidebar-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .sidebar-button-secondary {
        background: linear-gradient(90deg, #4b6cb7 0%, #253546 100%);
    }
    
    /* Custom expander styling */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        margin-bottom: 1rem;
        overflow: hidden;
        background-color: rgba(20, 22, 30, 0.3);
    }
    
    [data-testid="stExpander"] > details > summary {
        padding: 1rem;
        font-weight: 600;
        display: flex;
        align-items: center;
    }
    
    [data-testid="stExpander"] > details > summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    [data-testid="stExpander"] > details > summary::before {
        content: "↓";
        margin-right: 0.5rem;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stExpander"] > details[open] > summary::before {
        content: "↓";
        transform: rotate(180deg);
    }
    
    [data-testid="stExpander"] > details > div {
        padding: 1rem;
        animation: fadeIn 0.3s ease;
    }
    
    /* === CHAT STYLING === */
    /* Modern chat message container */
    [data-testid="stChatMessage"] {
        background-color: #23252f;
        border-radius: 12px;
        margin: 0.9rem 0;
        padding: 1.2rem;
        border: none;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
        animation: fadeInUp 0.3s ease;
        transition: all 0.3s ease;
        border-left: 4px solid transparent;
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #2a304a;
        border-left: 4px solid #4168e4;
    }
    
    /* AI message styling */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #293042;
        border-left: 4px solid #38b6ff;
    }
    
    /* Chat message animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Fixed chat input */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 20%;
        right: 0;
        background: linear-gradient(180deg, rgba(14, 17, 23, 0) 0%, rgba(14, 17, 23, 0.95) 20%);
        backdrop-filter: blur(10px);
        padding: 1.5rem 2rem;
        border-top: none;
        z-index: 99;
    }
    
    /* Chat input field */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(35, 37, 47, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px 15px;
        font-size: 15px;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stChatInput"] textarea:focus {
        background-color: rgba(35, 37, 47, 1);
        border-color: #38b6ff;
        box-shadow: 0 0 0 2px rgba(56, 182, 255, 0.2);
    }
    
    /* Chat container spacing */
    .chat-container {
        margin-top: 20px;
        margin-bottom: 100px;
        padding: 1rem 2rem;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* === UTILITY STYLES === */
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 34, 44, 0.2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(106, 116, 143, 0.5);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(106, 116, 143, 0.8);
    }
    
    /* Thinking animation */
    .thinking-container {
        display: flex;
        align-items: center;
        padding: 14px 18px;
        background: linear-gradient(135deg, #293042 0%, #324155 100%);
        border-radius: 12px;
        margin: 12px 0;
        width: fit-content;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #5e87f5;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(94, 135, 245, 0.3);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(94, 135, 245, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(94, 135, 245, 0);
        }
    }
    
    .thinking-icon {
        display: inline-block;
        width: 24px;
        height: 24px;
        margin-right: 12px;
        background: rgba(94, 135, 245, 0.3);
        border-radius: 50%;
        position: relative;
        animation: iconPulse 1.5s infinite;
    }
    
    @keyframes iconPulse {
        0% { transform: scale(0.95); }
        50% { transform: scale(1.05); }
        100% { transform: scale(0.95); }
    }
    
    .thinking-icon::before,
    .thinking-icon::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: rgba(94, 135, 245, 0.4);
        transform: translate(-50%, -50%);
    }
    
    .thinking-icon::after {
        width: 8px;
        height: 8px;
        background: rgba(94, 135, 245, 0.8);
    }
    
    .thinking-text {
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
        margin-right: 8px;
    }
    
    .thinking-dots {
        display: inline-block;
    }
    
    .thinking-dots span {
        animation: dot 1.4s infinite;
        animation-fill-mode: both;
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.8);
        margin-right: 4px;
    }
    
    .thinking-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .thinking-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes dot {
        0%, 80%, 100% { opacity: 0; transform: scale(0.6); }
        40% { opacity: 1; transform: scale(1); }
    }
    
    /* Copy button styling */
    .copy-button {
        background: rgba(94, 135, 245, 0.2);
        border: 1px solid rgba(94, 135, 245, 0.4);
        color: rgba(255, 255, 255, 0.9);
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-flex;
        align-items: center;
        margin-top: 10px;
    }
    
    .copy-button:hover {
        background: rgba(94, 135, 245, 0.3);
        transform: translateY(-2px);
    }
    
    .copy-button svg {
        margin-right: 5px;
        width: 14px;
        height: 14px;
    }
    
    .copy-success {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(46, 125, 50, 0.9);
        color: white;
        padding: 10px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideInRight 0.3s ease, fadeOut 0.5s ease 2s forwards;
        display: flex;
        align-items: center;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
    
    /* Brand logo */
    .brand-logo {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding: 10px 15px;
        background: linear-gradient(135deg, #1a1c24 0%, #13151c 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
        margin-right: 10px;
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
    }
    
    .logo-text {
        font-size: 18px;
        font-weight: 600;
        background: linear-gradient(90deg, #eef2f3, #8e9eab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* App watermark */
    .watermark {
        position: fixed;
        bottom: 80px;
        right: 20px;
        color: rgba(255, 255, 255, 0.4);
        font-size: 12px;
        z-index: 1000;
        pointer-events: none;
        background-color: rgba(0, 0, 0, 0.2);
        padding: 5px 10px;
        border-radius: 6px;
        backdrop-filter: blur(5px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
    }
    
    .watermark svg {
        width: 14px;
        height: 14px;
        margin-right: 5px;
        opacity: 0.7;
    }
</style>

<!-- Copy Success Notification (Hidden by default) -->
<div id="copySuccess" class="copy-success" style="display: none;">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px;">
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
    </svg>
    Text copied!
</div>

<!-- Clipboard.js for better copy functionality -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>

<!-- Custom JavaScript for copy functionality and animations -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize clipboard functionality for all copy buttons
    const clipboard = new ClipboardJS('.copy-btn');
    
    clipboard.on('success', function() {
        const successEl = document.getElementById('copySuccess');
        successEl.style.display = 'flex';
        
        // Hide the notification after 2 seconds
        setTimeout(function() {
            successEl.style.display = 'none';
        }, 2500);
    });
    
    // Function to create copy buttons for each message
    function addCopyButtons() {
        const messages = document.querySelectorAll('[data-testid="stChatMessage"]');
        
        messages.forEach((message, index) => {
            // Only add if button doesn't already exist
            if (!message.querySelector('.copy-button')) {
                const content = message.textContent;
                
                // Create button
                const btn = document.createElement('button');
                btn.className = 'copy-button copy-btn';
                btn.setAttribute('data-clipboard-text', content);
                
                // Add SVG icon
                btn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                        <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                    </svg>
                    Copy
                `;
                
                // Add button to message
                message.appendChild(btn);
            }
        });
    }
    
    // Add copy buttons initially and when messages change
    addCopyButtons();
    
    // Check for new messages every second
    setInterval(addCopyButtons, 1000);
});
</script>

<div class="watermark">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="2" y1="12" x2="22" y2="12"></line>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg>
    Created by Zakaria
</div>
""", unsafe_allow_html=True)

# Define function to get page content
def get_page_content():
    # Dictionary of page content descriptions
    page_content = {
        208: """
        Page 208 contains the following exercises:
        
        10. The relation between the quantity and the cost price (in euros) is linear.
        Fill in the missing values in the table.
        
        a. 
        Quantity | 0 | 1 | 2 | 3
        Cost price (€) | 50 | 40 | | 
        
        b.
        Quantity | 0 | 1 | 2 | 3
        Cost price (€) | 10 | 15 | | 
        
        c.
        Quantity | 0 | 1 | 2 | 3
        Cost price (€) | 16 | 16 | | 
        
        d.
        Quantity | 0 | 1 | 2 | 3
        Cost price (€) | 0 | 2.5 | | 
        
        11. You buy a number of the products below.
        a. Show the relation between the quantity and the cost price (in euros) with a table.
        Product A: €4.5/piece
        Product B: €1.25/piece
        
        12. Complete the table using the formulas.
        a. p = 4 x z
        z | 0 | 1 | 2 | 3 | 5 | 15
        p | | | | | | 
        
        b. p = 10 + (2 x t)
        t | 0 | 1 | 2 | 3 | 5 | 15
        p | | | | | | 
        
        c. p = d x 3.14
        d | 0 | 1 | 2 | 3 | 5 | 15
        p | | | | | | 
        
        13. The linear relation between temperature [T] and time [t] is presented in tables.
        """,
        
        209: """
        Page 209 contains the following exercises:
        
        13. (continued)
        a. Fill in the missing values in the tables.
        
        Table A:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 0 | 4 | 8 | 
        
        Table B:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 1 | 4 | 7 | 
        
        Table C:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 8 | 6 | 4 | 
        
        Table D:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 3 | 3 | 3 | 
        
        b. Which table matches which formula?
        T = 4 x t
        T = 1 + (3 x t)
        T = 3
        T = 8 - (2 x t)
        
        c. Which table matches which graph? [Four graphs are shown in the book]
        
        d. In which table do you notice an increasing linear relation?
        In which table do you notice a decreasing linear relation?
        In which table do you notice a constant linear relation?
        """,
        
        210: """
        Page 210 contains the following exercises:
        
        14. The relation between mass [in kilograms] and cost price [in euros] is linear.
        Fill in the missing values in the table.
        
        a. mass | 0 | 1 | 2 | 3
           cost price | 0 | 3.5 | | 
        
        b. mass | 0.5 | 1 | 1.5 | 5
           cost price | 5 | 10 | | 
           
        c. mass | 0.1 | 0.2 | 0.5 | 1
           cost price | 2 | 4 | | 
           
        d. mass | 0.25 | 0.5 | 1 | 1.5
           cost price | | | 8 | 12
        
        15. The relation between time [in hours] and cost price [in euros] is linear.
        Fill in the missing values in the table.
        
        a. time | 0 | 0.5 | 1 | 1.5
           cost price | 10 | | 60 | 
           
        b. time | 0 | 0.25 | 1 | 2
           cost price | 0 | 25 | | 
           
        c. time | 0 | 0.1 | 0.5 | 1
           cost price | 50 | | | 110
           
        d. time | 0 | 0.25 | 0.5 | 1
           cost price | 5 | | 15 | 
        """,
        
        211: """
        Page 211 contains the following exercises:
        
        16. The relation between time [in weeks] and mass [in kilograms] is linear.
        a. Fill in the missing values in the table.
        
        Table A:
        time | 0 | 1 | 2 | 5
        mass | 80 | 75 | | 
        
        Table B:
        time | 0 | 1 | 2.5 | 6
        mass | 50 | 48 | | 
        
        b. Which table matches which description?
        When time increases by one week, then:
        • the mass increases by 5 kg.
        • the mass increases by 2 kg.
        • the mass decreases by 5 kg.
        • the mass decreases by 2 kg.
        
        c. Which table matches which graph? [Graphs are shown in the book]
        
        17. Complete the table using the formulas.
        a. z = 35 x t
        t | 0 | 1 | 2 | 3 | 5 | 10
        z | | | | | | 
        
        b. h = 100 - (5 x u)
        u | 0 | 1 | 2 | 3 | 5 | 20
        h | | | | | | 
        
        c. k = 7.5 + (0.5 x m)
        m | 0 | 1 | 2 | 3 | 5 | 30
        k | | | | | | 
        """,
        
        212: """
        Page 212 contains the following exercises:
        
        18. Show the relation between the number of drinks and the amount with a table.
        Which formula did you use to calculate the amount? Fill in.
        Do you notice an increasing, decreasing, or constant relation? Indicate.
        
        a. For one drink you pay € 2.40 on the terrace of the Grand Place.
        
        number of drinks (n) | 0 | 1 | 2 | 3 | 4 | 10
        amount (a) in euros | | | | | | 
        
        b. You pay € 8 entry at a party. Drinks cost € 1.80.
        
        number of drinks (n) | 0 | 1 | 2 | 3 | 4 | 10
        amount (a) in euros | | | | | | 
        
        c. You have € 30 with you. In the cafeteria, a drink costs € 2.10.
        
        number of drinks | 0 | 1 | 2 | 3 | 4 | 10
        amount (a) in euros | | | | | | 
        
        d. For € 2 extra you can use the toilet for free all evening.
        
        number of toilet visits | 0 | 1 | 2 | 3 | 4 | 10
        amount (a) in euros | | | | | | 
        """
    }
    
    # Pages 220-221 to add
    page_content[220] = """
    Page 220 contains the following exercises:
    
    34. When you buy a new freezer, the appliance has taken on the room temperature of 20 °C.
    Only after connecting does the temperature (T) begin to drop according to the formula T = 20 - (5 x t),
    where t represents the number of hours.
    
    a. Complete the table with the relation between temperature and time.
       
       time (t) in hours | 0 | 1 | 2 | 3 | 4
       temperature (T) in °C | | | | | 
    
    b. After how many hours is the freezing point reached?
    
    c. After how many hours is a temperature of -10 °C reached?
    
    35. In a thermometer, the colored rod consists of a liquid.
    The height (h) of the liquid increases as the temperature T (in °C) rises.
    The height of the liquid in cm can be calculated with the formula h = 3.3 + (T x 0.068).
    
    a. What is the height of the liquid when it is 20 °C?
    
    b. At what temperature is the height of the liquid 6 cm?
    Round to one decimal place.
    """
    
    page_content[221] = """
    Page 221 contains the following exercises:
    
    36. With a microwave oven, you can defrost and heat frozen food. The time required
    depends on the mass of the food product.
    The time it takes to defrost and heat 0.5 liters of soup is determined by the formula
    T = -20 + (8 x t), where t is the time in minutes and T is the temperature in °C.
    
    a. Complete the table with the relation between temperature and time.
       
       time (t) in minutes | 0 | 1 | 2 | 3 | 4
       temperature (T) in °C | | | | | 
    
    b. After how many minutes and seconds is the freezing point (0 °C) reached?
    
    c. After how many minutes and seconds is the soup 30 °C?
    """
    
    # Simplified content for the remaining pages
    for page_num in range(213, 220):
        page_content[page_num] = f"""
        Page {page_num} contains various math exercises about linear relations, 
        formulas, tables, and graphs. 
        """
    
    # Add more detailed information for specific pages
    page_content[218] = """
    Page 218 contains the following exercises:
    
    30. Two cylindrical candles burn evenly.
