# LegalSaathi AI — Indian LegalTech Companion

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20GenAI-SDK-34A853.svg)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An academic Indian LegalTech companion designed to bring calm, accessible clarity to citizen legal inquiries and formal document drafting. Built with **Streamlit** and the **Google Gemini API** (`google-genai` SDK), LegalSaathi AI helps individuals understand procedural options, organize factual records, and prepare structured starting drafts for advocate review.

Developed as a **BTech Computer Science & Engineering Final-Year Major Project** and technical portfolio piece.

---

## 🏛️ Problem Statement & Objective

Accessing formal legal assistance in India can be daunting due to procedural complexity, language barriers, and legal information asymmetry. Many citizens lack a clear understanding of:
- Whether a dispute belongs to consumer commissions, civil courts, or labor tribunals.
- How to structure a formal grievance or representation letter before approaching a lawyer.
- How the July 1, 2024 transition from IPC, CrPC, and IEA to BNS, BNSS, and BSA affects their situation.

**LegalSaathi AI** bridges this initial informational gap by offering:
1. **Plain-Language Legal Guidance**: Explaining procedural pathways, jurisdictional tiers, and necessary evidentiary records in English, Hindi, or Hinglish.
2. **Standardized First-Draft Generation**: Producing structured representations with standardized uppercase placeholders, ready for advocate review and exportable in TXT and DOCX formats.
3. **Rigorous Legal Safeguards**: Refusing to invent citations, hallucinate case law, or guarantee court outcomes, with active helpline suggestions (112, 1930, 1915, 181, 1098).

---

## ✨ Key Features

