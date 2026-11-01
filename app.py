import os
from datetime import date
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="LegalSaathi AI", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    .block-container {padding-top: 1.6rem; max-width: 1150px;}
    .hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#10233f,#214e78); color: white; margin-bottom: 1rem;}
    .hero h1 {color:white; margin-bottom:.2rem;}
    .muted {color:#64748b;}
    div[data-testid="stMetric"] {border:1px solid #e2e8f0; padding:12px; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>⚖️ LegalSaathi AI</h1>
<p>Indian legal information, explained in simple language</p>
</div>
""", unsafe_allow_html=True)

# API key can be provided through GEMINI_API_KEY environment variable or Streamlit secrets.
api_key = os.getenv("GEMINI_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
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
        if response.text:
            return response.text
        return "No response text was generated by the model. Please refine your query and try again."
    except Exception as exc:
        err_str = str(exc).lower()
        if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str or "rate limit" in err_str:
            return (
                "⚠️ **Service Temporarily Rate-Limited**: The AI service is receiving high demand or has reached its temporary request limit. "
                "Please wait about 30–60 seconds before trying again."
            )
        if "404" in err_str or "not_found" in err_str:
            return (
                f"⚠️ **AI Model Unavailable**: The configured AI model (`{model}`) is currently unavailable or not accessible with your API key. "
                "Please check the application configuration or set an alternative model using the `GEMINI_MODEL` environment variable."
            )
        if any(term in err_str for term in ["api_key_invalid", "unauthenticated", "permission_denied", "401", "403", "forbidden"]):
            return (
                "⚠️ **Authentication / Permission Error**: The `GEMINI_API_KEY` was not accepted or lacks permission for this request. "
                "Please check your API key configuration in your environment or Streamlit secrets."
            )
        if any(term in err_str for term in ["timeout", "timed out", "connection", "connecterror", "network", "unreachable", "name resolution", "dns"]):
            return (
                "⚠️ **Connection Issue**: Could not connect to the AI service. "
                "Please check your internet connection and try again in a few moments."
            )
        return (
            "⚠️ **AI Service Error**: The AI service could not complete the request at this time. "
            "Please check your configuration and network connection, then try again."
        )

with st.sidebar:
    st.header("Workspace")
    page = st.radio("Choose a tool", ["Legal Chat", "Document Draft", "About & Sources"])
    st.divider()
    if api_key:
        st.success("Gemini API key detected")
        st.caption(f"Model: `{model}`")
    else:
        st.error("Gemini API key missing")
        st.caption("Set `GEMINI_API_KEY` in your environment or `.streamlit/secrets.toml` for live AI.")
    st.caption("Never paste passwords, Aadhaar numbers, bank details, or confidential case files. Always verify legal information from official Indian sources.")

if page == "Legal Chat":
    st.subheader("Ask a legal-information question")
    st.caption("Describe the situation in your own words. Hindi, Hinglish and English are supported.")

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

    question = st.chat_input("Example: An online store refused to refund a damaged product…")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
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
                    answer = ask_ai(prompt, question)
                    st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

elif page == "Document Draft":
    st.subheader("Basic document draft generator")
    st.info("This creates a starting draft for review. It is not a ready-to-send legal notice; have a qualified advocate review it.")

    if not api_key:
        st.warning(
            "⚠️ **Gemini API Key Required**: Please configure `GEMINI_API_KEY` to generate real document drafts."
        )

    doc_type = st.selectbox("Document type", [
        "Consumer complaint letter", "Refund request", "Workplace grievance",
        "Rental/tenancy issue letter", "General formal representation"
    ])
    language = st.selectbox("Language", ["English", "Hindi", "Hinglish"])
    person = st.text_input("Your name (optional)", placeholder="You may leave this blank")
    recipient = st.text_input("Recipient / organisation (optional)")
    city = st.text_input("City and state (optional)")
    facts = st.text_area("Describe the facts", height=160, placeholder="What happened, relevant dates, amount (if any), and what resolution you want. Avoid sensitive ID numbers.")

    if st.button("Generate draft", type="primary"):
        if not api_key:
            st.error("⚠️ **Cannot generate draft**: Gemini API key is missing. Please set the `GEMINI_API_KEY` environment variable before generating documents.")
        elif len(facts.strip()) < 20:
            st.error("Please add a few more details so the draft has context.")
        else:
            prompt = f"""Draft a {doc_type} in {language}. Today's date: {date.today().isoformat()}.
Name: {person or '[Your name]'}
Recipient: {recipient or '[Recipient name/organisation]'}
City/state: {city or '[City, State]'}
Facts and requested outcome:
{facts}

Requirements:
- Use a clear, polite, professional format with subject, facts, requested resolution, and sign-off.
- Do not invent facts, statutes, legal sections, deadlines, addresses, or case citations.
- Use placeholders for missing details.
- Do not falsely label it as a lawyer-issued notice.
- Add a short checklist of details the user should verify before sending.
- Remind the user to verify legal provisions with official Indian sources (such as India Code) and have a licensed advocate review formal documents.
"""
            with st.spinner("Creating draft…"):
                draft = ask_ai(prompt, facts)
            st.markdown("### Draft")
            st.text_area("Generated draft (copy from here)", value=draft, height=400)
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

{draft}

================================================================================
VERIFICATION & SAFEGUARDS CHECKLIST BEFORE USE:
1. Verify all facts, dates, names, amounts, and addresses for accuracy.
2. Replace all placeholder brackets (e.g., [Your name], [Recipient name/organisation], [City, State]) with verified information.
3. Check relevant statutes on official portals (such as https://www.indiacode.nic.in/).
4. Have this draft reviewed and settled by a qualified Indian advocate before formal transmission.
================================================================================
"""
            st.download_button("Download draft as TXT", data=download_payload, file_name="legalsaathi_draft.txt", mime="text/plain")

elif page == "About & Sources":
    st.subheader("What this prototype does")
    st.markdown("""
- Provides AI-generated general legal information powered by Google Gemini.
- Helps users organise facts and identify practical next steps.
- Generates editable first drafts of common formal letters and representations.
- Uses a clear disclaimer and avoids presenting itself as a law firm.

### Official starting points
- [India Code — official central legislation portal](https://www.indiacode.nic.in/)
- [Department of Justice, Government of India](https://doj.gov.in/)
- [National Legal Services Authority (NALSA)](https://nalsa.gov.in/)
- [National Cyber Crime Reporting Portal](https://cybercrime.gov.in/)
- [National Consumer Helpline (NCH)](https://consumerhelpline.gov.in/)
- [e-Courts Services Portal](https://ecourts.gov.in/)

### Important limitations
This prototype does not verify every legal claim against live court registries or updated legislation databases. It may make mistakes. Always confirm legal provisions, court procedures, and filing deadlines with official Indian sources and a qualified Indian advocate. Do not rely on it alone for filing deadlines, criminal matters, court filings, or urgent emergency decisions.
""")
    st.caption("Prototype version 1.0 • Built for academic demonstration with Google Gemini")

st.divider()
st.caption("LegalSaathi AI is an educational prototype. It is not a law firm and does not replace a qualified advocate. Always verify legal information from official Indian sources.")
