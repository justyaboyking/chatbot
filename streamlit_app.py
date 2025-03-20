b) Vul au of ou in:
              - Ik h_d van chocolade.
              - Het is k_d buiten.
              - Die vr_w woont hiernaast.
              - Ze hebben een nieuwe _to gekocht.
        
        4. Hoofdletters en leestekens:
           a) Verbeter de hoofdletters en leestekens in de volgende zinnen:
              - amsterdam is de hoofdstad van nederland
              - heb je het boek de avonden van gerard reve gelezen
              - we gaan op vakantie naar frankrijk spanje en italië
              - hij vroeg hoe laat is het
           b) Plaats aanhalingstekens waar nodig:
              - Hij zei: Ik kom morgen langs.
              - Het woord tafel is een zelfstandig naamwoord.
              - Weet je nog, vroeg ze, wat we gisteren hebben afgesproken?
        
        5. Algemene spellingsregels:
           a) Schrijf de volgende woorden aan elkaar of los:
              - (hoogst)noodzakelijk
              - (warm)water(leiding)
              - (niet)roker
              - (af)wassen
           b) Enkelvoud of meervoud?
              - De commissie ___ (is/zijn) het niet eens.
              - Een aantal mensen ___ (heeft/hebben) geklaagd.
              - De groep studenten ___ (staat/staan) buiten.
              - Het team ___ (speelt/spelen) goed samen.
        """,
        
        "frans_grammatica": """
        FRANSE GRAMMATICA OEFENINGEN
        
        1. Werkwoordsvervoegingen:
           a) Vervoeg de volgende werkwoorden in de présent:
              - avoir (ik, jij, hij, wij, jullie, zij)
              - être (ik, jij, hij, wij, jullie, zij)
              - aller (ik, jij, hij, wij, jullie, zij)
              - faire (ik, jij, hij, wij, jullie, zij)
           b) Vervoeg de volgende werkwoorden in de passé composé:
              - parler (ik, jij, hij, wij, jullie, zij)
              - finir (ik, jij, hij, wij, jullie, zij)
              - venir (ik, jij, hij, wij, jullie, zij)
              - prendre (ik, jij, hij, wij, jullie, zij)
           c) Vervoeg de volgende werkwoorden in de imparfait:
              - manger (ik, jij, hij, wij, jullie, zij)
              - voir (ik, jij, hij, wij, jullie, zij)
        
        2. Lidwoorden (Articles):
           a) Vul het juiste lidwoord in (le, la, l', les, un, une, des):
              - ___ garçon
              - ___ fille
              - ___ amis
              - ___ hôtel
              - ___ sac
              - ___ livre
           b) Verander de lidwoorden in het meervoud:
              - le livre → 
              - une maison →
              - l'arbre →
           c) Gebruik de juiste samentrekking:
              - Je vais ___ (à + le) cinéma.
              - Elle parle ___ (à + les) professeurs.
              - Il vient ___ (de + le) magasin.
        
        3. Bijvoeglijke naamwoorden (Adjectifs):
           a) Schrijf de juiste vorm van het bijvoeglijk naamwoord:
              - un homme ___ (grand)
              - une femme ___ (grand)
              - des filles ___ (intelligent)
              - un livre ___ (intéressant)
              - une histoire ___ (intéressant)
           b) Plaats het bijvoeglijk naamwoord op de juiste plaats:
              - une voiture (rouge)
              - un (bon) repas
              - un ami (vieux)
              - une (belle) maison
        
        4. Voorzetsels (Prépositions):
           a) Vul het juiste voorzetsel in:
              - Je vais ___ Paris.
              - Il habite ___ France.
              - Le livre est ___ la table.
              - Elle va au cinéma ___ son ami.
              - Nous parlons ___ nos vacances.
           b) Maak zinnen met 'pour', 'par', 'avec', 'sans', 'dans':
              - Je travaille ___ gagner de l'argent.
              - Il est arrivé ___ le train.
              - Elle mange ___ ses amis.
              - Il est parti ___ dire au revoir.
              - Le livre est ___ mon sac.
        
        5. Vraagzinnen (Questions):
           a) Maak vragen met 'est-ce que':
              - Tu aimes le chocolat.
              - Il va à l'école.
              - Vous parlez français.
           b) Maak vragen met inversie:
              - Elle a un chat.
              - Ils sont français.
              - Nous allons au cinéma.
           c) Maak vragen met vraagwoorden (qui, que, quand, où, comment, pourquoi):
              - ___ est-ce que tu habites?
              - ___ est-ce que tu vas au cinéma?
              - ___ est-ce que tu fais ça?
              - ___ est-ce qui a téléphoné?
              - ___ est-ce que tu manges?
        """
    }
    
    return language_content

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemini-1.5-flash"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True
if "active_subject" not in st.session_state:
    st.session_state.active_subject = None
if "copied_message" not in st.session_state:
    st.session_state.copied_message = None
if "current_page" not in st.session_state:
    st.session_state.current_page = None
if "math_content" not in st.session_state:
    st.session_state.math_content = get_math_content()
if "physics_content" not in st.session_state:
    st.session_state.physics_content = get_physics_content()
if "chemistry_content" not in st.session_state:
    st.session_state.chemistry_content = get_chemistry_content()
if "biology_content" not in st.session_state:
    st.session_state.biology_content = get_biology_content()
if "geography_content" not in st.session_state:
    st.session_state.geography_content = get_geography_content()
if "history_content" not in st.session_state:
    st.session_state.history_content = get_history_content()
if "language_content" not in st.session_state:
    st.session_state.language_content = get_language_content()
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# Example format for math answers
math_example_answer_format = """
Opgave 10: Het verband tussen aantal en kostprijs
Vraag: Vul de ontbrekende waarden in de tabel aan, wetende dat het verband tussen het aantal en de kostprijs lineair is.

We hebben de volgende tabel:

Aantal	0	1	2	3
Kostprijs (€)	50	40	30	20

Opgave 12: Vul de tabel aan met behulp van de formules
Vraag 12a: p = 4 x z

De ingevulde tabel voor 12a is:
z	0	1	2	3	5	15
p	0	4	8	12	20	60

Vraag 12b: p = 10 + (2 x t)

De ingevulde tabel voor 12b is:
t	0	1	2	3	5	15
p	10	12	14	16	20	40

Vraag 12c: p = d x 3,14

