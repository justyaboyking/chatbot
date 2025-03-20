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
if "current_page" not in st.session_state:
    st.session_state.current_page = None

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
    },
    "wiskunde huiswerk": {
        "content": """# Wiskunde Huiswerk Helper Prompt

Je bent een behulpzame wiskunde assistent die gespecialiseerd is in het oplossen van Nederlandse wiskundeproblemen voor middelbare scholieren. Je helpt leerlingen met hun wiskunde huiswerk door duidelijke, stapsgewijze uitleg te geven van de opgaven.

## Instructies:

1. Begin door de leerling te vragen: "Welke pagina('s) van je wiskunde werkboek wil je behandelen? (pagina 208-221)"

2. Zodra de leerling een paginanummer of bereik opgeeft, identificeer je de specifieke opdrachten op die pagina's.

3. Voor elke opdracht:
   - Lees de vraag zorgvuldig
   - Geef een volledige, stapsgewijze oplossing
   - Leg de wiskundige concepten duidelijk uit
   - Toon alle berekeningen
   - Presenteer het antwoord in de vorm zoals het werkboek verwacht

4. Focus op de volgende onderwerpen die in het werkboek voorkomen:
   - Lineaire verbanden
   - Formules en vergelijkingen
   - Grafieken interpreteren en opstellen
   - Tabellen invullen
   - Toepassingsproblemen (kosten, tijd, afstand, etc.)
   - Stijgende, dalende of constante verbanden

5. Gebruik de juiste Nederlandse wiskundige terminologie.

6. Als er meerdere vragen op een pagina staan (a, b, c, d, etc.), behandel ze dan één voor één en markeer duidelijk welke vraag je beantwoordt.

7. Als een tabel moet worden ingevuld, maak dan een duidelijke tabel met alle berekende waarden.

8. Voor grafiekvragen, leg uit welke grafiek bij welke formule hoort en waarom.

9. Blijf vriendelijk, geduldig en begrijpend, maar blijf altijd in het Nederlands antwoorden.

10. Als een vraag extra uitleg nodig heeft, geef dan aanvullende context over het wiskundige concept.

Herinner je: het doel is om de leerling te helpen de stof te begrijpen, niet alleen de antwoorden te geven.

## Pagina Informatie

De werkboekpagina's 208-221 bevatten opgaven over de volgende onderwerpen:
- Lineaire verbanden
- Formules opstellen en toepassen
- Grafieken interpreteren en analyseren 
- Tabellen invullen en verbanden bepalen
- Toepassingsproblemen met kosten, tijd, afstand, etc.

Er zijn verschillende opdrachten zoals:
- Opdracht 10-13: Lineaire verbanden tussen variabelen
- Opdracht 14-17: Tabellen invullen met formules
- Opdracht 18-21: Grafieken en formules koppelen
- Opdracht 22-25: Toepassingen met prijzen, afstanden en tijd
- Opdracht 26-29: Verbanden tussen verschillende variabelen
- Opdracht 30-33: Toepassingen met groei, kosten en brandstof

Elk opdrachtnummer kan deelvragen hebben (a, b, c, d, etc.) die je per stuk moet beantwoorden.
"""
    }
}

# Configure Gemini API - Use environment variables for security
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"  # Fallback for testing
genai.configure(api_key=api_key)

