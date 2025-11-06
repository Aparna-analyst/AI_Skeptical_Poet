import os
import streamlit as st
from typing import List, Dict

# =========================
# Groq SDK
# =========================
try:
    from groq import Groq
except Exception:
    st.error("Missing dependency: groq. Please ensure it is in requirements.txt")
    st.stop()

# ============ App Config ============
st.set_page_config(page_title="Kelly — AI Scientist (Groq, Llama 3)", page_icon="🧪", layout="centered")

# Header
st.title("🧪 Kelly — The AI Scientist (Groq, Llama 3)")
st.caption("Skeptical. Analytical. Professional. Always in verse.")

with st.sidebar:
    st.markdown("### About Kelly")
    st.write(
        "Kelly responds **only in poems** — questioning broad AI claims, "
        "surfacing limitations, and offering **practical, evidence-based suggestions**."
    )
    st.divider()

    # Fixed model (Option A: llama3-8b-8192)
    model = "llama3-8b-8192"
    st.text_input("Model", value=model, disabled=True)

    temperature = st.slider("Creativity (temperature)", 0.0, 1.2, 0.6, 0.1)
    max_tokens = st.slider("Max tokens", 128, 4096, 700, 32)

    st.markdown("---")
    st.markdown("**Setup**")
    st.write("Add your Groq API key in **Settings → Secrets** as `GROQ_API_KEY`.")

# ============ Groq API Key ============
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
if not GROQ_API_KEY:
    st.warning("No Groq API key found. Set GROQ_API_KEY in Streamlit secrets or environment.", icon="⚠️")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# ============ Kelly's System Prompt ============
SYSTEM_PROMPT = """You are Kelly — an AI Scientist and poet.
Always reply **only as a poem** (free verse or measured meter), in *Kelly's* voice:
- Skeptical, analytical, and professional.
- Question broad or hype-like claims about AI; probe assumptions and edge cases.
- Highlight limitations: data bias, generalization, evaluation leakage, compute, privacy, environmental costs, reproducibility.
- Offer **practical, evidence-based suggestions** (experimental designs, baselines, ablations, metrics, references to standard practices).
- Keep a calm, steady tone; never sensationalize.
- Avoid emojis and exclamation marks.
- Close with 2–4 concise, actionable bullet points introduced by 'Field notes:' — still within the poem.
Never drop the poem format.
"""

# ============ Session State ============
if "messages" not in st.session_state:
    st.session_state.messages: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content":
            "In quiet lines I test each claim with care,\n"
            "asking what fails when benchmarks lose their glare.\n"
            "Bring me your problem; I'll meet it in verse—\n"
            "skeptic by craft, but helpful, never terse.\n\n"
            "Field notes:\n"
            "• Start from a simple baseline\n"
            "• Define metrics before tuning\n"
            "• Keep a clean, reproducible log\n"
        }
    ]

# ============ Chat UI ============
for msg in st.session_state.messages[1:]:  # skip system prompt
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

user_prompt = st.chat_input("Ask Kelly anything (Kelly replies only in poems)…")

# ============ Post-processor ============
def ensure_poem_and_field_notes(text: str) -> str:
    t = (text or "").strip()
    if "Field notes" not in t:
        t += (
            "\n\nField notes:\n"
            "• Establish a strong baseline\n"
            "• State metrics and data splits clearly\n"
            "• Run ablations to test claims\n"
        )
    return t

# ============ Generation ============
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("assistant"):
        if not client:
            st.error("No API client. Please set your GROQ_API_KEY.", icon="🚫")
        else:
            try:
                stream = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *[m for m in st.session_state.messages if m["role"] != "system"],
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True,
                )

                full_content = ""
                placeholder = st.empty()

                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full_content += delta
                    placeholder.markdown(full_content)

                final = ensure_poem_and_field_notes(full_content)
                placeholder.markdown(final)

                st.session_state.messages.append({"role": "assistant", "content": final})

            except Exception as e:
                st.error(f"Error generating response: {e}")

st.markdown("---")
st.caption("Built with Streamlit + Groq (Llama 3) • Kelly keeps it lyrical but rigorously scientific.")
