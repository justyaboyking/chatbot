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

# Enhanced CSS with modern UI elements
st.markdown("""
<style>
    /* Dark theme base */
    body {
        color: white;
        background-color: #0e1117;
    }
    
    /* Sidebar styling - modern look */
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
        border-right: 1px solid #2a2d36;
        padding-top: 0;
    }
    
    /* Sidebar header */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
        padding: 0.5rem 0;
    }
    
    /* New chat button */
    .new-chat-btn {
        background-color: #404756;
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0 1.5rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .new-chat-btn:hover {
        background-color: #505666;
    }
    
    /* Chat history items */
    .chat-history-item {
        background-color: transparent;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        cursor: pointer;
        display: flex;
        align-items: center;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        transition: all 0.2s ease;
    }
    
    .chat-history-item:hover {
        background-color: #2a2d36;
    }
    
    /* Sidebar sections */
    .sidebar-section {
        margin: 1.5rem 0;
        border-top: 1px solid #2a2d36;
        padding-top: 1rem;
    }
    
    /* Top bar */
    .topbar {
        position: fixed;
        top: 0;
        left: 20%; /* Match sidebar width */
        right: 0;
        height: 60px;
        background-color: #0e1117;
        border-bottom: 1px solid #262730;
        display: flex;
        align-items: center;
        padding: 0 2rem;
        z-index: 99;
    }
    
    /* Model selector in top bar */
    .model-selector {
        background-color: #1a1c24;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    /* Fixed chat input at bottom */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 20%;
        right: 0;
        background-color: #0e1117;
        padding: 1rem 2rem;
        border-top: 1px solid #262730;
        z-index: 99;
    }
    
    /* Chat container with proper spacing */
    .chat-container {
        margin-top: 70px; /* Space for topbar */
        margin-bottom: 80px; /* Space for input box */
        padding: 1rem 2rem;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #262730;
        border-radius: 0.75rem;
        margin: 0.75rem 0;
        padding: 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* User vs assistant messages */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #383b44;
    }
    
    /* Icons */
    .icon {
        margin-right: 0.5rem;
        display: inline-flex;
        align-items: center;
    }
    
    /* Collapsible sections */
    .collapsible {
        cursor: pointer;
        padding: 0.5rem 0;
    }
    
    /* Preset cards */
    .preset-card {
        background-color: #262730;
        border-radius: 0.75rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .preset-card:hover {
        background-color: #2a2d36;
        border-color: #3a3d46;
    }
    
    /* Watermark */
    .watermark {
        position: fixed;
        top: 10px;
        left: 10px;
        color: rgba(255, 255, 255, 0.5);
        font-size: 12px;
        z-index: 1000;
    }
</style>

<!-- Watermark -->
<div class="watermark">
    home work bot - made by zakaria
</div>

<!-- Top Bar with Model Selector -->
<div class="topbar">
    <div class="model-selector">
        <span id="current-model">Gemini 1.5 Flash</span>
        <span style="margin-left: 5px;">▼</span>
    </div>
</div>
""", unsafe_allow_html=True)

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
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None

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
    }
}

# Configure Gemini API
genai.configure(api_key="AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w")

