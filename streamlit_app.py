import streamlit as st 
import google.generativeai as genai
import time
import os
import re
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="Wiskunde Assistant",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with animations and professional styling
st.markdown("""
<style>
    /* === FONTS === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* === BASE STYLES === */
    body {
        color: white;
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    /* === SIDEBAR STYLING === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1c24 0%, #13151c 100%);
        border-right: 1px solid rgba(42, 45, 54, 0.5);
        box-shadow: 2px 0 10px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 1.5rem;
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
    
    /* Sidebar buttons */
    .sidebar-button {
        background: linear-gradient(90deg, #3a7bd5 0%, #2b5876 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        padding: 10px 15px;
        margin: 5px 0;
        text-align: center;
        transition: all 0.3s ease;
        width: 100%;
        cursor: pointer;
        display: block;
        font-size: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .sidebar-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .sidebar-button-secondary {
        background: linear-gradient(90deg, #4b6cb7 0%, #253546 100%);
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
        padding: 10px 15px;
        background: linear-gradient(135deg, #1a1c24 0%, #13151c 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
        margin-right: 10px;
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
    }
    
    .logo-text {
        font-size: 18px;
        font-weight: 600;
        background: linear-gradient(90deg, #eef2f3, #8e9eab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
</style>

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
    
    # Pagina's 220-221 toevoegen
    page_content[220] = """
    Pagina 220 bevat de volgende opgaven:
    
    34. Als je een nieuwe diepvriezer koopt, heeft het toestel de kamertemperatuur van 20 °C aangenomen.
    Pas na het aansluiten begint de temperatuur (T) te dalen volgens de formule T = 20 - (5 x t),
    waarbij t het aantal uren voorstelt.
    
    a. Vul de tabel met het verband tussen de temperatuur en de tijd aan.
       
       tijd (t) in uur | 0 | 1 | 2 | 3 | 4
       temperatuur (T) in °C | | | | | 
    
    b. Na hoeveel uur is het vriespunt bereikt?
    
    c. Na hoeveel uur is een temperatuur van -10 °C bereikt?
    
    35. In een thermometer bestaat het gekleurde staafje uit een vloeistof.
    De hoogte (h) van de vloeistof neemt toe als de temperatuur T (in °C) stijgt.
    De hoogte van de vloeistof in cm kun je berekenen met de formule h = 3,3 + (T x 0,068).
    
    a. Wat is de hoogte van de vloeistof als het 20 °C is?
    
    b. Bij welke temperatuur is de hoogte van de vloeistof 6 cm?
    Rond af op één cijfer na de komma.
    """
    
    page_content[221] = """
    Pagina 221 bevat de volgende opgaven:
    
    36. Met een microgolfoven kun je ingevroren voeding ontdooien en opwarmen. De tijd die daarvoor nodig is,
    hangt af van de massa van het voedingsproduct.
    De tijd dat het duurt om 0,5 liter soep te ontdooien en op te warmen wordt bepaald door de formule
    T = -20 + (8 x t), waarbij t de tijd is in minuten en T de temperatuur in °C.
    
    a. Vul de tabel met het verband tussen de temperatuur en de tijd aan.
       
       tijd (t) in minuten | 0 | 1 | 2 | 3 | 4
       temperatuur (T) in °C | | | | | 
    
    b. Na hoeveel minuten en seconden is het vriespunt (0 °C) bereikt?
    
    c. Na hoeveel minuten en seconden is de soep 30 °C?
    """
    
    # Simplified content for the remaining pages
    for page_num in range(213, 220):
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
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# Define direct answers prompt
formatted_answers_prompt = """# Wiskunde Antwoorden Formatter

Je taak is om volledige antwoorden te geven op wiskundeopgaven in een duidelijke, gestructureerde format.

## Instructies:

1. Wanneer de leerling alleen een paginanummer invoert, geef automatisch ALLE antwoorden voor die pagina in het juiste format.

2. Format voor antwoorden:
   - Gebruik duidelijke kopjes zoals "Opgave 10" (met nummer)
   - De vraag kort vermelden
   - Het antwoord direct geven
   - Bij tabellen, alle waardes invullen
   - Bij berekeningen, toon basisbewerkingen maar geen lange uitleg

3. Voorbeeld van goede formattering:
   Opgave 10: Het verband tussen aantal en kostprijs
   Vraag: Vul de ontbrekende waarden in de tabel aan.

   a. 
   Aantal | 0 | 1 | 2 | 3
   Kostprijs (€) | 50 | 40 | 30 | 20

4. Gebruik een consistent format voor alle antwoorden met duidelijke scheiding tussen opgaven.

5. Geef directe, duidelijke antwoorden zonder lange toelichtingen.
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
        "content": formatted_answers_prompt
    }
}

