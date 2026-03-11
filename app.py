import streamlit as st
from openai import OpenAI, RateLimitError, OpenAIError
from dotenv import load_dotenv
import os
from pathlib import Path

# Load API key from .env file
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))


def generate_fallback_analysis(conversation: str) -> str:
    lines = [line.strip() for line in conversation.splitlines() if line.strip()]
    customer_lines = [line for line in lines if line.lower().startswith("customer:")]
    agent_lines = [line for line in lines if line.lower().startswith("agent:")]

    negative_markers = ["not", "can't", "cant", "problem", "late", "delay", "angry", "upset", "goodbye"]
    empathy_markers = ["sorry", "understand", "help", "thanks", "please"]

    text_lower = conversation.lower()
    customer_negative = any(marker in " ".join(customer_lines).lower() for marker in negative_markers)
    agent_negative = any(marker in " ".join(agent_lines).lower() for marker in ["can't", "cant", "goodbye"])
    agent_empathy = any(marker in " ".join(agent_lines).lower() for marker in empathy_markers)

    customer_score = 3 if customer_negative else 6
    agent_score = 4 if agent_negative else (7 if agent_empathy else 6)
    overall_score = round((customer_score + agent_score) / 2)

    overall_tone = (
        "The conversation appears tense and partially unresolved. "
        "The customer shows signs of frustration, and the interaction could have been handled with more empathy and guidance."
        if customer_negative or agent_negative
        else "The conversation appears mostly neutral. Both sides exchange information, though there is room for clearer support and structure."
    )

    breakdown_points = [
        "The issue is not fully acknowledged with empathy before requesting additional details.",
        "The conversation moves to a hard stop instead of offering alternative next steps.",
        "Expectations and ownership are not clearly communicated."
    ]
    if "order" in text_lower:
        breakdown_points[0] = "The customer reports an order delay, but emotional acknowledgment is limited before troubleshooting."

    what_went_well = [
        "The agent attempts to gather information needed to investigate.",
        "The conversation stays focused on the core issue.",
        "The exchange is concise and easy to follow."
    ]

    suggestions = [
        "Start with empathy (e.g., acknowledge delay/frustration) before asking for details.",
        "If required information is missing, offer alternatives (email lookup, phone number, or follow-up path).",
        "Close with a clear next step and timeline instead of ending the conversation abruptly."
    ]

    return f"""
## Overall Tone
{overall_tone}

## Sentiment Score
- Customer Sentiment: {customer_score}/10
- Agent Performance: {agent_score}/10
- Overall Experience: {overall_score}/10

## Communication Breakdown
- {breakdown_points[0]}
- {breakdown_points[1]}
- {breakdown_points[2]}

## What Went Well
- {what_went_well[0]}
- {what_went_well[1]}
- {what_went_well[2]}

## Improvement Suggestions
- {suggestions[0]}
- {suggestions[1]}
- {suggestions[2]}

## Summary
The conversation captures the customer issue but misses empathetic handling and a constructive resolution path.
"""

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="ConvoLens",
    page_icon="🔍",
    layout="centered"
)

# ── Header ────────────────────────────────────────────────────
st.title("🔍 ConvoLens")
st.subheader("AI-Powered Conversation Analyzer")
st.write("Paste any conversation below — customer support, sales call, chat transcript — and get instant AI analysis.")

st.divider()

# ── Input ─────────────────────────────────────────────────────
conversation = st.text_area(
    label="Paste your conversation here:",
    placeholder="""Example:
Customer: Hi, my order hasn't arrived yet and it's been 2 weeks.
Agent: What's your order number?
Customer: I don't have it handy.
Agent: I can't help without it. Goodbye.""",
    height=250
)

analyze_btn = st.button("🔍 Analyze Conversation", use_container_width=True)

# ── Analysis ──────────────────────────────────────────────────
if analyze_btn:
    if not conversation.strip():
        st.warning("Please paste a conversation first!")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.warning("OPENAI_API_KEY not found. Using offline fallback analysis.")
            result = generate_fallback_analysis(conversation)
        else:
            client = OpenAI(api_key=api_key)

        with st.spinner("Analyzing conversation..."):

            prompt = f"""
You are an expert communication analyst. Analyze the following conversation and provide a structured report.

CONVERSATION:
{conversation}

Provide your analysis in exactly this format:

## Overall Tone
[Describe the overall tone of the conversation in 2-3 sentences]

## Sentiment Score
[Give a score from 1-10 for: Customer Sentiment, Agent Performance, Overall Experience. Format as a list]

## Communication Breakdown
[Identify specific moments where communication broke down or could have gone better. Be specific about what was said]

## What Went Well
[List 2-3 things that were handled well in this conversation]

## Improvement Suggestions
[Give 3 specific, actionable suggestions for how the agent could have handled this better]

## Summary
[One sentence summary of the conversation quality]
"""

            if api_key:
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert communication analyst who helps businesses improve their customer interactions."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    result = response.choices[0].message.content
                except RateLimitError:
                    st.warning("OpenAI quota exceeded (HTTP 429). Showing offline fallback analysis instead.")
                    result = generate_fallback_analysis(conversation)
                except OpenAIError as exc:
                    st.warning(f"OpenAI API error ({exc}). Showing offline fallback analysis instead.")
                    result = generate_fallback_analysis(conversation)

        # ── Display Results ────────────────────────────────────
        st.divider()
        st.subheader("📊 Analysis Results")
        st.markdown(result)

        st.divider()
        st.success("✅ Analysis complete! Copy or screenshot your results above.")

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption("Built by Adedamola Olayefun · ConvoLens v1.0 · Powered by OpenAI")