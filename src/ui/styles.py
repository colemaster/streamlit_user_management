def get_css():
    return """
<style>
    /* -------------------------------------------------------------------------- */
    /*                                 VARIABLES                                  */
    /* -------------------------------------------------------------------------- */
    :root {
        /* Color Palette - Dark Premium */
        --bg-dark: #0A0C0E;
        --bg-card: #14181C;
        --bg-card-hover: #1A1F24;
        --text-primary: #EDEDED;
        --text-secondary: #A0A5AA;
        --accent-primary: #FF5500; /* Vibrant Orange */
        --accent-glow: rgba(255, 85, 0, 0.4);
        --border-color: #2A3036;
        --success: #00D16C;
        --warning: #FFB020;
        --error: #FF3333;
        
        /* Spacing */
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        
        /* Effects */
        --shadow-card: 0 8px 16px rgba(0, 0, 0, 0.4);
        --shadow-glow: 0 0 20px var(--accent-glow);
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 20px;
    }

    /* -------------------------------------------------------------------------- */
    /*                                BASE RESETS                                 */
    /* -------------------------------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400&display=swap');

    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: -0.02em;
        color: var(--text-primary) !important;
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Hide standard Streamlit header/footer for cleaner look */
    header[data-testid="stHeader"] {
        background-color: transparent; 
        backdrop-filter: blur(10px);
    }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* -------------------------------------------------------------------------- */
    /*                                 COMPONENTS                                 */
    /* -------------------------------------------------------------------------- */

    /* Glass Card Standard */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-card);
        padding: var(--spacing-lg);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        backdrop-filter: blur(12px);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: var(--accent-primary);
        box-shadow: var(--shadow-glow), var(--shadow-card);
    }

    /* Custom Metric Styling within Cards */
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(120deg, #fff, #ccc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--spacing-xs);
    }

    .metric-delta {
        font-size: 0.9rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .delta-up { color: var(--success); }
    .delta-down { color: var(--error); }
    .delta-neutral { color: var(--text-secondary); }

    /* Buttons Override */
    div[data-testid="stButton"] button {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: var(--radius-sm);
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    div[data-testid="stButton"] button:hover {
        border-color: var(--accent-primary);
        color: var(--accent-primary);
        background: var(--bg-card-hover);
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: var(--accent-primary);
        border: none;
        color: white;
        box-shadow: 0 4px 12px var(--accent-glow);
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        box-shadow: 0 6px 16px var(--accent-glow);
        transform: scale(1.02);
    }

    /* -------------------------------------------------------------------------- */
    /*                                 ANIMATIONS                                 */
    /* -------------------------------------------------------------------------- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(255, 85, 0, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 85, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 85, 0, 0); }
    }

    .animate-enter {
        animation: fadeIn 0.6s ease-out forwards;
    }

    /* -------------------------------------------------------------------------- */
    /*                             STREAMLIT OVERRIDES                            */
    /* -------------------------------------------------------------------------- */
    
    /* Input Fields */
    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: var(--radius-sm);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: var(--text-secondary);
        font-weight: 500;
        background: transparent !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }
    
    /* Metrics Override */
    div[data-testid="stMetric"] {
        background-color: transparent; 
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F1215;
        border-right: 1px solid var(--border-color);
    }
</style>
"""
