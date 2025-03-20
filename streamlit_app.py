import streamlit as st 
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="Homework Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS styling
st.markdown("""
<style>
    /* === FONTS === */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* === BASE STYLES === */
    body {
        color: white;
        background-color: #0e0e16;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.3s ease;
    }
    
    h1, h2, h3, h4, h5 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* === SIDEBAR STYLING === */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #111124 0%, #0d0d1a 100%);
        border-right: 1px solid rgba(60, 65, 94, 0.2);
        box-shadow: 2px 0 20px rgba(0,0,0,0.4);
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
        padding: 0.5rem 0;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Sidebar dividers */
    .sidebar-divider {
        border-top: 1px solid rgba(255,255,255,0.07);
        margin: 1.2rem 0;
    }
    
    /* Subject cards */
    .subject-card {
        display: flex;
        align-items: center;
        background: rgba(42, 48, 80, 0.2);
        border: 1px solid rgba(80, 90, 140, 0.2);
        border-radius: 12px;
        color: white;
        font-weight: 500;
        padding: 12px 16px;
        margin: 10px 0;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
    }
    
    .subject-card:hover {
        transform: translateY(-3px);
        border: 1px solid rgba(100, 110, 160, 0.4);
        background: rgba(42, 48, 80, 0.4);
    }
    
    .subject-card .icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 14px;
        font-size: 20px;
        flex-shrink: 0;
    }
    
    .subject-card .content {
        flex-grow: 1;
    }
    
    .subject-card .title {
        font-weight: 600;
        margin-bottom: 2px;
        font-size: 15px;
    }
    
    .subject-card .description {
        font-size: 12px;
        color: rgba(255,255,255,0.6);
    }
    
    /* Themes for different subjects */
    .math-card .icon {
        background: linear-gradient(135deg, #3a7bd5, #3a6073);
    }
    
    .science-card .icon {
        background: linear-gradient(135deg, #11998e, #38ef7d);
    }
    
    .language-card .icon {
        background: linear-gradient(135deg, #f46b45, #eea849);
    }
    
    .history-card .icon {
        background: linear-gradient(135deg, #614385, #516395);
    }
    
    /* Custom button styling */
    .stButton > button {
        background: rgba(42, 48, 80, 0.6);
        border: 1px solid rgba(80, 90, 140, 0.4);
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: rgba(65, 71, 112, 0.8);
        border-color: rgba(95, 112, 219, 0.6);
        transform: translateY(-2px);
    }
    
    /* === CHAT STYLING === */
    /* Modern chat message container */
    [data-testid="stChatMessage"] {
        background-color: rgba(35, 37, 47, 0.5);
        border-radius: 14px;
        margin: 1.1rem 0;
        padding: 1.4rem;
        border: 1px solid rgba(60, 65, 94, 0.2);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: fadeInUp 0.4s ease;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(140deg, rgba(42, 48, 74, 0.6) 0%, rgba(40, 45, 75, 0.4) 100%);
        border-color: rgba(84, 96, 148, 0.25);
    }
    
    /* AI message styling */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(140deg, rgba(41, 48, 66, 0.5) 0%, rgba(50, 65, 85, 0.35) 100%);
        border-color: rgba(80, 120, 170, 0.2);
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
    
    /* Fixed chat input */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 16.5%;
        right: 0;
        background: linear-gradient(180deg, rgba(14, 14, 22, 0) 0%, rgba(14, 14, 22, 0.9) 20%, rgba(14, 14, 22, 1) 100%);
        backdrop-filter: blur(16px);
        padding: 1.7rem 2.5rem;
        border-top: none;
        z-index: 99;
    }
    
    /* Chat input field */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(48, 52, 75, 0.4);
        border: 1px solid rgba(80, 90, 140, 0.3);
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 15px;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        color: rgba(255, 255, 255, 0.9);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        background-color: rgba(48, 52, 75, 0.6);
        border-color: rgba(95, 112, 219, 0.5);
        box-shadow: 0 0 0 3px rgba(95, 112, 219, 0.2);
    }
    
    /* Chat container spacing */
    .chat-container {
        margin-top: 20px;
        margin-bottom: 120px;
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
        border-radius: 20px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(106, 116, 143, 0.5);
        border-radius: 20px;
    }
    
    /* Brand logo */
    .brand-logo {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding: 14px;
        background: linear-gradient(135deg, rgba(42, 48, 80, 0.3) 0%, rgba(30, 34, 55, 0.3) 100%);
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(80, 90, 140, 0.15);
    }
    
    .logo-icon {
        width: 42px;
        height: 42px;
        margin-right: 14px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        background: linear-gradient(120deg, #5f70db, #8e54e9);
        box-shadow: 0 4px 10px rgba(95, 112, 219, 0.3);
    }
    
    .logo-text {
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(90deg, #d4e1ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    .logo-slogan {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 2px;
    }
    
    /* App watermark */
    .watermark {
        position: fixed;
        bottom: 85px;
        right: 20px;
        color: rgba(255, 255, 255, 0.4);
        font-size: 12px;
        z-index: 1000;
        pointer-events: none;
        background-color: rgba(20, 22, 30, 0.4);
        padding: 6px 12px;
        border-radius: 8px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Code blocks */
    pre {
        background: rgba(30, 30, 50, 0.4) !important;
        border: 1px solid rgba(95, 112, 219, 0.3) !important;
        border-radius: 10px !important;
        padding: 1em !important;
    }
    
    code {
        color: #a6b2ff !important;
        background: rgba(95, 112, 219, 0.1) !important;
        padding: 0.2em 0.4em !important;
        border-radius: 4px !important;
        font-size: 0.9em !important;
    }
</style>

<!-- Simple JavaScript for copy functionality -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Simple button function to copy assistant messages
    function addCopyButtons() {
        const messages = document.querySelectorAll('[data-testid="stChatMessage"][data-testid*="assistant"]');
        
        messages.forEach(message => {
            if (!message.querySelector('.copy-button')) {
                const btn = document.createElement('button');
                btn.className = 'copy-button';
                btn.innerHTML = 'Copy';
                btn.style.cssText = 'position: absolute; top: 8px; right: 8px; background: rgba(95, 112, 219, 0.2); border: none; color: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;';
                
                btn.addEventListener('click', function() {
                    const text = message.textContent.replace('Copy', '');
                    navigator.clipboard.writeText(text);
                    
                    // Show copied feedback
                    btn.textContent = 'Copied!';
                    setTimeout(() => { btn.innerHTML = 'Copy'; }, 2000);
                });
                
                message.appendChild(btn);
                message.style.paddingTop = '30px';
            }
        });
    }
    
    // Add copy buttons when DOM changes
    const observer = new MutationObserver(function() {
        addCopyButtons();
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Initial check
    addCopyButtons();
});
</script>

<div class="watermark">
    <span style="margin-left: 5px;">Created by Zakaria</span>
</div>
""", unsafe_allow_html=True)

