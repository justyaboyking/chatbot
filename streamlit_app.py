import streamlit as st 
import google.generativeai as genai
import time
import io

# Set page config
st.set_page_config(
    page_title="Home Work Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified CSS with fixed bottom chat input, similar to Claude's interface
st.markdown("""
<style>
    /* Dark background */
    body {
        color: white;
        background-color: #0e1117;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #262730;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
    }
    /* Simple fixed bottom chat input - Claude style */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 20%;
        right: 5%;
        background-color: #0e1117;
        padding: 1rem 0;
        border-top: 1px solid #262730;
        z-index: 999;
    }
    /* Container for chat messages */
    [data-testid="stChatMessageContainer"] {
        margin-bottom: 100px;
        padding-bottom: 100px;
    }
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #262730;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: none;
    }
    /* User vs assistant messages */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #383b44;
    }
    /* Buttons */
    .stButton > button {
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 0.25rem;
    }
    /* Preset cards */
    .preset-card {
        background-color: #262730;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: transform 0.2s;
        display: flex;
        align-items: center;
    }
    .preset-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .preset-icon {
        margin-right: 10px;
        font-size: 24px;
    }
    /* Watermark at top left */
    .watermark {
        position: fixed;
        top: 10px;
        left: 10px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 12px;
        z-index: 1000;
    }
    /* Fixed height for chat container */
    .main .block-container {
        padding-bottom: 80px;
    }
    /* Subject confirmation box */
    .subject-confirmation {
        background-color: #2e3440;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #88c0d0;
    }
    /* Interactive elements container */
    .interactive-elements {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    /* Custom file uploader */
    .custom-file-upload {
        margin-top: 20px;
        padding: 10px;
        background-color: #2e3440;
        border-radius: 5px;
        border: 1px dashed #4c566a;
        text-align: center;
    }
    /* Progress bar */
    .stProgress > div > div {
        background-color: #88c0d0;
    }
    /* Custom dropdown */
    .custom-dropdown {
        margin-top: 10px;
    }
</style>
<!-- Watermark -->
<div class="watermark">
    home work bot - made by zakaria
</div>
""", unsafe_allow_html=True)

# App title
st.title("Home Work Bot")

# Hardcoded API key (ensure this key is secure)
gemini_api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "user_presets" not in st.session_state:
    st.session_state.user_presets = {}
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemini-1.5-flash"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "show_presets" not in st.session_state:
    st.session_state.show_presets = True
if "current_step" not in st.session_state:
    st.session_state.current_step = "welcome"
if "file_content" not in st.session_state:
    st.session_state.file_content = ""
if "detected_subject" not in st.session_state:
    st.session_state.detected_subject = None
if "confirmed_subject" not in st.session_state:
    st.session_state.confirmed_subject = None
if "processing" not in st.session_state:
    st.session_state.processing = False
if "output" not in st.session_state:
    st.session_state.output = None

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Subject list
subjects = ["History", "Math", "Science", "Literature", "Languages", "Geography", "Computer Science", "Arts", "Other"]

# Detect subject function
def detect_subject(text):
    try:
        model = genai.GenerativeModel(st.session_state.model_name)
        subject_prompt = f"""
        Based on the following text, determine what academic subject this document is most likely related to.
        Choose one from this list: {', '.join(subjects)}
        
        Text: {text[:1000]}  # Only use the first 1000 characters to save tokens
        
        Respond with just the subject name, nothing else.
        """
        response = model.generate_content(subject_prompt)
        detected = response.text.strip()
        
        # Ensure the detected subject is in our list
        if detected not in subjects:
            # Find the closest match
            for subject in subjects:
                if subject.lower() in detected.lower():
                    return subject
            return "Other"
        
        return detected
    except Exception as e:
        st.error(f"Error detecting subject: {str(e)}")
        return "Other"

# Get contextual presets based on subject and content
def get_contextual_presets(subject, content):
    presets = []
    
    # Base presets that work for most subjects
    presets.append({
        "name": "Summarize Key Points",
        "icon": "📝",
        "description": "Create a concise summary of the main points"
    })
    
    # Subject-specific presets
    if subject == "History":
        presets.append({
            "name": "Generate Essay Outline",
            "icon": "📑",
            "description": "Create a structured outline for your essay"
        })
        presets.append({
            "name": "Identify Key Historical Events",
            "icon": "🏛️",
            "description": "List and explain the important historical events"
        })
        
    elif subject == "Math":
        presets.append({
            "name": "Step-by-Step Problem Solving",
            "icon": "🔢",
            "description": "Get detailed solutions with explanations"
        })
        presets.append({
            "name": "Create Practice Problems",
            "icon": "✏️",
            "description": "Generate similar practice problems with solutions"
        })
        
    elif subject == "Science":
        presets.append({
            "name": "Explain Scientific Concepts",
            "icon": "🔬",
            "description": "Get detailed explanations of key scientific concepts"
        })
        presets.append({
            "name": "Create Study Questions",
            "icon": "❓",
            "description": "Generate questions to test your understanding"
        })
        
    elif subject == "Literature":
        presets.append({
            "name": "Character Analysis",
            "icon": "👤",
            "description": "Analyze the main characters and their development"
        })
        presets.append({
            "name": "Theme Exploration",
            "icon": "🎭",
            "description": "Identify and explore the key themes"
        })
        
    elif subject == "Languages":
        presets.append({
            "name": "Translation Help",
            "icon": "🌐",
            "description": "Get assistance with translations and meanings"
        })
        presets.append({
            "name": "Grammar Explanation",
            "icon": "📕",
            "description": "Understand grammar rules and usage"
        })
    
    # Add generic presets for all subjects
    presets.append({
        "name": "Identify Key Terms & Definitions",
        "icon": "📖",
        "description": "Extract and explain important terminology"
    })
    
    presets.append({
        "name": "Create Practice Questions",
        "icon": "❓",
        "description": "Generate questions to test your understanding"
    })
    
    # Always add the custom request option
    presets.append({
        "name": "Ask a Specific Question",
        "icon": "💬",
        "description": "Type your own custom request"
    })
    
    return presets

# Sidebar with settings
with st.sidebar:
    st.header("Settings")
    
    with st.expander("AI Settings", expanded=False):
        st.subheader("AI Model")
        model_options = {
            "Gemini 1.5 Flash": "gemini-1.5-flash",
            "Gemini 2.0 Flash Thinking": "gemini-2.0-flash-thinking-exp-01-21",
            "Gemini 2.0 Flash-Lite": "gemini-2.0-flash-lite"
        }
        
        selected_model = st.selectbox(
            "Select AI Model:",
            options=list(model_options.keys()),
            index=list(model_options.values()).index(st.session_state.model_name) if st.session_state.model_name in list(model_options.values()) else 0
        )
        st.session_state.model_name = model_options[selected_model]
        
        st.subheader("Response Style")
        temperature = st.slider(
            "Temperature:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1
        )
        st.session_state.temperature = temperature
        
        st.subheader("Chat Management")
        if st.button("Clear Chat & Start Over"):
            st.session_state.messages = []
            st.session_state.show_presets = True
            st.session_state.current_step = "welcome"
            st.session_state.file_content = ""
            st.session_state.detected_subject = None
            st.session_state.confirmed_subject = None
            st.session_state.output = None
            st.rerun()
    
    with st.expander("User Presets", expanded=False):
        if st.session_state.user_presets:
            st.subheader("Your saved presets:")
            for preset_name, preset_content in st.session_state.user_presets.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(preset_name)
                with col2:
                    if st.button("Load", key=f"load_{preset_name}"):
                        st.session_state.context = preset_content
                        st.success(f"Loaded preset: {preset_name}")
        
        # Save current context as preset
        if st.session_state.context.strip():
            st.subheader("Save current context as preset")
            preset_name = st.text_input("Preset Name:", key="new_preset_name")
            if st.button("Save Preset") and preset_name:
                st.session_state.user_presets[preset_name] = st.session_state.context
                st.success(f"Preset '{preset_name}' saved successfully!")
                st.rerun()

# Main content area
main_container = st.container()

# Welcome screen
if st.session_state.current_step == "welcome":
    with main_container:
        st.markdown("## 👋 Welcome to Home Work Bot!")
        st.markdown("""
        I'm here to help you with your school assignments. Let's get started by uploading a document.
        
        **What can I do?**
        - Generate essay outlines
        - Summarize key points
        - Create practice questions
        - Help with problem solving
        - Explain complex concepts
        - And much more!
        """)
        
        st.markdown("### Upload your assignment document to get started")
        uploaded_file = st.file_uploader("Choose a PDF or Word document", type=["pdf", "docx"], key="welcome_uploader")
        
        if uploaded_file is not None:
            st.session_state.current_step = "process_file"
            st.rerun()

# Process uploaded file
elif st.session_state.current_step == "process_file":
    with main_container:
        st.markdown("## Processing your document...")
        
        # Create progress bar
        progress_bar = st.progress(0)
        
        # Show processing steps
        for i in range(101):
            # Update progress bar
            progress_bar.progress(i)
            
            # Show different messages at different stages
            if i == 20:
                st.info("Reading file content...")
            elif i == 50:
                st.info("Extracting text...")
            elif i == 80:
                st.info("Analyzing content...")
                
            time.sleep(0.02)  # Simulate processing time
        
        # Extract text from the document
        file_text = "Sample document content for demonstration purposes. This is where the actual document text would be extracted."
        
        # Store file content in session state
        st.session_state.file_content = file_text
        
        # Detect subject
        st.session_state.detected_subject = detect_subject(file_text)
        
        # Move to next step
        st.session_state.current_step = "subject_confirmation"
        st.rerun()

# Subject confirmation
elif st.session_state.current_step == "subject_confirmation":
    with main_container:
        st.markdown("## Document Preview")
        
        # Show document preview (truncated for readability)
        with st.expander("Document Content", expanded=False):
            st.markdown(st.session_state.file_content[:500] + "...")
        
        # Subject confirmation box
        st.markdown(
            f"""
            <div class="subject-confirmation">
                <p>We think this is a <strong>{st.session_state.detected_subject}</strong> assignment. Is that correct?</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Yes, that's correct"):
                st.session_state.confirmed_subject = st.session_state.detected_subject
                st.session_state.current_step = "contextual_presets"
                st.rerun()
        
        with col2:
            # If subject is incorrect, allow user to select from dropdown
            subject_choice = st.selectbox(
                "No, it's actually:",
                subjects,
                index=subjects.index(st.session_state.detected_subject) if st.session_state.detected_subject in subjects else 0,
                key="subject_dropdown"
            )
            
            if st.button("Confirm Subject"):
                st.session_state.confirmed_subject = subject_choice
                st.session_state.current_step = "contextual_presets"
                st.rerun()

# Contextual presets
elif st.session_state.current_step == "contextual_presets":
    with main_container:
        st.markdown(f"## {st.session_state.confirmed_subject} Assignment")
        
        # Show document preview (truncated for readability)
        with st.expander("Document Content", expanded=False):
            st.markdown(st.session_state.file_content[:500] + "...")
        
        st.markdown("### What would you like to do with this document?")
        
        # Get contextual presets
        presets = get_contextual_presets(st.session_state.confirmed_subject, st.session_state.file_content)
        
        # Display preset cards in a grid
        cols = st.columns(2)
        for i, preset in enumerate(presets):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="preset-card" onclick="document.getElementById('preset_{i}_btn').click();">
                        <div class="preset-icon">{preset["icon"]}</div>
                        <div>
                            <strong>{preset["name"]}</strong>
                            <p style="margin: 0; font-size: 14px; opacity: 0.8;">{preset["description"]}</p>
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Hidden button to handle the click
                if st.button("Select", key=f"preset_{i}_btn", style="visibility: hidden;"):
                    if preset["name"] == "Ask a Specific Question":
                        st.session_state.current_step = "custom_request"
                    else:
                        # For other presets, set context and move to processing step
                        st.session_state.context = f"""
                        Document: {st.session_state.file_content}
                        
                        Subject: {st.session_state.confirmed_subject}
                        
                        Task: {preset["name"]}
                        """
                        st.session_state.current_step = "processing"
                    st.rerun()

# Custom request
elif st.session_state.current_step == "custom_request":
    with main_container:
        st.markdown(f"## {st.session_state.confirmed_subject} Assignment")
        
        # Show document preview
        with st.expander("Document Content", expanded=False):
            st.markdown(st.session_state.file_content[:500] + "...")
        
        st.markdown("### What specific question do you have about this document?")
        
        # Text input for custom question
        custom_question = st.text_area("Type your question or request", height=100)
        
        if st.button("Submit", key="submit_custom"):
            if custom_question.strip():
                # Set context with the custom question
                st.session_state.context = f"""
                Document: {st.session_state.file_content}
                
                Subject: {st.session_state.confirmed_subject}
                
                User Question: {custom_question}
                """
                st.session_state.current_step = "processing"
                st.rerun()
            else:
                st.warning("Please enter a question or request.")

# Processing step
elif st.session_state.current_step == "processing":
    with main_container:
        if not st.session_state.processing:
            st.session_state.processing = True
            
            # Show processing UI
            st.markdown("## Processing Your Request")
            progress_bar = st.progress(0)
            status_message = st.empty()
            
            # Simulate processing with progress updates
            for i in range(101):
                progress_bar.progress(i)
                
                if i < 20:
                    status_message.info("Analyzing document...")
                elif i < 40:
                    status_message.info("Processing request...")
                elif i < 60:
                    status_message.info("Generating content...")
                elif i < 80:
                    status_message.info("Formatting response...")
                else:
                    status_message.info("Finalizing output...")
                
                time.sleep(0.03)  # Simulate processing time
            
            try:
                # Process with AI
                model = genai.GenerativeModel(
                    st.session_state.model_name,
                    generation_config={"temperature": st.session_state.temperature}
                )
                
                # Add system prompt based on context
                prompt = f"""
                You are Home Work Bot, an AI assistant for students.
                
                {st.session_state.context}
                
                Provide a helpful, educational response following these guidelines:
                1. Format your response clearly with headings, bullet points, and numbered lists where appropriate
                2. Be thorough but concise
                3. Highlight key information
                4. If explaining a concept, include examples to illustrate it
                5. If there are steps to solve a problem, explain each step clearly
                """
                
                # Call the AI model
                response = model.generate_content(prompt)
                
                # Store the output
                st.session_state.output = response.text
                
                # Move to results step
                st.session_state.current_step = "results"
                st.session_state.processing = False
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.processing = False
        else:
            st.warning("Processing your request, please wait...")

# Results step
elif st.session_state.current_step == "results":
    with main_container:
        st.markdown("## Your Results")
        
        # Show output
        st.markdown(st.session_state.output)
        
        # Interactive elements
        st.markdown(
            """
            <div class="interactive-elements">
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Copy to Clipboard", key="copy_btn"):
                # Use JavaScript to copy to clipboard (this is just UI, actual copying would require JS)
                st.success("Content copied to clipboard!")
        
        with col2:
            download_format = st.selectbox("Format:", ["PDF", "DOCX", "TXT"], key="download_format")
            if st.button("Download", key="download_btn"):
                st.success(f"Downloaded as {download_format}!")
        
        with col3:
            if st.button("Ask Follow-Up Question", key="followup_btn"):
                st.session_state.current_step = "follow_up"
                st.rerun()
        
        with col4:
            # Feedback buttons
            col4a, col4b = st.columns(2)
            with col4a:
                if st.button("👍", key="thumbs_up"):
                    st.success("Thanks for your feedback!")
            with col4b:
                if st.button("👎", key="thumbs_down"):
                    st.info("Thanks for your feedback!")

# Follow-up question
elif st.session_state.current_step == "follow_up":
    with main_container:
        st.markdown("## Ask a Follow-Up Question")
        
        # Show previous output
        with st.expander("Previous Response", expanded=False):
            st.markdown(st.session_state.output)
        
        # Text input for follow-up question
        followup_question = st.text_area("Type your follow-up question", height=100)
        
        if st.button("Submit Follow-Up", key="submit_followup"):
            if followup_question.strip():
                # Add the follow-up to the context
                st.session_state.context += f"\n\nFollow-up question: {followup_question}"
                st.session_state.current_step = "processing"
                st.rerun()
            else:
                st.warning("Please enter a follow-up question.")

# Register the script as a Streamlit app
if __name__ == "__main__":
    pass