# Voorbeeld antwoord format voor Gemini
example_answer_format = """
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

# Sidebar with improved styling
with st.sidebar:
    # Logo and Brand
    st.markdown("""
    <div class="brand-logo">
        <div class="logo-icon">📐</div>
        <div class="logo-text">Wiskunde Assistent</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom buttons instead of standard Streamlit ones
    st.markdown("""
    <button class="sidebar-button" id="new-chat-btn" onclick="window.location.reload()">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style="margin-right: 5px;">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
        </svg>
        Nieuwe Chat
    </button>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Homework sections
    st.markdown("#### 📚 Huiswerk Modules")
    
    # Wiskunde button
    if st.button("📐 Wiskunde Huiswerk", key="wiskunde_btn"):
        st.session_state.messages = []
        st.session_state.context = presets["wiskunde huiswerk"]["content"]
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Welke pagina('s) van je wiskunde werkboek wil je behandelen? (pagina 208-221)"
        })
        st.session_state.show_presets = False
        st.session_state.active_chat = "Wiskunde Huiswerk Helper"
        st.rerun()
    
    # Duits button
    if st.button("🇩🇪 Duits Deelstaten", key="duits_btn"):
        st.session_state.messages = []
        st.session_state.context = presets["duits deelstaten"]["content"]
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Wat is je deelstaat? (Bijvoorbeeld: Bayern, Hessen, Nordrhein-Westfalen)"
        })
        st.session_state.show_presets = False
        st.session_state.active_chat = "Duitse Deelstaten Referentie"
        st.rerun()
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # AI Settings
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
            "Creativiteit:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            format="%.1f"
        )

# Main chat interface
main_container = st.container()

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Initial greeting
if st.session_state.show_presets and not st.session_state.messages:
    with main_container:
        st.session_state.messages = []
        st.session_state.context = ""
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "👋 Hallo! Hoe kan ik je vandaag helpen met je huiswerk? Kies een module in het menu aan de linkerkant."
        })
        st.session_state.show_presets = False
        st.rerun()

# Display chat messages with modern styling
with main_container:
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Display thinking animation if needed
    if st.session_state.thinking:
        with st.chat_message("assistant"):
            st.markdown("""
            <div class="thinking-container">
                <div class="thinking-icon"></div>
                <span class="thinking-text">Denken</span>
                <div class="thinking-dots"><span></span><span></span><span></span></div>
            </div>
            """, unsafe_allow_html=True)

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
        
        # Check if user is requesting a specific page in Wiskunde mode
        if st.session_state.active_chat == "Wiskunde Huiswerk Helper":
            # Direct page number input - check if it's just a number
            if user_input.isdigit() and 208 <= int(user_input) <= 221:
                st.session_state.current_page = int(user_input)
            
            # Check for page number in text input
            elif "pagina" in user_input.lower():
                page_nums = [int(s) for s in user_input.split() if s.isdigit() and 208 <= int(s) <= 221]
                if page_nums:
                    st.session_state.current_page = page_nums[0]
            
            # Alternative detection for "maak pagina X" pattern
            elif "maak" in user_input.lower() and "pagina" in user_input.lower():
                page_nums = [int(s) for s in user_input.split() if s.isdigit() and 208 <= int(s) <= 221]
                if page_nums:
                    st.session_state.current_page = page_nums[0]
        
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
                
                # Als alleen een paginanummer is ingevoerd, geef automatisch alle antwoorden
                if user_input.isdigit() and 208 <= int(user_input) <= 221:
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    Format voorbeeld:
                    {example_answer_format}
                    
                    De leerling heeft pagina {st.session_state.current_page} geselecteerd. Geef alle antwoorden volgens het format voorbeeld.
                    Format belangrijk:
                    - Gebruik duidelijke kopjes met opdrachtnummers: "Opgave 10"
                    - Vermeld kort de vraag bij elke opgave
                    - Toon alle ingevulde tabellen volledig
                    - Gebruik een vergelijkbaar format als het voorbeeld
                    
                    Geef nu alle volledige antwoorden voor pagina {st.session_state.current_page}.
                    """
                # Anders, gewoon de specifieke vraag beantwoorden
                else:
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    Format voorbeeld:
                    {example_answer_format}
                    
                    De leerling werkt aan pagina {st.session_state.current_page} en vraagt: "{user_input}"
                    
                    Beantwoord deze vraag volgens het format voorbeeld. Als het een specifiek opdrachtennummer betreft, 
                    behandel dat specifieke nummer volledig.
                    """
            else:
                # No page selected yet - maar probeer het uit de input te halen
                if user_input.isdigit() and 208 <= int(user_input) <= 221:
                    st.session_state.current_page = int(user_input)
                    page_content = st.session_state.page_content_data.get(st.session_state.current_page, f"Pagina {st.session_state.current_page} bevat diverse wiskundeopgaven.")
                    
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    Paginainhoud:
                    {page_content}
                    
                    Format voorbeeld:
                    {example_answer_format}
                    
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
                    complete_prompt = f"""
                    Context informatie:
                    {st.session_state.context}
                    
                    De leerling heeft nog geen specifieke pagina geselecteerd. Vraag om alleen een paginanummer in te typen (tussen 208-221).
                    """
        else:
            complete_prompt = user_input
        
        # Turn off thinking state
        st.session_state.thinking = False
        
        # Generate AI response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Stream the response with enhanced animation
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
        
        # Turn off thinking state
        st.session_state.thinking = False
    
    # Rerun to update UI with new messages
    st.rerun()
