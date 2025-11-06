# Kelly — The AI Scientist Chatbot (Streamlit)

Kelly responds **only in poems**. Tone: skeptical, analytical, professional.  
Each answer questions broad AI claims, surfaces limitations, and closes with **Field notes** (practical, evidence-based steps).

## ✨ Features
- Streamlit chat interface
- OpenAI Chat Completions (streaming)
- Strong system prompt guarantees: poem-only, skeptical tone, limitations, and actionable bullets
- Lightweight post-processor to enforce a 'Field notes' section

## 🚀 Local Run
1. Create a virtual environment and install deps:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI key:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
3. Launch:
   ```bash
   streamlit run streamlit_app.py
   ```

## ☁️ One-Click Deploy (Streamlit Community Cloud)
1. Push these files to a **public GitHub repo** (e.g., `kelly-ai-scientist-chatbot`).
2. Go to **share.streamlit.io** → **New app**.
3. Select your repo/branch and set **Main file path** to `streamlit_app.py`.
4. In **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY="sk-..."
   ```
5. Click **Deploy**. Your app URL will look like:
   `https://<your-username>-kelly-ai-scientist-chatbot.streamlit.app`

## 🔧 Configuration
- Choose model from the sidebar (`gpt-5-thinking`, `gpt-4o`, or `gpt-4.1-mini`).
- Adjust temperature and max tokens as desired.

## 🧪 Guaranteeing the Style
- The system prompt hard-requires poem-only responses.
- The app appends a minimal 'Field notes' block if the model forgets to include it.
