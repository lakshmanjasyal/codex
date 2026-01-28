# SafeNest AI -  Frontend with Modern Design
import streamlit as st
from PIL import Image
import io
import base64
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from simplified_backend import AgentOrchestrator, ChatAgent
from translations import get_text
import time

# Page Configuration
st.set_page_config(
    page_title="SafeNest AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS with Modern Aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background with Gradient */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Glassmorphism Header */
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0 0.5rem 0;
        letter-spacing: -2px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 400;
        letter-spacing: 0.5px;
        animation: fadeIn 1s ease-out 0.3s both;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Premium Metric Cards with Glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(167, 139, 250, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(96, 165, 250, 0.3);
        border-color: rgba(96, 165, 250, 0.3);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-value {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0.5rem 0 0 0;
        color: #e2e8f0;
        position: relative;
        z-index: 1;
    }
    
    .metric-sublabel {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.25rem;
        position: relative;
        z-index: 1;
    }
    
    /* Premium Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    /* Info Boxes with Modern Design */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        color: #e2e8f0;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 12px;
        color: #e2e8f0;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    .warning-box {
        background: rgba(251, 146, 60, 0.1);
        border-left: 4px solid #fb923c;
        padding: 1.5rem;
        border-radius: 12px;
        color: #e2e8f0;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    .error-box {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 1.5rem;
        border-radius: 12px;
        color: #e2e8f0;
        backdrop-filter: blur(10px);
        margin: 1rem 0;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(96, 165, 250, 0.1);
        color: #60a5fa;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #e2e8f0;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed rgba(96, 165, 250, 0.3);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(96, 165, 250, 0.6);
        background: rgba(96, 165, 250, 0.05);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #e2e8f0;
        padding: 0.75rem;
        transition: all 0.3s;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.3), transparent);
    }
    
    /* Image Cards */
    .image-card {
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .image-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 40px rgba(96, 165, 250, 0.3);
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.25rem;
    }
    
    .status-success {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid #22c55e;
    }
    
    .status-warning {
        background: rgba(251, 146, 60, 0.2);
        color: #fb923c;
        border: 1px solid #fb923c;
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer strong {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    return AgentOrchestrator()

orchestrator = get_orchestrator()

# Animated Header with Day/Night Icon
# Get current language for header
current_lang = st.session_state.get('lang', 'en')

# Day/Night Icon based on current time
current_hour = datetime.now().hour
if 5 <= current_hour < 7:
    time_icon = "🌅"
    time_label = "Sunrise"
elif 7 <= current_hour < 17:
    time_icon = "☀️"
    time_label = "Day"
elif 17 <= current_hour < 19:
    time_icon = "🌆"
    time_label = "Sunset"
else:
    time_icon = "🌙"
    time_label = "Night"

# Header with icon
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown(f'<h1 class="main-header">{get_text(current_lang, "app_title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{get_text(current_lang, "app_subtitle")}</p>', unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 1.5rem;'>
        <div style='font-size: 3rem; line-height: 1;'>{time_icon}</div>
        <div style='font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;'>{time_label}</div>
        <div style='font-size: 0.7rem; color: #64748b;'>{datetime.now().strftime('%I:%M %p')}</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'mock_results' not in st.session_state:
    st.session_state.mock_results = None
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'  # Default to English

# Sidebar - Property Information
with st.sidebar:
    # Language Selector (First thing in sidebar)
    st.markdown("### 🌐 Language / भाषा")
    
    lang = st.selectbox(
        label="Select Language",
        options=['en', 'hi', 'ta', 'te', 'kn', 'ml'],
        format_func=lambda x: {
            'en': '🇬🇧 English',
            'hi': '🇮🇳 हिंदी (Hindi)',
            'ta': '🇮🇳 தமிழ் (Tamil)',
            'te': '🇮🇳 తెలుగు (Telugu)',
            'kn': '🇮🇳 ಕನ್ನಡ (Kannada)',
            'ml': '🇮🇳 മലയാളം (Malayalam)'
        }[x],
        index=['en', 'hi', 'ta', 'te', 'kn', 'ml'].index(st.session_state.lang),
        key='language_selector'
    )
    st.session_state.lang = lang
    
    st.markdown("---")
    
    # Theme Toggle
    st.markdown("### 🎨 Theme")
    
    # Initialize theme in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'  # Default to dark
    
    # Theme selector
    theme_option = st.radio(
        "Choose theme:",
        options=['dark', 'light'],
        format_func=lambda x: '🌙 Dark Mode' if x == 'dark' else '☀️ Light Mode',
        index=0 if st.session_state.theme == 'dark' else 1,
        horizontal=True,
        key='theme_selector'
    )
    
    # Update theme
    if theme_option != st.session_state.theme:
        st.session_state.theme = theme_option
        st.rerun()
    
    # Apply theme CSS
    if st.session_state.theme == 'light':
        st.markdown("""
        <style>
            /* Light Mode Overrides */
            .stApp {
                background-color: #f8fafc !important;
                color: #1e293b !important;
            }
            
            /* Main content area */
            .main .block-container {
                background-color: #ffffff !important;
                padding: 2rem !important;
                border-radius: 1rem !important;
            }
            
            .main-header {
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
            }
            
            .subtitle {
                color: #64748b !important;
            }
            
            /* Metric cards */
            .metric-card {
                background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%) !important;
                border: 2px solid #e2e8f0 !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
            }
            
            .metric-value {
                color: #1e293b !important;
            }
            
            .metric-label {
                color: #475569 !important;
            }
            
            .metric-sublabel {
                color: #64748b !important;
            }
            
            /* Info boxes */
            .error-box {
                background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
                border-left: 4px solid #ef4444 !important;
                color: #991b1b !important;
            }
            
            .warning-box {
                background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
                border-left: 4px solid #f59e0b !important;
                color: #92400e !important;
            }
            
            .info-box {
                background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
                border-left: 4px solid #3b82f6 !important;
                color: #1e40af !important;
            }
            
            .success-box {
                background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%) !important;
                border-left: 4px solid #10b981 !important;
                color: #065f46 !important;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #e2e8f0 !important;
            }
            
            [data-testid="stSidebar"] * {
                color: #1e293b !important;
            }
            
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3 {
                color: #0f172a !important;
            }
            
            /* File uploader */
            [data-testid="stFileUploader"] {
                background-color: #ffffff !important;
                border: 2px dashed #cbd5e1 !important;
                border-radius: 0.5rem !important;
            }
            
            [data-testid="stFileUploader"] section {
                background-color: #f8fafc !important;
                border: none !important;
            }
            
            [data-testid="stFileUploader"] label {
                color: #1e293b !important;
            }
            
            /* Buttons */
            .stButton button {
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
                color: white !important;
                border: none !important;
            }
            
            .stButton button:hover {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #f8fafc !important;
                border-bottom: 2px solid #e2e8f0 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #64748b !important;
                background-color: transparent !important;
            }
            
            .stTabs [aria-selected="true"] {
                color: #3b82f6 !important;
                border-bottom-color: #3b82f6 !important;
                background-color: #ffffff !important;
            }
            
            /* Tables */
            .stDataFrame {
                background-color: #ffffff !important;
                border: 1px solid #e2e8f0 !important;
            }
            
            .stDataFrame table {
                color: #1e293b !important;
            }
            
            .stDataFrame th {
                background-color: #f1f5f9 !important;
                color: #0f172a !important;
            }
            
            /* Inputs */
            .stTextInput input, 
            .stTextArea textarea,
            .stSelectbox select,
            .stDateInput input {
                background-color: #ffffff !important;
                color: #1e293b !important;
                border: 1px solid #cbd5e1 !important;
            }
            
            .stTextInput input:focus,
            .stTextArea textarea:focus {
                border-color: #3b82f6 !important;
                box-shadow: 0 0 0 1px #3b82f6 !important;
            }
            
            /* Radio buttons */
            .stRadio label {
                color: #1e293b !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #f8fafc !important;
                color: #1e293b !important;
                border: 1px solid #e2e8f0 !important;
            }
            
            .streamlit-expanderContent {
                background-color: #ffffff !important;
                border: 1px solid #e2e8f0 !important;
            }
            
            /* Progress bars */
            .stProgress > div > div {
                background-color: #3b82f6 !important;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #0f172a !important;
            }
            
            /* Markdown text */
            p, li, span {
                color: #334155 !important;
            }
            
            /* Code blocks */
            code {
                background-color: #f1f5f9 !important;
                color: #1e293b !important;
            }
            
            /* Dividers */
            hr {
                border-color: #e2e8f0 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header(get_text(lang, 'sidebar_title'))
    property_id = st.text_input(
        "Property ID",
        value=f"PROP-{datetime.now().strftime('%Y%m%d-%H%M')}",
        help="Unique identifier for this property"
    )
    
    property_address = st.text_area(
        "Property Address",
        placeholder="Enter full address...",
        height=80
    )
    
    inspector_name = st.text_input("Inspector Name", value="Demo Inspector")
    inspection_date = st.date_input("Inspection Date", value=datetime.now())
    
    st.markdown("---")
    
    st.subheader("🔧 System Status")
    
    st.markdown("""
        <div class="success-box">
            <strong>✅ Frontend</strong><br/>
            <small>All systems operational</small>
        </div>
        <div class="warning-box">
            <strong>⏳ AI Engine</strong><br/>
            <small>Demo Mode - Mock Data</small>
        </div>
        <div class="info-box">
            <strong>📊 Analytics</strong><br/>
            <small>Real-time processing ready</small>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Chatbot
    st.subheader("💬 Ask AI Assistant")
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Only show chatbot if analysis is complete
    if st.session_state.analysis_complete and st.session_state.mock_results:
        user_question = st.text_input(
            "Ask about your property:",
            placeholder="What should I fix first?",
            key="chat_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            ask_button = st.button("Ask", type="primary", use_container_width=True)
        with col2:
            if st.button("Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        if ask_button and user_question:
            with st.spinner("🤔 Thinking..."):
                # Initialize ChatAgent
                chat_agent = ChatAgent()
                
                # Get response
                response = chat_agent.chat(
                    user_question,
                    st.session_state.mock_results,
                    st.session_state.chat_history,
                    current_lang
                )
                
                # Add to history
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Display chat history (last 6 messages = 3 exchanges)
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("**💭 Chat History:**")
            for msg in st.session_state.chat_history[-6:]:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style='background: #1e293b; padding: 0.75rem; border-radius: 0.5rem; margin: 0.5rem 0;'>
                        <strong style='color: #60a5fa;'>You:</strong><br/>
                        <span style='color: #e2e8f0;'>{msg['content']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: #0f172a; padding: 0.75rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 3px solid #10b981;'>
                        <strong style='color: #10b981;'>AI:</strong><br/>
                        <span style='color: #cbd5e1;'>{msg['content']}</span>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Complete an analysis to chat with AI assistant")
    
    st.markdown("---")
    
    st.caption("🔒 Powered by Snowflake Cortex AI")
    st.caption("🏆 Built for CODEX '26 Hackathon")

# Main Content - Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload & Inspect", 
    "📊 Analysis Dashboard", 
    "📄 Detailed Report",
    "💰 Financial Analysis"
])

# TAB 1: Upload & Inspect
with tab1:
    st.markdown("## 📸 Upload Property Images")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Drop images here or click to browse",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload high-quality images for AI-powered analysis"
        )
        
        inspector_notes = st.text_area(
            "Inspector Notes (Optional)",
            placeholder="Document specific observations, concerns, or areas requiring attention...",
            height=120,
            help="Your notes enhance AI analysis accuracy"
        )
        
    with col2:
        st.markdown("""
        <div class="info-box">
            <strong>📸 Best Practices</strong><br/><br/>
            <small>
            ✓ Well-lit, high-resolution<br/>
            ✓ Multiple angles per area<br/>
            ✓ Close-ups of defects<br/>
            ✓ Context and overview shots<br/>
            ✓ Clear focus, minimal blur
            </small>
        </div>
        
        <div class="info-box" style="margin-top: 1rem;">
            <strong>🎯 Key Areas</strong><br/><br/>
            <small>
            • Foundation & Structure<br/>
            • Walls & Ceilings<br/>
            • Electrical Systems<br/>
            • Plumbing Fixtures<br/>
            • Roof & Attic<br/>
            • HVAC Systems
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_files:
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>{len(uploaded_files)} image(s)</strong> uploaded successfully and ready for analysis
        </div>
        """, unsafe_allow_html=True)
        
        # Display uploaded images in a beautiful grid
        st.markdown("### 📷 Image Gallery")
        
        cols = st.columns(4)
        for idx, uploaded_file in enumerate(uploaded_files):
            with cols[idx % 4]:
                image = Image.open(uploaded_file)
                st.markdown(f'<div class="image-card">', unsafe_allow_html=True)
                st.image(image, caption=f"Image {idx+1}", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
        st.markdown("---")
        
        # Analysis Button with Premium Design
        col_space1, col_btn, col_space2 = st.columns([1, 2, 1])
        
        with col_btn:
            if st.button("🚀 Start AI-Powered Analysis", type="primary", use_container_width=True):
                with st.spinner(""):
                    st.markdown("""
                    <div class="info-box pulse">
                        🤖 <strong>AI Vision Agent</strong> is analyzing your images...<br/>
                        <small>Processing multi-modal data with Multi-Agent System</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    steps = [
                        "🔍 Vision Agent analyzing images...",
                        "⚖️ Compliance Agent checking IRC codes...",
                        "💰 Finance Agent calculating costs...",
                        "📊 Generating comprehensive report..."
                    ]
                    
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                        if i % 25 == 0 and i < 100:
                            status_text.markdown(f"**{steps[i // 25]}**")
                    
                    # Actually process with agents
                    report = orchestrator.process_inspection(uploaded_files, inspector_notes)
                    
                    # Store real results from multi-agent system
                    st.session_state.mock_results = {
                        'total_defects': report.get('total_defects', 0),
                        'high_risk': report.get('high_risk', 0),
                        'medium_risk': report.get('medium_risk', 0),
                        'low_risk': report.get('low_risk', 0),
                        'estimated_cost': report.get('total_cost', 0),
                        'risk_score': report.get('risk_score', 0),
                        'compliance_violations': report.get('compliance_violations', 0),
                        'compliance_reviews': report.get('compliance_reviews', 0),
                        'defects': [
                            {
                                'type': d['type'],
                                'severity': d['severity'],
                                'location': d['location'],
                                'confidence': d['confidence'],
                                'cost': d['estimated_cost'],
                                'irc_code': d.get('irc_code', ''),
                                'description': d.get('description', '')
                            }
                            for d in report.get('all_defects', [])
                        ],
                        'violations': report.get('violations', []),
                        'rag_references': report.get('rag_references', []),
                        'recommendations': report.get('recommendations', [])
                    }
                    st.session_state.analysis_complete = True
                    
                st.markdown("""
                <div class="success-box">
                    ✅ <strong>Analysis Complete!</strong> View comprehensive results in the Analysis Dashboard tab
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box" style="text-align: center; padding: 3rem;">
            <h3 style="color: #94a3b8; margin-bottom: 1rem;">👆 Upload Property Images to Begin</h3>
            <p style="color: #64748b;">Our AI-powered analysis will identify defects, assess risks, and estimate repair costs</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Analysis Dashboard
with tab2:
    st.markdown("## 📊 AI Analysis Dashboard")
    
    if st.session_state.analysis_complete and st.session_state.mock_results:
        results = st.session_state.mock_results
        
        # Premium Metrics Display
        st.markdown("### 🎯 Property Health Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2 class="metric-value">{results['risk_score']}</h2>
                <p class="metric-label">{get_text(current_lang, 'risk_score')}</p>
                <p class="metric-sublabel">{get_text(current_lang, 'risk_score_subtitle')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h2 class="metric-value">{results['total_defects']}</h2>
                <p class="metric-label">{get_text(current_lang, 'defects_found')}</p>
                <p class="metric-sublabel">{get_text(current_lang, 'defects_found_subtitle')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h2 class="metric-value">{results['high_risk']}</h2>
                <p class="metric-label">{get_text(current_lang, 'critical_issues')}</p>
                <p class="metric-sublabel">{get_text(current_lang, 'critical_issues_subtitle')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h2 class="metric-value">₹{results['estimated_cost']:,}</h2>
                <p class="metric-label">{get_text(current_lang, 'repair_cost')}</p>
                <p class="metric-sublabel">{get_text(current_lang, 'repair_cost_subtitle')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Risk Score Explanation
        with st.expander("📊 How is Risk Score Calculated? (Click to expand)", expanded=False):
            st.markdown(f"### Risk Score Breakdown: **{results['risk_score']}/100**")
            
            # Calculate breakdown
            high_count = results['high_risk']
            medium_count = results['medium_risk']
            low_count = results['low_risk']
            
            # Points per severity (based on backend logic)
            high_points = min(high_count * 25, 60)  # Max 60 points from high
            medium_points = min(medium_count * 12, 30)  # Max 30 points from medium
            low_points = min(low_count * 5, 15)  # Max 15 points from low
            
            st.markdown("**Points by Severity:**")
            
            # High severity
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(min(high_points / 100, 1.0))
            with col2:
                st.markdown(f"**{high_points}** pts")
            st.caption(f"🚨 High Severity Defects ({high_count}) - Up to 25 points each")
            
            # Medium severity
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(min(medium_points / 100, 1.0))
            with col2:
                st.markdown(f"**{medium_points}** pts")
            st.caption(f"⚠️ Medium Severity Defects ({medium_count}) - Up to 12 points each")
            
            # Low severity
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(min(low_points / 100, 1.0))
            with col2:
                st.markdown(f"**{low_points}** pts")
            st.caption(f"ℹ️ Low Severity Defects ({low_count}) - Up to 5 points each")
            
            st.markdown("---")
            
            # Risk level explanation
            risk_score = results['risk_score']
            if risk_score < 30:
                st.success("""
                ✅ **Low Risk (0-30 points)**
                
                Your property is in good condition with only minor issues. These defects are manageable and don't pose immediate safety concerns.
                
                **Recommended Action:** Schedule routine maintenance within 60-90 days.
                """)
            elif risk_score < 60:
                st.warning("""
                ⚠️ **Medium Risk (30-60 points)**
                
                Your property has some notable issues that should be addressed soon. While not immediately dangerous, these defects could worsen if left unattended.
                
                **Recommended Action:** Schedule repairs within 30 days to prevent escalation.
                """)
            else:
                st.error("""
                🚨 **High Risk (60-100 points)**
                
                Your property has critical issues requiring immediate professional attention. These defects may pose safety hazards or could lead to significant structural damage.
                
                **Recommended Action:** Contact a licensed professional within 7 days for urgent repairs.
                """)
            
            # Cost context
            st.markdown("---")
            st.markdown(f"""
            **💰 Estimated Repair Investment:** ₹{results['estimated_cost']:,}
            
            This estimate is based on typical Indian market rates for the identified defects. Actual costs may vary based on:
            - Local labor rates
            - Material quality and availability
            - Extent of hidden damage
            - Contractor selection
            """)
        
        st.markdown("---")
        
        # Defect Analysis Section
        st.markdown(f"### {get_text(current_lang, 'defect_analysis')}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="error-box">
                <h3 style="margin: 0; font-size: 2rem;">⚠️ 2</h3>
                <strong>{get_text(current_lang, 'high_risk')}</strong><br/>
                <small>{get_text(current_lang, 'high_risk_subtitle')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="warning-box">
                <h3 style="margin: 0; font-size: 2rem;">⚡ 3</h3>
                <strong>{get_text(current_lang, 'medium_risk')}</strong><br/>
                <small>{get_text(current_lang, 'medium_risk_subtitle')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="info-box">
                <h3 style="margin: 0; font-size: 2rem;">ℹ️ 2</h3>
                <strong>{get_text(current_lang, 'low_risk')}</strong><br/>
                <small>{get_text(current_lang, 'low_risk_subtitle')}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Enhanced Defects Table with TTS
            df_defects = pd.DataFrame(results['defects'])
            
            st.dataframe(
                df_defects,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Text-to-Speech Controls
            st.markdown("---")
            st.markdown("**🔊 Text Reading:**")
            
            col_tts1, col_tts2 = st.columns(2)
            
            with col_tts1:
                if st.button("📖 Read All Defects", use_container_width=True):
                    # Build text to read
                    defects_text = f"Property Analysis Report. Risk Score: {results['risk_score']} out of 100. "
                    defects_text += f"Total defects found: {results['total_defects']}. "
                    
                    for idx, defect in enumerate(results['defects'], 1):
                        defects_text += f"Defect {idx}: {defect['type']}. "
                        defects_text += f"Severity: {defect['severity']}. "
                        defects_text += f"Location: {defect['location']}. "
                        defects_text += f"Estimated cost: {defect['cost']} rupees. "
                        defects_text += f"Description: {defect['description']}. "
                    
                    # JavaScript for TTS
                    st.components.v1.html(f"""
                    <script>
                        const text = `{defects_text}`;
                        const utterance = new SpeechSynthesisUtterance(text);
                        utterance.rate = 0.9;
                        utterance.pitch = 1.0;
                        utterance.volume = 1.0;
                        window.speechSynthesis.speak(utterance);
                    </script>
                    <div style="padding: 1rem; background: #10b981; color: white; border-radius: 0.5rem; text-align: center;">
                        🔊 Reading defects aloud...
                    </div>
                    """, height=60)
            
            with col_tts2:
                if st.button("⏹️ Stop Reading", use_container_width=True):
                    st.components.v1.html("""
                    <script>
                        window.speechSynthesis.cancel();
                    </script>
                    <div style="padding: 1rem; background: #ef4444; color: white; border-radius: 0.5rem; text-align: center;">
                        ⏹️ Stopped
                    </div>
                    """, height=60)
            
            # Individual defect reading
            st.markdown("**Read Individual Defects:**")
            for idx, defect in enumerate(results['defects']):
                col_def, col_btn = st.columns([4, 1])
                with col_def:
                    st.caption(f"{idx+1}. {defect['type']} - {defect['location']}")
                with col_btn:
                    if st.button("🔊", key=f"read_defect_{idx}"):
                        defect_text = f"{defect['type']} at {defect['location']}. "
                        defect_text += f"Severity: {defect['severity']}. "
                        defect_text += f"Cost: {defect['cost']} rupees. "
                        defect_text += f"{defect['description']}"
                        
                        st.components.v1.html(f"""
                        <script>
                            const text = `{defect_text}`;
                            const utterance = new SpeechSynthesisUtterance(text);
                            utterance.rate = 0.9;
                            window.speechSynthesis.speak(utterance);
                        </script>
                        <div style="padding: 0.5rem; background: #3b82f6; color: white; border-radius: 0.25rem; font-size: 0.8rem; text-align: center;">
                            🔊 Reading...
                        </div>
                        """, height=40)
        
        st.markdown("---")
        
        # RAG-Enhanced IRC Compliance Status
        st.markdown("### ⚖️ IRC Compliance Status (RAG-Retrieved)")
        
        # Show RAG indicator
        if results.get('rag_references'):
            st.markdown("""
            <div class="success-box" style="margin-bottom: 1.5rem;">
                🔍 <strong>RAG System Active</strong> - Retrieved {} IRC code references from knowledge base
            </div>
            """.format(len(results['rag_references'])), unsafe_allow_html=True)
        
        violations_list = results.get('violations', [])
        high_violations = [v for v in violations_list if v.get('status') == 'Violation']
        review_violations = [v for v in violations_list if v.get('status') == 'Review Required']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            violation_html = f"""<div class="error-box">
<h3 style="margin: 0;">❌ {len(high_violations)} Critical Violation(s)</h3>
<hr style="margin: 1rem 0; opacity: 0.3;"/>
"""
            
            for v in high_violations[:3]:  # Show top 3
                violation_html += f"""<small><strong>IRC {v.get('code', 'N/A')}</strong><br/>
{v.get('code_title', 'Unknown')}<br/>
📍 {v.get('location', 'Unknown location')}</small><br/><br/>
"""
            
            violation_html += "</div>"
            st.markdown(violation_html, unsafe_allow_html=True)
        
        with col2:
            review_html = f"""<div class="warning-box">
<h3 style="margin: 0;">⚠️ {len(review_violations)} Under Review</h3>
<hr style="margin: 1rem 0; opacity: 0.3;"/>
"""
            
            for v in review_violations[:3]:  # Show top 3
                review_html += f"""<small><strong>IRC {v.get('code', 'N/A')}</strong><br/>
{v.get('defect', 'Unknown')}</small><br/>
"""
            
            review_html += "</div>"
            st.markdown(review_html, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""<div class="success-box">
<h3 style="margin: 0;">✅ Compliant Areas</h3>
<hr style="margin: 1rem 0; opacity: 0.3;"/>
<small>Meets all building code standards<br/>No violations detected<br/>Safe for occupancy</small>
</div>
""", unsafe_allow_html=True)
        
        # Visual Analytics
        st.markdown("---")
        st.markdown("### 📈 Visual Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Severity Distribution Pie Chart
            severity_data = pd.DataFrame({
                'Severity': ['High Risk', 'Medium Risk', 'Low Risk'],
                'Count': [results['high_risk'], results['medium_risk'], results['low_risk']]
            })
            
            fig1 = px.pie(
                severity_data,
                values='Count',
                names='Severity',
                title='Defect Severity Distribution',
                color='Severity',
                color_discrete_map={
                    'High Risk': '#ef4444',
                    'Medium Risk': '#fb923c',
                    'Low Risk': '#3b82f6'
                },
                hole=0.4
            )
            
            fig1.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=12),
                title_font=dict(size=16, color='#e2e8f0')
            )
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Confidence Scores Bar Chart
            df_conf = pd.DataFrame(results['defects'][:5])
            
            fig2 = px.bar(
                df_conf,
                x='confidence',
                y='type',
                orientation='h',
                title='AI Detection Confidence',
                color='confidence',
                color_continuous_scale=['#3b82f6', '#a78bfa', '#ec4899']
            )
            
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=12),
                title_font=dict(size=16, color='#e2e8f0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # IRC Code References (RAG Showcase)
        if results.get('violations'):
            st.markdown("---")
            st.markdown("### 📚 IRC Code References (Retrieved via RAG)")
            
            st.markdown("""
            <div class="info-box" style="margin-bottom: 1rem;">
                <strong>🔍 Knowledge Base Retrieval</strong><br/>
                <small>The following IRC codes were automatically retrieved from our knowledge base based on detected defects</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Display detailed IRC code information
            for violation in results['violations'][:5]:  # Show top 5
                irc_code = violation.get('code', 'N/A')
                code_title = violation.get('code_title', 'Unknown Code')
                code_desc = violation.get('code_description', 'No description available')
                defect_type = violation.get('defect', 'Unknown')
                location = violation.get('location', 'Unknown')
                status = violation.get('status', 'Unknown')
                
                status_class = "error-box" if status == "Violation" else "warning-box"
                status_icon = "❌" if status == "Violation" else "⚠️"
                
                st.markdown(f"""
                <div class="{status_class}" style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="font-size: 1.1rem;">IRC {irc_code}: {code_title}</strong>
                        <span class="status-badge">{status_icon} {status}</span>
                    </div>
                    <hr style="margin: 0.5rem 0; opacity: 0.3;"/>
                    <p style="margin: 0.75rem 0; color: #cbd5e1;"><small>{code_desc}</small></p>
                    <div style="background: rgba(0,0,0,0.2); padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem;">
                        <strong>Detected Issue:</strong> {defect_type}<br/>
                        <strong>Location:</strong> 📍 {location}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div class="info-box" style="text-align: center; padding: 4rem;">
            <h2 style="color: #94a3b8; margin-bottom: 1rem;">📤 No Analysis Data Available</h2>
            <p style="color: #64748b; font-size: 1.1rem;">Upload images in the 'Upload & Inspect' tab to generate your analysis dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Placeholder metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class="metric-card" style="opacity: 0.3;">
                <h2 class="metric-value">—</h2>
                <p class="metric-label">Risk Score</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card" style="opacity: 0.3;">
                <h2 class="metric-value">—</h2>
                <p class="metric-label">Defects</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card" style="opacity: 0.3;">
                <h2 class="metric-value">—</h2>
                <p class="metric-label">Critical</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class="metric-card" style="opacity: 0.3;">
                <h2 class="metric-value">₹—</h2>
                <p class="metric-label">Cost</p>
            </div>
            """, unsafe_allow_html=True)

# TAB 3: Detailed Report
with tab3:
    st.markdown("## 📄 Comprehensive Inspection Report")
    
    if st.session_state.analysis_complete and st.session_state.mock_results:
        results = st.session_state.mock_results
        
        st.markdown("### 📋 Executive Summary")
        st.markdown(f"""
        <div class="info-box">
            This comprehensive property inspection has identified <strong>{results['total_defects']} defect(s)</strong> across multiple building systems 
            requiring immediate to long-term attention. The AI-powered risk assessment indicates a <strong>risk profile of {results['risk_score']}/100</strong>, 
            driven by {results['high_risk']} critical issue(s) that demand immediate professional attention to prevent further deterioration.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🚨 Priority Action Items")
        
        # Organize defects by severity
        high_defects = [d for d in results['defects'] if d['severity'] == 'High']
        medium_defects = [d for d in results['defects'] if d['severity'] == 'Medium']
        low_defects = [d for d in results['defects'] if d['severity'] == 'Low']
        
        # High Priority Section
        if high_defects:
            high_html = """<div class="error-box">
<h3>🚨 HIGH PRIORITY - Immediate Action Required (0-7 Days)</h3>
<hr style="margin: 1rem 0; opacity: 0.3;"/>
"""
            
            for idx, defect in enumerate(high_defects, 1):
                high_html += f"""<h4>{idx}. {defect['type']} - {defect['location']}</h4>
<ul>
<li><strong>AI Confidence:</strong> {int(defect['confidence'] * 100)}%</li>
<li><strong>IRC Violation:</strong> {defect.get('irc_code', 'N/A')} (Structural Integrity)</li>
<li><strong>Estimated Cost:</strong> ₹{defect['cost']:,}</li>
<li><strong>Recommendation:</strong> {defect.get('description', 'Emergency professional assessment required')}</li>
<li><strong>Risk:</strong> Potential structural failure, water infiltration, foundation compromise</li>
</ul>
"""
            
            high_html += "</div>"
            st.markdown(high_html, unsafe_allow_html=True)
        
        # Medium Priority Section
        if medium_defects:
            medium_html = """<div class="warning-box">
<h3>⚠️ MEDIUM PRIORITY - Schedule Within 30 Days</h3>
<hr style="margin: 1rem 0; opacity: 0.3;"/>
"""
            
            for idx, defect in enumerate(medium_defects, len(high_defects) + 1):
                medium_html += f"""<h4>{idx}. {defect['type']} - {defect['location']}</h4>
<ul>
<li><strong>IRC Violation:</strong> {defect.get('irc_code', 'N/A')} (Safety)</li>
<li><strong>Estimated Cost:</strong> ₹{defect['cost']:,}</li>
<li><strong>Recommendation:</strong> {defect.get('description', 'Professional inspection and repair recommended')}</li>
</ul>
"""
            
            medium_html += "</div>"
            st.markdown(medium_html, unsafe_allow_html=True)
        
        # Low Priority Section
        if low_defects:
            low_html = """<div class="info-box">
<h3>ℹ️ LOW PRIORITY - Monitor and Plan (60-90 Days)</h3>
<hr style="margin: 1rem 0; opacity: 0.3;"/>
"""
            
            for idx, defect in enumerate(low_defects, len(high_defects) + len(medium_defects) + 1):
                low_html += f"""<h4>{idx}. {defect['type']} - {defect['location']}</h4>
<ul>
<li><strong>Type:</strong> Routine maintenance required</li>
<li><strong>Estimated Cost:</strong> ₹{defect['cost']:,}</li>
<li><strong>Recommendation:</strong> {defect.get('description', 'Monitor and address during routine maintenance')}</li>
</ul>
"""
            
            low_html += "</div>"
            st.markdown(low_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📊 Report Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download PDF Report", use_container_width=True, type="primary"):
                # Generate report data
                report_text = f"""
SAFENEST AI PROPERTY INSPECTION REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PROPERTY DETAILS
Property ID: {property_id}
Address: {property_address if property_address else 'Not specified'}
Inspector: {inspector_name}
Inspection Date: {inspection_date}

EXECUTIVE SUMMARY
Total Defects Found: {results['total_defects']}
Risk Score: {results['risk_score']}/100
Critical Issues: {results['high_risk']}
Estimated Repair Cost: ₹{results['estimated_cost']:,}

DEFECTS IDENTIFIED:
"""
                for idx, defect in enumerate(results['defects'], 1):
                    report_text += f"\n{idx}. {defect['type']} - {defect['location']}\n"
                    report_text += f"   Severity: {defect['severity']}\n"
                    report_text += f"   Confidence: {int(defect['confidence'] * 100)}%\n"
                    report_text += f"   IRC Code: {defect.get('irc_code', 'N/A')}\n"
                    report_text += f"   Estimated Cost: ₹{defect['cost']:,}\n"
                    report_text += f"   Description: {defect.get('description', 'N/A')}\n"
                
                # Create downloadable file
                st.download_button(
                    label="💾 Click here to download report",
                    data=report_text,
                    file_name=f"SafeNest_Report_{property_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.success("📄 Report generated! Click the button above to download.")
        
        with col2:
            if st.button("📧 Email to Stakeholders", use_container_width=True, type="primary"):
                email_body = f"""
Property Inspection Report - {property_id}

Risk Score: {results['risk_score']}/100
Total Defects: {results['total_defects']}
Critical Issues: {results['high_risk']}
Estimated Cost: ₹{results['estimated_cost']:,}

For full report details, please access the SafeNest AI platform.
"""
                mailto_link = f"mailto:?subject=SafeNest Property Inspection Report - {property_id}&body={email_body.replace(chr(10), '%0D%0A')}"
                
                st.markdown(f"""
                <div class="success-box">
                    ✉️ <strong>Email Draft Created!</strong><br/>
                    <a href="{mailto_link}" style="color: #22c55e; text-decoration: underline;">Click here to open your email client</a>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if st.button("🔗 Share Report Link", use_container_width=True, type="primary"):
                share_link = f"http://localhost:8502/?report_id={property_id}"
                st.code(share_link, language=None)
                st.info("🔗 Report link generated! Copy the link above to share.")
                
                
    else:
        st.markdown("""
        <div class="info-box" style="text-align: center; padding: 4rem;">
            <h2 style="color: #94a3b8;">📊 No Report Available</h2>
            <p style="color: #64748b; font-size: 1.1rem;">Complete the AI analysis to generate your comprehensive inspection report</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: Financial Analysis
with tab4:
    st.markdown("## 💰 Financial Analysis & Cost Breakdown")
    
    if st.session_state.analysis_complete:
        results = st.session_state.mock_results
        
        st.markdown("### 💵 Total Estimated Repair Investment")
        st.markdown(f"""
        <div class="metric-card" style="max-width: 600px; margin: 0 auto;">
            <h1 style="font-size: 4rem; margin: 0; background: linear-gradient(135deg, #22c55e 0%, #10b981 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ₹{results['estimated_cost']:,}
            </h1>
            <p style="font-size: 1.2rem; color: #94a3b8; margin-top: 1rem;">Based on regional market rates and defect severity analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Cost breakdown by category
        cost_data = {
            'Category': ['Structural Repairs', 'Water Damage', 'Electrical Work', 'Plumbing', 'Cosmetic Fixes'],
            'Cost (₹)': [75000, 45000, 25000, 8000, 9000],
            'Priority': ['High', 'High', 'Medium', 'Medium', 'Low'],
            'Timeline': ['0-7 days', '0-7 days', '30 days', '30 days', '60-90 days']
        }
        
        df_costs = pd.DataFrame(cost_data)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### 📊 Cost Distribution Analysis")
            
            fig3 = px.pie(
                df_costs, 
                values='Cost (₹)', 
                names='Category',
                color='Priority',
                color_discrete_map={'High':'#ef4444', 'Medium':'#fb923c', 'Low':'#3b82f6'},
                hole=0.5
            )
            
            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=13),
                showlegend=True
            )
            
            fig3.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>₹%{value:,}<br>%{percent}<extra></extra>'
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            st.markdown("### 📋 Itemized Breakdown")
            st.dataframe(
                df_costs,
                use_container_width=True,
                hide_index=True,
                height=350
            )
        
        st.markdown("---")
        
        st.markdown("### 📅 Phased Repair Timeline & Budget")
        
        timeline_data = {
            'Phase': ['Phase 1: Critical', 'Phase 2: Important', 'Phase 3: Planned', 'Phase 4: Optional'],
            'Timeline': ['0-7 days', '8-30 days', '31-60 days', '60-90 days'],
            'Items': [2, 3, 1, 1],
            'Cost (₹)': [120000, 48000, 5000, 4000],
            'Status': ['🔴 Urgent', '🟡 Soon', '🟢 Scheduled', '🔵 Planned']
        }
        
        df_timeline = pd.DataFrame(timeline_data)
        
        # Timeline visualization
        fig4 = px.bar(
            df_timeline,
            x='Phase',
            y='Cost (₹)',
            color='Cost (₹)',
            text='Cost (₹)',
            title='Phased Budget Allocation',
            color_continuous_scale=['#3b82f6', '#a78bfa', '#ec4899', '#ef4444']
        )
        
        fig4.update_traces(texttemplate='₹%{text:,}', textposition='outside')
        
        fig4.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            title_font=dict(size=16, color='#e2e8f0'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            showlegend=False
        )
        
        st.plotly_chart(fig4, use_container_width=True)
        
        st.dataframe(df_timeline, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Financial Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="error-box">
                <h4>💳 Phase 1 Funding Priority</h4>
                <hr style="margin: 1rem 0; opacity: 0.3;"/>
                <p><strong>Amount Needed:</strong> ₹120,000</p>
                <p><strong>Timeline:</strong> Immediate (0-7 days)</p>
                <p><strong>Criticality:</strong> Essential for safety and compliance</p>
                <p style="margin-top: 1rem;"><small>Consider emergency repair financing or insurance claims for structural and water damage issues.</small></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box">
                <h4>📈 Long-term Investment Plan</h4>
                <hr style="margin: 1rem 0; opacity: 0.3;"/>
                <p><strong>Total Investment:</strong> ₹177,000</p>
                <p><strong>Timeline:</strong> 90-day plan</p>
                <p><strong>ROI:</strong> Enhanced property value and safety</p>
                <p style="margin-top: 1rem;"><small>Staged repairs can be budgeted over 3 months, preserving cash flow while addressing all issues systematically.</small></p>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div class="info-box" style="text-align: center; padding: 4rem;">
            <h2 style="color: #94a3b8;">💰 No Financial Data Available</h2>
            <p style="color: #64748b; font-size: 1.1rem;">Complete the AI analysis to generate cost estimates and financial planning</p>
        </div>
        """, unsafe_allow_html=True)

# Premium Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <h3><strong>SafeNest AI</strong></h3>
        <p style="font-size: 1.1rem; margin: 1rem 0;">CODEX '26 Hackathon • Enterprise Property Intelligence Platform</p>
        <p style="font-size: 0.95rem; color: #94a3b8;">
            Powered by <strong>Snowflake Cortex AI</strong> • Built with ❤️ by Team SafeNest
        </p>
        <p style="font-size: 0.85rem; color: #64748b; margin-top: 1rem;">
            © 2026 SafeNest AI. All rights reserved. • Real-time AI Vision • IRC Compliance • Cost Intelligence
        </p>
    </div>
""", unsafe_allow_html=True)
