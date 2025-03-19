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
    
    /* Modern chat input */
    [data-testid="stChatInput"] {
        background-color: #0a0a0a;
        border: 1px solid #333;
        border-radius: 30px !important;
        color: white;
        padding: 12px 18px !important;
        margin-top: 1rem;
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
    
    /* Clean footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(5px);
        color: white;
        text-align: center;
        padding: 12px;
        font-size: 14px;
        border-top: 1px solid #222;
        letter-spacing: 0.5px;
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
        padding: 50px;
        color: #e0e0e0;
        background-color: rgba(0, 0, 0, 0.5);
        border-radius: 16px;
        margin: 2rem 0;
        animation: fadeIn 1.5s ease-out;
        backdrop-filter: blur(10px);
        border: 1px solid #222;
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
""", unsafe_allow_html=True)

# App title with custom styling
st.markdown("""
<div class="app-title">
    <div class="app-icon">📚</div>
    <h1 class="app-name">Home Work Bot</h1>
</div>
""", unsafe_allow_html=True)

# Hardcoded API key and model
gemini_api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"
model_name = "gemini-1.5-flash"

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "user_presets" not in st.session_state:
    st.session_state.user_presets = {}

# Sidebar with clean design
with st.sidebar:
    st.header("Presets")
    
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
            "description": "PowerPoint-presentatie instructies in Duits en Nederlands"
        }
    }
    
    # Clean preset selection with animated cards
    st.subheader("Kies een preset:")
    for preset_name, preset_data in presets.items():
        # Display a clean card with animation
        st.markdown(f"""
        <div class="preset-card">
            <strong>{preset_name}</strong><br>
            <small>{preset_data["description"]}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Clean button for selection
        if st.button(f"Selecteer {preset_name}", key=f"{preset_name.replace(' ', '_')}_btn"):
            with st.spinner('Preset laden...'):
                time.sleep(0.3)  # Slight delay for feedback
                st.session_state.context = preset_data["content"]
                st.rerun()
    
    # Show user presets if any with clean styling
    if st.session_state.user_presets:
        st.subheader("Je aangepaste presets:")
        for preset_name, preset_content in st.session_state.user_presets.items():
            description = f"Eigen preset ({len(preset_content)} karakters)"
            st.markdown(f"""
            <div class="preset-card">
                <strong>{preset_name}</strong><br>
                <small>{description}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Selecteer {preset_name}", key=f"user_{preset_name.replace(' ', '_')}_btn"):
                with st.spinner('Preset laden...'):
                    time.sleep(0.3)
                    st.session_state.context = preset_content
                    st.rerun()
    
    # Clean custom context section
    st.subheader("Aangepaste context")
    
    # Clean toggle button for custom context
    if st.button("Aangepaste context " + ("verbergen" if "show_custom_context" in st.session_state and st.session_state.show_custom_context else "tonen")):
        if "show_custom_context" not in st.session_state:
            st.session_state.show_custom_context = True
        else:
            st.session_state.show_custom_context = not st.session_state.show_custom_context
        st.rerun()
    
    # Show custom context section if toggled with clean styling
    if "show_custom_context" in st.session_state and st.session_state.show_custom_context:
        custom_context = st.text_area(
            "Voeg je eigen context toe:",
            value=st.session_state.context,
            height=300,
            key="custom_context"
        )
        
        # Clean save buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Opslaan", key="save_context"):
                with st.spinner("Context opslaan..."):
                    time.sleep(0.3)
                    st.session_state.context = custom_context
                    st.success("Context opgeslagen!")
        
        with col2:
            if st.button("Wissen", key="clear_context"):
                with st.spinner("Wissen..."):
                    time.sleep(0.3)
                    st.session_state["custom_context"] = ""
                    st.session_state.context = ""
                    st.rerun()
        
        # Clean preset saving option
        new_preset_name = st.text_input("Preset naam (optioneel):")
        if st.button("Opslaan als preset") and new_preset_name:
            with st.spinner("Preset opslaan..."):
                time.sleep(0.3)
                st.session_state.user_presets[new_preset_name] = custom_context
                st.success(f"Preset '{new_preset_name}' opgeslagen!")
    
    # Clean warning box
    st.markdown("""
    <div class="warning-box">
        <strong>Let op:</strong> Gesprekken worden niet opgeslagen en worden verwijderd wanneer je de pagina verlaat.
    </div>
    """, unsafe_allow_html=True)

# Clean main chat interface
chat_container = st.container()

# Clean chat clear button
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Gesprek wissen"):
        with st.spinner("Gesprek wissen..."):
            time.sleep(0.3)
            st.session_state.messages = []
            st.rerun()

# Display welcome screen if no messages with clean styling
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-screen">
            <h3>Welkom bij Home Work Bot</h3>
            <p>Kies een preset of stel een vraag om te beginnen.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages with clean styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Clean chat input
if prompt := st.chat_input("Stel een vraag..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Initialize the model
        model = genai.GenerativeModel(model_name)
        
        # Create the complete prompt including context
        complete_prompt = prompt
        if st.session_state.context:
            complete_prompt = f"""
            Context informatie:
            {st.session_state.context}
            
            Op basis van bovenstaande context, beantwoord deze vraag of verzoek:
            {prompt}
            """
        
        # Generate content with clean styling
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Show typing indicator with clean styling
            message_placeholder.markdown("<span style='color: #999999;'>Bezig met nadenken...</span>", unsafe_allow_html=True)
            
            # Generate content
            response = model.generate_content(
                complete_prompt,
                stream=True
            )
            
            # Stream the response with clean styling
            for chunk in response:
                if hasattr(chunk, 'text'):
                    full_response += chunk.text
                    message_placeholder.markdown(full_response)
                    
            # Store the response
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        error_msg = str(e)
        st.error(f"Fout bij het genereren van een antwoord: {error_msg}")

# Clean footer
st.markdown("""
<div class="footer">
    Home Work Bot — Gemaakt door een professioneel team © 2025
</div>
""", unsafe_allow_html=True)
