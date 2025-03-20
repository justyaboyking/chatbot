import streamlit as st 
import google.generativeai as genai
import time
import os
import re
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

# Define function to get page content
def get_page_content():
    # Dictionary of page content descriptions
    page_content = {
        208: """
        Pagina 208 bevat de volgende opgaven:
        
        10. Het verband tussen het aantal en de kostprijs (in euro) is lineair.
        Vul de ontbrekende waarden in de tabel aan.
        
        a. 
        Aantal | 0 | 1 | 2 | 3
        Kostprijs (€) | 50 | 40 | | 
        
        b.
        Aantal | 0 | 1 | 2 | 3
        Kostprijs (€) | 10 | 15 | | 
        
        c.
        Aantal | 0 | 1 | 2 | 3
        Kostprijs (€) | 16 | 16 | | 
        
        d.
        Aantal | 0 | 1 | 2 | 3
        Kostprijs (€) | 0 | 2,5 | | 
        
        11. Je koopt een aantal van de onderstaande producten.
        a. Stel het verband tussen het aantal en de kostprijs (in euro) met een tabel voor.
        Product A: €4,5/stuk
        Product B: €1,25/stuk
        
        12. Vul de tabel aan met behulp van de formules.
        a. p = 4 x z
        z | 0 | 1 | 2 | 3 | 5 | 15
        p | | | | | | 
        
        b. p = 10 + (2 x t)
        t | 0 | 1 | 2 | 3 | 5 | 15
        p | | | | | | 
        
        c. p = d x 3,14
        d | 0 | 1 | 2 | 3 | 5 | 15
        p | | | | | | 
        
        13. Het lineair verband tussen de temperatuur [T] en de tijd [t] is telkens met tabellen
        voorgesteld.
        """,
        
        209: """
        Pagina 209 bevat de volgende opgaven:
        
        13. (vervolg)
        a. Vul de ontbrekende waarden in de tabellen aan.
        
        Tabel A:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 0 | 4 | 8 | 
        
        Tabel B:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 1 | 4 | 7 | 
        
        Tabel C:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 8 | 6 | 4 | 
        
        Tabel D:
        t (h) | 0 | 1 | 2 | 3
        T (°C) | 3 | 3 | 3 | 
        
        b. Welke tabel past bij welke formule?
        T = 4 x t
        T = 1 + (3 x t)
        T = 3
        T = 8 - (2 x t)
        
        c. Welke tabel past bij welke grafiek? [Er zijn vier grafieken getoond in het boek]
        
        d. Bij welke tabel merk je een stijgend lineair verband?
        Bij welke tabel merk je een dalend lineair verband?
        Bij welke tabel merk je een constant lineair verband?
        """,
        
        210: """
        Pagina 210 bevat de volgende opgaven:
        
        14. Het verband tussen de massa [in kilogram] en de kostprijs [in euro] is lineair.
        Vul de ontbrekende waarden in de tabel aan.
        
        a. massa | 0 | 1 | 2 | 3
           kostprijs | 0 | 3,5 | | 
        
        b. massa | 0,5 | 1 | 1,5 | 5
           kostprijs | 5 | 10 | | 
           
        c. massa | 0,1 | 0,2 | 0,5 | 1
           kostprijs | 2 | 4 | | 
           
        d. massa | 0,25 | 0,5 | 1 | 1,5
           kostprijs | | | 8 | 12
        
        15. Het verband tussen de tijd [in uur] en de kostprijs [in euro] is lineair.
        Vul de ontbrekende waarden in de tabel aan.
        
        a. tijd | 0 | 0,5 | 1 | 1,5
           kostprijs | 10 | | 60 | 
           
        b. tijd | 0 | 0,25 | 1 | 2
           kostprijs | 0 | 25 | | 
           
        c. tijd | 0 | 0,1 | 0,5 | 1
           kostprijs | 50 | | | 110
           
        d. tijd | 0 | 0,25 | 0,5 | 1
           kostprijs | 5 | | 15 | 
        """,
        
        211: """
        Pagina 211 bevat de volgende opgaven:
        
        16. Het verband tussen de tijd [in weken] en de massa [in kilogram] is lineair.
        a. Vul de ontbrekende waarden in de tabel aan.
        
        Tabel A:
        tijd | 0 | 1 | 2 | 5
        massa | 80 | 75 | | 
        
        Tabel B:
        tijd | 0 | 1 | 2,5 | 6
        massa | 50 | 48 | | 
        
        b. Welke tabel past bij welke omschrijving?
        Als de tijd met één week toeneemt, dan:
        • stijgt de massa telkens met 5 kg.
        • stijgt de massa telkens met 2 kg.
        • daalt de massa telkens met 5 kg.
        • daalt de massa telkens met 2 kg.
        
        c. Welke tabel past bij welke grafiek? [Er zijn grafieken getoond in het boek]
        
        17. Vul de tabel aan met behulp van de formules.
        a. z = 35 x t
        t | 0 | 1 | 2 | 3 | 5 | 10
        z | | | | | | 
        
        b. h = 100 - (5 x u)
        u | 0 | 1 | 2 | 3 | 5 | 20
        h | | | | | | 
        
        c. k = 7,5 + (0,5 x m)
        m | 0 | 1 | 2 | 3 | 5 | 30
        k | | | | | | 
        """,
        
        212: """
        Pagina 212 bevat de volgende opgaven:
        
        18. Stel het verband tussen het aantal drankjes en het bedrag voor met een tabel.
        Welke formule heb je gebruikt om het bedrag te berekenen? Vul aan.
        Merk je een stijgend, dalend of constant verband? Duid aan.
        
        a. Voor één drankje betaal je op het terras van de Grote Markt € 2,40.
        
        aantal drankjes (n) | 0 | 1 | 2 | 3 | 4 | 10
        bedrag (b) in euro | | | | | | 
        
        b. Je betaalt op een feest € 8 inkom. Drankjes kosten er € 1,80.
        
        aantal drankjes (n) | 0 | 1 | 2 | 3 | 4 | 10
        bedrag (b) in euro | | | | | | 
        
        c. Je hebt € 30 bij. In de cafetaria kost een drankje € 2,10.
        
        aantal drankjes | 0 | 1 | 2 | 3 | 4 | 10
        bedrag (b) in euro | | | | | | 
        
        d. Voor € 2 extra kun je de hele avond gratis gebruik maken van het toilet.
        
        aantal toiletbezoeken | 0 | 1 | 2 | 3 | 4 | 10
        bedrag (b) in euro | | | | | | 
        """
    }
    
    # Simplified content for the remaining pages
    for page_num in range(213, 222):
        page_content[page_num] = f"""
        Pagina {page_num} bevat verschillende wiskundeopgaven over lineaire verbanden, 
        formules, tabellen en grafieken. 
        """
    
    # Add more detailed information for specific pages
    page_content[218] = """
    Pagina 218 bevat de volgende opgaven:
    
    30. Twee cilindervorming kaarsen branden gelijkmatig op.
    Het lineair verband tussen de lengte [l] in cm en de tijd [t] in uren
    van die twee kaarsen is hieronder grafisch voorgesteld.
    
    a. Welke grafiek hoort bij de dikste kaars?
    b. Waarom denk je dat?
    c. Je steekt beide kaarsen tegelijkertijd aan.
       Na hoeveel uur is de dunne kaars even hoog als de dikkere kaars?
    d. Welke formule past bij de dunste kaars?
    e. Hoelang duurt het om de dikste kaars 10 cm op te branden?
    
    31. Twee taxibedrijven berekenen hun prijs op een verschillende manier.
    Bedrijf A gebruikt de formule: prijs = € 2,50 x aantal km + € 3,10.
    Bedrijf B gebruikt de formule: prijs = € 2,30 x aantal km + € 5,50.
    
    a. Welk bedrijf is het goedkoopst voor een rit van 7 km?
    b. Je moet 20 km naar huis. Welke bedrijf kies je?
    c. Bij welk aantal gereden kilometer zijn beide bedrijven even duur?
       Maak gebruik van ICT om de oplossing te vinden.
    d. Hoeveel moet je dan betalen?
    """
    
    page_content[219] = """
    Pagina 219 bevat de volgende opgaven:
    
    32. Tuiniersbedrijf VABI rekent voor het onderhoud van een tuin € 75 plus € 3,45 per m².
    
    a. Wat kost het onderhoud van een tuin van 380 m²?
    b. Mevrouw Lesage heeft een tuin van 12 a 75 ca. Hoeveel zal ze moeten betalen?
    c. Meneer Vanhee heeft zijn tuin laten opknappen. Hij kreeg een rekening van 2.638,35 euro.
       Hoe groot is de tuin van meneer Vanhee?
    
    33. De vrachtwagen van Yasin heeft 45 liter brandstof verbruikt na 250 km.
    
    a. Hoeveel liter brandstof verbruikt de vrachtwagen om 100 km af te leggen?
    b. In de brandstoftank van de vrachtwagen kan 500 liter. Hoeveel kilometer kan Yasin daarmee rijden?
       Rond af op de eenheid.
    """
    
    return page_content

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
if "page_content_data" not in st.session_state:
    st.session_state.page_content_data = get_page_content()

