# LegalSaathi AI — Indian Legal Information Assistant

A minimal Indian legal-information assistant built with **Streamlit** and the **Google Gemini API** using the `google-genai` Python SDK.

## Features
- **Legal Chat**: Conversational interface for educational and general legal information in English, Hindi, and Hinglish.
- **Document Draft**: Editable first drafts for common letters (consumer complaints, refund requests, workplace grievances, rental issues, formal representations).
- **About & Sources**: Direct links to official Indian legislation and legal aid portals.

## Requirements
- Python 3.10+
- A Google Gemini API key (`GEMINI_API_KEY`) from [Google AI Studio](https://aistudio.google.com/)
- Internet access for AI responses

## Run locally (macOS/Linux)
```bash
cd legalsaathi_ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY="your_gemini_api_key_here"
streamlit run app.py
```

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY="your_gemini_api_key_here"
streamlit run app.py
```

### Streamlit Secrets (Alternative)
You can also configure your API key locally by creating `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### Model Selection
By default, LegalSaathi AI uses `gemini-3.8-flash`. You can override this using the `GEMINI_MODEL` environment variable:
```bash
export GEMINI_MODEL="gemini-3.8-flash"
```

## Missing API Key Behavior
If `GEMINI_API_KEY` is not configured, the application displays a clear setup message guiding you to set the environment variable or configure Streamlit secrets. It does not silently return demo responses.

## Security & Privacy
- **Never hardcode or commit your API key.**
- `.env`, `.streamlit/secrets.toml`, and `.venv/` are listed in `.gitignore`.
- Do not paste sensitive personal identifiers (Aadhaar numbers, PAN, bank account details, passwords) or confidential case files.
- The application reads the key securely from the environment without printing or logging it.

## Legal Disclaimer & Official Sources
LegalSaathi AI is an educational prototype. It does not provide formal legal advice and does not establish an advocate-client relationship.

Users must always verify legal information and statutory provisions against official Indian sources:
- **India Code (Official Central Legislation)**: [https://www.indiacode.nic.in/](https://www.indiacode.nic.in/)
- **Department of Justice, Government of India**: [https://doj.gov.in/](https://doj.gov.in/)
- **National Legal Services Authority (NALSA)**: [https://nalsa.gov.in/](https://nalsa.gov.in/)
- For court filings, formal notices, or urgent legal matters, consult a qualified, licensed Indian advocate.

## Quick Test Plan
1. **API Key Setup Check**: Run the app without `GEMINI_API_KEY` set. Confirm that the sidebar reports `Gemini API key missing` and Legal Chat / Document Draft show clear setup messages rather than silent demo responses.
2. **API Key Detection**: Set `export GEMINI_API_KEY="..."` and launch the app. Confirm the sidebar displays `Gemini API key detected`.
3. **Legal Chat**: Ask: *"An online seller delivered a damaged product and refuses a refund. What information should I collect and what general legal options can I explore in India?"* Confirm a live Gemini response is generated with appropriate disclaimers.
4. **Document Draft**: Select *Consumer complaint letter*, fill in non-sensitive details, and click *Generate draft*. Verify that a structured draft is generated and can be downloaded as a TXT file.
5. **About & Sources**: Navigate to *About & Sources* and verify the official portal links open properly.
