if (lastMessage.textContent.endsWith('▌') && typingSoundEnabled) {
                        // Play typing sound at random intervals
                        if (Math.random() > 0.7) {
                            typingAudio();
                        }
                    }
                }
            }
        });
    });
    
    // Observe the entire document for changes
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Add sound toggle button
    const settingsDiv = document.createElement('div');
    settingsDiv.innerHTML = `
        <div style="position: fixed; top: 60px; right: 20px; background: rgba(30, 34, 44, 0.6); border: 1px solid rgba(80, 90, 140, 0.2); backdrop-filter: blur(8px); padding: 8px 12px; border-radius: 8px; font-size: 12px; color: rgba(255,255,255,0.8); z-index: 1000; display: flex; align-items: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 5px;">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
            </svg>
            <label style="margin-right: 8px;">Sound</label>
            <label class="switch">
                <input type="checkbox" id="sound-toggle">
                <span class="slider round"></span>
            </label>
        </div>
        <style>
            /* Toggle switch styling */
            .switch {
                position: relative;
                display: inline-block;
                width: 30px;
                height: 16px;
            }
            
            .switch input {
                opacity: 0;
                width: 0;
                height: 0;
            }
            
            .slider {
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(80, 90, 140, 0.2);
                transition: .3s;
                border-radius: 16px;
            }
            
            .slider:before {
                position: absolute;
                content: "";
                height: 12px;
                width: 12px;
                left: 2px;
                bottom: 2px;
                background-color: white;
                transition: .3s;
                border-radius: 50%;
            }
            
            input:checked + .slider {
                background-color: rgba(95, 112, 219, 0.6);
            }
            
            input:checked + .slider:before {
                transform: translateX(14px);
            }
        </style>
    `;
    
    document.body.appendChild(settingsDiv);
    
    // Set up toggle functionality
    const soundToggle = document.getElementById('sound-toggle');
    if (soundToggle) {
        soundToggle.addEventListener('change', function() {
            typingSoundEnabled = this.checked;
            // Play a test sound when enabled
            if (typingSoundEnabled) {
                typingAudio();
            }
        });
    }
});
</script>
"""

st.markdown(typing_sound_effect, unsafe_allow_html=True)

# 6. Add floating particles background for extra premium feel
particles_background = """
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Create the particles container
    const particlesContainer = document.createElement('div');
    particlesContainer.id = 'particles-js';
    particlesContainer.style.position = 'fixed';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100%';
    particlesContainer.style.height = '100%';
    particlesContainer.style.zIndex = '-1';
    particlesContainer.style.opacity = '0.4';
    
    document.body.appendChild(particlesContainer);
    
    // Initialize particles
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#5f70db"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 5
                }
            },
            "opacity": {
                "value": 0.3,
                "random": true,
                "anim": {
                    "enable": true,
                    "speed": 0.5,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 3,
                "random": true,
                "anim": {
                    "enable": true,
                    "speed": 2,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#5f70db",
                "opacity": 0.2,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 0.5,
                "direction": "none",
                "random": true,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": true,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 0.6
                    }
                },
                "push": {
                    "particles_nb": 3
                }
            }
        },
        "retina_detect": true
    });
});
</script>
"""

st.markdown(particles_background, unsafe_allow_html=True)

# 7. Add onboarding tooltip help (first-time users)
onboarding_help = """
<script>
// Check if this is first time visit
if (!localStorage.getItem('hasVisitedBefore')) {
    localStorage.setItem('hasVisitedBefore', 'true');
    
    // Create onboarding tooltips
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            showOnboardingTooltips();
        }, 1500);
    });
}

