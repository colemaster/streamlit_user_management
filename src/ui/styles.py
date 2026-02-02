from .brave_theme_system import BraveThemeSystem, BraveThemeConfig

def get_css():
    """Get enhanced CSS with modern features and preserved Brave Design aesthetic"""
    # Initialize the enhanced theme system
    theme_system = BraveThemeSystem()
    
    # Generate the complete enhanced CSS
    return f"""
<style>
{theme_system.generate_complete_css()}
</style>
"""

def get_legacy_css():
    """Legacy CSS function for backward compatibility"""
    return """
<style>
    /* -------------------------------------------------------------------------- */
    /*                                 VARIABLES                                  */
    /* -------------------------------------------------------------------------- */
    :root {
        /* Color Palette - Brave Dark & Orange */
        --bg-deep: #000000;
        --bg-dark: #050505;
        --bg-panel: #0E0E0E;
        --bg-glass: rgba(20, 20, 20, 0.6);
        
        --text-primary: #FFFFFF;
        --text-secondary: #888888;
        --text-orange: #FF5500;
        
        /* The Brave Orange */
        --accent-primary: #FF4500;     /* Orange Red */
        --accent-secondary: #FF8C00;   /* Dark Orange */
        --accent-glow: rgba(255, 69, 0, 0.5);
        --neon-shadow: 0 0 10px var(--accent-primary), 0 0 20px var(--accent-primary);
        
        /* Status */
        --success: #00FF9D;
        --warning: #FFD700;
        --error: #FF0055;
        
        /* 3D & Depth */
        --card-shadow: 
            0 20px 40px rgba(0,0,0,0.8),
            0 0 0 1px rgba(255,255,255,0.05) inset;
            
        --text-shadow-3d: 
            1px 1px 0px #AA2200, 
            2px 2px 0px #AA2200, 
            3px 3px 0px #AA2200;
            
        --radius-sm: 8px;
        --radius-md: 16px;
        --radius-lg: 24px;
    }

    /* -------------------------------------------------------------------------- */
    /*                                BASE RESETS                                 */
    /* -------------------------------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;600&display=swap');

    .stApp {
        background-color: var(--bg-deep);
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(255, 69, 0, 0.05) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(255, 140, 0, 0.05) 0%, transparent 20%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-primary) !important;
    }

    h1 {
        font-weight: 700;
        text-shadow: var(--text-shadow-3d);
        margin-bottom: 0.5rem;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-dark); 
    }
    ::-webkit-scrollbar-thumb {
        background: #333; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-primary); 
    }

    /* -------------------------------------------------------------------------- */
    /*                                 COMPONENTS                                 */
    /* -------------------------------------------------------------------------- */

    /* Glass Panel - The Core Card */
    .brave-card {
        background: rgba(20, 20, 20, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    /* Orange Line Top */
    .brave-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
        opacity: 0.5;
        transition: opacity 0.3s;
    }

    .brave-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 30px 60px rgba(0,0,0,0.9), 0 0 20px rgba(255,69,0,0.2);
        border-color: rgba(255, 69, 0, 0.3);
    }
    
    .brave-card:hover::before {
        opacity: 1;
    }

    /* 3D Stat */
    .stat-val {
        font-family: 'Rajdhani', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
        background: -webkit-linear-gradient(90deg, #fff, #bbb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: var(--text-secondary);
    }

    /* Buttons Override - "Standard" Streamlit buttons to look like cyber-pills */
    div[data-testid="stButton"] button {
        background: var(--bg-panel);
        border: 1px solid var(--text-secondary);
        color: var(--text-primary);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border-radius: 4px;
        transition: all 0.2s;
        box-shadow: 0 4px 0 #333; /* 3D press effect */
        width: 100%;
        margin-top: 4px;
    }

    div[data-testid="stButton"] button:hover {
        border-color: var(--accent-primary);
        color: var(--accent-primary);
        transform: translateY(-2px);
        box-shadow: 0 6px 0 var(--accent-primary), 0 0 15px var(--accent-glow);
    }
    
    div[data-testid="stButton"] button:active {
        transform: translateY(4px);
        box-shadow: 0 0 0 transparent;
    }
    
    div[data-testid="stButton"] button[kind="primary"] {
        background: var(--accent-primary);
        border-color: var(--accent-primary);
        color: #000;
        box-shadow: 0 4px 0 #cc3700;
    }
    
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #FF5500;
        color: #fff;
        box-shadow: 0 6px 0 #cc3700, 0 0 20px var(--accent-primary);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-dark);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* 3D Animations */
    @keyframes rotateIn {
        from { transform: perspective(1000px) rotateX(10deg) opacity(0); }
        to { transform: perspective(1000px) rotateX(0) opacity(1); }
    }
    
    .animate-3d {
        animation: rotateIn 0.8s ease-out forwards;
    }

    /* Input Fields */
    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #0F0F0F;
        border: 1px solid #333;
        color: #fff;
        border-radius: 4px;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 10px rgba(255,69,0,0.3);
    }


    /* 
     * METALLIC TYPOGRAPHY SYSTEM 
     * Inspired by Nano Banana 3D Styles
     */
    .metallic-title {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        background: linear-gradient(
            to bottom,
            #FFFFFF 0%,
            #CCCCCC 50%,
            #999999 51%,
            #FFFFFF 100%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        text-shadow: 
            0px 2px 0px #555,
            0px 3px 0px #444,
            0px 4px 0px #333,
            0px 5px 0px #222,
            0px 6px 5px rgba(0,0,0,0.5),
            0px 0px 20px rgba(255, 255, 255, 0.5); /* Outer Glow */
        letter-spacing: 0.05em;
        filter: drop-shadow(0 0 5px rgba(255, 69, 0, 0.4)); /* Subtle Orange Glow */
    }

    .metallic-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        background: linear-gradient(90deg, #FF4500, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 10px rgba(255, 69, 0, 0.5);
    }
</style>
"""