# Enhanced sidebar with modern design
with st.sidebar:
    # New Chat Button
    st.markdown("""
    <div class="new-chat-btn" onclick="document.getElementById('new_chat_btn').click();">
        <span class="icon">➕</span> New Chat
    </div>
    """, unsafe_allow_html=True)
    if st.button("New Chat", key="new_chat_btn", help="Start a new chat"):
        st.session_state.messages = []
        st.session_state.show_presets = True
        st.session_state.active_chat = None
        st.rerun()
    
    # Remove the Recent Chats section completely
    
    # Collapsible Gems Section
    with st.expander("✨ Gems", expanded=False):
        st.markdown("### Saved Responses")
        
        # Make gem items clickable and functional
        st.markdown("""
        <div class="chat-history-item" onclick="document.getElementById('gem_german_states').click();">
            <span class="icon">⭐</span> German States Reference
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load", key="gem_german_states", help="Load German States Reference"):
            st.session_state.context = presets["duits deelstaten"]["content"]
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Wat is je deelstaat? (Bijvoorbeeld: Bayern, Hessen, Nordrhein-Westfalen)"
            })
            st.session_state.show_presets = False
            st.session_state.active_chat = "German States Reference"
            st.rerun()
            
        st.markdown("""
        <div class="chat-history-item" onclick="document.getElementById('gem_dutch_verb').click();">
            <span class="icon">⭐</span> Dutch Verb Conjugations
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load", key="gem_dutch_verb", help="Load Dutch Verb Conjugations"):
            # You can customize the context for Dutch verbs here
            dutch_verbs_context = "Help with Dutch verb conjugations for different tenses and forms."
            st.session_state.context = dutch_verbs_context
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Which Dutch verb would you like me to conjugate?"
            })
            st.session_state.show_presets = False
            st.session_state.active_chat = "Dutch Verb Conjugations"
            st.rerun()
    
    # Collapsible AI Settings
    with st.expander("🤖 AI Settings", expanded=False):
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
    
    # Bottom section removed - keeping only Gems expander above
    
    # Context Management (moved from old design)
    with st.expander("📄 Context Management", expanded=False):
        # File uploader for PDF and Word documents
        uploaded_file = st.file_uploader("Upload PDF or Word Document", type=["pdf", "docx"])
        if uploaded_file is not None:
            file_text = ""
            if uploaded_file.name.lower().endswith("pdf"):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded_file)
                    for page in reader.pages:
                        file_text += page.extract_text() + "\n"
                except ModuleNotFoundError:
                    st.error("PyPDF2 is not installed. Please include it in your requirements.txt.")
                except Exception as e:
                    st.error(f"Error reading PDF: {str(e)}")
            elif uploaded_file.name.lower().endswith("docx"):
                try:
                    import docx
                    doc = docx.Document(uploaded_file)
                    file_text = "\n".join([para.text for para in doc.paragraphs])
                except ModuleNotFoundError:
                    st.error("python-docx is not installed. Please include it in your requirements.txt.")
                except Exception as e:
                    st.error(f"Error reading Word document: {str(e)}")
            if file_text:
                if st.button("Load File Content into Context"):
                    st.session_state.context += "\n" + file_text
                    st.success("File content added to context.")
                    st.rerun()
        
        # Text area to edit context
        custom_context = st.text_area(
            "Edit context:",
            value=st.session_state.context,
            height=300,
            key="custom_context"
        )
        
        # Save Preset functionality
        if st.session_state.context.strip():
            st.subheader("Save as Preset")
            preset_name = st.text_input("Preset Name:", key="new_preset_name")
            if st.button("Save Preset") and preset_name:
                st.session_state.user_presets[preset_name] = st.session_state.context
                st.success(f"Preset '{preset_name}' saved successfully!")
                st.rerun()
        
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

# Main content area with chat interface
main_container = st.container()

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Show presets if there are no messages or we're starting a new chat
if st.session_state.show_presets and not st.session_state.messages:
    with main_container:
        st.markdown("<h2>Kies een preset om te beginnen</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        col_idx = 0
        
        # Built-in presets
        for preset_name, preset_data in presets.items():
            with cols[col_idx]:
                st.markdown(f"""
                <div class="preset-card" onclick="document.getElementById('{preset_name.replace(' ', '_')}_btn').click();">
                    <strong>{preset_name}</strong>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Select", key=f"{preset_name.replace(' ', '_')}_btn"):
                    st.session_state.context = preset_data["content"]
                    
                    # Welcome message for German states preset
                    welcome_msg = "Wat is je deelstaat? (Bijvoorbeeld: Bayern, Hessen, Nordrhein-Westfalen)"
                        
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": welcome_msg
                    })
                    st.session_state.show_presets = False
                    st.session_state.active_chat = preset_name
                    st.rerun()
            col_idx = (col_idx + 1) % 3
        
        # User presets
        if st.session_state.user_presets:
            st.markdown("<h3>Je eigen presets:</h3>", unsafe_allow_html=True)
            user_cols = st.columns(3)
            col_idx = 0
            for preset_name, preset_content in st.session_state.user_presets.items():
                with user_cols[col_idx]:
                    st.markdown(f"""
                    <div class="preset-card" onclick="document.getElementById('user_{preset_name.replace(' ', '_')}_btn').click();">
                        <strong>{preset_name}</strong>
                        <p style="margin-top: 0.5rem; font-size: 0.9em; opacity: 0.8;">
                            {preset_content[:100]}...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Select", key=f"user_{preset_name.replace(' ', '_')}_btn"):
                        st.session_state.context = preset_content
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": "Wat is je vraag?"
                        })
                        st.session_state.show_presets = False
                        st.session_state.active_chat = preset_name
                        st.rerun()
                col_idx = (col_idx + 1) % 3

# Display chat messages
with main_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Typ je vraag..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.show_presets = False
        
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # If no active chat, create one based on first message
        if not st.session_state.active_chat:
            chat_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
            st.session_state.active_chat = chat_title
            st.session_state.chat_history.insert(0, {
                "title": chat_title,
                "timestamp": "Just now"
            })
        
        try:
            model = genai.GenerativeModel(
                st.session_state.model_name,
                generation_config={"temperature": st.session_state.temperature}
            )
            
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
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                response = model.generate_content(
                    complete_prompt,
                    stream=True
                )
                full_response = ""
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                        message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)