function showOnboardingTooltips() {
    // Create tooltip style
    const style = document.createElement('style');
    style.textContent = `
        .tooltip {
            position: absolute;
            background: linear-gradient(140deg, rgba(95, 112, 219, 0.9), rgba(142, 84, 233, 0.9));
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 14px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            animation: tooltipPulse 2s infinite;
            max-width: 250px;
        }
        
        .tooltip::after {
            content: "";
            position: absolute;
            border-style: solid;
            border-width: 8px;
            border-color: transparent;
        }
        
        .tooltip.right::after {
            top: 50%;
            right: 100%;
            transform: translateY(-50%);
            border-right-color: rgb(95, 112, 219);
        }
        
        .tooltip.left::after {
            top: 50%;
            left: 100%;
            transform: translateY(-50%);
            border-left-color: rgb(95, 112, 219);
        }
        
        .tooltip.top::after {
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-top-color: rgb(95, 112, 219);
        }
        
        .tooltip.bottom::after {
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-bottom-color: rgb(95, 112, 219);
        }
        
        @keyframes tooltipPulse {
            0% { box-shadow: 0 0 0 0 rgba(95, 112, 219, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(95, 112, 219, 0); }
            100% { box-shadow: 0 0 0 0 rgba(95, 112, 219, 0); }
        }
        
        .tooltip-close {
            position: absolute;
            top: 5px;
            right: 5px;
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 14px;
            padding: 0;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }
        
        .tooltip-close:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    `;
    document.head.appendChild(style);
    
    // Create the tooltips
    const tooltips = [
        {
            selector: '.subject-card',
            position: 'right',
            text: 'Select a subject to get started with your homework questions'
        },
        {
            selector: '[data-testid="stChatInput"]',
            position: 'top',
            text: 'Type your homework question here to get help'
        },
        {
            selector: '.brand-logo',
            position: 'bottom',
            text: 'Welcome to Homework Pro! Your premium AI tutor for all subjects'
        }
    ];
    
    let currentTooltipIndex = 0;
    showNextTooltip();
    
    function showNextTooltip() {
        if (currentTooltipIndex >= tooltips.length) return;
        
        const tooltipInfo = tooltips[currentTooltipIndex];
        const element = document.querySelector(tooltipInfo.selector);
        
        if (element) {
            const tooltip = document.createElement('div');
            tooltip.className = `tooltip ${tooltipInfo.position}`;
            tooltip.textContent = tooltipInfo.text;
            
            // Add close button
            const closeBtn = document.createElement('button');
            closeBtn.className = 'tooltip-close';
            closeBtn.innerHTML = '×';
            closeBtn.addEventListener('click', function() {
                tooltip.remove();
                currentTooltipIndex++;
                
                // Show next tooltip after a delay
                setTimeout(showNextTooltip, 500);
            });
            tooltip.appendChild(closeBtn);
            
            // Position the tooltip
            document.body.appendChild(tooltip);
            positionTooltip(tooltip, element, tooltipInfo.position);
            
            // Auto-advance after 5 seconds
            setTimeout(function() {
                if (document.body.contains(tooltip)) {
                    tooltip.remove();
                    currentTooltipIndex++;
                    showNextTooltip();
                }
            }, 8000);
        } else {
            currentTooltipIndex++;
            showNextTooltip();
        }
    }
    
    function positionTooltip(tooltip, element, position) {
        const rect = element.getBoundingClientRect();
        
        switch (position) {
            case 'right':
                tooltip.style.left = `${rect.right + 15}px`;
                tooltip.style.top = `${rect.top + rect.height/2 - tooltip.offsetHeight/2}px`;
                break;
            case 'left':
                tooltip.style.right = `${window.innerWidth - rect.left + 15}px`;
                tooltip.style.top = `${rect.top + rect.height/2 - tooltip.offsetHeight/2}px`;
                break;
            case 'top':
                tooltip.style.bottom = `${window.innerHeight - rect.top + 15}px`;
                tooltip.style.left = `${rect.left + rect.width/2 - tooltip.offsetWidth/2}px`;
                break;
            case 'bottom':
                tooltip.style.top = `${rect.bottom + 15}px`;
                tooltip.style.left = `${rect.left + rect.width/2 - tooltip.offsetWidth/2}px`;
                break;
        }
    }
}
</script>
"""

st.markdown(onboarding_help, unsafe_allow_html=True)

# 8. Add a premium footer
premium_footer = """
<div style="position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%); background: rgba(30, 34, 44, 0.4); border: 1px solid rgba(80, 90, 140, 0.15); backdrop-filter: blur(8px); padding: 6px 14px; border-radius: 20px; font-size: 12px; color: rgba(255,255,255,0.5); z-index: 900; display: flex; align-items: center;">
    <span style="display: flex; align-items: center; margin-right: 12px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;">
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
            <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
            <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
        </svg>
        @homework.pro
    </span>
    <span style="display: flex; align-items: center; margin-right: 12px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;">
            <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
        </svg>
        @homeworkpro
    </span>
    <span style="display: flex; align-items: center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;">
            <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
        </svg>
        homeworkpro
    </span>
