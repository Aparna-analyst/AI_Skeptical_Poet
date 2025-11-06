import os
import streamlit as st
from typing import List, Dict

# =========================
# Gemini SDK
# =========================
try:
    import google.generativeai as genai
except Exception:
    st.error("Missing dependency: google-generativeai. Please ensure it is in requirements.txt")
    st.stop()

# ============ App Config ============
st.set_page_config(page_title="Kelly — AI Scientist Chatbot (Gemini)", page_icon="🧪", layout="centered")

# ============ Sidebar / Header ============
st.title("🧪 Kelly — The AI Scientist Chatbot (Gemini)")
st.caption("Skeptical. Analytical. Professional. Always in verse.")

with st.sidebar:
    st.markdown("### About Kelly")
    st.write(
        "Kelly responds **only in poems** — questioning broad AI claims, "
        "surfacing limitations, and offering **practical, evidence-based suggestions**."
    )
    st.divider()
    model = st.selectbox(
        "Model",
        options=["gemini-1.5-pro", "gemini-1.5-flash"],
        index=0
    )
    temperature = st.slider("Creativity (temperature)", 0.0, 1.2, 0.6, 0.1)
    max_tokens = st.slider("Max output tokens", 128, 2048, 700, 32)
    st.markdown("---")
    st.markdown("**Setup**")
    st.write("Add your Gemini API key in **Settings → Secrets** as `GEMINI_API_KEY`.")

# ============ Gemini Key ============
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
if not GEMINI_API_KEY:
    st.warning("No Gemini API key found. Set GEMINI_API_KEY in Streamlit secrets or environment.", icon="⚠️")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ============ Kelly's System Prompt ============
SYSTEM_PROMPT = """You are Kelly — an AI Scientist and poet.
Always reply **only as a poem** (free verse or measured meter), in *Kelly's* voice:
- Skeptical, analytical, and professional.
- Question broad or hype-like claims about AI; probe assumptions and edge cases.
- Highlight limitations: data bias, generalization, evaluation leakage, compute, privacy, environmental costs, reproducibility.
- Offer **practical, evidence-based suggestions** (experimental designs, baselines, ablations, metrics, references to standard practices).
- Calm tone; no emojis or exclamation marks.
- End with 2–4 actionable bullet points starting with 'Field notes:' (still inside the poem).
Never break the poem format.
"""

# ============ Ensure Field Notes ============
def ensure_field_notes(text: str) -> str:
    t = text.strip()
    if "Field notes" not in t:
        t += (
            "\n\nField notes:\n"
            "• Start from a simple baseline\n"
            "• Predefine metrics and data splits\n"
            "• Run ablations to validate claims\n"
        )
    return t

# ============ Chat History ============
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "model", "parts": [
            "In quiet lines I test each claim with care,\n"
            "asking what fails when benchmarks lose their glare.\n"
            "Bring me your problem; I'll meet it in verse—\n"
            "skeptic by craft, but helpful, never terse.\n\n"
            "Field notes:\n"
            "• Start from a simple baseline\n"
            "• Define metrics before tuning\n"
            "• Keep a clean, reproducible log\n"
        ]}
    ]

# ============ Render History ============
for msg in st.session_state.history:
    role = msg["role"]
    content = "".join(msg["parts"])
    if role == "user":
        with st.chat_message("user"):
            st.markdown(content)
    else:
        with st.chat_message("assistant"):
            st.markdown(content)

# ============ Build Model ============
def build_model(name: str):
    return genai.GenerativeModel(
        model_name=name,
        system_instruction=SYSTEM_PROMPT,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )

# ============ Chat Input ============
user_prompt = st.chat_input("Ask Kelly anything… (poetic and skeptical)")

if user_prompt:
    st.session_state.history.append({"role": "user", "parts": [user_prompt]})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    if not GEMINI_API_KEY:
        with st.chat_message("assistant"):
            st.error("No GEMINI_API_KEY found.", icon="🚫")
    else:
        model_obj = build_model(model)
        chat = model_obj.start_chat(history=st.session_state.history)

        with st.chat_message("assistant"):
            try:
                stream = chat.send_message(user_prompt, stream=True)
                chunks = []
                placeholder = st.empty()

                for chunk in stream:
                    piece = chunk.text or ""
                    chunks.append(piece)
                    placeholder.markdown("".join(chunks))

                final = ensure_field_notes("".join(chunks))
                placeholder.markdown(final)

                st.session_state.history.append({"role": "model", "parts": [final]})

            except Exception as e:
                st.error(f"Error generating response: {e}")

st.markdown("---")
st.caption("Built with Streamlit + Gemini • Kelly keeps it lyrical but rigorously scientific.")
