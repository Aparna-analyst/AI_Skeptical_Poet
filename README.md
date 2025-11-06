# Kelly — The AI Scientist Chatbot  
Powered by Groq (llama-3.1-8b-instant) • Built with Streamlit

Kelly is an AI Scientist who responds only in poems — skeptical, analytical, and grounded in evidence. Every answer questions assumptions, highlights limitations, and ends with “Field notes,” a set of practical, actionable scientific steps.

This project uses Groq’s ultra-fast llama-3.1-8b-instant model for real-time inference.

------------------------------------------------------------
FEATURES
------------------------------------------------------------

Kelly’s Scientific Poetic Persona:
- Writes entirely in poetic form
- Uses a skeptical, analytical tone
- Questions hype-driven AI claims
- Highlights limitations: bias, generalization, compute, reproducibility
- Gives evidence-based guidance: baselines, ablations, metrics
- Ends every reply with “Field notes”

Groq-Powered Llama 3:
- Extremely fast inference (sub-10ms)
- Free-tier friendly
- Perfect for Streamlit Cloud

Streamlit UI:
- Smooth streaming responses
- Adjustable temperature and max tokens
- Persistent chat history

------------------------------------------------------------
TECH STACK
------------------------------------------------------------

- Python 3.10+
- Groq API (llama-3.1-8b-instant)
- Streamlit
- groq-python SDK

------------------------------------------------------------
RUN LOCALLY
------------------------------------------------------------

1. Install dependencies:
    pip install -r requirements.txt

2. Set your Groq API key:

   On Windows CMD:
        setx GROQ_API_KEY "your-groq-api-key"

   On macOS / Linux:
        export GROQ_API_KEY="your-groq-api-key"

3. Start the app:
    streamlit run streamlit_app.py

------------------------------------------------------------
DEPLOY TO STREAMLIT CLOUD
------------------------------------------------------------

1. Push the project to a public GitHub repo.

2. Go to: https://share.streamlit.io → New app

3. Set the main file to:
    streamlit_app.py

4. Add your API key (Settings → Secrets):
    GROQ_API_KEY="your-groq-api-key"

5. Deploy — you will get a URL like:
    https://<your-username>-kelly-groq-streamlit.streamlit.app

------------------------------------------------------------
FILE STRUCTURE
------------------------------------------------------------

streamlit_app.py      - Main app
requirements.txt       - Dependencies
README.md              - Documentation
LICENSE                - MIT License

------------------------------------------------------------
ABOUT “FIELD NOTES”
------------------------------------------------------------

Field notes are short, practical scientific reminders included at the end of every poem. They reinforce Kelly’s identity as a poetic yet rigorous scientist, summarizing actionable steps such as defining baselines, metrics, testing assumptions, and ensuring reproducibility.

------------------------------------------------------------
LICENSE
------------------------------------------------------------

Released under the MIT License.

