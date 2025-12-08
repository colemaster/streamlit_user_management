def get_css():
    return """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    /* General App Styling */
    .stApp {
        font-family: 'Outfit', sans-serif;
        background-color: #121619;
    }
    
    /* Animated Gradient Background for Header (Optional, adds flair) */
    /*
    div[data-testid="stHeader"] {
        background: linear-gradient(90deg, #121619 0%, #1E2226 100%);
    }
    */

    /* Card-like Containers with Hover Lift */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: #1E2226;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 102, 0, 0.15); /* Orange glow */
        border-color: #FF6600; 
    }

    /* Chat Message Container */
    [data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }

    /* Avatar Styling */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #333;
        color: #fff;
        border-radius: 50%;
        border: 1px solid #444;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #FF6600;
        color: #000;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(255, 102, 0, 0.4);
    }

    /* User Message (Right Aligned) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse;
        text-align: right;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:first-child {
        background-color: #2D3238;
        color: #E0E0E0;
        padding: 1rem 1.5rem;
        border-radius: 24px 24px 4px 24px;
        margin-right: 12px;
        max-width: 75%;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        font-size: 0.95rem;
        line-height: 1.5;
        border: 1px solid #444;
    }

    /* Assistant Message (Left Aligned) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:first-child {
        background: linear-gradient(135deg, #FF6600 0%, #E35302 100%);
        color: #FFFFFF;
        padding: 1rem 1.5rem;
        border-radius: 24px 24px 24px 4px;
        margin-left: 12px;
        max-width: 75%;
        box-shadow: 0 2px 5px rgba(255, 102, 0, 0.3);
        font-size: 0.95rem;
        font-weight: 500;
        line-height: 1.5;
    }

    /* Thinking Process Styling */
    .thinking-box {
        border-left: 3px solid #FF6600;
        background-color: #1E2226;
        padding: 12px;
        margin-bottom: 16px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85em;
        color: #AAAAAA;
        font-family: monospace;
    }
    
    /* Streamlit Status Container Customization */
    [data-testid="stStatusWidget"] {
        background-color: #1E2226;
        border: 1px solid #444;
        border-radius: 8px;
    }

    /* Primary Button Pulse Animation */
    button[kind="primary"] {
        background: #FF6600 !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(255, 102, 0, 0.6);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    h4, h5, h6 {
        color: #DDDDDD !important;
    }

    /* Input Area Styling */
    .stChatInputContainer {
        padding-bottom: 1rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
"""
