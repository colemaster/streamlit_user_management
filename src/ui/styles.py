def get_css():
    return """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* General App Styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Card-like Containers */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
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
        background-color: #F0F2F6;
        color: #252525;
        border-radius: 50%;
        border: 1px solid #E0E0E0;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #E35302;
        color: #ffffff;
        border-radius: 50%;
    }

    /* User Message (Right Aligned) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse;
        text-align: right;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:first-child {
        background-color: #F0F2F6;
        color: #252525;
        padding: 1rem 1.5rem;
        border-radius: 24px 24px 4px 24px;
        margin-right: 12px;
        max-width: 75%;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Assistant Message (Left Aligned) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:first-child {
        background-color: #FFF5F0; /* Very light orange tint */
        border: 1px solid #FFE0D1;
        color: #252525;
        padding: 1rem 1.5rem;
        border-radius: 24px 24px 24px 4px;
        margin-left: 12px;
        max-width: 75%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Thinking Process Styling */
    .thinking-box {
        border-left: 3px solid #E35302;
        background-color: #FAFAFA;
        padding: 12px;
        margin-bottom: 16px;
        border-radius: 0 8px 8px 0;
        font-size: 0.85em;
        color: #666666;
        font-family: monospace;
    }
    
    /* Streamlit Status Container Customization */
    [data-testid="stStatusWidget"] {
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
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
