import io
import os
import base64
from datetime import date
import streamlit as st
from google import genai
from google.genai import errors, types

try:
    from docx import Document
except ImportError:
    Document = None

st.set_page_config(
    page_title="LegalSaathi AI — Indian LegalTech Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_asset_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

HERO_ART_B64 = get_asset_b64("assets/hero_scales_books_blended.png")
COURT_ART_B64 = get_asset_b64("assets/sidebar_court_blended.png")

st.markdown("""
<style>
    /* Modern, Cosy LegalTech Theme Palette (Reference Specification):
       - Background: #F6F3EC (Warm ivory / off-white)
       - Primary: #24463B (Deep forest green)
       - Accent: #D4B47A (Muted gold)
       - Secondary Surface: #E8EDE5 (Pale sage)
       - Body Text: #343831 (Warm charcoal)
       - Muted Text: #5A6255
    */

    .stApp {
        background-color: #F6F3EC !important;
        color: #343831 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 7.5rem !important;
        max-width: 1180px !important;
    }

    /* 1. Persistent Left Sidebar */
    section[data-testid="stSidebar"] {
        width: 290px !important;
        min-width: 290px !important;
        background-color: #F6F3EC !important;
        border-right: 1px solid #E5E0D5 !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
    }
    .ls-sidebar-header-box {
        background: #24463B;
        border-radius: 0 0 20px 20px;
        padding: 1.5rem 1rem 1.35rem 1rem;
        text-align: center;
        margin: -1rem -0.9rem 1.25rem -0.9rem;
        position: relative;
        box-shadow: 0 4px 14px rgba(36, 70, 59, 0.12);
        border-bottom: 3.5px solid #D4B47A;
    }
    .ls-sidebar-header-box .ls-brand-icon {
        font-size: 2rem;
        line-height: 1;
        margin-bottom: 0.35rem;
    }
    .ls-sidebar-header-box .ls-brand-title {
        font-family: Georgia, "Playfair Display", serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.01em;
    }
    .ls-sidebar-header-box .ls-brand-title span {
        color: #D4B47A;
    }
    .ls-sidebar-header-box .ls-brand-sub {
        font-size: 0.76rem;
        color: #D4B47A;
        font-weight: 500;
        margin-top: 0.25rem;
        letter-spacing: 0.02em;
    }

    /* Sidebar Radio Navigation as 3 Large Rounded Cards */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] {
        margin-bottom: 1.25rem;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 0.65rem;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: #FFFFFF;
        border: 1px solid #E2DDD5;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
        width: 100%;
        margin: 0;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #24463B !important;
        border-color: #24463B !important;
        box-shadow: 0 4px 12px rgba(36, 70, 59, 0.15);
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:not(:has(input:checked)):hover {
        background-color: #EDE8DF;
        border-color: #D4B47A;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:not(:has(input:checked)) p {
        color: #343831 !important;
        font-weight: 500 !important;
    }

    /* Sidebar Gemini Status Card */
    .ls-sidebar-status-card {
        background: #E8EDE5;
        border: 1px solid #D2DDD0;
        border-radius: 12px;
        padding: 0.75rem 0.95rem;
        margin-bottom: 0.85rem;
    }
    .ls-sidebar-status-card .ls-status-connected {
        font-size: 0.84rem;
        font-weight: 700;
        color: #24463B;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }
    .ls-sidebar-status-card .ls-status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #2E7D32;
        display: inline-block;
    }
    .ls-sidebar-status-card .ls-status-model {
        font-size: 0.75rem;
        color: #5A6255;
        margin-top: 0.2rem;
        margin-left: 1rem;
    }
    .ls-sidebar-status-card.missing {
        background: #FDF6ED;
        border-color: #F1DCC9;
    }
    .ls-sidebar-status-card.missing .ls-status-dot {
        background: #B45309;
    }
    .ls-sidebar-status-card.missing .ls-status-connected {
        color: #B45309;
    }

    /* Sidebar Privacy & Safety Card */
    .ls-sidebar-privacy-card {
        background: #FAF4EB;
        border: 1px solid #EEDFCA;
        border-radius: 12px;
        padding: 0.85rem 0.95rem;
        margin-bottom: 0.75rem;
    }
    .ls-sidebar-privacy-card .ls-privacy-title {
        font-size: 0.86rem;
        font-weight: 700;
        color: #8C6228;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 0.35rem;
    }
    .ls-sidebar-privacy-card .ls-privacy-desc {
        font-size: 0.76rem;
        color: #5A6255;
        line-height: 1.45;
    }

    /* Sidebar Court Illustration */
    .ls-sidebar-court {
        text-align: center;
        margin-top: 0.85rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    .ls-sidebar-court img {
        max-width: 175px;
        width: 85%;
        height: auto;
    }

    /* 2. Large Hero Banner */
    .ls-hero-banner {
        background-color: #24463B;
        border-radius: 18px;
        padding: 1.55rem 2rem;
        color: #F6F3EC;
        margin-bottom: 1.25rem;
        position: relative;
        overflow: hidden;
        min-height: 220px;
        box-shadow: 0 4px 16px rgba(36, 70, 59, 0.12);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .ls-hero-text {
        position: relative;
        z-index: 2;
        max-width: 60%;
        flex: 1 1 58%;
    }
    .ls-hero-eyebrow {
        color: #D4B47A;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .ls-hero-title {
        font-family: Georgia, "Playfair Display", serif;
        font-size: 2.25rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.01em;
        line-height: 1.15;
    }
    .ls-hero-title span {
        color: #D4B47A !important;
    }
    .ls-hero-headline {
        font-size: 1.16rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 0.35rem;
    }
    .ls-hero-desc {
        font-size: 0.86rem;
        color: #DCE7DF;
        line-height: 1.45;
        margin-bottom: 0.95rem;
        max-width: 540px;
    }
    .ls-hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        align-items: center;
    }
    .ls-hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background-color: #F6F3EC;
        color: #24463B;
        font-size: 0.76rem;
        font-weight: 600;
        padding: 0.32rem 0.75rem;
        border-radius: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }
    .ls-hero-art {
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        width: 42%;
        height: 100%;
        z-index: 1;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        pointer-events: none;
    }
    .ls-hero-art img {
        height: 100%;
        width: 100%;
        object-fit: cover;
        object-position: right center;
    }

    /* 3. Two Large Feature Cards */
    div[data-testid="stColumn"]:has(.ls-feature-card-chat),
    div[data-testid="stColumn"]:has(.ls-feature-card-draft) {
        position: relative !important;
        cursor: pointer !important;
    }
    div[data-testid="stColumn"]:has(.ls-feature-card-chat) div[data-testid="stVerticalBlock"],
    div[data-testid="stColumn"]:has(.ls-feature-card-draft) div[data-testid="stVerticalBlock"] {
        position: relative !important;
    }
    .ls-feature-card-chat {
        background-color: #E8EDE5;
        border: 1px solid #D2DDD0;
        border-radius: 14px;
        padding: 1.15rem 1.4rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.5rem;
        min-height: 82px;
        pointer-events: none !important;
        user-select: none;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .ls-feature-card-draft {
        background-color: #FAF4EB;
        border: 1px solid #EADBCA;
        border-radius: 14px;
        padding: 1.15rem 1.4rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.5rem;
        min-height: 82px;
        pointer-events: none !important;
        user-select: none;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stColumn"]:has(.ls-feature-card-chat):hover .ls-feature-card-chat,
    div[data-testid="stColumn"]:has(.ls-feature-card-draft):hover .ls-feature-card-draft {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px rgba(36, 70, 59, 0.12);
    }
    .ls-fc-left {
        display: flex;
        align-items: center;
        gap: 0.95rem;
        pointer-events: none !important;
    }
    .ls-fc-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        flex-shrink: 0;
        pointer-events: none !important;
    }
    .ls-fc-icon-box.green {
        background-color: #DDE6DB;
    }
    .ls-fc-icon-box.gold {
        background-color: #F0E6D2;
    }
    .ls-fc-text {
        pointer-events: none !important;
    }
    .ls-fc-text h4 {
        font-size: 1.05rem;
        font-weight: 700;
        color: #24463B !important;
        margin: 0 0 0.2rem 0;
    }
    .ls-fc-text p {
        font-size: 0.84rem;
        color: #343831;
        margin: 0;
        line-height: 1.4;
    }
    .ls-fc-arrow {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        flex-shrink: 0;
        pointer-events: none !important;
    }
    .ls-fc-arrow.dark {
        background-color: #24463B;
        color: #FFFFFF;
    }
    .ls-fc-arrow.light {
        background-color: #EDE3CE;
        color: #24463B;
    }

    /* Invisible overlay button covering entire feature card */
    div.st-key-btn_feature_chat,
    div.st-key-btn_feature_draft,
    div[data-testid="stColumn"]:has(.ls-feature-card-chat) div.stButton,
    div[data-testid="stColumn"]:has(.ls-feature-card-draft) div.stButton {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 20 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div.st-key-btn_feature_chat button,
    div.st-key-btn_feature_draft button,
    div[data-testid="stColumn"]:has(.ls-feature-card-chat) div.stButton > button,
    div[data-testid="stColumn"]:has(.ls-feature-card-draft) div.stButton > button {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100% !important;
        height: 100% !important;
        min-height: 82px !important;
        opacity: 0 !important;
        cursor: pointer !important;
        z-index: 25 !important;
        border: none !important;
        background: transparent !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* 4. Section Headings & Notices */
    .ls-section-heading {
        font-size: 1.45rem;
        font-weight: 700;
        color: #24463B;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0 0.25rem 0;
    }
    .ls-section-sub {
        font-size: 0.88rem;
        color: #5A6255;
        margin-bottom: 0.85rem;
    }
    .ls-guidance-notice {
        background: #E8EDE5;
        border: 1px solid #D2DDD0;
        border-radius: 10px;
        padding: 0.85rem 1.15rem;
        font-size: 0.86rem;
        color: #343831;
        display: flex;
        align-items: flex-start;
        gap: 0.65rem;
        margin-bottom: 1.15rem;
        line-height: 1.5;
    }
    .ls-guidance-notice .ls-notice-icon {
        font-size: 1.15rem;
        color: #24463B;
        flex-shrink: 0;
        margin-top: -1px;
    }
    .ls-guidance-notice strong {
        color: #24463B;
    }

    /* Cards general */
    .ls-card {
        background: #FFFFFF;
        border: 1px solid #DCE4D9;
        border-radius: 12px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(36, 70, 59, 0.03);
    }
    .ls-card h4 {
        color: #24463B !important;
        margin-top: 0;
        margin-bottom: 0.65rem;
        font-size: 1.05rem;
        font-weight: 600;
    }
    .ls-card p, .ls-card li {
        font-size: 0.875rem;
        color: #343831;
        line-height: 1.55;
    }
    .ls-card a {
        color: #24463B;
        text-decoration: underline;
        font-weight: 500;
    }

    /* Step Labels in Draft */
    .ls-step-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #24463B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0.85rem 0 0.35rem 0;
    }

    /* Buttons */
    div.stButton > button[kind="primary"] {
        background-color: #24463B;
        border-color: #24463B;
        color: #F6F3EC;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1.3rem;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1A342C;
        border-color: #1A342C;
        color: #F6F3EC;
        box-shadow: 0 2px 6px rgba(36, 70, 59, 0.2);
    }
    div.stButton > button:not([kind="primary"]) {
        background-color: #E8EDE5;
        border: 1px solid #CAD5C7;
        color: #24463B;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:not([kind="primary"]):hover {
        background-color: #DDE5DA;
        border-color: #24463B;
        color: #1A342C;
    }
    div.stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: 1.5px solid #24463B;
        color: #24463B;
        background-color: #FFFFFF;
        transition: all 0.15s ease-in-out;
    }
    div.stDownloadButton > button:hover {
        border-color: #1A342C;
        color: #1A342C;
        background-color: #E8EDE5;
        box-shadow: 0 2px 6px rgba(36, 70, 59, 0.1);
    }

    /* Form Inputs (Document Draft & Other Forms) */
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"],
    div[data-testid="stTextArea"] div[data-baseweb="textarea"] {
        border-color: #CCD6C9 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
    div[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within,
    div[data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within {
        border-color: #24463B !important;
        box-shadow: 0 0 0 1.5px #24463B !important;
    }
    .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #24463B !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* Chat Messages */
    div[data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 0.85rem 1.15rem;
        margin-bottom: 0.75rem;
        border: 1px solid #DCE4D9;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #E8EDE5 !important;
        border-color: #D2DDD0 !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #FFFFFF !important;
        border-color: #DCE4D9 !important;
        box-shadow: 0 1px 4px rgba(36, 70, 59, 0.04);
    }
    div[data-testid="stChatMessage"] p {
        color: #343831;
        line-height: 1.6;
    }

    /* Bottom Chat Portal & Input Spacing */
    div[data-testid="stBottom"] {
        background-color: #F6F3EC !important;
        border-top: 1px solid rgba(210, 221, 208, 0.6) !important;
        padding-bottom: 0.75rem !important;
        padding-top: 0.5rem !important;
        z-index: 99 !important;
    }
    div[data-testid="stBottom"] > div {
        max-width: 1180px !important;
        margin: 0 auto !important;
    }

    /* Chat Input Container & Single Pill Border */
    div[data-testid="stChatInput"] {
        border: none !important;
        outline: none !important;
        background: transparent !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInput"] > div {
        border: 1px solid #CCD6C9 !important;
        border-radius: 28px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(36, 70, 59, 0.05) !important;
        outline: none !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        padding-left: 0.75rem !important;
        padding-right: 0.35rem !important;
    }
    div[data-testid="stChatInput"] > div:focus-within {
        border-color: #24463B !important;
        box-shadow: 0 0 0 1.5px #24463B, 0 2px 8px rgba(36, 70, 59, 0.1) !important;
        outline: none !important;
    }

    /* Reset inner textarea wrappers to eliminate duplicate outlines or default red focus */
    div[data-testid="stChatInput"] div[data-baseweb="textarea"],
    div[data-testid="stChatInput"] div[data-baseweb="textarea"]:focus-within,
    div[data-testid="stChatInput"] div[class*="base-input"] {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
    }
    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] textarea:focus {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
        color: #343831 !important;
        font-size: 0.92rem !important;
        line-height: 1.45 !important;
    }

    /* Green Circular Send Button */
    div[data-testid="stChatInput"] button {
        background-color: #24463B !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        transition: background-color 0.15s ease !important;
        box-shadow: 0 1px 3px rgba(36, 70, 59, 0.2) !important;
    }
    div[data-testid="stChatInput"] button:hover:not(:disabled) {
        background-color: #1A342C !important;
        box-shadow: 0 2px 6px rgba(36, 70, 59, 0.3) !important;
    }

    /* Suggested Question Chips */
    div[class*="st-key-chip_"] button,
    div[data-testid="stColumn"]:has(button[key^="chip_"]) button {
        background-color: #FFFFFF !important;
        border: 1px solid #DFD9CE !important;
        border-radius: 20px !important;
        color: #343831 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.75rem !important;
        min-height: 42px !important;
        line-height: 1.3 !important;
        transition: all 0.15s ease-in-out !important;
        box-shadow: 0 1px 3px rgba(36, 70, 59, 0.04) !important;
    }
    div[class*="st-key-chip_"] button:hover,
    div[data-testid="stColumn"]:has(button[key^="chip_"]) button:hover {
        background-color: #E8EDE5 !important;
        border-color: #24463B !important;
        color: #24463B !important;
        box-shadow: 0 3px 8px rgba(36, 70, 59, 0.1) !important;
        transform: translateY(-1px) !important;
    }

    /* Footer */
    .ls-footer {
        text-align: center;
        font-size: 0.8rem;
        color: #64748b;
        padding: 1.25rem 0 0.5rem 0;
        line-height: 1.5;
    }
    .ls-footer a {
        color: #24463B;
        text-decoration: underline;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# API key can be provided through GEMINI_API_KEY environment variable or Streamlit secrets.
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key:
    try:
        raw_secret = st.secrets.get("GEMINI_API_KEY", "")
        api_key = str(raw_secret).strip() if raw_secret is not None else ""
    except Exception:
        api_key = ""

model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

MISSING_KEY_MESSAGE = (
    "⚠️ **Gemini API key is not configured.**\n\n"
    "To enable live AI responses, set the `GEMINI_API_KEY` environment variable:\n"
    "```bash\n"
    "export GEMINI_API_KEY=\"your_api_key_here\"\n"
    "```\n"
    "Or configure `GEMINI_API_KEY = \"your_api_key_here\"` in `.streamlit/secrets.toml`.\n\n"
    "You can get an API key from [Google AI Studio](https://aistudio.google.com/).\n\n"
    "*Note: LegalSaathi AI provides general educational legal information only. "
    "Always verify legal provisions from official Indian sources such as [India Code](https://www.indiacode.nic.in/) "
    "or consult a licensed advocate.*"
)

SYSTEM_PROMPT = """You are LegalSaathi AI, an Indian legal information assistant for educational and general-information purposes.
Important rules:
- You are not a lawyer and must not claim to provide formal legal advice or create an advocate-client relationship.
- Clearly distinguish general legal information from advice provided by a qualified advocate.
- Give concise, practical answers in the user's chosen language: English, Hindi, or Hinglish.
- Ask clarifying questions when key facts, jurisdiction, or dates are missing.
- When state-specific legislation or procedures (such as local rent control, state consumer dispute rules, police procedures, or municipal bylaws) may affect the answer, ask for the relevant Indian state or note state variations.
- Criminal-law transition: Recognize the transition effective July 1, 2024, where the Bharatiya Nyaya Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA) replaced the Indian Penal Code (IPC), Code of Criminal Procedure (CrPC), and Indian Evidence Act (IEA), subject to applicable transitional provisions.
  * When the incident date could affect the applicable law, ask for or clearly account for that date.
  * Do not automatically assume the new or old code applies solely from a simplified date rule; relevant facts, continuous offenses, and transitional provisions may matter.
  * Do not hardcode or guarantee any statutory section as definitely correct without verification.
- Do not invent statutes, section numbers, case names, deadlines, court procedures, or citations. Never claim that an unverified provision has been checked.
- If uncertain about a legal provision, say so and suggest checking the official India Code portal (https://www.indiacode.nic.in/) or consulting a qualified Indian advocate.
- Explain practical, safe next steps and mention that outcomes depend on facts and current law.
- Contextual emergency and practical helpline guidance (provide only when directly relevant to the situation; do not display every helpline in every answer):
  * Immediate danger or life-safety emergency: advise contacting emergency services immediately at 112.
  * Recent suspected online financial fraud or cybercrime: advise contacting India's cyber-fraud helpline 1930 promptly, reporting through the National Cyber Crime Reporting Portal (https://cybercrime.gov.in/), and notifying the bank/payment provider immediately. Do not guarantee that funds will be recovered or transfers reversed.
  * Women in distress: mention 181 or 1091 as potentially relevant helplines, noting that availability and applicability can vary by state.
  * Child protection issues: mention Childline 1098 where applicable.
  * Consumer grievances: mention the National Consumer Helpline (NCH) 1915 and https://consumerhelpline.gov.in/ where appropriate.
- Do not encourage evading law enforcement, fraud, threats, evidence destruction, or other illegal conduct.
- End legal responses with a short note that the answer is general educational information, not a substitute for a qualified lawyer, and instruct the user to verify legal provisions from official Indian sources (such as India Code, official court portals, or a licensed advocate).
"""

def ask_ai(prompt, user_text=None):
    if not api_key:
        return MISSING_KEY_MESSAGE
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
                max_output_tokens=1500,
            ),
        )
        candidate = response.candidates[0] if (hasattr(response, "candidates") and response.candidates) else None
        finish_reason = getattr(candidate, "finish_reason", None)
        finish_str = str(finish_reason).upper() if finish_reason else ""

        text_content = ""
        try:
            text_content = response.text or ""
        except Exception:
            text_content = ""

        if any(term in finish_str for term in ["SAFETY", "BLOCKLIST", "PROHIBITED"]):
            print(f"[LegalSaathi Diagnosis] Generation truncated by finish_reason: {finish_str}")
            safety_note = (
                "\n\n[Notice: AI draft generation stopped early due to safety moderation policies. "
                "For emergency reporting or official police complaints, please approach the local police station directly or dial 112.]"
            )
            return (text_content + safety_note).strip() if text_content else (
                "⚠️ **Safety Filter Notice**: The AI service stopped generating this draft due to content or safety restrictions. "
                "For emergency situations, life-safety matters, or official police complaints, please approach the local police station directly or dial 112."
            )

        if text_content:
            return text_content
        return "No response text was generated by the model. Please refine your query and try again."
    except Exception as exc:
        err_str = str(exc).lower()
        exc_type_name = type(exc).__name__.lower()
        status_code = getattr(exc, "code", None)
        api_status = getattr(exc, "status", None)

        if (
            status_code == 429
            or str(api_status).upper() == "RESOURCE_EXHAUSTED"
            or any(term in err_str for term in ["429", "resource_exhausted", "quota", "rate limit", "ratelimit"])
        ):
            category = "RATE_LIMITED"
            user_message = (
                "⚠️ **Service Temporarily Rate-Limited**: The AI service is receiving high demand or has reached its temporary request limit. "
                "Please wait about 30–60 seconds before trying again."
            )
        elif (
            status_code == 404
            or str(api_status).upper() == "NOT_FOUND"
            or any(term in err_str for term in ["404", "not_found", "model not found"])
        ):
            category = "MODEL_UNAVAILABLE"
            user_message = (
                f"⚠️ **AI Model Unavailable**: The configured AI model (`{model}`) is currently unavailable or not accessible with your API key. "
                "Please check the application configuration or set an alternative model using the `GEMINI_MODEL` environment variable."
            )
        elif (
            status_code in (401, 403)
            or str(api_status).upper() in ("UNAUTHENTICATED", "PERMISSION_DENIED")
            or any(term in err_str for term in ["api key not valid", "api_key_invalid", "unauthenticated", "permission_denied", "401", "403", "forbidden"])
            or (status_code == 400 and any(term in err_str for term in ["api key", "api_key", "key not valid"]))
        ):
            category = "AUTHENTICATION_ERROR"
            user_message = (
                "⚠️ **Authentication / Permission Error**: The `GEMINI_API_KEY` was not accepted or lacks permission for this request. "
                "Please check your API key configuration in your environment or Streamlit secrets."
            )
        elif (
            isinstance(exc, (ConnectionError, TimeoutError, OSError))
            or any(term in exc_type_name for term in ["connect", "timeout", "network", "socket", "unreachable"])
            or any(term in err_str for term in ["timeout", "timed out", "connection", "connecterror", "network", "unreachable", "name resolution", "dns", "nodename", "servname", "errno 8", "errno 61", "errno 54"])
        ):
            category = "CONNECTION_ERROR"
            user_message = (
                "⚠️ **Connection Issue**: Could not connect to the AI service. "
                "Please check your internet connection and try again in a few moments."
            )
        else:
            category = "SERVICE_ERROR"
            user_message = (
                "⚠️ **AI Service Error**: The AI service could not complete the request at this time. "
                "Please check your configuration and network connection, then try again."
            )

        log_parts = [f"[LegalSaathi Diagnosis] Exception: {type(exc).__name__}", f"Category: {category}"]
        if status_code is not None:
            log_parts.append(f"HTTP Code: {status_code}")
        if isinstance(api_status, str) and api_status:
            log_parts.append(f"Status: {api_status}")
        print(" | ".join(log_parts))

        return user_message


def generate_docx_bytes(draft_text):
    if not Document:
        raise RuntimeError("The 'python-docx' package is not installed. Please install it to generate DOCX files.")

    doc = Document()

    # Title
    doc.add_heading("LegalSaathi AI — Educational First Draft", level=1)

    # Disclaimer Section
    doc.add_heading("Important Notice", level=2)
    disclaimer_p = doc.add_paragraph()
    disclaimer_p.add_run(
        "• This document is an AI-generated educational starting draft prepared for initial review.\n"
        "• It does NOT constitute legal advice and does NOT substitute for a qualified Indian advocate.\n"
        "• This draft has NOT been reviewed, settled, or verified by an advocate.\n"
        "• You must carefully review and verify all names, facts, dates, legal provisions, and recipient details before any use.\n"
        "• Do not label this document an advocate-issued notice or imply that it is legally validated."
    ).italic = True

    # Draft Content Section
    doc.add_heading("Generated Draft", level=2)
    draft_clean = draft_text.replace("\r\n", "\n").replace("\r", "\n")
    for paragraph_text in draft_clean.split("\n\n"):
        p_text = paragraph_text.strip()
        if not p_text:
            continue
        lines = p_text.split("\n")
        first_line = lines[0].strip()
        remaining_lines = lines[1:]

        if first_line.startswith("### "):
            doc.add_heading(first_line[4:].strip(), level=3)
            p_lines = remaining_lines
        elif first_line.startswith("## "):
            doc.add_heading(first_line[3:].strip(), level=2)
            p_lines = remaining_lines
        elif first_line.startswith("# "):
            doc.add_heading(first_line[2:].strip(), level=2)
            p_lines = remaining_lines
        elif first_line.startswith("**") and first_line.endswith("**") and len(first_line) < 100:
            doc.add_heading(first_line.strip("*"), level=3)
            p_lines = remaining_lines
        else:
            p_lines = lines

        if p_lines:
            p = doc.add_paragraph()
            for i, line in enumerate(p_lines):
                if i > 0:
                    p.add_run("\n")
                p.add_run(line)

    # Verification Checklist Section
    doc.add_heading("Verification & Safeguards Checklist Before Use", level=2)
    checklist_p = doc.add_paragraph()
    checklist_p.add_run(
        "1. Verify all facts, dates, names, amounts, and addresses for accuracy.\n"
        "2. Replace all placeholder brackets (e.g., [SENDER FULL NAME], [RECIPIENT NAME / DESIGNATION / ORGANISATION], [CITY, STATE]) with verified information.\n"
        "3. Check relevant statutes on official portals (such as https://www.indiacode.nic.in/).\n"
        "4. Have this draft reviewed and settled by a qualified Indian advocate before formal transmission."
    )

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def set_nav_page(target_page):
    st.session_state.nav_selection = target_page
    st.session_state.nav_page = target_page

nav_icons = {
    "Legal Chat": "💬  Legal Chat",
    "Document Draft": "📄  Document Draft",
    "About & Sources": "ℹ️  About & Sources"
}
nav_options = ["Legal Chat", "Document Draft", "About & Sources"]

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = st.session_state.get("nav_page", "Legal Chat")
if st.session_state.nav_selection not in nav_options:
    st.session_state.nav_selection = "Legal Chat"
st.session_state.nav_page = st.session_state.nav_selection

with st.sidebar:
    st.markdown("""
    <div class="ls-sidebar-header-box">
        <div class="ls-brand-icon">⚖️</div>
        <div class="ls-brand-title">LegalSaathi <span>AI</span></div>
        <div class="ls-brand-sub">Indian LegalTech Companion</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Choose a tool",
        nav_options,
        key="nav_selection",
        format_func=lambda x: nav_icons.get(x, x),
        label_visibility="collapsed"
    )
    st.session_state.nav_page = page

    if api_key:
        st.markdown(f"""
        <div class="ls-sidebar-status-card">
            <div class="ls-status-connected">
                <span class="ls-status-dot"></span> Gemini API Connected
            </div>
            <div class="ls-status-model">Model: {model}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ls-sidebar-status-card missing">
            <div class="ls-status-connected">
                <span class="ls-status-dot"></span> Gemini API Key Missing
            </div>
            <div class="ls-status-model">Set GEMINI_API_KEY in secrets</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ls-sidebar-privacy-card">
        <div class="ls-privacy-title">🛡️ Privacy &amp; Safety</div>
        <div class="ls-privacy-desc">Do not share passwords, Aadhaar numbers, bank details or other confidential information.</div>
    </div>
    """, unsafe_allow_html=True)

    if COURT_ART_B64:
        st.markdown(f"""
        <div class="ls-sidebar-court">
            <img src="data:image/png;base64,{COURT_ART_B64}" alt="Supreme Court of India" />
        </div>
        """, unsafe_allow_html=True)

# 2. Main Workspace Hero Banner (Matches Reference UI)
hero_image_html = f'<img src="data:image/png;base64,{HERO_ART_B64}" alt="Justice Scales &amp; Codes" />' if HERO_ART_B64 else ''
st.markdown(f"""
<div class="ls-hero-banner">
    <div class="ls-hero-text">
        <div class="ls-hero-eyebrow">YOUR PERSONAL LEGAL ASSISTANT</div>
        <h1 class="ls-hero-title">LegalSaathi <span class="ls-gold-text">AI</span></h1>
        <div class="ls-hero-headline">Legal help, made simpler.</div>
        <div class="ls-hero-desc">Understand your legal options, get procedural guidance, and create structured starting drafts for common legal matters in India.</div>
        <div class="ls-hero-badges">
            <span class="ls-hero-badge">🎓 Educational Prototype</span>
            <span class="ls-hero-badge">⚖️ BNSS / BNS Transition Ready</span>
            <span class="ls-hero-badge">📚 Official India Code Grounding</span>
        </div>
    </div>
    <div class="ls-hero-art">
        {hero_image_html}
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Two Large Feature Cards (Side-by-side with interactive navigation)
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.markdown("""
    <div class="ls-feature-card-chat">
        <div class="ls-fc-left">
            <div class="ls-fc-icon-box green">💬</div>
            <div class="ls-fc-text">
                <h4>Legal Chat Assistant</h4>
                <p>Ask legal questions, understand procedures, rights and next steps.</p>
            </div>
        </div>
        <div class="ls-fc-arrow dark">➔</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Open Legal Chat", key="btn_feature_chat", on_click=set_nav_page, args=("Legal Chat",))

with col_f2:
    st.markdown("""
    <div class="ls-feature-card-draft">
        <div class="ls-fc-left">
            <div class="ls-fc-icon-box gold">📄</div>
            <div class="ls-fc-text">
                <h4>Document Draft Assistant</h4>
                <p>Create a first draft for complaints, applications, notices and more.</p>
            </div>
        </div>
        <div class="ls-fc-arrow light">➔</div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Open Document Draft", key="btn_feature_draft", on_click=set_nav_page, args=("Document Draft",))

if page == "Legal Chat":
    st.markdown("""
    <div class="ls-section-heading">💬 Legal Chat</div>
    <div class="ls-section-sub">Ask questions about Indian civil, criminal, consumer, cyber, tenancy, or other legal matters.</div>
    <div class="ls-guidance-notice">
        <span class="ls-notice-icon">ℹ️</span>
        <div><strong>Educational Guidance Only:</strong> LegalSaathi AI explains general legal procedures, rights and next steps in simple terms. It does not provide formal legal representation or advocate advice.</div>
    </div>
    """, unsafe_allow_html=True)

    if not api_key:
        st.warning(
            "⚠️ **Gemini API Key Required**: The `GEMINI_API_KEY` environment variable is not configured. "
            "Set your Gemini API key in your terminal or Streamlit secrets to get live legal answers."
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Suggested Question Chips Bar (matching reference UI, positioned above bottom input)
    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #24463B; margin-top: 1.15rem; margin-bottom: 0.45rem;'>Try asking:</div>", unsafe_allow_html=True)
    c_chip1, c_chip2, c_chip3, c_chip4 = st.columns(4)
    with c_chip1:
        chip_q1 = st.button("⚖️ How to file a consumer complaint?", key="chip_consumer", use_container_width=True)
    with c_chip2:
        chip_q2 = st.button("🛡️ Steps in a cyber fraud case?", key="chip_cyber", use_container_width=True)
    with c_chip3:
        chip_q3 = st.button("🏠 Tenant rights in India?", key="chip_tenant", use_container_width=True)
    with c_chip4:
        chip_q4 = st.button("📖 How to draft a police complaint?", key="chip_police", use_container_width=True)

    question = st.chat_input("Ask a legal question (e.g., \"What steps should I take if an online store refuses a refund?\")...")

    active_prompt = None
    if question:
        active_prompt = question
    elif chip_q1:
        active_prompt = "How to file a consumer complaint?"
    elif chip_q2:
        active_prompt = "Steps in a cyber fraud case?"
    elif chip_q3:
        active_prompt = "Tenant rights in India?"
    elif chip_q4:
        active_prompt = "How to draft a police complaint?"

    if active_prompt:
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)
        with st.chat_message("assistant"):
            if not api_key:
                answer = MISSING_KEY_MESSAGE
                st.warning(answer)
            else:
                with st.spinner("Preparing response…"):
                    history = st.session_state.messages[-8:]
                    prompt = "\n\n".join(
                        ("User: " if m["role"] == "user" else "Assistant: ") + m["content"]
                        for m in history
                    )
                    answer = ask_ai(prompt, active_prompt)
                    st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.messages:
        st.markdown("<div style='margin-top: 0.6rem;'>", unsafe_allow_html=True)
        if st.button("Clear chat history", key="btn_clear_chat"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Document Draft":
    st.markdown("""
    <div class="ls-section-heading">📝 Formal Document Draft Assistant</div>
    <div class="ls-section-sub">Generate a structured starting representation or grievance letter with placeholders for review by a licensed advocate.</div>
    <div class="ls-guidance-notice">
        <span class="ls-notice-icon">ℹ️</span>
        <div><strong>Drafting Disclaimer:</strong> This creates an initial educational draft for review. It is not an advocate-issued legal notice. Verify all facts, dates, amounts, and provisions before transmission.</div>
    </div>
    """, unsafe_allow_html=True)

    if not api_key:
        st.warning(
            "⚠️ **Gemini API Key Required**: Please configure `GEMINI_API_KEY` to generate real document drafts."
        )

    if "document_draft" not in st.session_state:
        st.session_state.document_draft = ""

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("<div class='ls-step-label'>1. Document Details &amp; Language</div>", unsafe_allow_html=True)
        doc_type = st.selectbox(
            "Document type",
            [
                "Consumer complaint letter",
                "Refund request",
                "Workplace grievance",
                "Rental/tenancy issue letter",
                "General formal representation",
            ],
            help="Select the category of legal representation or grievance letter."
        )
        language = st.selectbox(
            "Language",
            ["English", "Hindi", "Hinglish"],
            help="Choose the language for the generated draft."
        )
    with col_d2:
        st.markdown("<div class='ls-step-label'>2. Parties &amp; Jurisdiction</div>", unsafe_allow_html=True)
        person = st.text_input(
            "Your name (optional)",
            placeholder="e.g. Pooja Sharma (or leave blank)",
            help="Appears in the sender header and sign-off block."
        )
        recipient = st.text_input(
            "Recipient / organisation (optional)",
            placeholder="e.g. Manager, Customer Support, XYZ Ltd",
            help="The organisation or person receiving this letter."
        )

    city = st.text_input(
        "City and state (optional)",
        placeholder="e.g. Jaipur, Rajasthan",
        help="Included in the letterhead and date location."
    )
    st.markdown("<div class='ls-step-label'>3. Factual Narrative &amp; Requested Resolution</div>", unsafe_allow_html=True)
    facts = st.text_area(
        "Describe the facts",
        height=160,
        placeholder="What happened, relevant dates, amount (if any), and what resolution you want. Avoid sensitive ID numbers.",
        help="Provide clear factual background so the assistant can distinguish established facts from missing information."
    )

    if st.button("Generate draft", type="primary"):
        if not api_key:
            st.error("⚠️ **Cannot generate draft**: Gemini API key is missing. Please set the `GEMINI_API_KEY` environment variable before generating documents.")
        elif len(facts.strip()) < 20:
            st.error("Please add a few more details so the draft has context.")
        else:
            prompt = f"""You are drafting a {doc_type} in {language}. Today's date: {date.today().isoformat()}.

User-Provided Inputs:
- Sender Name: {person or '[SENDER FULL NAME]'}
- Recipient / Organisation: {recipient or '[RECIPIENT NAME / DESIGNATION / ORGANISATION]'}
- City / State: {city or '[CITY, STATE]'}
- Factual Background & Requested Resolution:
{facts}

Instructions:
1. Document Nature & Purpose:
   - Prepare a polite, professional, formal first draft tailored specifically to: {doc_type}.
   - Do NOT falsely label this as a lawyer-drafted legal notice or advocate representation.
   - Do NOT invent facts, dates, transaction numbers, addresses, statutory sections, or case citations. Use only facts supplied above; for any missing detail, insert an uppercase bracketed placeholder (e.g., [DATE OF INCIDENT], [INVOICE/REFERENCE NUMBER], [AMOUNT IN INR], [POSTAL ADDRESS]).
   - Do NOT force consumer-specific remedies, clauses, or statutory timelines into non-consumer documents (such as workplace grievances, tenancy disputes, or general representations). Tailor the tone and requested resolution strictly to the nature of {doc_type}.
   - Single Coherent Perspective: When the sender's role or relationship is unclear from the inputs, do NOT generate multiple alternative options or branching drafts. Write one single, coherent draft from the perspective of the aggrieved party seeking resolution, using uppercase bracketed placeholders (e.g., [TENANT / LANDLORD]) for unconfirmed details.
   - Police & Administrative Representation Scope: When addressed to administrative or police authorities (such as 'The Station House Officer' or 'The Station House'), format strictly as a formal, civil written representation or factual intimation/record (e.g., loss of personal property, civic disturbance, or record of incident). Complete the full narrative, requested administrative record/action, formal sign-off, and the required 'Gaps to Fill Before Sending' section without stopping mid-draft.

2. Required Document Structure:
   - Header: Sender details, Current date ({date.today().isoformat()}), Recipient details.
   - Subject Line: Concise, clear, and relevant to {doc_type}.
   - Salutation: Formal (e.g., 'Dear Sir/Madam,').
   - Opening: Clearly state the identity of the sender and the primary purpose of this letter/representation.
   - Factual Narrative: Set out the facts chronologically based strictly on the user's input, distinguishing supplied facts from gaps. Keep the letter body concise (under 400 words) and fully completed.
   - Specific Relief / Resolution: Clearly state what outcome, remedy, or action is requested, with a reasonable timeframe if appropriate.
   - Polite Concluding Clause: Mention next appropriate steps if unaddressed (e.g., relevant grievance mechanism, department escalation, or legal counsel review), without making unsupported legal threats or outcome guarantees.
   - Formal Sign-off: 'Yours sincerely,', sender name placeholder, and list of enclosures (e.g., [Encl: Relevant receipts/documents]).

3. Post-Draft Section (Include at the bottom):
   - **Gaps to Fill Before Sending**: Provide 3 to 5 concise, relevant bullet points identifying specific placeholders and missing evidence (e.g., receipts, dates, contract copies) the sender must verify or attach before sending. Do not duplicate the general verification checklist already appended by the application.
"""
            with st.spinner("Creating draft…"):
                st.session_state.document_draft = ask_ai(prompt, facts)

    if st.session_state.document_draft:
        st.markdown("<div class='ls-step-label'>4. Generated Document Preview &amp; Export</div>", unsafe_allow_html=True)
        st.markdown("### Generated Draft Preview")
        st.caption("Review your draft below. You can copy the text or download it in TXT or DOCX format:")
        st.text_area("Generated draft (copy from here)", value=st.session_state.document_draft, height=420)
        download_payload = f"""================================================================================
LEGALSAATHI AI — EDUCATIONAL FIRST DRAFT ONLY
================================================================================
IMPORTANT NOTICE:
- This document is an AI-generated educational starting draft prepared for initial review.
- It does NOT constitute legal advice and does NOT substitute for a qualified Indian advocate.
- This draft has NOT been reviewed, settled, or verified by an advocate.
- You must carefully review and verify all names, facts, dates, legal provisions, and recipient details before any use.
- Do not label this document an advocate-issued notice or imply that it is legally validated.
================================================================================

{st.session_state.document_draft}

================================================================================
VERIFICATION & SAFEGUARDS CHECKLIST BEFORE USE:
1. Verify all facts, dates, names, amounts, and addresses for accuracy.
2. Replace all placeholder brackets (e.g., [SENDER FULL NAME], [RECIPIENT NAME / DESIGNATION / ORGANISATION], [CITY, STATE]) with verified information.
3. Check relevant statutes on official portals (such as https://www.indiacode.nic.in/).
4. Have this draft reviewed and settled by a qualified Indian advocate before formal transmission.
================================================================================
"""
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📄 Download draft as TXT",
                data=download_payload,
                file_name="legalsaathi_draft.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            if Document is None:
                st.info("ℹ️ DOCX download requires `python-docx` to be installed.")
            else:
                try:
                    docx_bytes = generate_docx_bytes(st.session_state.document_draft)
                    st.download_button(
                        "📝 Download draft as DOCX",
                        data=docx_bytes,
                        file_name="legalsaathi_draft.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                except Exception as docx_err:
                    st.error(f"⚠️ Could not generate DOCX file: {docx_err}")

elif page == "About & Sources":
    st.markdown("""
    <div class="ls-section-heading">ℹ️ About LegalSaathi AI</div>
    <div class="ls-section-sub">An academic Indian LegalTech prototype built with Streamlit and Google Gemini</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ls-card" style="border-left: 4px solid #D4B47A;">
        <h4 style="font-size: 1.15rem; margin-bottom: 0.45rem;">🌿 Welcome to LegalSaathi AI</h4>
        <p style="margin-bottom: 0.9rem; line-height: 1.6;">
            LegalSaathi AI is an Indian LegalTech companion designed to bring calm clarity to legal queries and document drafting. Built for educational guidance and academic demonstration, it helps citizens understand procedural options and prepare structured first drafts for advocate review.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.85rem; margin-top: 0.75rem;">
            <div style="background: #E8EDE5; border: 1px solid #D2DDD0; border-radius: 8px; padding: 1rem;">
                <div style="font-weight: 700; color: #24463B; font-size: 0.95rem; margin-bottom: 0.35rem;">💬 Legal Chat Assistant</div>
                <div style="font-size: 0.84rem; color: #343831; margin-bottom: 0.65rem; line-height: 1.5;">
                    Ask questions on consumer rights, workplace disputes, tenancy rules, and criminal law transitions (BNS / BNSS / BSA) in English, Hindi, or Hinglish.
                </div>
                <div style="font-size: 0.78rem; font-weight: 600; color: #24463B;">👈 Select "Legal Chat" in the sidebar</div>
            </div>
            <div style="background: #E8EDE5; border: 1px solid #D2DDD0; border-radius: 8px; padding: 1rem;">
                <div style="font-weight: 700; color: #24463B; font-size: 0.95rem; margin-bottom: 0.35rem;">📝 Document Draft Assistant</div>
                <div style="font-size: 0.84rem; color: #343831; margin-bottom: 0.65rem; line-height: 1.5;">
                    Generate structured formal representations, refund requests, consumer complaints, and tenancy letters with one-click TXT &amp; DOCX export.
                </div>
                <div style="font-size: 0.78rem; font-weight: 600; color: #24463B;">👈 Select "Document Draft" in the sidebar</div>
            </div>
        </div>
    </div>

    <div class="ls-card">
        <h4>⚖️ What This Prototype Does</h4>
        <ul>
            <li><strong>Plain-Language Legal Explanations:</strong> Helps citizens understand Indian civil, consumer, labor, and tenancy procedures.</li>
            <li><strong>Criminal Law Transition Awareness:</strong> Incorporates the July 1, 2024 transition from IPC, CrPC, and IEA to BNS, BNSS, and BSA.</li>
            <li><strong>Structured First Drafts:</strong> Produces clean starting letters for formal representations with standardized uppercase placeholders.</li>
            <li><strong>Restrained &amp; Safe Guidance:</strong> Contextual helplines (112, 1930, 1915, 181, 1098) without making false legal outcome guarantees.</li>
        </ul>
    </div>

    <div class="ls-card">
        <h4>🏛️ Official Indian Legal Portals</h4>
        <p>Always verify statutory sections, court procedures, and filing deadlines with authorized sources:</p>
        <ul>
            <li><a href="https://www.indiacode.nic.in/" target="_blank"><strong>India Code Portal</strong></a> — Official central and state legislation database.</li>
            <li><a href="https://doj.gov.in/" target="_blank"><strong>Department of Justice, Govt. of India</strong></a> — Legal aid, e-Courts, and administration of justice.</li>
            <li><a href="https://nalsa.gov.in/" target="_blank"><strong>National Legal Services Authority (NALSA)</strong></a> — Free legal aid under the Legal Services Authorities Act.</li>
            <li><a href="https://cybercrime.gov.in/" target="_blank"><strong>National Cyber Crime Reporting Portal</strong></a> (Helpline 1930) — Official portal for reporting cyber financial fraud.</li>
            <li><a href="https://consumerhelpline.gov.in/" target="_blank"><strong>National Consumer Helpline (NCH 1915)</strong></a> — Grievance redressal before consumer commissions.</li>
            <li><a href="https://ecourts.gov.in/" target="_blank"><strong>e-Courts Services Portal</strong></a> — Nationwide case status and registry portal.</li>
        </ul>
    </div>

    <div class="ls-notice">
        <strong>Academic Demonstration Limitations:</strong> This software is an educational prototype developed for a final-year BTech CSE project. It does not verify claims against live court registries or updated legislation databases. It does not provide legal advice, representation, or guarantee outcomes. Do not rely on it alone for court filings, criminal proceedings, or emergency situations.
    </div>
    """, unsafe_allow_html=True)
    st.caption("Prototype version 1.0 • Built for academic demonstration with Google Gemini")

st.divider()
st.markdown("""
<div class="ls-footer">
    LegalSaathi AI is an educational technology prototype. It does not provide formal legal advice. Always verify legal provisions from official Indian sources such as <a href="https://www.indiacode.nic.in/" target="_blank">India Code</a>.
</div>
""", unsafe_allow_html=True)
