import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Show title and description.
st.title("💬 Gemini Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
)

# Sidebar for context management only
with st.sidebar:
    # Hidden configurations (not shown in UI)
    gemini_api_key = "AIzaSyBry97WDtrisAkD52ZbbTShzoEUHenMX_w"  # Hardcoded
    model_name = "gemini-1.5-flash"  # Hardcoded default model
    
    # Presets section
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
    
    # Preset buttons
    preset_cols = st.columns(2)
    for idx, (preset_name, preset_content) in enumerate(presets.items()):
        col_idx = idx % 2
        with preset_cols[col_idx]:
            if st.button(preset_name):
                st.session_state.context = preset_content
                st.experimental_rerun()
    
    # Add more presets button
    with st.expander("Add Custom Preset"):
        new_preset_name = st.text_input("Preset Name")
        if st.button("Save Current Context as Preset") and new_preset_name:
            if "user_presets" not in st.session_state:
                st.session_state.user_presets = {}
            st.session_state.user_presets[new_preset_name] = st.session_state.context
            st.success(f"Preset '{new_preset_name}' saved!")
    
    # Show user presets if any
    if "user_presets" in st.session_state and st.session_state.user_presets:
        st.subheader("Your Custom Presets")
        user_preset_cols = st.columns(2)
        for idx, (preset_name, preset_content) in enumerate(st.session_state.user_presets.items()):
            col_idx = idx % 2
            with user_preset_cols[col_idx]:
                if st.button(preset_name, key=f"user_preset_{idx}"):
                    st.session_state.context = preset_content
                    st.experimental_rerun()
    
    # Just the context management section
    st.header("Context Management")
    
    # Initialize context in session state if not present
    if "context" not in st.session_state:
        st.session_state.context = ""
    
    st.text(f"Current context length: {len(st.session_state.context)} characters")
    st.session_state.context = st.text_area(
        "Add Background Information/Context",
        st.session_state.context,
        height=400,
        help="This information will be included with every prompt sent to the model."
    )
    
    # File uploader for additional context
    uploaded_file = st.file_uploader("Or Upload a Text File", type=["txt", "md", "csv", "json"])
    if uploaded_file is not None:
        try:
            file_contents = uploaded_file.read().decode("utf-8")
            file_size_kb = len(file_contents) / 1024
            st.write(f"File size: {file_size_kb:.1f} KB")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Add File Contents to Context"):
                    st.session_state.context += "\n\n" + file_contents
                    st.experimental_rerun()
            with col2:
                if st.button("Replace Context with File"):
                    st.session_state.context = file_contents
                    st.experimental_rerun()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    # Clear context button
    if st.button("Clear Context"):
        st.session_state.context = ""
        st.experimental_rerun()

# Main chat interface
if not gemini_api_key:
    st.info("Please add your Google AI API key in the sidebar to continue.", icon="🗝️")
else:
    # Configure the Gemini API
    genai.configure(api_key=gemini_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Initialize the model
            model = genai.GenerativeModel(model_name)
            
            # Create the complete prompt by combining context and the user's prompt
            complete_prompt = prompt
            if st.session_state.context:
                complete_prompt = f"""
                Context information:
                {st.session_state.context}
                
                Based on the above context, please respond to this question or request:
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
                    
                # Store the response (only storing the original prompt, not the context-enhanced one)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            st.info("Please check if your API key has access to Gemini 1.5 models.")

    # Add a button to clear the chat history
    if st.session_state.messages and st.button("Clear Conversation"):
        st.session_state.messages = []
        st.experimental_rerun()
