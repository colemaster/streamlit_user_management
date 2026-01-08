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
        
        /* Accents */
        --accent-primary: #FF5500; /* Vibrant Orange */
        --accent-glow: rgba(255, 85, 0, 0.4);
        --accent-highlight: #FF7733;
        
        /* Status Colors */
        --success: #00D16C;
        --warning: #FFB020;
        --error: #FF3333;
        
        /* Spacing */
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        
        /* 3D & Depth Effects */
        --shadow-card: 
            0 8px 16px rgba(0, 0, 0, 0.5), 
            inset 0 1px 0 rgba(255, 255, 255, 0.05); /* Deep shadow + top hi-light */
        --shadow-elevated: 
            0 12px 24px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        --shadow-button:
            0 4px 6px rgba(0,0,0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -2px 0 rgba(0, 0, 0, 0.2);
        --shadow-button-pressed:
            0 1px 2px rgba(0,0,0, 0.3),
            inset 0 2px 4px rgba(0, 0, 0, 0.2);
            
        --glass-overlay: rgba(255, 255, 255, 0.03);
        
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
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
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

    /* Advanced Glass Card with Noise Texture & 3D Lighting */
    .glass-card {
        background: linear-gradient(145deg, var(--bg-card), #0F1215); /* Subtle gradient */
        position: relative;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-card);
        padding: var(--spacing-lg);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        overflow: hidden; /* For texture containment */
    }
    
    /* Noise texture overlay */
    .glass-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
    }
    
    /* Content wrapper to sit above noise */
    .glass-card > * {
        position: relative;
        z-index: 1;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 85, 0, 0.3);
        box-shadow: 
            0 0 20px var(--accent-glow), 
            var(--shadow-elevated);
    }

    /* Custom Metric Styling within Cards */
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(180deg, #fff 0%, #aaa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }

    .metric-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--spacing-xs);
        font-weight: 500;
    }

    .metric-delta {
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 2px 6px;
        border-radius: 4px;
        background: rgba(0,0,0,0.2);
        width: fit-content;
    }
    
    .delta-up { color: var(--success); border: 1px solid rgba(0, 209, 108, 0.2); }
    .delta-down { color: var(--error); border: 1px solid rgba(255, 51, 51, 0.2); }
    .delta-neutral { color: var(--text-secondary); }

    /* 3D Buttons Override */
    div[data-testid="stButton"] button {
        background: linear-gradient(180deg, var(--bg-card-hover) 0%, var(--bg-card) 100%);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: var(--radius-sm);
        transition: all 0.1s ease; /* Faster transition for button press feel */
        font-weight: 600;
        box-shadow: var(--shadow-button);
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        padding: 0.5rem 1rem;
    }
    
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(180deg, #252A30 0%, #1A1F24 100%);
        border-color: var(--text-secondary);
        color: #fff;
        transform: translateY(-1px);
    }
    
    div[data-testid="stButton"] button:active {
        transform: translateY(1px);
        box-shadow: var(--shadow-button-pressed);
        background: var(--bg-card);
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(180deg, var(--accent-highlight) 0%, var(--accent-primary) 100%);
        border: 1px solid #CC4400; /* Darker orange border */
        color: white;
        box-shadow: 
            0 4px 12px var(--accent-glow),
            inset 0 1px 0 rgba(255,255,255,0.3), /* Top highlight */
            inset 0 -2px 0 rgba(0,0,0,0.2); /* Bottom bevel */
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 
            0 6px 16px var(--accent-glow),
            inset 0 1px 0 rgba(255,255,255,0.4),
            inset 0 -2px 0 rgba(0,0,0,0.2);
        filter: brightness(1.1);
    }
    
    div[data-testid="stButton"] button[kind="primary"]:active {
        transform: translateY(2px);
        box-shadow: 
            0 0 0 rgba(0,0,0,0),
            inset 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .status-active { background: rgba(0, 209, 108, 0.15); color: var(--success); border-color: rgba(0, 209, 108, 0.2); }
    .status-inactive { background: rgba(160, 165, 170, 0.15); color: var(--text-secondary); border-color: rgba(160, 165, 170, 0.2); }
    .status-warning { background: rgba(255, 176, 32, 0.15); color: var(--warning); border-color: rgba(255, 176, 32, 0.2); }
    .status-error { background: rgba(255, 51, 51, 0.15); color: var(--error); border-color: rgba(255, 51, 51, 0.2); }

    /* Dot indicator logic handled in Python or via ::before if strictly CSS, keeping it simple here */


    /* -------------------------------------------------------------------------- */
    /*                                 ANIMATIONS                                 */
    /* -------------------------------------------------------------------------- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-enter {
        animation: fadeIn 0.6s ease-out forwards;
    }

    /* -------------------------------------------------------------------------- */
    /*                             STREAMLIT OVERRIDES                            */
    /* -------------------------------------------------------------------------- */
    
    /* Input Fields - Deep inset look */
    div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #050608;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: var(--radius-sm);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5); /* Inner shadow for depth */
    }
    
    div[data-testid="stTextInput"] input:focus, div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
        border-color: var(--accent-primary);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5), 0 0 0 1px var(--accent-primary);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: var(--text-secondary);
        font-weight: 500;
        background: transparent !important;
        transition: color 0.2s;
    }
    
    button[data-baseweb="tab"]:hover {
        color: var(--text-primary);
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
        background: linear-gradient(90deg, #0A0C0E 0%, #111418 100%);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] h1 {
        font-size: 1.5rem !important;
        background: linear-gradient(90deg, #fff, #bbb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
"""