### 1. 💬 Legal Chat Assistant
- Conversational multi-turn guidance powered by Gemini with strict system safeguards.
- Multilingual assistance in **English**, **Hindi**, and **Hinglish**.
- Criminal law transition awareness (IPC/CrPC/IEA vs BNS/BNSS/BSA).
- Contextual emergency helplines:
  - **112**: Immediate danger / life safety.
  - **1930** & [cybercrime.gov.in](https://cybercrime.gov.in/): Cyber financial fraud.
  - **1915** & [consumerhelpline.gov.in](https://consumerhelpline.gov.in/): Consumer grievances.
  - **181 / 1091**: Women's helplines.
  - **1098**: Childline support.
- Quick-prompt suggested question chips for immediate exploration.

### 2. 📝 Formal Document Draft Assistant
Generates structured educational starting drafts tailored specifically to 5 core representation types:
- **Consumer Complaint Letter** (Consumer Protection Act 2019 / e-Daakhil)
- **Refund Request** (E-commerce, retail, or service defect dispute)
- **Workplace Grievance** (Internal formal representation)
- **Rental / Tenancy Issue Letter** (Maintenance, security deposit refund, lease matters)
- **General Formal Representation** (Administrative, institutional, or civic intimation)

**Export & Safeguards:**
- One-click export to **Plain Text (.TXT)** and formatted **Microsoft Word (.DOCX)**.
- Formatted with formal sender/recipient headers, subject lines, chronological facts, and specific relief requests.
- Standardized uppercase placeholders (e.g., `[SENDER FULL NAME]`, `[DATE OF INCIDENT]`, `[AMOUNT IN INR]`).
- Appended with an Advocate Verification & Safeguards Checklist and "Gaps to Fill Before Sending".

### 3. ℹ️ About & Official Indian Sources
- Direct references to official central portals:
  - **India Code**: [https://www.indiacode.nic.in/](https://www.indiacode.nic.in/)
  - **Department of Justice (Govt. of India)**: [https://doj.gov.in/](https://doj.gov.in/)
  - **National Legal Services Authority (NALSA)**: [https://nalsa.gov.in/](https://nalsa.gov.in/)
  - **National Cyber Crime Reporting Portal**: [https://cybercrime.gov.in/](https://cybercrime.gov.in/)
  - **e-Courts Services Portal**: [https://ecourts.gov.in/](https://ecourts.gov.in/)

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend & UI** | Streamlit 1.40+ | Custom-styled LegalTech UI (Warm Ivory `#F6F3EC`, Forest Green `#24463B`, Muted Gold `#D4B47A`) |
| **Language** | Python 3.10+ | Clean, type-annotated application architecture |
| **AI Integration** | `google-genai` SDK | Official Google GenAI SDK interfacing with `gemini-3.8-flash` |
| **Document Generation** | `python-docx` 1.1+ | OpenXML DOCX document package construction |
| **Asset Pipeline** | Base64 Encoding | Embedded high-resolution local imagery for offline reliability |
| **Deployment Target** | Streamlit Community Cloud | Zero-server cloud deployment with encrypted secrets management |

---

## 📁 Project Structure

```text
legalsaathi_ai/
├── app.py                     # Main Streamlit application with UI, state & Gemini logic
├── requirements.txt           # Production dependencies
├── .gitignore                 # Strict Git hygiene excluding secrets, virtualenvs & caches
├── README.md                  # Comprehensive project documentation
└── assets/
    ├── hero_scales_books_blended.png  # Justice scales hero banner artwork (131 KB)
    └── sidebar_court_blended.png      # Supreme Court sidebar illustration (42 KB)
```

---

## 🚀 Local Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher installed.
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### 2. Clone the Repository
```bash
git clone https://github.com/Sarveshsinghbaghel/legalsaathi-ai.git
cd legalsaathi-ai
```

### 3. Create and Activate Virtual Environment
**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key
Choose one of the two methods below:

**Method A: Environment Variable (Recommended for local dev)**
```bash
# macOS / Linux
export GEMINI_API_KEY="your_gemini_api_key_here"

# Windows PowerShell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

**Method B: Streamlit Secrets File**
Create a local `.streamlit/secrets.toml` file (this file is excluded by `.gitignore` and never committed):
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment Guide (Streamlit Community Cloud)

To deploy LegalSaathi AI publicly on Streamlit Community Cloud:

1. **Push Repository to GitHub**:
   Ensure your code is pushed to your GitHub repository (e.g., `Sarveshsinghbaghel/legalsaathi-ai`) on branch `main`.

2. **Connect Streamlit Community Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
   - Click **New app**.

3. **Configure App Settings**:
   - **Repository**: `Sarveshsinghbaghel/legalsaathi-ai`
   - **Branch**: `main`
   - **Main file path**: `app.py`

4. **Add Encrypted Secrets**:
   - Before deploying, click **Advanced settings...**
   - In the **Secrets** text area, enter your production Gemini API key:
     ```toml
     GEMINI_API_KEY = "your_actual_gemini_api_key"
     ```
   - Click **Save**.

5. **Deploy**:
   - Click **Deploy!**
   - Streamlit Cloud will install dependencies from `requirements.txt` and launch the application.

---

## 🔒 Security, Safety & Privacy

- **Zero Credential Leakage**: API keys are read strictly from runtime environment variables or Streamlit secrets. Keys are never printed, written to logs, exposed in UI error cards, or included in exported files.
- **No Disk or Database Logging**: User chat messages and generated draft facts are retained strictly in-memory within `st.session_state` for the active browser session. When the tab is closed, data is discarded.
- **Sanitized Diagnosis Logging**: Network or API exceptions are categorized (e.g., `AUTHENTICATION_ERROR`, `RATE_LIMITED`, `CONNECTION_ERROR`) without printing raw request URLs or header data to stdout.
- **Zero Third-Party Telemetry**: No external trackers, cookies, or analytics scripts are embedded.

---

## ⚖️ Legal Disclaimer

> **Important Notice:** LegalSaathi AI is an educational technology prototype developed for academic demonstration. It does not provide formal legal representation, advocate advice, or guarantee any dispute outcome.
>
> Indian statutory provisions, case law citations, and procedural timelines must always be verified with official government portals (such as [India Code](https://www.indiacode.nic.in/)) or settled by a licensed Indian advocate before formal transmission or filing.

---

## 🔮 Future Roadmap

- [ ] **e-Courts Registry Integration**: Live status queries for district and high court cases via open judicial APIs.
- [ ] **Vernacular Voice Interface**: Speech-to-text and text-to-speech for rural accessibility in Indian regional languages.
- [ ] **Document OCR Intake**: Ingesting scanned merchant invoices or landlord notices for automated gap analysis.
- [ ] **State-Specific Lexicon Grounding**: Dynamic filtering for state tenancy acts (e.g., Maharashtra Rent Control Act, Delhi Rent Act).

---

## 👤 Author & Acknowledgments

- **Developer**: Sarvesh Singh Baghel
- **Academic Context**: BTech CSE Major Project
- **Institution / Portals**: Grounded in official Indian legislative data from [India Code](https://www.indiacode.nic.in/) and [Department of Justice](https://doj.gov.in/).