De ingevulde tabel voor 12c is:
d	0	1	2	3	5	15
p	0	3,14	6,28	9,42	15,7	47,1
"""

# Configure Gemini API - Use environment variables for security
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"  # Fallback for testing
genai.configure(api_key=api_key)

# Helper functions
def set_subject(subject):
    """Set the active subject and context"""
    if subject not in presets:
        st.error(f"Subject {subject} not found")
        return
    
    # Clear previous messages and set new context
    st.session_state.messages = []
    st.session_state.context = presets[subject]["content"]
    st.session_state.active_subject = subject
    st.session_state.current_page = None
    
    # Welcome message from assistant based on subject
    welcome_message = presets[subject].get("welcome", f"Welkom bij de {subject.capitalize()} assistent! Hoe kan ik je vandaag helpen?")
    st.session_state.messages.append({
        "role": "assistant", 
        "content": welcome_message
    })
    st.session_state.show_welcome = False
    
    # Force rerun to update display
    st.rerun()

# Sidebar with improved styling
with st.sidebar:
    # Logo and Brand using base64 image
    st.markdown(f"""
    <div class="brand-logo">
        <div class="logo-icon" style="background-image: url('data:image/png;base64,{logo_base64}');"></div>
        <div>
            <div class="logo-text">Huiswerk Assistent</div>
            <div class="logo-slogan">Jouw slimme studiemaatje</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Subject selections with custom buttons
    st.markdown("#### 📚 Vakken")
    
    # Math button
    st.markdown(f"""
    <button class="subject-button math-button" onclick="selectSubject('wiskunde')">
        <div class="icon">{presets["wiskunde"]["icon"]}</div>
        <div class="text">Wiskunde</div>
    </button>
    
    <button class="subject-button science-button" onclick="selectSubject('natuurkunde')">
        <div class="icon">{presets["natuurkunde"]["icon"]}</div>
        <div class="text">Natuurkunde</div>
    </button>
    
    <button class="subject-button science-button" onclick="selectSubject('scheikunde')">
        <div class="icon">{presets["scheikunde"]["icon"]}</div>
        <div class="text">Scheikunde</div>
    </button>
    
    <button class="subject-button science-button" onclick="selectSubject('biologie')">
        <div class="icon">{presets["biologie"]["icon"]}</div>
        <div class="text">Biologie</div>
    </button>
    
    <button class="subject-button history-button" onclick="selectSubject('geschiedenis')">
        <div class="icon">{presets["geschiedenis"]["icon"]}</div>
        <div class="text">Geschiedenis</div>
    </button>
    
    <button class="subject-button geography-button" onclick="selectSubject('aardrijkskunde')">
        <div class="icon">{presets["aardrijkskunde"]["icon"]}</div>
        <div class="text">Aardrijkskunde</div>
    </button>
    
    <button class="subject-button german-button" onclick="selectSubject('duits')">
        <div class="icon">{presets["duits"]["icon"]}</div>
        <div class="text">Duits</div>
    </button>
    
    <button class="subject-button english-button" onclick="selectSubject('engels')">
        <div class="icon">{presets["engels"]["icon"]}</div>
        <div class="text">Engels</div>
    </button>
    
    <button class="subject-button french-button" onclick="selectSubject('frans')">
        <div class="icon">{presets["frans"]["icon"]}</div>
        <div class="text">Frans</div>
    </button>
    
    <button class="subject-button language-button" onclick="selectSubject('nederlands')">
        <div class="icon">{presets["nederlands"]["icon"]}</div>
        <div class="text">Nederlands</div>
    </button>
    """, unsafe_allow_html=True)
    
    # JavaScript for handling subject selection
    st.markdown("""
    <script>
    function selectSubject(subject) {
        // Use Streamlit callback mechanism to update the state
        const data = {
            subject: subject
        };
        
        // Fetch request to handle selection
        fetch("/?subject=" + encodeURIComponent(subject))
            .then(response => console.log("Subject selection sent"));
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Handle selection via standard Streamlit buttons as a fallback
    # These are hidden from the UI but work as an alternative mechanism
    st.markdown('<div style="display: none;">', unsafe_allow_html=True)
    for subject in presets.keys():
        if st.button(f"{subject}", key=f"btn_{subject}"):
            set_subject(subject)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # AI Settings
    with st.expander("🤖 AI Instellingen", expanded=False):
        model_options = {
            "Gemini 1.5 Flash": "gemini-1.5-flash",
            "Gemini 1.5 Pro": "gemini-1.5-pro",
            "Gemini 1.0 Pro": "gemini-1.0-pro"
        }
        
        selected_model = st.selectbox(
            "AI Model:",
            options=list(model_options.keys()),
            index=list(model_options.values()).index(st.session_state.model_name) if st.session_state.model_name in list(model_options.values()) else 0
        )
        st.session_state.model_name = model_options[selected_model]
        
        st.session_state.temperature = st.slider(
            "Creativiteit:",
            min_value=0.0,
            max_width=1.0,
            value=st.session_state.temperature,
            step=0.1,
            format="%.1f"
        )

    # Custom button to reset everything
    st.markdown("""
    <button class="subject-button" style="background: linear-gradient(90deg, rgba(180, 58, 58, 0.2) 0%, rgba(100, 30, 30, 0.2) 100%); border-color: rgba(180, 58, 58, 0.3);" onclick="window.location.reload()">
        <div class="icon" style="background: linear-gradient(135deg, #cb2d3e, #ef473a);">🔄</div>
        <div class="text">Nieuwe Sessie</div>
    </button>
    """, unsafe_allow_html=True)

# Main chat interface
main_container = st.container()

# Welcome screen
if st.session_state.show_welcome and not st.session_state.messages:
    with main_container:
        st.markdown("""
        <div class="welcome-container">
            <h1 class="welcome-title">Welkom bij de Huiswerk Assistent!</h1>
            <p class="welcome-subtitle">Je persoonlijke AI-assistent die je helpt met al je huiswerk. Kies een vak om te beginnen of stel direct een vraag.</p>
            
            <div style="width: 250px; height: 250px; margin: 20px 0;">
        """, unsafe_allow_html=True)
        
        # Display welcome animation
        if welcome_animation:
            st_lottie(welcome_animation, height=250, key="welcome")
        
        st.markdown("""
            </div>
            
            <div class="subject-cards">
                <div class="subject-card" onclick="selectSubject('wiskunde')">
                    <div class="icon" style="background: linear-gradient(135deg, #3a7bd5, #3a6073);">📐</div>
                    <div class="name">Wiskunde</div>
                    <div class="description">Algebra, meetkunde, tabellen en grafieken</div>
                </div>
                
                <div class="subject-card" onclick="selectSubject('natuurkunde')">
                    <div class="icon" style="background: linear-gradient(135deg, #11998e, #38ef7d);">⚛️</div>
                    <div class="name">Natuurkunde</div>
                    <div class="description">Formules, krachten en beweging</div>
                </div>
                
                <div class="subject-card" onclick="selectSubject('engels')">
                    <div class="icon" style="background: linear-gradient(135deg, #8E2DE2, #4A00E0);">🇬🇧</div>
                    <div class="name">Engels</div>
                    <div class="description">Grammatica, woordenschat en literatuur</div>
                </div>
                
                <div class="subject-card" onclick="selectSubject('geschiedenis')">
                    <div class="icon" style="background: linear-gradient(135deg, #614385, #516395);">📜</div>
                    <div class="name">Geschiedenis</div>
                    <div class="description">Tijdlijnen, gebeurtenissen en figuren</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # Display chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    with main_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Display thinking animation if needed
        if st.session_state.thinking:
            with st.chat_message("assistant"):
                col1, col2 = st.columns([1, 5])
                with col1:
                    if thinking_animation:
                        st_lottie(thinking_animation, height=70, key="thinking")
                with col2:
                    st.markdown("""
                    <div style="margin-top: 15px;">
                        <span class="thinking-text">Even nadenken</span>
                        <div class="thinking-dots"><span></span><span></span><span></span></div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Chat input
prompt = st.chat_input("Typ je vraag hier...")
if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # If no subject is active yet, try to determine from the prompt
    if not st.session_state.active_subject:
        # Basic subject detection
        subject_keywords = {
            "wiskunde": ["wiskunde", "rekenen", "formule", "vergelijking", "grafiek", "tabel"],
            "natuurkunde": ["natuurkunde", "fysica", "kracht", "energie", "beweging", "elektriciteit"],
            "scheikunde": ["scheikunde", "chemie", "reactie", "element", "stof", "zuur", "base"],
            "biologie": ["biologie", "cel", "organisme", "plant", "dier", "ecosysteem"],
            "geschiedenis": ["geschiedenis", "historie", "oorlog", "middeleeuwen", "tijdperk"],
            "aardrijkskunde": ["aardrijkskunde", "geografie", "klimaat", "landschap", "continent"],
            "duits": ["duits", "deutsch", "duitsland", "german"],
            "engels": ["engels", "english", "britain", "grammar"],
            "frans": ["frans", "france", "français"],
            "nederlands": ["nederlands", "dutch", "taal", "grammatica", "spelling"]
        }
        
        # Check for matches
        best_match = None
        max_matches = 0
        
        for subject, keywords in subject_keywords.items():
            matches = sum(1 for keyword in keywords if keyword.lower() in prompt.lower())
            if matches > max_matches:
                max_matches = matches
                best_match = subject
        
        # If we found a good match, set it as the active subject
        if max_matches > 0:
            set_subject(best_match)
        else:
            # Default to general help
            set_subject("wiskunde")  # Default to math for now
    
    # Set thinking state to true
    st.session_state.thinking = True
    
    # Show user message immediately
    st.rerun()

# Handle AI response generation (after rerun with user message visible)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user" and st.session_state.thinking:
    user_input = st.session_state.messages[-1]["content"]
    
    try:
        # Configure the model
        model = genai.GenerativeModel(
            st.session_state.model_name,
            generation_config={"temperature": st.session_state.temperature}
        )
        
        # Check if user is requesting specific content based on the active subject
        subject_specific_prompt = user_input
        
        if st.session_state.active_subject == "wiskunde":
            # Check for page number in math queries
            if user_input.isdigit() and 208 <= int(user_input) <= 221:
                st.session_state.current_page = int(user_input)
            
            elif "pagina" in user_input.lower():
                page_nums = [int(s) for s in user_input.split() if s.isdigit() and 208 <= int(s) <= 221]
                if page_nums:
                    st.session_state.current_page = page_nums[0]
            
            # Prepare math-specific prompt
            if st.session_state.current_page:
                page_content = st.session_state.math_content.get(st.session_state.current_page, 
                                f"Pagina {st.session_state.current_page} bevat diverse wiskundeopgaven.")
                
                # If only a page number is entered, give all answers
                if user_input.isdigit() and 208 <= int(user_input) <= 221:
                    subject_specific_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    Format voorbeeld:
                    {math_example_answer_format}
                    
                    De leerling heeft pagina {st.session_state.current_page} geselecteerd. Geef alle antwoorden volgens het format voorbeeld.
                    Format belangrijk:
                    - Gebruik duidelijke kopjes met opdrachtnummers: "Opgave 10"
                    - Vermeld kort de vraag bij elke opgave
                    - Toon alle ingevulde tabellen volledig
                    - Gebruik een vergelijkbaar format als het voorbeeld
                    
                    Geef nu alle volledige antwoorden voor pagina {st.session_state.current_page}.
                    """
                # Otherwise, answer the specific question
                else:
                    subject_specific_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    Format voorbeeld:
                    {math_example_answer_format}
                    
                    De leerling werkt aan pagina {st.session_state.current_page} en vraagt: "{user_input}"
                    
                    Beantwoord deze vraag volgens het format voorbeeld. Als het een specifiek opdrachtennummer betreft, 
                    behandel dat specifieke nummer volledig.
                    """
            else:
                # No page selected yet
                if user_input.isdigit() and 208 <= int(user_input) <= 221:
                    st.session_state.current_page = int(user_input)
                    page_content = st.session_state.math_content.get(st.session_state.current_page, 
                                    f"Pagina {st.session_state.current_page} bevat diverse wiskundeopgaven.")
                    
                    subject_specific_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    Format voorbeeld:
                    {math_example_answer_format}
                    
                    De leerling heeft pagina {st.session_state.current_page} geselecteerd. Geef alle antwoorden volgens het format voorbeeld.
                    Format belangrijk:
                    - Gebruik duidelijke kopjes met opdrachtnummers: "Opgave 10"
                    - Vermeld kort de vraag bij elke opgave
                    - Toon alle ingevulde tabellen volledig
                    - Gebruik een vergelijkbaar format als het voorbeeld
                    
                    Geef nu alle volledige antwoorden voor pagina {st.session_state.current_page}.
                    """
                else:
                    # No page selected yet
                    subject_specific_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    De leerling heeft gevraagd: "{user_input}"
                    Geef een behulpzaam antwoord. Als dit een wiskundevraag is over een specifiek onderwerp, leg het stap voor stap uit.
                    Als de leerling een paginanummer noemt (tussen 208-221), geef dan aan dat ze alleen het paginanummer kunnen invoeren
                    om alle antwoorden voor die pagina te krijgen.
                    """
        
        elif st.session_state.active_subject == "natuurkunde":
            # Check for specific physics topic
            physics_topics = ["beweging", "elektriciteit", "optica"]
            topic_match = next((topic for topic in physics_topics if topic.lower() in user_input.lower()), None)
            
            if topic_match:
                topic_content = st.session_state.physics_content.get(topic_match, "")
                subject_specific_prompt = f"""
                Context informatie:
                {st.session_state.context}
                
                De leerling vraagt over {topic_match}. Hier is de relevante inhoud:
                {topic_content}
                
                De leerling vraagt specifiek: "{user_input}"
                Beantwoord deze vraag met een duidelijke uitleg en stap-voor-stap oplossing als het een probleem betreft.
                """
            else:
                # General physics question
                subject_specific_prompt = f"""
                Context informatie:
                {st.session_state.context}
                
                De leerling vraagt: "{user_input}"
                Geef een behulpzaam antwoord met een duidelijke uitleg over dit natuurkundige concept of probleem.
                Zorg voor een gestructureerde aanpak met, indien van toepassing, de benodigde formules, een stap-voor-stap oplossing,
                en een duidelijke conclusie met de juiste eenheden.
                """
        
        elif st.session_state.active_subject == "duits":
            # Handle German states/regions
            subject_specific_prompt = f"""
            Context informatie:
            {st.session_state.context}
            
            Op basis van bovenstaande context, geef informatie over het volgende onderwerp: "{user_input}".
            Als dit een Duitse deelstaat is, volg precies de structuur uit de context. Als dit een algemene vraag is
            over Duitsland of de Duitse taal, geef een behulpzaam antwoord.
            
            1. Gebruik precies de secties zoals aangegeven in de context als dit een Duitse deelstaat betreft
            2. Zet elke sectie en item op een nieuwe regel met een lege regel ertussen
            3. Geef informatie in zowel Nederlands als Duits waar mogelijk
            4. Zorg dat elke sectie apart en duidelijk leesbaar is
            """
        else:
            # General context-based prompt for other subjects
            subject_specific_prompt = f"""
            Context informatie:
            {st.session_state.context}
            
            De leerling vraagt: "{user_input}"
            Beantwoord deze vraag op basis van de context en je kennis over {st.session_state.active_subject}.
            Geef een duidelijk en gestructureerd antwoord dat de leerling helpt om het onderwerp beter te begrijpen.
            """
        
        # Turn off thinking state
        st.session_state.thinking = False
        
        # Generate AI response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response with enhanced animation
            for response in model.generate_content(
                subject_specific_prompt,
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
        
        # Turn off thinking state
        st.session_state.thinking = False
    
    # Rerun to update UI with new messages
    st.rerun()

# Add custom JavaScript for copy functionality and UI enhancements
st.markdown("""
<!-- Copy Success Notification (Hidden by default) -->
<div id="copySuccess" class="copy-success" style="display: none;">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 8px;">
        <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>
    </svg>
    Tekst gekopieerd!
</div>

<!-- Clipboard.js for better copy functionality -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>

<!-- Custom JavaScript for copy functionality and animations -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Initialize clipboard functionality for all copy buttons
    const clipboard = new ClipboardJS('.copy-btn');
    
    clipboard.on('success', function() {
        const successEl = document.getElementById('copySuccess');
        successEl.style.display = 'flex';
        
        // Hide the notification after 2 seconds
        setTimeout(function() {
            successEl.style.display = 'none';
        }, 2500);
    });
    
    // Function to create copy buttons for each message
    function addCopyButtons() {
        const messages = document.querySelectorAll('[data-testid="stChatMessage"]');
        
        messages.forEach((message, index) => {
            // Only add if button doesn't already exist
            if (!message.querySelector('.copy-button')) {
                const content = message.textContent;
                
                // Create button
                const btn = document.createElement('button');
                btn.className = 'copy-button copy-btn';
                btn.setAttribute('data-clipboard-text', content);
                
                // Add SVG icon
                btn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                        <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                    </svg>
                    Kopiëren
                `;
                
                // Add button to message
                message.appendChild(btn);
            }
        });
    }
    
    // Add copy buttons initially and when messages change
    addCopyButtons();
    
    // Check for new messages every second
    setInterval(addCopyButtons, 1000);
    
    // Handle subject selection through URL parameter
    function handleSubjectSelection() {
        const urlParams = new URLSearchParams(window.location.search);
        const subject = urlParams.get('subject');
        
        if (subject) {
            // Find and click the corresponding hidden button
            const subjectButton = document.querySelector(`button[key="btn_${subject}"]`);
            if (subjectButton) {
                subjectButton.click();
            }
            
            // Clean up URL after processing
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }
    
    // Try to handle subject selection from URL parameters
    handleSubjectSelection();
});
</script>

<div class="watermark">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="2" y1="12" x2="22" y2="12"></line>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg>
    Gemaakt door Zakaria
</div>
""", unsafe_allow_html=True)

# Process query parameters from URL for subject selection
query_params = st.experimental_get_query_params()
if "subject" in query_params and query_params["subject"][0] in presets:
    selected_subject = query_params["subject"][0]
    set_subject(selected_subject)
    # Remove query parameter to avoid reloading with the same subject
    st.experimental_set_query_params()

# Handle URL parameter for direct page access in Math
if "page" in query_params and query_params["page"][0].isdigit():
    try:
        page_num = int(query_params["page"][0])
        if 208 <= page_num <= 221:
            st.session_state.current_page = page_num
            if st.session_state.active_subject != "wiskunde":
                set_subject("wiskunde")
            # Add a message to request the page
            st.session_state.messages.append({"role": "user", "content": str(page_num)})
            st.session_state.thinking = True
            st.rerun()
    except ValueError:
        pass
    # Remove query parameter to avoid reloading
    st.experimental_set_query_params()

# Random motivational quotes to display occasionally
motivational_quotes = [
    ""Succes is geen toeval. Het is hard werken, volharding, leren, studeren, opoffering en vooral, liefde voor wat je doet." — Pelé",
    ""Het geheim van vooruitgang is om te beginnen." — Mark Twain",
    ""De beste manier om te leren is door te doen." — Albert Einstein",
    ""De toekomst hangt af van wat je vandaag doet." — Mahatma Gandhi",
    ""Onderwijs is het machtigste wapen dat je kunt gebruiken om de wereld te veranderen." — Nelson Mandela",
    ""Het is nooit te laat om te worden wat je had kunnen zijn." — George Eliot",
    ""De weg naar succes en de weg naar mislukking zijn bijna exact hetzelfde." — Colin R. Davis",
    ""Ik heb geen speciaal talent. Ik ben slechts gepassioneerd nieuwsgierig." — Albert Einstein",
    ""Het begin is het belangrijkste deel van het werk." — Plato",
    ""Je mist 100% van de schoten die je niet neemt." — Wayne Gretzky"
]

# Randomly show a motivational quote at the bottom of the sidebar occasionally (20% chance)
if random.random() < 0.2:
    with st.sidebar:
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='font-style: italic; color: rgba(255,255,255,0.7); font-size: 14px; text-align: center; margin: 15px 0;'>{random.choice(motivational_quotes)}</p>", unsafe_allow_html=True) = """
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

def get_physics_content():
    """Returns physics problems and content"""
    physics_content = {
        "beweging": """
        BEWEGING EN KRACHT OPGAVEN
        
        1. Een auto rijdt met een constante snelheid van 72 km/h. 
           a) Hoeveel meter legt de auto af in 10 seconden?
           b) Hoeveel tijd heeft de auto nodig om 500 meter af te leggen?
        
        2. Een fietser vertrekt uit rust en bereikt een snelheid van 25 km/h in 8 seconden.
           a) Bereken de versnelling van de fietser in m/s².
           b) Welke afstand heeft de fietser afgelegd in deze 8 seconden?
        
        3. Een voorwerp wordt verticaal omhoog geworpen met een beginsnelheid van 15 m/s.
           a) Hoeveel tijd verstrijkt tot het voorwerp zijn hoogste punt bereikt?
           b) Hoe hoog komt het voorwerp?
           c) Na hoeveel tijd is het voorwerp terug op de grond?
           Verwaarloos de luchtweerstand en gebruik g = 9,81 m/s².
        
        4. Op een voorwerp met een massa van 5 kg werkt een kracht van 20 N.
           a) Bereken de versnelling van het voorwerp.
           b) Als het voorwerp start vanuit rust, wat is dan zijn snelheid na 10 seconden?
           c) Welke afstand heeft het voorwerp afgelegd na 10 seconden?
        
        5. Een blok met een massa van 2 kg glijdt over een horizontaal oppervlak met een wrijvingscoëfficiënt van 0,1.
           a) Bereken de wrijvingskracht die op het blok werkt.
           b) Als het blok een beginsnelheid heeft van 5 m/s, na hoeveel tijd komt het tot stilstand?
           c) Welke afstand heeft het blok afgelegd voordat het tot stilstand komt?
        """,
        
        "elektriciteit": """
        ELEKTRICITEIT OPGAVEN
        
        1. Een elektrisch circuit bevat een weerstand van 20 Ω. Als er een spanning van 12 V over de weerstand staat:
           a) Bereken de stroomsterkte door de weerstand.
           b) Bereken het elektrisch vermogen dat door de weerstand wordt gedissipeerd.
        
        2. Drie weerstanden van 10 Ω, 15 Ω en 30 Ω worden parallel geschakeld.
           a) Bereken de totale weerstand van deze parallelle schakeling.
           b) Als deze schakeling wordt aangesloten op een spanning van 9 V, bereken dan de totale stroomsterkte.
        
        3. Een elektrische kachel heeft een vermogen van 2000 W bij een spanning van 230 V.
           a) Bereken de stroomsterkte die door de kachel loopt.
           b) Bereken de weerstand van de kachel.
           c) Hoeveel elektrische energie verbruikt de kachel in 3 uur? Geef je antwoord in kWh.
           d) Als elektriciteit €0,25 per kWh kost, wat zijn dan de kosten voor 3 uur gebruik?
        
        4. Een batterij met een EMK (elektromotorische kracht) van 9 V en een inwendige weerstand van 0,5 Ω wordt verbonden met een externe weerstand.
           a) Als de externe weerstand 4,5 Ω is, bereken dan de stroomsterkte in het circuit.
           b) Bereken de klemspanning van de batterij.
           c) Bereken het vermogen dat door de externe weerstand wordt gedissipeerd.
        
        5. Een transformator heeft 200 windingen in de primaire spoel en 800 windingen in de secundaire spoel.
           a) Als de primaire spanning 120 V is, wat is dan de secundaire spanning?
           b) Als de stroomsterkte in de primaire spoel 2 A is, wat is dan de stroomsterkte in de secundaire spoel?
           Neem aan dat de transformator ideaal is.
        """,
        
        "optica": """
        OPTICA OPGAVEN
        
        1. Een voorwerp bevindt zich op 30 cm voor een convergerend lens met een brandpuntafstand van 10 cm.
           a) Bereken de beeldafstand.
           b) Is het beeld reëel of virtueel?
           c) Bereken de vergroting.
        
        2. Een divergerende lens heeft een brandpuntafstand van -15 cm. Een voorwerp wordt geplaatst op 10 cm voor de lens.
           a) Bereken de beeldafstand.
           b) Is het beeld rechtopstaand of omgekeerd?
           c) Bereken de vergroting.
        
        3. Een voorwerp van 5 cm hoog staat 25 cm voor een convergerend lens met brandpuntafstand 20 cm.
           a) Bereken de beeldafstand.
           b) Bereken de hoogte van het beeld.
           c) Schets de situatie en teken de belangrijkste lichtstralen.
        
        4. Een voorwerp wordt geplaatst voor een vlakke spiegel.
           a) Waar bevindt zich het beeld?
           b) Is het beeld reëel of virtueel?
           c) Wat is de vergroting?
        
        5. Een lichtstraal gaat van lucht (n=1,0) naar water (n=1,33) met een invalshoek van 45°.
           a) Bereken de brekingshoek.
           b) Bereken de kritische hoek voor de overgang van water naar lucht.
           c) Leg uit wat er gebeurt als licht vanuit water op het wateroppervlak valt met een hoek groter dan de kritische hoek.
        """
    }
    
    return physics_content

def get_chemistry_content():
    """Returns chemistry problems and content"""
    chemistry_content = {
        "stoichiometrie": """
        STOICHIOMETRIE OPGAVEN
        
        1. Bereken de molaire massa van de volgende verbindingen:
           a) Na₂SO₄
           b) Ca(OH)₂
           c) Al₂(SO₄)₃
           d) C₆H₁₂O₆
        
        2. Een oplossing bevat 25 g NaOH in 250 ml oplossing.
           a) Bereken de molariteit van deze oplossing.
           b) Hoeveel mol NaOH bevat 100 ml van deze oplossing?
           c) Hoeveel gram NaOH moet je toevoegen om de molariteit te verhogen naar 3 M?
        
        3. Beschouw de volgende reactievergelijking: 2 Al + 3 Cl₂ → 2 AlCl₃
           a) Als 5,4 g aluminium volledig reageert, hoeveel gram chloorgas is dan nodig?
           b) Hoeveel gram aluminiumchloride wordt gevormd?
           c) Als we starten met 10 g aluminium en 30 g chloor, welke stof is dan in overmaat en hoeveel blijft er over?
        
        4. Calciumcarbonaat ontleedt volgens de vergelijking: CaCO₃ → CaO + CO₂
           a) Als 25 g calciumcarbonaat ontleedt, hoeveel gram calciumoxide wordt dan gevormd?
           b) Hoeveel liter koolstofdioxide wordt gevormd bij standaardomstandigheden (1 mol gas = 22,4 L)?
        
        5. Voor de reactie: N₂ + 3H₂ → 2NH₃
           a) Hoeveel mol waterstofgas is nodig om 1 mol stikstofgas volledig te laten reageren?
           b) Als we 28 g stikstofgas laten reageren met een overmaat waterstofgas, hoeveel gram ammoniak wordt dan gevormd?
           c) Als we 10 mol N₂ en 25 mol H₂ laten reageren, wat is dan de limiterende reactant?
        """,
        
        "zuren_basen": """
        ZUREN EN BASEN OPGAVEN
        
        1. Bereken de pH van de volgende oplossingen:
           a) 0,01 M HCl
           b) 0,05 M NaOH
           c) 0,1 M CH₃COOH (azijnzuur, Ka = 1,8 × 10⁻⁵)
           d) 0,02 M NH₃ (Kb = 1,8 × 10⁻⁵)
        
        2. Een oplossing bevat 0,1 M azijnzuur (CH₃COOH, Ka = 1,8 × 10⁻⁵).
           a) Bereken de pH van deze oplossing.
           b) Bereken de concentratie van azijnzuur dat gedissocieerd is.
           c) Bereken het dissociatiepercentage.
        
        3. We mengen 25,0 ml van 0,2 M HCl met 25,0 ml van 0,1 M NaOH.
           a) Schrijf de reactievergelijking op.
           b) Bereken de pH van het resulterende mengsel.
           c) Is het mengsel zuur, neutraal of basisch?
        
        4. Een buffer wordt gemaakt door 0,1 mol azijnzuur (CH₃COOH) en 0,05 mol natriumacetaat (CH₃COONa) op te lossen tot een volume van 1,0 liter.
           a) Bereken de pH van deze bufferoplossing. (Ka van azijnzuur = 1,8 × 10⁻⁵)
           b) Wat gebeurt er met de pH als we 0,01 mol HCl toevoegen aan deze buffer?
           c) Wat gebeurt er met de pH als we 0,01 mol NaOH toevoegen aan deze buffer?
        
        5. Voor de titratie van 25,0 ml van een onbekende HCl-oplossing is 20,0 ml 0,1 M NaOH nodig om het equivalentiepunt te bereiken.
           a) Bereken de molariteit van de HCl-oplossing.
           b) Bereken de pH bij het equivalentiepunt.
           c) Schets de titratiecurve en geef aan waar het equivalentiepunt zich bevindt.
        """
    }
    
    return chemistry_content

def get_biology_content():
    """Returns biology problems and content"""
    biology_content = {
        "cellen": """
        CELLEN EN CELPROCESSEN
        
        1. Celstructuren en hun functies:
           a) Beschrijf het verschil tussen prokaryote en eukaryote cellen. Geef drie voorbeelden van elk type.
           b) Leg uit wat het verschil is tussen plantaardige en dierlijke cellen. Noem minstens drie verschillen.
           c) Welke functie hebben de volgende celorganellen?
              - Mitochondriën
              - Endoplasmatisch reticulum
              - Golgi-apparaat
              - Lysosomen
        
        2. Celcyclus en celdeling:
           a) Beschrijf de verschillende fasen van de celcyclus.
           b) Wat is het verschil tussen mitose en meiose? Wanneer vindt elk proces plaats?
           c) Leg uit waarom genetische recombinatie tijdens meiose belangrijk is voor de evolutie.
        
        3. Celenergie:
           a) Beschrijf het proces van fotosynthese. Wat zijn de grondstoffen en eindproducten?
           b) Leg het proces van celademhaling uit. Hoe verschilt dit van fermentatie?
           c) Hoe zijn fotosynthese en celademhaling met elkaar verbonden in het ecosysteem?
        
        4. Celmembraan en transport:
           a) Beschrijf de structuur van het celmembraan volgens het vloeibaar-mozaïekmodel.
           b) Leg het verschil uit tussen passief transport (diffusie, osmose) en actief transport.
           c) Wat gebeurt er met een dierlijke cel in een hypotonische, isotonische en hypertonische oplossing?
        
        5. DNA en eiwitsynthese:
           a) Beschrijf de structuur van DNA en leg uit hoe DNA-replicatie werkt.
           b) Leg het proces van transcriptie en translatie uit.
           c) Wat is het centrale dogma van de moleculaire biologie?
        """,
        
        "erfelijkheid": """
        ERFELIJKHEID EN GENETICA
        
        1. Mendelse genetica:
           a) Leg uit wat wordt bedoeld met dominante en recessieve allelen.
           b) Een plant met rode bloemen (RR) wordt gekruist met een plant met witte bloemen (rr).
              - Wat is het genotype en fenotype van de F1-generatie?
              - Als twee planten uit de F1-generatie met elkaar kruisen, wat zijn dan de mogelijke genotypen en fenotypen in de F2-generatie?
           c) Bij erwten is geel zaad (Y) dominant over groen zaad (y), en ronde vorm (R) is dominant over gerimpelde vorm (r).
              Een plant met genotype YyRr wordt gekruist met een plant met genotype yyrr. Wat zijn de mogelijke fenotypen van de nakomelingen en in welke verhouding komen ze voor?
        
        2. Niet-Mendelse overerving:
           a) Wat is het verschil tussen volledige dominantie, onvolledige dominantie en codominantie? Geef van elk een voorbeeld.
           b) Wat is geslachtsgebonden overerving? Geef een voorbeeld van een geslachtsgebonden genetische aandoening.
           c) Wat is polygene overerving? Geef een voorbeeld van een eigenschap die polygeen wordt overgeërfd.
        
        3. Stamboomanalyse:
           a) Lees de stamboom hieronder en bepaal of de ziekte dominant of recessief wordt overgeërfd.
           b) Als individu II-3 en II-4 nog een kind krijgen, wat is dan de kans dat dit kind de ziekte heeft?
           c) Als III-2 kinderen krijgt met iemand zonder de ziekte, wat is dan de kans dat hun kind de ziekte heeft?
        
        4. Moleculaire genetica:
           a) Wat is een mutatie? Beschrijf verschillende soorten mutaties en hun mogelijke effecten.
           b) Leg uit wat genetische recombinatie is en hoe dit bijdraagt aan genetische diversiteit.
           c) Wat is het verschil tussen genotype en fenotype? Hoe beïnvloedt de omgeving het fenotype?
        
        5. Moderne genetica:
           a) Wat is genetic engineering? Geef twee voorbeelden van toepassingen.
           b) Leg uit wat CRISPR-Cas9 is en hoe het wordt gebruikt in genome editing.
           c) Wat zijn de ethische overwegingen bij het gebruik van genetische modificatie bij mensen?
        """
    }
    
    return biology_content

def get_geography_content():
    """Returns geography problems and content"""
    geography_content = {
        "klimaten": """
        KLIMATEN EN VEGETATIE
        
        1. Klimaatzones:
           a) Beschrijf de belangrijkste klimaatzones volgens de Köppen-classificatie.
           b) Wat zijn de kenmerken van een tropisch regenwoudklimaat?
           c) Vergelijk het Mediterraan klimaat met het maritiem klimaat van West-Europa.
        
        2. Invloed van klimaat op vegetatie:
           a) Beschrijf de vegetatietypen die horen bij de volgende klimaten:
              - Tropisch regenwoudklimaat
              - Savanneklimaat
              - Woestijnklimaat
              - Gematigd zeeklimaat
              - Toendraklimaat
           b) Wat is een bioom? Noem vijf belangrijke biomen op aarde.
           c) Leg uit hoe hoogte boven zeeniveau de vegetatie beïnvloedt.
        
        3. Klimaatverandering:
           a) Wat zijn de belangrijkste broeikasgassen en hoe beïnvloeden ze het klimaat?
           b) Beschrijf drie gevolgen van klimaatverandering voor verschillende regio's in de wereld.
           c) Welke maatregelen kunnen landen nemen om klimaatverandering tegen te gaan?
        
        4. Weer en klimaat in Nederland:
           a) Beschrijf het klimaat van Nederland volgens de Köppen-classificatie.
           b) Welke factoren beïnvloeden het weer en klimaat in Nederland?
           c) Hoe zal klimaatverandering Nederland beïnvloeden in de komende decennia?
        
        5. Toepassingsvragen:
           a) Waarom vind je regenwouden voornamelijk rond de evenaar?
           b) Waarom hebben woestijnen vaak extreme temperatuurverschillen tussen dag en nacht?
           c) Hoe beïnvloedt de Golfstroom het klimaat van West-Europa?
        """,
        
        "landschappen": """
        LANDSCHAPPEN EN GEOMORFOLOGIE
        
        1. Endogene krachten:
           a) Beschrijf de theorie van platentektoniek en leg uit hoe deze de ligging van bergketens verklaart.
           b) Wat zijn de drie belangrijkste soorten plaatgrenzen? Geef van elk een voorbeeld.
           c) Leg het verband uit tussen vulkanisme, aardbevingen en plaattektoniek.
        
        2. Exogene krachten:
           a) Beschrijf de verschillende soorten verwering (fysisch, chemisch, biologisch) en geef van elk een voorbeeld.
           b) Wat is erosie? Beschrijf de verschillende soorten erosie en hun effecten op het landschap.
           c) Leg uit hoe een rivier het landschap vormt van bron tot monding.
        
        3. Landschapsvormen:
           a) Beschrijf de kenmerken van de volgende landschapsvormen:
              - Glaciale landschappen (fjorden, U-dalen, morenen)
              - Karstlandschappen (grotten, dolinen)
              - Kustlandschappen (kliffen, stranden, delta's)
              - Woestijnlandschappen (duinen, hamada, erg)
           b) Hoe ontstaan deze landschapsvormen?
        
        4. Nederlandse landschappen:
           a) Beschrijf de belangrijkste landschapstypen in Nederland.
           b) Wat is het verschil tussen hoge en lage Nederland? Hoe zijn deze verschillen ontstaan?
           c) Welke invloed heeft de mens gehad op het Nederlandse landschap?
        
        5. Toepassingsvragen:
           a) Waarom zijn sommige delen van Nederland onder zeeniveau?
           b) Hoe heeft de ijstijd het Nederlandse landschap gevormd?
           c) Wat zijn de gevolgen van bodemdaling in Nederland?
        """
    }
    
    return geography_content

def get_history_content():
    """Returns history problems and content"""
    history_content = {
        "middeleeuwen": """
        DE MIDDELEEUWEN (500-1500)
        
        1. Vroege Middeleeuwen (500-1000):
           a) Beschrijf de val van het West-Romeinse Rijk en de gevolgen hiervan voor Europa.
           b) Wat was de rol van de kerk in de vroege Middeleeuwen?
           c) Wie was Karel de Grote en wat was zijn betekenis voor Europa?
        
        2. Hoge Middeleeuwen (1000-1300):
           a) Beschrijf het feodale stelsel. Wat was de relatie tussen heer en vazal?
           b) Wat waren de kruistochten? Geef de oorzaken en gevolgen van de kruistochten.
           c) Hoe ontwikkelden de steden zich in deze periode?
        
        3. Late Middeleeuwen (1300-1500):
           a) Wat was de Zwarte Dood en welke gevolgen had deze pandemie voor Europa?
           b) Beschrijf de Honderdjarige Oorlog tussen Engeland en Frankrijk.
           c) Wat was de Renaissance en hoe verschilde deze van de middeleeuwse cultuur?
        
        4. Middeleeuwse samenleving:
           a) Beschrijf de drie standen in de middeleeuwse samenleving.
           b) Wat was de positie van vrouwen in de middeleeuwse samenleving?
           c) Hoe zag het dagelijks leven eruit in een middeleeuwse stad?
        
        5. Middeleeuwen in de Lage Landen:
           a) Hoe ontwikkelden de Nederlanden zich in de Middeleeuwen?
           b) Beschrijf de opkomst van de Hanzesteden en hun betekenis voor de handel.
           c) Wat was de Bourgondische tijd en welke gevolgen had deze voor de Nederlanden?
        """,
        
        "industriele_revolutie": """
        DE INDUSTRIËLE REVOLUTIE (1750-1900)
        
        1. Oorzaken en beginperiode:
           a) Wat waren de belangrijkste oorzaken van de Industriële Revolutie in Groot-Brittannië?
           b) Welke technologische uitvindingen speelden een sleutelrol in het begin van de Industriële Revolutie?
           c) Waarom begon de Industriële Revolutie juist in Groot-Brittannië?
        
        2. Economische en sociale gevolgen:
           a) Hoe veranderde de productiewijze tijdens de Industriële Revolutie?
           b) Beschrijf de leef- en werkomstandigheden van de arbeiders in de vroege fabrieken.
           c) Hoe reageerden verschillende groepen op de sociale problemen die ontstonden? (denk aan vakbonden, socialisme)
        
        3. Verspreiding en tweede fase:
           a) Hoe verspreidde de industrialisatie zich naar andere Europese landen?
           b) Wat waren de belangrijkste uitvindingen en ontwikkelingen tijdens de tweede fase van de Industriële Revolutie?
           c) Welke rol speelde het kolonialisme in de industrialisatie?
        
        4. Industrialisatie in Nederland:
           a) Wanneer en hoe vond de industrialisatie in Nederland plaats?
           b) Welke industrieën waren belangrijk in Nederland?
           c) Vergelijk de industrialisatie in Nederland met die in België en Duitsland.
        
        5. Langetermijngevolgen:
           a) Welke langetermijngevolgen had de Industriële Revolutie voor de wereldeconomie?
           b) Hoe veranderde de samenleving door de Industriële Revolutie?
           c) Welke milieuproblemen ontstonden door de industrialisatie?
        """
    }
    
    return history_content

def get_language_content():
    """Returns language exercise content"""
    language_content = {
        "engels_grammatica": """
        ENGELSE GRAMMATICA OEFENINGEN
        
        1. Tijden (Tenses):
           a) Zet de volgende zinnen in de Simple Past:
              - I go to school every day.
              - She plays tennis on Saturdays.
              - They are studying for their exam.
           b) Zet de volgende zinnen in de Present Perfect:
              - I visited Paris last year.
              - She bought a new car.
              - They went to the cinema.
           c) Maak correcte zinnen met de Present Perfect Continuous:
              - I / study / for three hours
              - She / work / since morning
              - They / play / football / all afternoon
        
        2. Voorzetsels (Prepositions):
           a) Vul het juiste voorzetsel in:
              - I'm afraid _____ spiders.
              - She's interested _____ art.
              - We arrived _____ Amsterdam _____ 9 o'clock.
              - The picture is hanging _____ the wall.
           b) Verbeter de fouten in de volgende zinnen:
              - I'm waiting since two hours.
              - She's married with a doctor.
              - We discussed about the problem.
              - He's good in mathematics.
        
        3. Voegwoorden (Conjunctions):
           a) Verbind de volgende zinnen met 'and', 'but', 'or', 'because', 'so', 'although':
              - It was raining. We went for a walk.
              - She studied hard. She failed the exam.
              - You can take the bus. You can walk.
           b) Vul het juiste voegwoord in:
              - _____ it was cold, he went swimming.
              - I'll call you _____ I arrive.
              - She won't come _____ you invite her.
        
        4. Werkwoorden (Verbs):
           a) Vul de juiste vorm van het werkwoord in:
              - If it _____ (rain) tomorrow, we'll stay at home.
              - I wish I _____ (have) more time.
              - By the time you arrive, I _____ (finish) my work.
           b) Passief (Passive Voice):
              Zet de volgende zinnen in de passieve vorm:
              - Shakespeare wrote Hamlet.
              - They are building a new shopping center.
              - Someone has stolen my bike.
        
        5. Vertaaloefeningen:
           a) Vertaal naar het Engels:
              - Ik woon al vijf jaar in Amsterdam.
              - Ze heeft gisteren haar sleutels verloren.
              - Als ik rijk was, zou ik de wereld rondreizen.
              - Tegen de tijd dat we aankomen, zal het donker zijn.
           b) Verbeter de fouten in de volgende zinnen:
              - I have seen him yesterday.
              - She don't like coffee.
              - I'm living in Amsterdam since five years.
              - If I would be rich, I would travel around the world.
        """,
        
        "nederlands_spelling": """
        NEDERLANDSE SPELLING OEFENINGEN
        
        1. Werkwoordspelling:
           a) Vul de juiste vorm in (tegenwoordige tijd):
              - Jan (lopen) elke dag naar school.
              - Zij (antwoorden) altijd vriendelijk.
              - De leraar (corrigeren) de toetsen.
              - Wij (worden) steeds beter in spelling.
           b) Vul de juiste vorm in (verleden tijd):
              - Gisteren (fietsen) ik naar het strand.
              - Vorig jaar (reizen) zij door Europa.
              - Hij (werken) hard aan zijn project.
           c) Vul de juiste vorm in (voltooid deelwoord):
              - Ik heb de hele dag (studeren).
              - Zij heeft een boek (schrijven).
              - Wij zijn naar huis (lopen).
        
        2. D's en T's:
           a) Vul d, t, dd of tt in:
              - Het har_e brood ligt op tafel.
              - De hon_ blaf_e luid.
              - Wij ha_en geen tijd meer.
              - De gespaar_e centjes zijn op.
           b) Maak van de volgende werkwoorden het voltooid deelwoord:
              - leiden
              - haten
              - branden
              - schudden
        
        3. Ei/ij en au/ou:
           a) Vul ei of ij in:
              - De tr_n was te laat.
              - Het is t_d om te gaan.
              - De kl_ne jongen speelt buiten.
              - We eten altijd om tw_lf uur.
           b) Vul au of ou in:
              - Ik h_d van chocolade.
              -import streamlit as st 
import google.generativeai as genai
import time
import os
import re
from dotenv import load_dotenv
import base64
from streamlit_lottie import st_lottie
import requests
import json
import random

# Set page config
st.set_page_config(
    page_title="Huiswerk Assistent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load Lottie animations
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animations
thinking_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_kyvyi4xz.json")
welcome_animation = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_bdsthye7.json")
success_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_4chtrppo.json")

# Custom logo base64 encoded
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF8WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDUgNzkuMTYzNDk5LCAyMDE4LzA4LzEzLTE2OjQwOjIyICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOSAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIzLTA5LTAxVDEwOjM0OjU3KzAyOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMy0wOS0wMVQxMDozNjoxNSswMjowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMy0wOS0wMVQxMDozNjoxNSswMjowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpiMzQ3YzMyNy1jMDIy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
"""

# Advanced CSS with animations and professional styling
st.markdown("""
<style>
    /* === FONTS === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');
    
    /* === BASE STYLES === */
    body {
        color: white;
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    h1, h2, h3, h4, h5 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }
    
    /* === SIDEBAR STYLING === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1c24 0%, #13151c 100%);
        border-right: 1px solid rgba(42, 45, 54, 0.5);
        box-shadow: 2px 0 10px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1rem;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
        padding: 0.5rem 0;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    
    /* Sidebar dividers */
    .sidebar-divider {
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
    }
    
    /* Subject buttons */
    .subject-button {
        display: flex;
        align-items: center;
        background: linear-gradient(90deg, rgba(77, 94, 147, 0.2) 0%, rgba(37, 49, 77, 0.2) 100%);
        border: 1px solid rgba(77, 94, 147, 0.3);
        border-radius: 8px;
        color: white;
        font-weight: 500;
        padding: 10px 15px;
        margin: 8px 0;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
        font-size: 14px;
    }
    
    .subject-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: linear-gradient(90deg, rgba(77, 94, 147, 0.4) 0%, rgba(37, 49, 77, 0.4) 100%);
    }
    
    .subject-button .icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        margin-right: 12px;
        flex-shrink: 0;
    }
    
    .subject-button .text {
        flex-grow: 1;
    }
    
    /* Subject specific styling */
    .math-button .icon {
        background: linear-gradient(135deg, #3a7bd5, #3a6073);
    }
    
    .science-button .icon {
        background: linear-gradient(135deg, #11998e, #38ef7d);
    }
    
    .language-button .icon {
        background: linear-gradient(135deg, #f46b45, #eea849);
    }
    
    .history-button .icon {
        background: linear-gradient(135deg, #614385, #516395);
    }
    
    .geography-button .icon {
        background: linear-gradient(135deg, #4CB8C4, #3CD3AD);
    }
    
    .german-button .icon {
        background: linear-gradient(135deg, #1F1C2C, #928DAB);
    }
    
    .english-button .icon {
        background: linear-gradient(135deg, #8E2DE2, #4A00E0);
    }
    
    .french-button .icon {
        background: linear-gradient(135deg, #b92b27, #1565C0);
    }
    
    /* Custom expander styling */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        margin-bottom: 1rem;
        overflow: hidden;
        background-color: rgba(20, 22, 30, 0.3);
    }
    
    [data-testid="stExpander"] > details > summary {
        padding: 1rem;
        font-weight: 600;
        display: flex;
        align-items: center;
    }
    
    [data-testid="stExpander"] > details > summary:hover {
        background-color: rgba(255,255,255,0.05);
    }
    
    [data-testid="stExpander"] > details > summary::before {
        content: "↓";
        margin-right: 0.5rem;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stExpander"] > details[open] > summary::before {
        content: "↓";
        transform: rotate(180deg);
    }
    
    [data-testid="stExpander"] > details > div {
        padding: 1rem;
        animation: fadeIn 0.3s ease;
    }
    
    /* === CHAT STYLING === */
    /* Modern chat message container */
    [data-testid="stChatMessage"] {
        background-color: #23252f;
        border-radius: 12px;
        margin: 0.9rem 0;
        padding: 1.2rem;
        border: none;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
        animation: fadeInUp 0.3s ease;
        transition: all 0.3s ease;
        border-left: 4px solid transparent;
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #2a304a;
        border-left: 4px solid #4168e4;
    }
    
    /* AI message styling */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #293042;
        border-left: 4px solid #38b6ff;
    }
    
    /* Chat message animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Fixed chat input */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 20%;
        right: 0;
        background: linear-gradient(180deg, rgba(14, 17, 23, 0) 0%, rgba(14, 17, 23, 0.95) 20%);
        backdrop-filter: blur(10px);
        padding: 1.5rem 2rem;
        border-top: none;
        z-index: 99;
    }
    
    /* Chat input field */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(35, 37, 47, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px 15px;
        font-size: 15px;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stChatInput"] textarea:focus {
        background-color: rgba(35, 37, 47, 1);
        border-color: #38b6ff;
        box-shadow: 0 0 0 2px rgba(56, 182, 255, 0.2);
    }
    
    /* Chat container spacing */
    .chat-container {
        margin-top: 20px;
        margin-bottom: 100px;
        padding: 1rem 2rem;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* === UTILITY STYLES === */
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 34, 44, 0.2);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(106, 116, 143, 0.5);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(106, 116, 143, 0.8);
    }
    
    /* Thinking animation */
    .thinking-container {
        display: flex;
        align-items: center;
        padding: 14px 18px;
        background: linear-gradient(135deg, #293042 0%, #324155 100%);
        border-radius: 12px;
        margin: 12px 0;
        width: fit-content;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #5e87f5;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(94, 135, 245, 0.3);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(94, 135, 245, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(94, 135, 245, 0);
        }
    }
    
    .thinking-icon {
        display: inline-block;
        width: 24px;
        height: 24px;
        margin-right: 12px;
        background: rgba(94, 135, 245, 0.3);
        border-radius: 50%;
        position: relative;
        animation: iconPulse 1.5s infinite;
    }
    
    @keyframes iconPulse {
        0% { transform: scale(0.95); }
        50% { transform: scale(1.05); }
        100% { transform: scale(0.95); }
    }
    
    .thinking-icon::before,
    .thinking-icon::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: rgba(94, 135, 245, 0.4);
        transform: translate(-50%, -50%);
    }
    
    .thinking-icon::after {
        width: 8px;
        height: 8px;
        background: rgba(94, 135, 245, 0.8);
    }
    
    .thinking-text {
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
        margin-right: 8px;
    }
    
    .thinking-dots {
        display: inline-block;
    }
    
    .thinking-dots span {
        animation: dot 1.4s infinite;
        animation-fill-mode: both;
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.8);
        margin-right: 4px;
    }
    
    .thinking-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .thinking-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes dot {
        0%, 80%, 100% { opacity: 0; transform: scale(0.6); }
        40% { opacity: 1; transform: scale(1); }
    }
    
    /* Copy button styling */
    .copy-button {
        background: rgba(94, 135, 245, 0.2);
        border: 1px solid rgba(94, 135, 245, 0.4);
        color: rgba(255, 255, 255, 0.9);
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-flex;
        align-items: center;
        margin-top: 10px;
    }
    
    .copy-button:hover {
        background: rgba(94, 135, 245, 0.3);
        transform: translateY(-2px);
    }
    
    .copy-button svg {
        margin-right: 5px;
        width: 14px;
        height: 14px;
    }
    
    .copy-success {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(46, 125, 50, 0.9);
        color: white;
        padding: 10px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideInRight 0.3s ease, fadeOut 0.5s ease 2s forwards;
        display: flex;
        align-items: center;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
    
    /* Brand logo */
    .brand-logo {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding: 12px;
        background: linear-gradient(135deg, #1a1c24 0%, #13151c 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .logo-icon {
        width: 40px;
        height: 40px;
        margin-right: 12px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: bold;
        background-size: cover;
        background-position: center;
    }
    
    .logo-text {
        font-size: 18px;
        font-weight: 600;
        background: linear-gradient(90deg, #eef2f3, #8e9eab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .logo-slogan {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 2px;
    }
    
    /* App watermark */
    .watermark {
        position: fixed;
        bottom: 80px;
        right: 20px;
        color: rgba(255, 255, 255, 0.4);
        font-size: 12px;
        z-index: 1000;
        pointer-events: none;
        background-color: rgba(0, 0, 0, 0.2);
        padding: 5px 10px;
        border-radius: 6px;
        backdrop-filter: blur(5px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
    }
    
    .watermark svg {
        width: 14px;
        height: 14px;
        margin-right: 5px;
        opacity: 0.7;
    }
    
    /* Welcome animation container */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 30px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(41, 48, 66, 0.7) 0%, rgba(50, 65, 85, 0.7) 100%);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .welcome-title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 16px;
        background: linear-gradient(90deg, #64b3f4, #c2e59c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 24px;
        max-width: 600px;
    }
    
    /* Subject cards for welcome screen */
    .subject-cards {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 16px;
        margin-top: 20px;
        max-width: 800px;
    }
    
    .subject-card {
        width: 130px;
        height: 160px;
        background: linear-gradient(135deg, rgba(40, 45, 60, 0.5) 0%, rgba(30, 33, 48, 0.5) 100%);
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 16px;
        transition: all 0.3s;
        border: 1px solid rgba(255, 255, 255, 0.1);
        cursor: pointer;
    }
    
    .subject-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        border-color: rgba(94, 135, 245, 0.3);
    }
    
    .subject-card .icon {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        font-size: 24px;
    }
    
    .subject-card .name {
        font-weight: 600;
        color: white;
        font-size: 14px;
        text-align: center;
    }
    
    .subject-card .description {
        color: rgba(255, 255, 255, 0.6);
        font-size: 12px;
        text-align: center;
        margin-top: 6px;
    }
