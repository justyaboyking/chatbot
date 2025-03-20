import streamlit as st 
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="Home Work Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, minimal CSS
st.markdown("""
<style>
    /* Modern clean theme */
    body {
        color: white;
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
        border-right: 1px solid rgba(42, 45, 54, 0.3);
    }
    
    /* Improved typography */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
        padding: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Sleek chat messages */
    [data-testid="stChatMessage"] {
        background-color: #262730;
        border-radius: 0.75rem;
        margin: 0.75rem 0;
        padding: 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #383b44;
    }
    
    /* Fixed chat input */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 20%;
        right: 0;
        background-color: rgba(14, 17, 23, 0.95);
        backdrop-filter: blur(5px);
        padding: 1rem 2rem;
        border-top: none;
        z-index: 99;
    }
    
    /* Chat container spacing */
    .chat-container {
        margin-top: 20px;
        margin-bottom: 80px;
        padding: 1rem 2rem;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean button styling */
    button[data-testid="baseButton-secondary"] {
        background-color: #404756 !important;
        color: white !important;
        border: none !important;
        border-radius: 0.25rem !important;
    }
    
    /* Minimal watermark */
    .watermark {
        position: fixed;
        bottom: 60px;
        right: 20px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
        z-index: 1000;
        pointer-events: none;
        background-color: rgba(0, 0, 0, 0.4);
        padding: 5px 10px;
        border-radius: 4px;
    }
</style>

<div class="watermark">
    Made by Zakaria
</div>
""", unsafe_allow_html=True)

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

# Define presets - simplified to core content
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
Lage auf der kaart: [Füge eine Karte ein]
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
Schritt 2: Die PowerPoint-Präsentation maken
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

# Configure Gemini API - Use environment variables for security
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Simplified streamlined sidebar
with st.sidebar:
    # New Chat Button
    if st.button("Nieuwe Chat", key="new_chat_btn"):
        st.session_state.messages = []
        st.session_state.show_presets = True
        st.session_state.active_chat = None
        st.session_state.context = ""
        st.rerun()
    
    # Essential sections only - Huiswerk section
    with st.expander("✨ Huiswerk", expanded=False):
        if st.button("Duits Deelstaten", key="gem_german_states"):
            st.session_state.messages = []
            st.session_state.context = presets["duits deelstaten"]["content"]
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Wat is je deelstaat? (Bijvoorbeeld: Bayern, Hessen, Nordrhein-Westfalen)"
            })
            st.session_state.show_presets = False
            st.session_state.active_chat = "Duitse Deelstaten Referentie"
            st.rerun()
    
    # Minimal AI Settings
    with st.expander("🤖 AI Instellingen", expanded=False):
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
            "Temperatuur:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1
        )
    
    # Simplified context management
    with st.expander("📄 Context", expanded=False):
        custom_context = st.text_area(
            "Context:",
            value=st.session_state.context,
            height=200
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Opslaan"):
                st.session_state.context = custom_context
                st.success("Opgeslagen!")
        with col2:
            if st.button("Wissen"):
                st.session_state.context = ""
                st.rerun()

# Main content area with chat interface
main_container = st.container()

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Initial greeting
if st.session_state.show_presets and not st.session_state.messages:
    with main_container:
        st.session_state.messages = []
        st.session_state.context = ""
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hallo! Hoe kan ik je vandaag helpen met je huiswerk?"
        })
        st.session_state.show_presets = False
        st.rerun()

# Display chat messages
with main_container:
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Simple copy button
            if st.button("Kopiëren", key=f"copy_btn_{i}"):
                st.session_state.copied_message = i
                st.rerun()
            
            # Copy confirmation
            if st.session_state.copied_message == i:
                st.success("Tekst gekopieerd!")
                time.sleep(1)
                st.session_state.copied_message = None

st.markdown('</div>', unsafe_allow_html=True)

# Chat input - MOVED OUTSIDE OF ANY CONTAINER
if prompt := st.chat_input("Typ je vraag hier..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.show_presets = False
    
    # Create active chat if none exists
    if not st.session_state.active_chat:
        chat_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
        st.session_state.active_chat = chat_title
    
    try:
        model = genai.GenerativeModel(
            st.session_state.model_name,
            generation_config={"temperature": st.session_state.temperature}
        )
        
        # Handle context for German states reference
        if st.session_state.active_chat == "Duitse Deelstaten Referentie" and st.session_state.context:
            complete_prompt = f"""
            Context informatie:
            {st.session_state.context}
            
            Op basis van bovenstaande context, geef informatie over de Duitse deelstaat "{prompt}" en volg exact de structuur uit de context:
            
            1. Gebruik precies de secties zoals aangegeven in de context
            2. Zet elke sectie en item op een nieuwe regel met een lege regel ertussen
            3. Gebruik duidelijke koppen gevolgd door dubbele regeleinden
            4. Antwoord alleen met de gestructureerde informatie, zonder inleidingen of conclusies
            5. Zorg dat elke sectie apart en duidelijk leesbaar is
            """
        else:
            complete_prompt = prompt
        
        # Add user message to chat history display
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate AI response
        response = model.generate_content(
            complete_prompt,
            stream=True
        )
        
        full_response = ""
        
        # Process the response
        for chunk in response:
            if hasattr(chunk, 'text'):
                full_response += chunk.text
        
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Rerun to display the new messages
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.rerun()