</div>
"""

st.markdown(premium_footer, unsafe_allow_html=True)

# 9. Add a "clear chat" button next to the input field
clear_chat_button = """
<div id="clear-chat-btn" style="position: absolute; right: -40px; top: 50%; transform: translateY(-50%); background: rgba(95, 112, 219, 0.15); border: 1px solid rgba(95, 112, 219, 0.3); border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.3s ease;">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 6h18"></path>
        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
    </svg>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Find the chat input container and append the clear button to it
    const chatInputContainer = document.querySelector('[data-testid="stChatInput"]');
    if (chatInputContainer) {
        const clearBtn = document.getElementById('clear-chat-btn');
        if (clearBtn) { // If button exists (from earlier creation)
            chatInputContainer.style.position = 'relative';
            chatInputContainer.appendChild(clearBtn);
        } else {
            // Create the button if it doesn't exist yet
            const clearBtn = document.createElement('div');
            clearBtn.id = 'clear-chat-btn';
            clearBtn.style = `position: absolute; right: -40px; top: 50%; transform: translateY(-50%); 
                            background: rgba(95, 112, 219, 0.15); border: 1px solid rgba(95, 112, 219, 0.3); 
                            border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; 
                            justify-content: center; cursor: pointer; transition: all 0.3s ease;`;
            
            clearBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                    stroke="rgba(255,255,255,0.8)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                </svg>
            `;
            
            clearBtn.addEventListener('click', function() {
                // Create a confirmation modal
                const confirmModal = document.createElement('div');
                confirmModal.style = `position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                                    background: rgba(0,0,0,0.5); backdrop-filter: blur(5px); z-index: 9999; 
                                    display: flex; align-items: center; justify-content: center;`;
                
                confirmModal.innerHTML = `
                    <div style="background: rgba(30, 34, 55, 0.95); border: 1px solid rgba(80, 90, 140, 0.3); 
                                border-radius: 12px; padding: 20px; width: 300px; text-align: center;">
                        <h3 style="margin-top: 0; color: white; font-weight: 600;">Clear conversation?</h3>
                        <p style="color: rgba(255,255,255,0.7); margin-bottom: 20px;">
                            This will delete the current conversation and start a new one.
                        </p>
                        <div style="display: flex; justify-content: center; gap: 10px;">
                            <button id="cancel-clear" style="background: rgba(255,255,255,0.1); border: none; 
                                                            padding: 8px 16px; border-radius: 8px; color: white; 
                                                            cursor: pointer;">Cancel</button>
                            <button id="confirm-clear" style="background: linear-gradient(120deg, #5f70db, #8e54e9); 
                                                            border: none; padding: 8px 16px; border-radius: 8px; 
                                                            color: white; cursor: pointer;">Clear</button>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(confirmModal);
                
                // Handle cancel
                document.getElementById('cancel-clear').addEventListener('click', function() {
                    confirmModal.remove();
                });
                
                // Handle confirm
                document.getElementById('confirm-clear').addEventListener('click', function() {
                    window.location.reload();
                });
            });
            
            chatInputContainer.style.position = 'relative';
            chatInputContainer.appendChild(clearBtn);
            
            // Add hover effect
            clearBtn.addEventListener('mouseenter', function() {
                this.style.background = 'rgba(95, 112, 219, 0.3)';
                this.style.transform = 'translateY(-50%) scale(1.1)';
            });
            
            clearBtn.addEventListener('mouseleave', function() {
                this.style.background = 'rgba(95, 112, 219, 0.15)';
                this.style.transform = 'translateY(-50%)';
            });
        }
    }
});
</script>
"""

st.markdown(clear_chat_button, unsafe_allow_html=True)
# Add these enhancements to the existing code

# 1. Add premium glass-morphism and subtle animations to the UI
additional_css = """
<style>
    /* Glassmorphism for all containers */
    [data-testid="stChatMessage"], 
    .brand-logo, 
    .subject-card, 
    .welcome-container,
    .thinking-container,
    [data-testid="stExpander"] {
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
    }
    
    /* Animated gradient background for the app */
    body::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(125deg, #080a14, #10102c, #101028, #0c071b);
        background-size: 400% 400%;
        z-index: -1;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Subtle floating animation for cards */
    .subject-card, .brand-logo {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Animated hover effects for interactive elements */
    .subject-card:hover, .premium-button:hover, .new-chat-button:hover {
        box-shadow: 0 8px 32px rgba(95, 112, 219, 0.3);
        transform: translateY(-5px) scale(1.02);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    /* Premium glow effects */
    .premium-button {
        position: relative;
    }
    
    .premium-button::after {
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(120deg, #5f70db, #8e54e9, #5f70db);
        z-index: -1;
        border-radius: 12px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .premium-button:hover::after {
        opacity: 1;
        animation: glow 1.5s linear infinite;
    }
    
    @keyframes glow {
        0% { filter: blur(4px); }
        50% { filter: blur(6px); }
        100% { filter: blur(4px); }
    }
    
    /* Polished chat message styling */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"]::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(140deg, rgba(95, 112, 219, 0.1) 0%, rgba(0, 0, 0, 0) 30%);
        pointer-events: none;
    }
    
    /* Code block styling */
    pre {
        background: rgba(30, 30, 50, 0.4) !important;
        border: 1px solid rgba(95, 112, 219, 0.3) !important;
        border-radius: 10px !important;
        padding: 1em !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        overflow-x: auto !important;
        margin: 1em 0 !important;
    }
    
    code {
        color: #a6b2ff !important;
        background: rgba(95, 112, 219, 0.1) !important;
        padding: 0.2em 0.4em !important;
        border-radius: 4px !important;
        font-size: 0.9em !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important;
    }
    
    /* Tables styling */
    table {
        border-collapse: separate !important;
        border-spacing: 0 !important;
        width: 100% !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        margin: 1em 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    thead {
        background: rgba(95, 112, 219, 0.2) !important;
    }
    
    th {
        padding: 12px 16px !important;
        text-align: left !important;
        font-weight: 600 !important;
        border-bottom: 1px solid rgba(80, 90, 140, 0.2) !important;
    }
    
    td {
        padding: 10px 16px !important;
        border-bottom: 1px solid rgba(80, 90, 140, 0.1) !important;
    }
    
    tr:last-child td {
        border-bottom: none !important;
    }
    
    /* Loading animation enhancement */
    .loading-animation {
        position: relative;
    }
    
    .loading-animation::after {
        content: "";
        position: absolute;
        bottom: -5px;
        left: 50%;
        transform: translateX(-50%);
        height: 2px;
        width: 60%;
        background: linear-gradient(90deg, rgba(95, 112, 219, 0), rgba(95, 112, 219, 0.8), rgba(95, 112, 219, 0));
        border-radius: 2px;
        animation: loadingBar 1.5s ease-in-out infinite;
    }
    
    @keyframes loadingBar {
        0% { width: 20%; opacity: 0.3; }
        50% { width: 60%; opacity: 1; }
        100% { width: 20%; opacity: 0.3; }
    }
    
    /* Premium scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 34, 44, 0.2);
        border-radius: 20px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, rgba(95, 112, 219, 0.5), rgba(142, 84, 233, 0.5));
        border-radius: 20px;
        border: 2px solid transparent;
        background-clip: content-box;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, rgba(95, 112, 219, 0.8), rgba(142, 84, 233, 0.8));
        border-radius: 20px;
        border: 2px solid transparent;
        background-clip: content-box;
    }
</style>
"""

st.markdown(additional_css, unsafe_allow_html=True)

# 2. Add keyboard shortcuts for better experience
keyboard_shortcuts = """
<script>
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + / for new conversation
    if ((event.ctrlKey || event.metaKey) && event.key === '/') {
        event.preventDefault();
        window.location.reload();
    }
    
    // Ctrl/Cmd + Enter to submit the chat input
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        const textarea = document.querySelector('[data-testid="stChatInput"] textarea');
        if (textarea && textarea.value.trim()) {
            // Find the submit button and click it
            const submitButton = document.querySelector('[data-testid="stChatInput"] button');
            if (submitButton) submitButton.click();
        }
    }
    
    // Escape to focus the chat input
    if (event.key === 'Escape') {
        event.preventDefault();
        const textarea = document.querySelector('[data-testid="stChatInput"] textarea');
        if (textarea) textarea.focus();
    }
});
</script>
"""

st.markdown(keyboard_shortcuts, unsafe_allow_html=True)

# 3. Add a shortcut hints display
shortcut_hints = """
<div style="position: fixed; bottom: 90px; right: 20px; background: rgba(30, 34, 44, 0.3); border: 1px solid rgba(80, 90, 140, 0.2); backdrop-filter: blur(8px); padding: 8px 12px; border-radius: 8px; font-size: 11px; color: rgba(255,255,255,0.6); z-index: 1000;">
    <div style="margin-bottom: 4px;">Keyboard Shortcuts:</div>
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <span style="background: rgba(255,255,255,0.1); padding: 2px 5px; border-radius: 4px; margin-right: 6px;">Ctrl+/</span>
        <span>New Chat</span>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <span style="background: rgba(255,255,255,0.1); padding: 2px 5px; border-radius: 4px; margin-right: 6px;">Ctrl+Enter</span>
        <span>Send Message</span>
    </div>
    <div style="display: flex; align-items: center;">
        <span style="background: rgba(255,255,255,0.1); padding: 2px 5px; border-radius: 4px; margin-right: 6px;">Esc</span>
        <span>Focus Input</span>
    </div>
</div>
"""

st.markdown(shortcut_hints, unsafe_allow_html=True)

# 4. Add a premium feature badge
premium_badge = """
<div style="position: fixed; top: 20px; right: 20px; background: linear-gradient(120deg, #5f70db, #8e54e9); border-radius: 20px; padding: 4px 10px; font-size: 12px; font-weight: 600; color: white; box-shadow: 0 4px 10px rgba(95, 112, 219, 0.3); display: flex; align-items: center; z-index: 1000;">
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 5px;">
        <path d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"></path>
    </svg>
    PREMIUM
</div>
"""

st.markdown(premium_badge, unsafe_allow_html=True)

# 5. Add typing sound effects (optional - user can toggle)
typing_sound_effect = """
<script>
// Typing sound effect (disabled by default)
let typingSoundEnabled = false;
let typingAudio;

function createTypingAudio() {
    // Create audio context
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    function playTypeSound() {
        if (!typingSoundEnabled) return;
        
        // Create oscillator
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        // Set properties
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(800 + Math.random() * 300, audioContext.currentTime);
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
        
        // Connect nodes
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Play sound
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.1);
    }
    
    return playTypeSound;
}

// Wait for DOM to be loaded
document.addEventListener('DOMContentLoaded', function() {
    typingAudio = createTypingAudio();
    
    // Observe for new chat messages
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                // If we're actively typing (assistant message with cursor)
                const assistantMessages = document.querySelectorAll('[data-testid="stChatMessage"][data-testid*="assistant"]');
                if (assistantMessages.length) {
                    const lastMessage = assistantMessages[assistantMessages.length - 1];
                    if (lastMessage.textContent
