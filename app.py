import os
import textwrap

import streamlit as st
from dotenv import load_dotenv

from rag_pipeline import CyberGuardRAG
from ui_components import (
    render_header,
    render_sidebar,
    render_results,
    render_use_cases,
    render_how_it_works,
)

load_dotenv()

st.set_page_config(
    page_title="CyberGuard AI – Real‑Time Threat Briefings",
    page_icon="🛡️",
    layout="wide",
)

def init_rag():
    if "rag" not in st.session_state:
        st.session_state.rag = CyberGuardRAG()
    return st.session_state.rag


def main():
    render_header()

    rag = init_rag()

    with st.sidebar:
        render_sidebar(rag)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Ask about any cybersecurity threat or incident")

        default_prompt = (
            "Give me an executive-ready briefing on recent ransomware activity "
            "targeting healthcare in the US. Include top threats, notable incidents "
            "from the last 6–12 months, and recommended mitigations for a mid-size company."
        )

        user_query = st.text_area(
            "Your question",
            value=default_prompt,
            height=160,
            help="Ask about a specific threat, industry, or incident. The app will research the web in real time.",
        )

        threat_focus = st.selectbox(
            "Focus area (optional)",
            [
                "All threats",
                "Ransomware",
                "Cloud & SaaS security",
                "Supply‑chain / third‑party risk",
                "AI & LLM security",
                "Identity & access (IAM)",
            ],
        )

        detail_level = st.select_slider(
            "Depth of analysis",
            options=["High-level summary", "Balanced", "Deep dive"],
            value="Balanced",
        )

        run_button = st.button("🚀 Generate Threat Briefing", type="primary")

        if run_button:
            if not user_query.strip():
                st.warning("Please enter a question first.")
            else:
                with st.spinner("Researching live sources and generating your briefing..."):
                    result = rag.generate_briefing(
                        query=user_query,
                        focus_area=threat_focus,
                        detail_level=detail_level,
                    )
                render_results(result)

    with col_right:
        render_use_cases()
        st.markdown("---")
        render_how_it_works()


if __name__ == "__main__":
    main()