# Define subject-specific contexts
subjects = {
    "math": {
        "title": "Mathematics",
        "icon": "📐",
        "description": "Algebra, Calculus, Geometry...",
        "class": "math-card",
        "context": """You are a specialized mathematics homework assistant. Help students understand mathematical concepts and solve problems by:

1. Breaking down problems into clear steps
2. Explaining mathematical concepts in simple language
3. Providing visual explanations where possible
4. Showing all work and calculations
5. Connecting concepts to real-world applications

Focus on helping students truly understand the material, not just get answers. For algebra, calculus, geometry, trigonometry, statistics, and other mathematical topics, show step-by-step solutions with clear explanations for each step."""
    },
    "science": {
        "title": "Science",
        "icon": "🔬",
        "description": "Physics, Chemistry, Biology...",
        "class": "science-card",
        "context": """You are a specialized science homework assistant. Help students understand scientific concepts and solve problems by:

1. Explaining scientific concepts clearly with examples
2. Breaking down complex problems into manageable steps
3. Showing all calculations with proper units
4. Connecting theoretical concepts to real-world applications
5. Using diagrams and visual explanations where helpful (described in text)

For physics, chemistry, biology, and other scientific disciplines, provide accurate information and step-by-step problem-solving approaches. Help students understand the underlying principles rather than just providing answers."""
    },
    "english": {
        "title": "English",
        "icon": "📝",
        "description": "Grammar, Essays, Literature...",
        "class": "language-card",
        "context": """You are a specialized English language and literature homework assistant. Help students with:

1. Grammar rules and proper usage
2. Essay structure, thesis development, and argumentation
3. Literary analysis and interpretation
4. Vocabulary development and word choice
5. Writing techniques and stylistic improvements

For writing assignments, help students craft strong thesis statements, develop coherent arguments, and improve their writing style. For literature questions, help them analyze themes, characters, symbolism, and literary techniques. Provide examples and clear explanations rather than completing assignments for them."""
    },
    "history": {
        "title": "History",
        "icon": "📜",
        "description": "World Events, Social Studies...",
        "class": "history-card",
        "context": """You are a specialized history and social studies homework assistant. Help students understand historical events and concepts by:

1. Providing accurate historical information with proper context
2. Explaining cause-and-effect relationships between events
3. Analyzing multiple perspectives on historical events
4. Connecting historical events to broader themes and patterns
5. Helping students develop critical thinking about historical sources

For history and social studies topics, provide comprehensive explanations that incorporate relevant dates, figures, and details. Help students understand not just what happened but why it happened and its significance."""
    }
}

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_subject" not in st.session_state:
    st.session_state.active_subject = None
if "context" not in st.session_state:
    st.session_state.context = "You are a helpful homework assistant."
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemini-1.5-flash"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# Configure Gemini API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"  # Fallback for testing
genai.configure(api_key=api_key)

