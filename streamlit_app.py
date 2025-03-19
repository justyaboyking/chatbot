# Required dependencies:
# pip install PyPDF2 python-docx

import streamlit as st 
import google.generativeai as genai
import time
import PyPDF2
import docx
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
</style>

<!-- Watermark -->
<div class="watermark">
    home work bot - made by zakaria
</div>
""", unsafe_allow_html=True)

# App title
st.title("Home Work Bot")

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
if "show_presets" not in st.session_state:
    st.session_state.show_presets = True

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
            "Temperature:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1
        )
        st.session_state.temperature = temperature
        
        # Clear chat button in settings
        st.subheader("Chat Management")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.show_presets = True
            st.rerun()
    
    # Custom context section with file upload support
    with st.expander("Context Management", expanded=False):
        # File uploader for PDF and Word documents
        uploaded_file = st.file_uploader("Upload PDF or Word Document", type=["pdf", "docx"])
        if uploaded_file is not None:
            file_text = ""
            if uploaded_file.name.lower().endswith("pdf"):
                try:
                    reader = PyPDF2.PdfReader(uploaded_file)
                    for page in reader.pages:
                        file_text += page.extract_text() + "\n"
                except Exception as e:
                    st.error(f"Error reading PDF: {str(e)}")
            elif uploaded_file.name.lower().endswith("docx"):
                try:
                    doc = docx.Document(uploaded_file)
                    file_text = "\n".join([para.text for para in doc.paragraphs])
                except Exception as e:
                    st.error(f"Error reading Word document: {str(e)}")
            if file_text:
                if st.button("Load File Content into Context"):
                    st.session_state.context += "\n" + file_text
                    st.success("File content added to context.")
                    st.experimental_rerun()
        
        # Text area to edit context
        custom_context = st.text_area(
            "Edit context:",
            value=st.session_state.context,
            height=300,
            key="custom_context"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", key="save_context"):
                st.session_state.context = custom_context
                st.success("Saved!")
        
        with col2:
            if st.button("Clear", key="clear_context"):
                st.session_state["custom_context"] = ""
                st.session_state.context = ""
                st.rerun()

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
Veel succes!"""
    }
}

# Main content area
main_container = st.container()

# First show presets if no conversation started
if st.session_state.show_presets and not st.session_state.messages:
    with main_container:
        st.subheader("Kies een preset om te beginnen")
        
        # Grid layout for presets
        cols = st.columns(3)
        col_idx = 0
        
        # Display default presets
        for preset_name, preset_data in presets.items():
            with cols[col_idx]:
                st.markdown(f"""
                <div class="preset-card" onclick="document.getElementById('{preset_name.replace(' ', '_')}_btn').click();">
                    <strong>{preset_name}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden button triggered by the card
                if st.button("Select", key=f"{preset_name.replace(' ', '_')}_btn"):
                    # Set context
                    st.session_state.context = preset_data["content"]
                    
                    # Add first AI message
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": "Wat is je deelstaat? (Bijvoorbeeld: Bayern, Hessen, Nordrhein-Westfalen)"
                    })
                    
                    # Hide presets once selected
                    st.session_state.show_presets = False
                    st.rerun()
            
            col_idx = (col_idx + 1) % 3
        
        # Display user presets if any
        if st.session_state.user_presets:
            st.subheader("Je eigen presets:")
            
            user_cols = st.columns(3)
            col_idx = 0
            
            for preset_name, preset_content in st.session_state.user_presets.items():
                with user_cols[col_idx]:
                    st.markdown(f"""
                    <div class="preset-card" onclick="document.getElementById('user_{preset_name.replace(' ', '_')}_btn').click();">
                        <strong>{preset_name}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Select", key=f"user_{preset_name.replace(' ', '_')}_btn"):
                        # Set context
                        st.session_state.context = preset_content
                        
                        # Add first AI message
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": "Wat is je vraag?"
                        })
                        
                        # Hide presets once selected
                        st.session_state.show_presets = False
                        st.rerun()
                
                col_idx = (col_idx + 1) % 3

# Always display chat messages (whether empty or not)
with main_container:
    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Always show the chat input at the bottom (Claude style)
    if prompt := st.chat_input("Typ je vraag..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hide presets once user starts typing
        st.session_state.show_presets = False
        
        # Display the user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            # Process with Gemini
            model = genai.GenerativeModel(
                st.session_state.model_name,
                generation_config={"temperature": st.session_state.temperature}
            )
            
            # Create appropriate prompt based on context
            if st.session_state.context:
                complete_prompt = f"""
                Context informatie:
                {st.session_state.context}
                
                Op basis van bovenstaande context, geef informatie over de deelstaat "{prompt}" en volg exact de structuur uit de context:
                
                1. Gebruik precies de secties zoals aangegeven in de context
                2. Zet elke sectie en item op een nieuwe regel met een lege regel ertussen
                3. Gebruik duidelijke koppen gevolgd door dubbele regeleinden
                4. Antwoord alleen met de gestructureerde informatie, zonder inleidingen of conclusies
                5. Zorg dat elke sectie apart en duidelijk leesbaar is
                
                Format de tekst zo:
                
                Algemene Informatie:
                
                Naam: [naam]
                
                Hoofdstad: [hoofdstad]
                
                Fläche: [oppervlakte]
                
                Einwohnerzahl: [inwoners]
                
                Enzovoort voor alle secties uit de context.
                """
            else:
                complete_prompt = prompt
            
            # Generate response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                # Generate content
                response = model.generate_content(
                    complete_prompt,
                    stream=True
                )
                
                # Display streaming response
                full_response = ""
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                        message_placeholder.markdown(full_response)
                
                # Store response
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