# Streamlined sidebar
with st.sidebar:
    # New Chat Button
    if st.button("Nieuwe Chat", key="new_chat_btn"):
        st.session_state.messages = []
        st.session_state.show_presets = True
        st.session_state.active_chat = None
        st.session_state.context = ""
        st.rerun()
    
    # Homework sections
    with st.expander("✨ Huiswerk", expanded=True):
        # Add the Wiskunde option
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Wiskunde", key="wiskunde_btn"):
                st.session_state.messages = []
                st.session_state.context = presets["wiskunde huiswerk"]["content"]
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "Welke pagina('s) van je wiskunde werkboek wil je behandelen? (pagina 208-221)"
                })
                st.session_state.show_presets = False
                st.session_state.active_chat = "Wiskunde Huiswerk Helper"
                st.rerun()
        
        with col2:
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
    
    # Page selector for Wiskunde (only shown when in Wiskunde mode)
    if st.session_state.active_chat == "Wiskunde Huiswerk Helper":
        with st.expander("📝 Wiskunde Pagina's", expanded=True):
            # Page range for the workbook
            page_range = list(range(208, 222))  # Pages 208-221
            
            selected_page = st.selectbox(
                "Selecteer een pagina:",
                page_range,
                index=0 if not st.session_state.current_page else page_range.index(st.session_state.current_page)
            )
            
            if selected_page != st.session_state.current_page:
                st.session_state.current_page = selected_page
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"Ik wil graag aan pagina {selected_page} werken"
                })
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
    
    # Context management
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
                # Simulate clipboard copying (actual implementation would need JavaScript)
                st.success("Tekst gekopieerd!")
                time.sleep(0.5)
                st.session_state.copied_message = None
                st.rerun()

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
    
    # Show user message immediately
    st.rerun()

# Handle AI response generation (after rerun with user message visible)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_input = st.session_state.messages[-1]["content"]
    
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
            
            Op basis van bovenstaande context, geef informatie over de Duitse deelstaat "{user_input}" en volg exact de structuur uit de context:
            
            1. Gebruik precies de secties zoals aangegeven in de context
            2. Zet elke sectie en item op een nieuwe regel met een lege regel ertussen
            3. Gebruik duidelijke koppen gevolgd door dubbele regeleinden
            4. Antwoord alleen met de gestructureerde informatie, zonder inleidingen of conclusies
            5. Zorg dat elke sectie apart en duidelijk leesbaar is
            """
        elif st.session_state.active_chat == "Wiskunde Huiswerk Helper" and st.session_state.context:
            # Check if user input contains a page number reference
            page_mention = any(str(p) in user_input for p in range(208, 222))
            
            if "pagina" in user_input.lower() and not page_mention:
                # Try to extract page number
                try:
                    import re
                    page_nums = re.findall(r'\d+', user_input)
                    if page_nums:
                        page_num = int(page_nums[0])
                        if 208 <= page_num <= 221:
                            st.session_state.current_page = page_num
                except:
                    pass
            
            if st.session_state.current_page:
                complete_prompt = f"""
                Context informatie:
                {st.session_state.context}
                
                De leerling werkt nu aan pagina {st.session_state.current_page} van het wiskunde werkboek en stelt de volgende vraag:
                "{user_input}"
                
                Beantwoord deze vraag volgens de volgende richtlijnen:
                1. Geef een stapsgewijze uitleg in duidelijk Nederlands
                2. Toon alle berekeningen en tussenresultaten
                3. Leg de wiskundige concepten helder uit
                4. Focus op het helpen van de leerling om het concept te begrijpen
                5. Als het een specifieke opdracht betreft, behandel deze volledig
                6. Bij tabellen of grafieken, geef een duidelijke uitleg van de relatie
                7. Houd de uitleg bondig maar volledig
                
                Als de vraag onduidelijk is of meer context nodig heeft, vraag dan om verduidelijking.
                """
            else:
                complete_prompt = f"""
                Context informatie:
                {st.session_state.context}
                
                De leerling heeft nog geen specifieke pagina geselecteerd en stelt de volgende vraag:
                "{user_input}"
                
                Help de leerling met deze vraag of vraag om een specifiek paginanummer tussen 208-221 om gerichter te kunnen helpen.
                """
        else:
            complete_prompt = user_input
        
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
                    time.sleep(0.01)  # Short delay to make typing visible
            
            # Final display without cursor
            message_placeholder.markdown(full_response)
                    
            # Add assistant message to chat history after streaming completes
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        # Handle errors
        st.error(f"Error: {str(e)}")
        
        # Add error message to chat
        st.session_state.messages.append({"role": "assistant", "content": f"Er is een fout opgetreden: {str(e)}"})
    
    # Rerun to update UI with new messages
    st.rerun()
