import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Set page config to wide mode and customize
st.set_page_config(
    page_title="Home Work Bot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make it look more like ChatGPT with red and white theme
st.markdown("""
<style>
    /* Main red and white theme */
    .main {
        background-color: #ffffff;
    }
    .stApp {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #c1121f;
    }
    /* Chat message styling */
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    .css-1544g2n {
        padding: 2rem 1rem;
    }
    /* Header styling */
    h1, h2, h3 {
        color: #e63946;
    }
    /* Input boxes */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    /* Chat input */
    .stChatInputContainer {
        border-top: 1px solid #e0e0e0;
        padding-top: 1rem;
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

# Sidebar for presets and context
with st.sidebar:
    st.header("Presets")
    
    # Define presets
    presets = {
        "duits deelstaten": """PowerPoint Präsentation / PowerPoint Presentatie
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
    
    # Preset selection - clean design with buttons in a grid
    st.subheader("Kies een preset:")
    preset_cols = st.columns(2)
    for idx, (preset_name, preset_content) in enumerate(presets.items()):
        col_idx = idx % 2
        with preset_cols[col_idx]:
            if st.button(preset_name):
                st.session_state.context = preset_content
                st.rerun()  # Using rerun instead of experimental_rerun
    
    # Show user presets if any
    if st.session_state.user_presets:
        st.subheader("Je aangepaste presets:")
        user_preset_cols = st.columns(2)
        for idx, (preset_name, preset_content) in enumerate(st.session_state.user_presets.items()):
            col_idx = idx % 2
            with user_preset_cols[col_idx]:
                if st.button(preset_name, key=f"user_preset_{idx}"):
                    st.session_state.context = preset_content
                    st.rerun()
    
    # Option to use custom context
    st.subheader("Of maak je eigen:")
    if st.button("Aangepaste context gebruiken"):
        if "show_custom_context" not in st.session_state:
            st.session_state.show_custom_context = True
        else:
            st.session_state.show_custom_context = not st.session_state.show_custom_context
        st.rerun()
    
    # Show custom context section if toggled
    if "show_custom_context" in st.session_state and st.session_state.show_custom_context:
        st.text_area(
            "Voeg aangepaste context toe:",
            value=st.session_state.context,
            height=300,
            key="custom_context"
        )
        
        if st.button("Opslaan als context"):
            st.session_state.context = st.session_state["custom_context"]
            st.success("Context opgeslagen!")
        
        # Save as preset option
        new_preset_name = st.text_input("Preset naam (optioneel):")
        if st.button("Opslaan als preset") and new_preset_name:
            st.session_state.user_presets[new_preset_name] = st.session_state["custom_context"]
            st.success(f"Preset '{new_preset_name}' opgeslagen!")
    
    # Dutch reminder at bottom
    st.markdown("---")
    st.caption("**Let op:** Gesprekken worden niet opgeslagen en worden verwijderd wanneer je de pagina verlaat.")

# Main chat interface
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
        
        # Generate content with streaming
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            
            # Generate content with the complete prompt
            response = model.generate_content(
                complete_prompt,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if hasattr(chunk, 'text'):
                    full_response += chunk.text
                    response_container.markdown(full_response)
                
            # Store the response
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        error_msg = str(e)
        st.error(f"Fout bij het genereren van een antwoord: {error_msg}")
        
# Professional footer
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #f8f9fa; padding: 10px; border-top: 1px solid #e0e0e0; text-align: center; font-size: 0.8em;">
    <p>Home Work Bot - Gemaakt door een professioneel team. © 2025</p>
</div>
""", unsafe_allow_html=True)
