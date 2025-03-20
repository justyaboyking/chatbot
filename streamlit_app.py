import streamlit as st 
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="Home Work Bot",
    page_icon="📚",
    layout="centered",  # Changed to centered for better mobile experience
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar on mobile
)

# Mobile-optimized CSS
st.markdown("""
<style>
    /* Base styles */
    body {
        color: white;
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Mobile-friendly sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
        border-right: 1px solid rgba(42, 45, 54, 0.3);
        min-width: 250px !important;
    }
    
    /* Improved typography */
    h1, h2, h3 {
        color: white;
        padding: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #262730;
        border-radius: 0.75rem;
        margin: 0.75rem 0;
        padding: 0.75rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #383b44;
    }
    
    /* Mobile responsive chat input */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: rgba(14, 17, 23, 0.95);
        backdrop-filter: blur(5px);
        padding: 0.75rem;
        border-top: none;
        z-index: 99;
    }
    
    /* Chat container spacing */
    .chat-container {
        margin-bottom: 60px;
        padding: 0.5rem;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Button styling */
    button[data-testid="baseButton-secondary"] {
        background-color: #404756 !important;
        color: white !important;
        border: none !important;
        border-radius: 0.25rem !important;
    }
    
    /* Mobile responsive design */
    @media (max-width: 768px) {
        .chat-container {
            padding: 0.25rem;
        }
        
        [data-testid="stChatMessage"] {
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        
        [data-testid="stChatInput"] {
            padding: 0.5rem;
        }
    }
</style>
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

# Define presets - only keep what's needed
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

# Configure Gemini API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"  # Fallback for testing
genai.configure(api_key=api_key)

# Simplified sidebar for mobile
with st.sidebar:
    # New Chat Button
    if st.button("Nieuwe Chat", key="new_chat_btn"):
        st.session_state.messages = []
        st.session_state.show_presets = True
        st.session_state.active_chat = None
        st.session_state.context = ""
        st.experimental_rerun()
    
    # Only essential sections
    st.subheader("✨ Huiswerk")
    if st.button("Duits Deelstaten", key="gem_german_states"):
        st.session_state.messages = []
        st.session_state.context = presets["duits deelstaten"]["content"]
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Wat is je deelstaat? (Bijvoorbeeld: Bayern, Hessen, Nordrhein-Westfalen)"
        })
        st.session_state.show_presets = False
        st.session_state.active_chat = "Duitse Deelstaten Referentie"
        st.experimental_rerun()
    
    # Simplified AI Settings
    st.subheader("🤖 AI Instellingen")
    model_options = {
        "Gemini 1.5 Flash": "gemini-1.5-flash",
        "Gemini 2.0 Flash": "gemini-2.0-flash-thinking-exp-01-21",
        "Gemini 2.0 Flash-Lite": "gemini-2.0-flash-lite"
    }
    
    selected_model = st.selectbox(
        "AI Model:",
        options=list(model_options.keys()),
        index=list(model_options.values()).index(st.session_state.model_name) if st.session_state.model_name in list(model_options.values()) else 0
    )
    st.session_state.model_name = model_options[selected_model]
    
    st.session_state.temperature = st.slider(
        "Temperatuur:", min_value=0.0, max_value=1.0, 
        value=st.session_state.temperature, step=0.1
    )
    
    # Simplified context management
    st.subheader("📄 Context")
    custom_context = st.text_area(
        "", value=st.session_state.context, height=150
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Opslaan"):
            st.session_state.context = custom_context
    with col2:
        if st.button("Wissen"):
            st.session_state.context = ""
            st.experimental_rerun()

# Main content area with chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Initial greeting - simplified
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hallo! Hoe kan ik je vandaag helpen met je huiswerk?"
    })
    st.session_state.show_presets = False

# Display chat messages - optimized for performance
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Typ je vraag hier...")
if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.show_presets = False
    
    # Create active chat if none exists
    if not st.session_state.active_chat:
        chat_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
        st.session_state.active_chat = chat_title
    
    # Handle AI response generation
    try:
        # Configure the model
        model = genai.GenerativeModel(
            st.session_state.model_name,
            generation_config={"temperature": st.session_state.temperature}
        )
        
        # Prepare prompt with context if needed
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
        
        # Generate AI response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for response in model.generate_content(
                complete_prompt,
                stream=True
            ):
                if hasattr(response, 'text'):
                    chunk = response.text
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
            
            # Final display without cursor
            message_placeholder.markdown(full_response)
                    
            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        # Handle errors
        with st.chat_message("assistant"):
            st.error(f"Error: {str(e)}")
        
        # Add error message to chat
        st.session_state.messages.append({"role": "assistant", "content": f"Er is een fout opgetreden: {str(e)}"})
    
    st.experimental_rerun()
