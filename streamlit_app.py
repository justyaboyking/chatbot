import streamlit as st
import google.generativeai as genai
import time

# Set page config
st.set_page_config(
    page_title="Home Work Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with background animations and cleaner design
st.markdown("""
<style>
    /* Animated background */
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
    
    /* Main background with animation */
    .main {
        background: linear-gradient(-45deg, #000000, #0a0a0a, #121212, #181818);
        background-size: 400% 400%;
        animation: gradientAnimation 15s ease infinite;
    }
    
    /* Star field animation */
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .star {
        position: absolute;
        width: 2px;
        height: 2px;
        background-color: white;
        border-radius: 50%;
        opacity: 0.3;
        animation: pulse 3s infinite;
    }
    
    /* Generate 50 random stars */
    ${Array.from({length: 50}, (_, i) => {
        const top = Math.random() * 100;
        const left = Math.random() * 100;
        const animationDelay = Math.random() * 5;
        const size = Math.random() * 2 + 1;
        
        return `.star:nth-child(${i+1}) {
            top: ${top}%;
            left: ${left}%;
            width: ${size}px;
            height: ${size}px;
            animation-delay: ${animationDelay}s;
        }`;
    }).join('\n')}
    
    /* Cleaner text elements with black backgrounds */
    body {
        color: white;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Sidebar styling - cleaner and more minimal */
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #222;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #333;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Clean, minimal text containers with black backgrounds */
    .stTextInput, .stTextArea > div > div, p, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .element-container, [data-testid="stChatMessageContent"] {
        background-color: #000000 !important;
        color: white !important;
    }
    
    /* Modern, minimal chat messages */
    [data-testid="stChatMessage"] {
        background-color: #0a0a0a;
        border: none;
        border-radius: 12px;
        margin: 16px 0;
        padding: 16px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Different styling for assistant vs user messages */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        border-left: 3px solid #e63946;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        border-left: 3px solid #4ecdc4;
        background-color: #0e0e0e;
    }
    
    /* Clean, minimal buttons */
    .stButton > button {
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(230, 57, 70, 0.3);
    }
    
    .stButton > button:hover {
        background-color: #c1121f;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(230, 57, 70, 0.4);
    }
    
    /* Clean input fields */
    input, textarea {
        background-color: #0a0a0a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    /* Position chat input at the very bottom of the page */
    .stChatInput {
        position: fixed;
        bottom: 5px;
        left: 400px; /* Account for sidebar width */
        right: 20px;
        z-index: 1000;
        margin-bottom: 0;
    }
    
    /* Add much more padding at the bottom of chat container */
    [data-testid="stChatMessageContainer"] {
        padding-bottom: 120px !important;
    }
    
    /* Give chat messages more room */
    .main .block-container {
        padding-bottom: 150px;
    }
    
    /* Footer adjustment to make room for chat input */
    .footer {
        display: none; /* Hide footer to avoid overlap */
    }
    
    /* Clean preset cards with subtle animation */
    .preset-card {
        background-color: #0a0a0a;
        color: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border-left: 4px solid #e63946;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        animation: slideInRight 0.5s ease-out;
        cursor: pointer;
    }
    
    .preset-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        border-left-color: #4ecdc4;
    }
    
    /* Clean success messages */
    .stSuccess {
        background-color: rgba(15, 61, 39, 0.8) !important;
        color: white !important;
        border-radius: 8px !important;
        backdrop-filter: blur(5px);
    }
    
    /* Clean error messages */
    .stError {
        background-color: rgba(61, 15, 15, 0.8) !important;
        color: white !important;
        border-radius: 8px !important;
        backdrop-filter: blur(5px);
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
    
    /* Cleaner warning box */
    .warning-box {
        background-color: rgba(10, 10, 10, 0.7);
        border-left: 3px solid #e63946;
        padding: 12px;
        border-radius: 8px;
        margin: 16px 0;
        font-size: 14px;
        color: white;
        animation: fadeIn 1s ease-out;
        backdrop-filter: blur(5px);
    }
    
    /* App title */
    .app-title {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }
    
    .app-icon {
        font-size: 2.5rem;
        color: #e63946;
        margin-right: 1rem;
    }
    
    .app-name {
        margin: 0;
        padding: 0;
        font-size: 2.2rem;
        font-weight: 600;
        background: linear-gradient(45deg, #e63946, #4ecdc4);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }
    
    /* Welcome screen */
    .welcome-screen {
        text-align: center;
        padding: 30px;
        color: #e0e0e0;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 16px;
        margin: 2rem 0;
        animation: fadeIn 1.5s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid #222;
    }
    
    /* Settings panel */
    .settings-panel {
        background-color: #0a0a0a;
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        border-left: 4px solid #4ecdc4;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Cleaner scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #444;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #e63946 transparent transparent transparent !important;
    }
</style>

<!-- Background stars effect -->
<div class="stars">
    ${Array.from({length: 50}, () => '<div class="star"></div>').join('')}
</div>

<!-- Watermark -->
<div class="watermark">
    home work bot - made by zakaria
</div>
""", unsafe_allow_html=True)

# App title with custom styling
st.markdown("""
<div class="app-title">
    <div class="app-icon">📚</div>
    <h1 class="app-name">Home Work Bot</h1>
</div>
""", unsafe_allow_html=True)

# Hardcoded API key
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

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Sidebar with settings
with st.sidebar:
    # Settings section
    st.header("Settings")
    
    # Add expandable settings panel
    with st.expander("AI Settings", expanded=False):
        # Model selection
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
        
        # Update model in session state
        st.session_state.model_name = model_options[selected_model]
        
        # Temperature slider
        st.subheader("Response Style")
        temperature = st.slider(
            "Temperature (lower = more focused, higher = more creative):",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1
        )
        st.session_state.temperature = temperature
        
        # Clear chat button in settings
        st.subheader("Chat Management")
        if st.button("Clear Chat History"):
            with st.spinner("Clearing chat..."):
                time.sleep(0.3)
                st.session_state.messages = []
                st.rerun()
    
    # Custom context section
    st.header("Context Management")
    if st.button("Show/Hide Context Editor"):
        if "show_custom_context" not in st.session_state:
            st.session_state.show_custom_context = True
        else:
            st.session_state.show_custom_context = not st.session_state.show_custom_context
        st.rerun()
    
    # Show custom context section if toggled
    if "show_custom_context" in st.session_state and st.session_state.show_custom_context:
        custom_context = st.text_area(
            "Edit context:",
            value=st.session_state.context,
            height=300,
            key="custom_context"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", key="save_context"):
                with st.spinner("Saving..."):
                    time.sleep(0.3)
                    st.session_state.context = custom_context
                    st.success("Saved!")
        
        with col2:
            if st.button("Clear", key="clear_context"):
                with st.spinner("Clearing..."):
                    time.sleep(0.3)
                    st.session_state["custom_context"] = ""
                    st.session_state.context = ""
                    st.rerun()
        
        # Save as preset option
        new_preset_name = st.text_input("Save as preset (name):")
        if st.button("Create Preset") and new_preset_name:
            with st.spinner("Creating preset..."):
                time.sleep(0.3)
                st.session_state.user_presets[new_preset_name] = custom_context
                st.success(f"Preset '{new_preset_name}' created!")
    
    # Privacy notice
    st.markdown("""
    <div class="warning-box">
        <strong>Privacy:</strong> Conversations are not stored and will be deleted when you leave the page.
    </div>
    """, unsafe_allow_html=True)

# Define presets
presets = {
    "duits deelstaten": {
        "content": """PowerPoint Präsentation / PowerPoint Presentatie
Deutsch:
Aufgabe: Mache eine PowerPoint-Präsentation über ein Thema, das du wählst. Der Prozess hat drei Teile: Schriftliche Vorbereitung, die PowerPoint machen, und die Präsentation vor der Klasse.
Schritt 1: Schriftliche Vorbereitung
Suche Informationen über dein Thema und schreibe die wichtigsten Sachen auf. Deine Vorbereitung soll diese Dinge haben:

Allgemeine Informationen:
Name:
Hauptstadt:
Fläche:
Einwohnerzahl:
Lage auf der Karte: [Füge eine Karte ein]
Geschichte:
Kurze Geschichte von dem Thema:
Sehenswürdigkeiten:
Wichtige Orte, Denkmäler oder Landschaften:
Kultur und Traditionen:
Regionale Feste, Bräuche, typische Essen:
Wirtschaft:
Wichtige Industrien und was man verdient:
Sonstiges:
Interessante Fakten oder besondere Sachen:
Schreibe deine Notizen in einer guten Reihenfolge, damit deine PowerPoint eine gute Struktur hat.
Schritt 2: Die PowerPoint-Präsentation machen
Mache jetzt eine PowerPoint-Präsentation mit mindestens 6 Folien. Achte auf diese Punkte:

Klare und einfache Struktur
Nicht zu viel Text auf einer Folie - Stichpunkte sind besser
Benutze Bilder, Karten oder Diagramme
Einheitliches Aussehen (Farben, Schriftarten)
Schritt 3: Präsentation vor der Klasse
Präsentiere deine Präsentation vor der Klasse. Achte auf diese Dinge:

Verständliche und deutliche Aussprache
Schaue die Leute an
Sprich nicht zu schnell
Benutze deine PowerPoint als Hilfe (nicht nur ablesen!)
Bewertungskriterien:

Qualität der Informationen: /20
Struktur und Aussehen der PowerPoint: /10
Wie du präsentierst und wie gut man dich versteht: /10
Viel Erfolg!
Nederlands:
Taak: Maak een PowerPoint-presentatie over een onderwerp naar keuze. Het proces omvat: schriftelijke voorbereiding, het maken van de PowerPoint-presentatie en de presentatie voor de klas.
Stap 1: Schriftelijke Voorbereiding
Verzamel informatie over je gekozen onderwerp en noteer de belangrijkste punten. Je voorbereiding moet de volgende aspecten bevatten:

Algemene informatie:
Naam:
Hoofdstad:
Oppervlakte:
Bevolking:
Ligging op de kaart: [Voeg een kaart toe]
Geschiedenis:
Korte geschiedenis van het onderwerp:
Bezienswaardigheden:
Belangrijke plaatsen, monumenten of landschappen:
Cultuur en Tradities:
Regionale festivals, gebruiken, typische gerechten:
Economie:
Belangrijke industrieën en wat men verdient:
Overige:
Interessante feiten of bijzondere dingen:
Orden je notities in een logische volgorde om een goede structuur voor je PowerPoint-presentatie te creëren.
Stap 2: De PowerPoint-presentatie maken
Maak nu een PowerPoint-presentatie met minstens 6 dia's. Let op de volgende punten:

Duidelijke en eenvoudige structuur
Niet te veel tekst op één dia - opsommingstekens zijn beter
Gebruik afbeeldingen, kaarten of diagrammen
Consistent ontwerp (kleuren, lettertypen)
Stap 3: Presentatie voor de klas
Geef je presentatie voor de klas. Let daarbij op het volgende:

Verstaanbare en duidelijke uitspraak
Kijk de mensen aan
Spreek niet te snel
Gebruik je PowerPoint als hulp (niet alleen voorlezen!)
Beoordelingscriteria:

Kwaliteit van de informatie: /20
Structuur en uiterlijk van de PowerPoint: /10
Hoe je presenteert en hoe goed men je begrijpt: /10
Veel succes!""",
        "description": ""
    }
}

# Main chat interface with preset-focused design
chat_container = st.container()

# Display preset options if no messages, or regular chat UI if conversation in progress
with chat_container:
    if not st.session_state.messages:
        # Welcome screen with preset selection options
        st.markdown("""
        <div class="welcome-screen">
            <h3>Kies een preset om te beginnen</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Main preset grid - replaces the chat input initially
        preset_cols = st.columns(3)
        
        # Display all available presets in a grid
        col_idx = 0
        for preset_name, preset_data in presets.items():
            with preset_cols[col_idx]:
                # Clickable preset card
                st.markdown(f"""
                <div class="preset-card" id="{preset_name.replace(' ', '_')}_card" onclick="document.getElementById('{preset_name.replace(' ', '_')}_btn').click();">
                    <strong>{preset_name}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden button that gets triggered by the card click
                if st.button("Select", key=f"{preset_name.replace(' ', '_')}_btn"):
                    with st.spinner("Loading..."):
                        time.sleep(0.5)
                        # Set the context
                        st.session_state.context = preset_data["content"]
                        
                        # Add first AI message asking for the state/region
                        st.session_state.messages.append({"role": "assistant", "content": "Wat is je deelstaat?"})
                        
                        st.rerun()
            
            # Update column index for next preset
            col_idx = (col_idx + 1) % 3
        
        # Show user presets if any
        if st.session_state.user_presets:
            st.subheader("Je eigen presets:")
            
            # Create new row of columns for user presets
            user_preset_cols = st.columns(3)
            
            # Display user presets
            col_idx = 0
            for preset_name, preset_content in st.session_state.user_presets.items():
                with user_preset_cols[col_idx]:
                    # Clickable user preset card
                    st.markdown(f"""
                    <div class="preset-card" id="user_{preset_name.replace(' ', '_')}_card" onclick="document.getElementById('user_{preset_name.replace(' ', '_')}_btn').click();">
                        <strong>{preset_name}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hidden button for the card
                    if st.button("Select", key=f"user_{preset_name.replace(' ', '_')}_btn"):
                        with st.spinner("Loading..."):
                            time.sleep(0.5)
                            # Set the context
                            st.session_state.context = preset_content
                            
                            # Start the conversation
                            st.session_state.messages.append({"role": "assistant", "content": "Wat is je vraag?"})
                            
                            st.rerun()
                
                # Update column index for next preset
                col_idx = (col_idx + 1) % 3
    else:
        # Regular chat interface when conversation has started
        # Display chat messages with styling
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Add spacer to ensure content doesn't get hidden behind fixed chat input
        st.markdown("<div style='height: 150px'></div>", unsafe_allow_html=True)
            
        # Chat input only appears after selecting a preset
        if prompt := st.chat_input("Typ je vraag..."):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                # Initialize the model with selected settings
                model = genai.GenerativeModel(
                    st.session_state.model_name,
                    generation_config={"temperature": st.session_state.temperature}
                )
                
                # Create the complete prompt including context
                complete_prompt = prompt
                if st.session_state.context:
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Op basis van bovenstaande context, beantwoord deze vraag direct en bondig zonder extra disclaimers of uitleg:
                    {prompt}
                    
                    Geef alleen het antwoord zonder inleidingen, disclaimers of conclusies. Houd het kort en to-the-point.
                    """
                
                # Generate content with streaming
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    # Generate content
                    response = model.generate_content(
                        complete_prompt,
                        stream=True
                    )
                    
                    # Stream the response
                    for chunk in response:
                        if hasattr(chunk, 'text'):
                            full_response += chunk.text
                            message_placeholder.markdown(full_response)
                            
                    # Store the response
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
            except Exception as e:
                error_msg = str(e)
                st.error(f"Fout: {error_msg}")
                st.info("Probeer een ander AI model in de instellingen.")
