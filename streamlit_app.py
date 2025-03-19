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

# Much more stylish CSS with animations and better contrast
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary: #e63946;
        --secondary: #1d3557;
        --light: #f1faee;
        --accent: #a8dadc;
        --dark: #457b9d;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(230, 57, 70, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(230, 57, 70, 0); }
        100% { box-shadow: 0 0 0 0 rgba(230, 57, 70, 0); }
    }
    
    /* Base styling */
    .main {
        background: linear-gradient(135deg, var(--light) 0%, #ffffff 100%);
        background-attachment: fixed;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--secondary);
        padding: 1rem;
        border-right: 1px solid rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--light);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--accent);
        animation: slideIn 0.5s ease-out;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--primary);
        color: white;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background-color: #c1121f;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        animation: fadeIn 0.5s ease-out;
        border-left: 4px solid var(--dark);
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatMessage"]:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* User messages vs AI messages */
    [data-testid="stChatMessage"][data-testid="user"] {
        border-left: 4px solid var(--primary);
        background-color: rgba(230, 57, 70, 0.05);
    }
    
    /* Chat input styling */
    [data-testid="stChatInput"] {
        border-radius: 30px;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatInput"]:focus {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: pulse 2s infinite;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid var(--accent);
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(230, 57, 70, 0.2);
    }
    
    /* Container styling */
    .css-1y4p8pa {
        padding: 2rem 3rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .main h1 {
        color: var(--secondary);
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid var(--primary);
        padding-bottom: 0.5rem;
        display: inline-block;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: var(--secondary);
        color: white;
        text-align: center;
        padding: 0.75rem;
        font-size: 0.9em;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 100;
    }
    
    /* Preset cards */
    .preset-card {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid var(--primary);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .preset-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 3px solid var(--dark);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8em;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: var(--accent);
        color: var(--secondary);
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Custom context toggle animation */
    .toggle-context {
        transition: all 0.5s ease;
    }
    
    .toggle-context.active {
        background-color: var(--dark);
    }
    
    /* Warning box */
    .warning-box {
        background-color: rgba(230, 57, 70, 0.1);
        border-left: 3px solid var(--primary);
        padding: 0.75rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-size: 0.9em;
    }
    
    /* Sidebar caption styling */
    [data-testid="stSidebar"] .stCaption {
        color: var(--light);
        opacity: 0.8;
        line-height: 1.4;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: var(--primary);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Clear chat button */
    .clear-button {
        background-color: transparent;
        border: 1px solid var(--primary);
        color: var(--primary);
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    
    .clear-button:hover {
        background-color: var(--primary);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# App title with custom HTML
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 2rem; animation: fadeIn 0.7s ease-out;">
    <div style="font-size: 2.5rem; color: #e63946; margin-right: 1rem;">📚</div>
    <h1 style="margin: 0; padding: 0;">Home Work Bot</h1>
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
if "animation_counter" not in st.session_state:
    st.session_state.animation_counter = 0

# Function to create preset card with HTML
def preset_card(title, key, description=""):
    html = f"""
    <div class="preset-card" id="{key}" onclick="document.getElementById('{key}-button').click();" 
         style="animation: fadeIn {0.3 + 0.1 * st.session_state.animation_counter}s ease-out">
        <h4 style="margin-top: 0; color: #1d3557;">{title}</h4>
        <div class="badge">Preset</div>
        <p style="margin-bottom: 0; font-size: 0.9em; color: #666;">{description}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    st.session_state.animation_counter += 1
    return st.button(title, key=f"{key}-button", label_visibility="collapsed")

# Sidebar with improved styling
with st.sidebar:
    st.markdown('<h2 style="animation: slideIn 0.5s ease-out;">Presets</h2>', unsafe_allow_html=True)
    
    # Define presets with descriptions
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
    
    # Reset animation counter
    st.session_state.animation_counter = 0
    
    # Preset cards with animation delay
    for preset_name, preset_data in presets.items():
        if preset_card(preset_name, preset_name.replace(" ", "_"), preset_data["description"]):
            with st.spinner('Preset laden...'):
                time.sleep(0.5)  # Slight delay for animation effect
                st.session_state.context = preset_data["content"]
                st.rerun()
    
    # Show user presets if any
    if st.session_state.user_presets:
        st.markdown('<h3 style="animation: slideIn 0.6s ease-out;">Je aangepaste presets</h3>', unsafe_allow_html=True)
        for preset_name, preset_content in st.session_state.user_presets.items():
            description = f"Eigen preset ({len(preset_content)} karakters)"
            if preset_card(preset_name, f"user_{preset_name.replace(' ', '_')}", description):
                with st.spinner('Preset laden...'):
                    time.sleep(0.5)  # Slight delay for animation effect
                    st.session_state.context = preset_content
                    st.rerun()
    
    # Custom context section with animation
    st.markdown('<h3 style="animation: slideIn 0.7s ease-out;">Aangepaste context</h3>', unsafe_allow_html=True)
    
    # Toggle for custom context
    toggle_class = "toggle-context active" if "show_custom_context" in st.session_state and st.session_state.show_custom_context else "toggle-context"
    custom_button_text = "Verberg aangepaste context" if "show_custom_context" in st.session_state and st.session_state.show_custom_context else "Toon aangepaste context"
    
    st.markdown(f'<div class="{toggle_class}">', unsafe_allow_html=True)
    if st.button(custom_button_text):
        if "show_custom_context" not in st.session_state:
            st.session_state.show_custom_context = True
        else:
            st.session_state.show_custom_context = not st.session_state.show_custom_context
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show custom context section if toggled
    if "show_custom_context" in st.session_state and st.session_state.show_custom_context:
        st.markdown('<div style="animation: fadeIn 0.5s ease-out;">', unsafe_allow_html=True)
        custom_context = st.text_area(
            "Voeg je eigen context toe:",
            value=st.session_state.context,
            height=300,
            key="custom_context"
        )
        
        save_col1, save_col2 = st.columns(2)
        with save_col1:
            if st.button("Opslaan", key="save_context"):
                with st.spinner("Context opslaan..."):
                    time.sleep(0.3)  # Animation effect
                    st.session_state.context = custom_context
                    st.success("Context opgeslagen!")
        
        with save_col2:
            if st.button("Wissen", key="clear_context"):
                with st.spinner("Wissen..."):
                    time.sleep(0.3)  # Animation effect
                    st.session_state["custom_context"] = ""
                    st.session_state.context = ""
                    st.rerun()
        
        # Save as preset option
        st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
        new_preset_name = st.text_input("Preset naam (optioneel):")
        if st.button("Opslaan als preset") and new_preset_name:
            with st.spinner("Preset opslaan..."):
                time.sleep(0.5)  # Animation effect
                st.session_state.user_presets[new_preset_name] = custom_context
                st.success(f"Preset '{new_preset_name}' opgeslagen!")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dutch reminder at bottom with styled box
    st.markdown("""
    <div class="warning-box" style="animation: fadeIn 1s ease-out; margin-top: 2rem;">
        <strong>Let op:</strong> Gesprekken worden niet opgeslagen en worden verwijderd wanneer je de pagina verlaat.
    </div>
    """, unsafe_allow_html=True)

# Main chat interface with improved layout
chat_container = st.container()

# Clear chat button with custom styling
col1, col2 = st.columns([4, 1])
with col2:
    st.markdown('<div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">', unsafe_allow_html=True)
    if st.button("Gesprek wissen", key="clear_chat_button", type="primary"):
        with st.spinner("Gesprek wissen..."):
            time.sleep(0.5)  # Animation effect
            st.session_state.messages = []
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Display chat messages with animation delay
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem; color: #666; animation: fadeIn 1s ease-out;">
            <img src="https://www.svgrepo.com/show/530438/robot.svg" style="width: 80px; height: 80px; margin-bottom: 1rem;">
            <h3>Welkom bij Home Work Bot</h3>
            <p>Kies een preset of stel een vraag om te beginnen.</p>
        </div>
        """, unsafe_allow_html=True)
    
    for i, message in enumerate(st.session_state.messages):
        # Add a small delay between messages for a nicer animation effect
        delay_style = f"animation-delay: {i * 0.1}s;"
        with st.chat_message(message["role"]):
            st.markdown(f'<div style="{delay_style}">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
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
        
        # Generate content with streaming and animation
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Show typing animation first
            message_placeholder.markdown('<div class="typing-animation">Denken<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></div>', unsafe_allow_html=True)
            
            # Generate content with the complete prompt
            response = model.generate_content(
                complete_prompt,
                stream=True
            )
            
            # Stream the response with typing effect
            for chunk in response:
                if hasattr(chunk, 'text'):
                    full_response += chunk.text
                    message_placeholder.markdown(full_response)
                    time.sleep(0.01)  # Slight delay for typing effect
                    
            # Store the response
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        error_msg = str(e)
        st.error(f"Fout bij het genereren van een antwoord: {error_msg}")

# Professional footer with animation
st.markdown("""
<div class="footer" style="animation: fadeIn 1s ease-out;">
    <div style="display: flex; justify-content: center; align-items: center;">
        <p style="margin: 0;">Home Work Bot — Gemaakt door een professioneel team © 2025</p>
    </div>
</div>
""", unsafe_allow_html=True)