# Define direct answers prompt
direct_answers_prompt = """# Wiskunde Directe Antwoorden

Je taak is om directe, beknopte antwoorden te geven op wiskundeopgaven zonder lange uitleg.

## Instructies:

1. Als de leerling "alles" typt, geef ALLEEN de ANTWOORDEN voor ALLE opgaven op de pagina.
   - GEEN uitleg, alleen de ingevulde tabellen of directe antwoorden

2. Geef alleen de antwoorden, geen uitleg of tussenstappen tenzij specifiek gevraagd

3. Voor tabellen, geef alleen de volledig ingevulde tabel zonder uitleg

4. Houd het format consistent:
   - Bij tabellen, toon alleen de volledig ingevulde tabel
   - Bij formules, geef alleen het eindresultaat
   - Bij ja/nee vragen, geef alleen het antwoord

5. Geen inleidingen, geen conclusies, alleen de directe antwoorden
"""

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
        "content": direct_answers_prompt
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
        st.session_state.current_page = None
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
        
        # Check if user is requesting a specific page in Wiskunde mode
        if st.session_state.active_chat == "Wiskunde Huiswerk Helper":
            # Check for page number in the input
            if "pagina" in user_input.lower():
                page_nums = [int(s) for s in user_input.split() if s.isdigit() and 208 <= int(s) <= 221]
                if page_nums:
                    st.session_state.current_page = page_nums[0]
            
            # Alternative detection for "maak pagina X" pattern
            if "maak" in user_input.lower() and "pagina" in user_input.lower():
                page_nums = [int(s) for s in user_input.split() if s.isdigit() and 208 <= int(s) <= 221]
                if page_nums:
                    st.session_state.current_page = page_nums[0]
            
            # Direct page number input
            if user_input.isdigit() and 208 <= int(user_input) <= 221:
                st.session_state.current_page = int(user_input)
        
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
            if st.session_state.current_page:
                page_content = st.session_state.page_content_data.get(st.session_state.current_page, f"Pagina {st.session_state.current_page} bevat diverse wiskundeopgaven.")
                
                # Check if it's "alles" command
                if user_input.lower().strip() == "alles":
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    De leerling heeft "alles" getypt voor pagina {st.session_state.current_page}. 
                    
                    BELANGRIJK: Geef ALLEEN de ANTWOORDEN voor ALLE opgaven op deze pagina zonder enige uitleg. 
                    GEEN kopjes met "Opgave X" - alleen het nummer (10a, 10b, etc.) en direct het antwoord.
                    
                    Tabellen moeten volledig zijn ingevuld, maar zonder uitleg hoe je de waarden berekend hebt.
                    """
                else:
                    # Handle page selection or specific exercise
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    De leerling werkt aan pagina {st.session_state.current_page} en vraagt: "{user_input}"
                    
                    Geef ALLEEN de antwoorden zonder uitleg. Als het om een specifieke opgave gaat, geef alleen het antwoord.
                    Als de leerling iets anders vraagt, reageer kort en vraag of ze "alles" willen typen om alle antwoorden te zien.
                    """
            else:
                # No page selected yet - extract from numeric input if possible
                if user_input.isdigit() and 208 <= int(user_input) <= 221:
                    st.session_state.current_page = int(user_input)
                    page_content = st.session_state.page_content_data.get(st.session_state.current_page, f"Pagina {st.session_state.current_page} bevat diverse wiskundeopgaven.")
                    
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    De leerling heeft pagina {st.session_state.current_page} geselecteerd. Vraag in één korte zin of ze "alles" willen zien (alle antwoorden voor deze pagina).
                    """
                else:
                    # No page selected yet
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    De leerling heeft nog geen specifieke pagina geselecteerd. Vraag om alleen een paginanummer in te typen (tussen 208-221).
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
