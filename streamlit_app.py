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

# Custom CSS with black backgrounds for text
st.markdown("""
<style>
    /* Dark theme with black backgrounds for text */
    body {
        color: white;
        background-color: #121212;
    }
    
    .main {
        background-color: #121212;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #000000;
    }
    
    /* All text containers get black backgrounds */
    .stTextInput, .stTextArea > div > div, p, h1, h2, h3, h4, h5, h6, 
    .stMarkdown, .element-container, [data-testid="stChatMessageContent"] {
        background-color: #000000 !important;
        color: white !important;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: #000000;
        border: 1px solid #333333;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Chat message from assistant vs user */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        border-left: 3px solid #e63946;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        border-left: 3px solid #4ecdc4;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background-color: #c1121f;
    }
    
    /* Input fields */
    input, textarea {
        background-color: #1f1f1f !important;
        color: white !important;
        border: 1px solid #333333 !important;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] {
        background-color: #1f1f1f;
        border: 1px solid #333333;
        color: white;
    }
    
    /* Preset cards */
    .preset-card {
        background-color: #1a1a1a;
        color: white;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 4px solid #e63946;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #0f3d27;
        color: white;
    }
    
    /* Error messages */
    .stError {
        background-color: #3d0f0f;
        color: white;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #000000;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #333333;
    }
    
    /* Warning box */
    .warning-box {
        background-color: #1a1a1a;
        border-left: 3px solid #e63946;
        padding: 10px;
        border-radius: 5px;
        margin: 15px 0;
        font-size: 14px;
        color: white;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #e63946 !important;
    }
</style>
""", unsafe_allow_html=True)

# App title 
st.title("📚 Home Work Bot")

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

# Sidebar with dark theme
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
    
    # Simplified preset selection with black backgrounds
    st.subheader("Kies een preset:")
    for preset_name, preset_data in presets.items():
        # Display a card with black background
        st.markdown(f"""
        <div class="preset-card">
            <strong>{preset_name}</strong><br>
            <small>{preset_data["description"]}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Actual button for selection
        if st.button(f"Selecteer {preset_name}", key=f"{preset_name.replace(' ', '_')}_btn"):
            with st.spinner('Preset laden...'):
                time.sleep(0.3)  # Slight delay for feedback
                st.session_state.context = preset_data["content"]
                st.rerun()
    
    # Show user presets if any
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
    
    # Custom context section
    st.subheader("Aangepaste context")
    
    # Toggle button for custom context
    if st.button("Aangepaste context " + ("verbergen" if "show_custom_context" in st.session_state and st.session_state.show_custom_context else "tonen")):
        if "show_custom_context" not in st.session_state:
            st.session_state.show_custom_context = True
        else:
            st.session_state.show_custom_context = not st.session_state.show_custom_context
        st.rerun()
    
    # Show custom context section if toggled
    if "show_custom_context" in st.session_state and st.session_state.show_custom_context:
        custom_context = st.text_area(
            "Voeg je eigen context toe:",
            value=st.session_state.context,
            height=300,
            key="custom_context"
        )
        
        # Save context button
        if st.button("Opslaan als context"):
            with st.spinner("Context opslaan..."):
                time.sleep(0.3)
                st.session_state.context = custom_context
                st.success("Context opgeslagen!")
        
        # Clear context button
        if st.button("Context wissen"):
            with st.spinner("Wissen..."):
                time.sleep(0.3)
                st.session_state["custom_context"] = ""
                st.session_state.context = ""
                st.rerun()
        
        # Save as preset option
        new_preset_name = st.text_input("Preset naam (optioneel):")
        if st.button("Opslaan als preset") and new_preset_name:
            with st.spinner("Preset opslaan..."):
                time.sleep(0.3)
                st.session_state.user_presets[new_preset_name] = custom_context
                st.success(f"Preset '{new_preset_name}' opgeslagen!")
    
    # Dutch reminder with black background
    st.markdown("""
    <div class="warning-box">
        <strong>Let op:</strong> Gesprekken worden niet opgeslagen en worden verwijderd wanneer je de pagina verlaat.
    </div>
    """, unsafe_allow_html=True)

# Main chat interface with black background
chat_container = st.container()

# Clear chat button
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Gesprek wissen"):
        with st.spinner("Gesprek wissen..."):
            time.sleep(0.3)
            st.session_state.messages = []
            st.rerun()

# Display welcome message if no messages
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 50px; color: #e0e0e0; background-color: #000000; border-radius: 10px;">
            <h3>Welkom bij Home Work Bot</h3>
            <p>Kies een preset of stel een vraag om te beginnen.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages with black backgrounds
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input with black background
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
        
        # Generate content with black background for messages
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Show typing indicator with black background
            message_placeholder.markdown("<span style='color: #999999;'>Bezig met nadenken...</span>", unsafe_allow_html=True)
            
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
        st.error(f"Fout bij het genereren van een antwoord: {error_msg}")

# Black background footer
st.markdown("""
<div class="footer">
    Home Work Bot — Gemaakt door een professioneel team © 2025
</div>
""", unsafe_allow_html=True)