# Function to set active subject
def set_subject(subject_key):
    if subject_key not in subjects:
        return
    
    # Start a new conversation with that subject
    st.session_state.messages = []
    st.session_state.active_subject = subject_key
    
    # Set the subject-specific context
    st.session_state.context = subjects[subject_key]["context"]
    
    # Add welcome message
    welcome_msg = f"👋 Welcome to the {subjects[subject_key]['title']} assistant! How can I help you today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Force rerun
    st.rerun()

# Sidebar with clean styling
with st.sidebar:
    # Logo and Brand
    st.markdown("""
    <div class="brand-logo">
        <div class="logo-icon">📚</div>
        <div>
            <div class="logo-text">Homework Pro</div>
            <div class="logo-slogan">Your study companion</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Subject selection header
    st.markdown("### Choose a Subject")
    
    # Subject cards with integrated buttons
    col1, col2 = st.columns(2)
    
    # Mathematics button
    with col1:
        st.markdown(f"""
        <div class="subject-card math-card">
            <div class="icon">{subjects['math']['icon']}</div>
            <div class="content">
                <div class="title">{subjects['math']['title']}</div>
                <div class="description">{subjects['math']['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("Select Mathematics"):
            set_subject("math")
    
    # Science button
    with col1:
        st.markdown(f"""
        <div class="subject-card science-card">
            <div class="icon">{subjects['science']['icon']}</div>
            <div class="content">
                <div class="title">{subjects['science']['title']}</div>
                <div class="description">{subjects['science']['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("Select Science"):
            set_subject("science")
    
    # English button
    with col1:
        st.markdown(f"""
        <div class="subject-card language-card">
            <div class="icon">{subjects['english']['icon']}</div>
            <div class="content">
                <div class="title">{subjects['english']['title']}</div>
                <div class="description">{subjects['english']['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("Select English"):
            set_subject("english")
    
    # History button
    with col1:
        st.markdown(f"""
        <div class="subject-card history-card">
            <div class="icon">{subjects['history']['icon']}</div>
            <div class="content">
                <div class="title">{subjects['history']['title']}</div>
                <div class="description">{subjects['history']['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("Select History"):
            set_subject("history")
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # AI Settings
    with st.expander("🤖 AI Settings", expanded=False):
        model_options = {
            "Gemini 1.5 Flash": "gemini-1.5-flash",
            "Gemini 1.5 Pro": "gemini-1.5-pro"
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

    # New conversation button
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_subject = None
        st.session_state.context = "You are a helpful homework assistant."
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "👋 I'm your homework assistant. Choose a subject or ask me any question!"
        })
        st.rerun()

# Main chat interface
main_container = st.container()

# Initialize with welcome message if needed
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "👋 I'm your homework assistant. Choose a subject or ask me any question!"
    })

# Display chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

with main_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Display thinking animation if needed
    if st.session_state.thinking:
        with st.chat_message("assistant"):
            st.markdown("Thinking...")

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Ask any homework question...")
if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Set thinking state to true
    st.session_state.thinking = True
    
    # Show user message immediately
    st.rerun()

# Handle AI response generation
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and st.session_state.thinking:
    user_input = st.session_state.messages[-1]["content"]
    
    # Detect subject if none is active
    if not st.session_state.active_subject:
        # Simple keyword matching for subject detection
        subject_keywords = {
            "math": ["math", "algebra", "calculus", "equation", "geometry", "number", "formula"],
            "science": ["science", "physics", "chemistry", "biology", "molecule", "cell", "force", "atom"],
            "english": ["english", "grammar", "essay", "write", "literature", "novel", "poem", "language"],
            "history": ["history", "war", "revolution", "century", "ancient", "medieval", "civilization", "country"]
        }
        
        detected_subject = None
        max_matches = 0
        
        for subject, keywords in subject_keywords.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in user_input.lower())
            if matches > max_matches:
                max_matches = matches
                detected_subject = subject
        
        # Use detected subject if we found a good match
        if max_matches > 0:
            st.session_state.active_subject = detected_subject
            st.session_state.context = subjects[detected_subject]["context"]
    
    try:
        # Configure the model
        model = genai.GenerativeModel(
            st.session_state.model_name,
            generation_config={"temperature": st.session_state.temperature}
        )
        
        # Prepare prompt with context
        complete_prompt = f"{st.session_state.context}\n\nStudent question: {user_input}"
        
        # Turn off thinking state
        st.session_state.thinking = False
        
        # Generate AI response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for response in model.generate_content(complete_prompt, stream=True):
                if hasattr(response, 'text'):
                    chunk = response.text
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
            
            # Final display without cursor
            message_placeholder.markdown(full_response)
                    
            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        # Handle errors
        st.error(f"Error: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": f"I'm sorry, an error occurred: {str(e)}"})
        st.session_state.thinking = False
    
    # Rerun to update UI
    st.rerun()
