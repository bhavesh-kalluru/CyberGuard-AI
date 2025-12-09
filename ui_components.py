import streamlit as st
import textwrap


def render_header():
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #22c1c3, #4a00e0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .sub-header {
            font-size: 0.95rem;
            color: #94a3b8;
        }
        .pill {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 500;
            background: rgba(56, 189, 248, 0.12);
            color: #38bdf8;
            margin-right: 0.35rem;
            border: 1px solid rgba(56, 189, 248, 0.25);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-header">🛡️ CyberGuard AI – Real‑Time Threat Briefings</div>
        <p class="sub-header">
            A Streamlit + GenAI web‑RAG app that turns live web data into executive‑ready cybersecurity briefings.
        </p>
        <div style="margin-top:0.4rem; margin-bottom:1.0rem;">
            <span class="pill">#RAG</span>
            <span class="pill">Perplexity‑powered search</span>
            <span class="pill">OpenAI reasoning</span>
            <span class="pill">Built with Streamlit</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(rag):
    st.markdown("### ⚙️ Runtime configuration")

    with st.expander("API key status", expanded=True):
        has_openai = bool(rag.openai_client)
        has_pplx = bool(rag.perplexity_client)

        st.write(
            f"✅ OPENAI_API_KEY loaded"
            if has_openai
            else "❌ OPENAI_API_KEY is missing – set it in your `.env` file."
        )
        st.write(
            f"✅ PERPLEXITY_API_KEY loaded"
            if has_pplx
            else "❌ PERPLEXITY_API_KEY is missing – set it in your `.env` file."
        )

        st.caption(
            "Keys are read from a local `.env` file using `python-dotenv`. "
            "The `.env` file is ignored by Git so you never commit secrets."
        )

    st.markdown("---")
    st.markdown("### 💡 Pro tips")
    st.write(
        "- Ask about *specific* incidents, sectors, or technologies.\n"
        "- Use the focus dropdown to steer Perplexity toward the right slice of the threat landscape.\n"
        "- Try the **Deep dive** option for more technical details."
    )

    st.markdown("---")
    st.markdown("### 📌 Example questions")
    st.caption(
        "- \"How are ransomware gangs monetizing access to healthcare orgs in 2025?\"\n"
        "- \"What do we know about recent supply‑chain compromises in CI/CD tools?\"\n"
        "- \"What are emerging attack patterns against LLM‑enabled internal tools?\""
    )


def render_results(result):
    st.markdown("### 📊 Threat briefing")

    st.markdown(
        f"""
        <div style="padding:0.8rem 1rem; border-radius:0.9rem; border:1px solid rgba(148, 163, 184, 0.4); background-color:rgba(15,23,42,0.35);">
            <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em; color:#64748b; margin-bottom:0.25rem;">
                Heuristic risk level
            </div>
            <div style="font-weight:600; color:#e5e7eb;">{result.risk_score}</div>
            <div style="font-size:0.8rem; color:#9ca3af; margin-top:0.35rem;">
                {result.audience}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### 🧾 Structured analysis")
    st.markdown(result.answer)

    with st.expander("🔍 Under the hood – web research context"):
        st.caption(
            "This is the raw web‑grounded context returned by Perplexity before being "
            "shaped into the final briefing by OpenAI."
        )
        st.markdown(result.web_context)

    st.caption(f"ℹ️ {result.sources_hint}")


def render_use_cases():
    st.markdown("### 🎯 Where this app is useful")

    st.markdown(
        """
        - **Security leadership:** Get a fast, defensible briefing before exec reviews or board decks.  
        - **Blue teams & IR:** Quickly scan what's publicly known about a new campaign or CVE.  
        - **Builders:** Use the codebase as a pattern for web‑RAG with Perplexity + OpenAI + Streamlit.  
        """
    )

    st.markdown("### 🧱 Tech stack")
    st.caption(
        "- Streamlit for the web UI\n"
        "- Perplexity's Sonar models for live web research\n"
        "- OpenAI models for structured reasoning and formatting\n"
        "- Python, dockerized for easy deployment (e.g., Render, Docker, k8s)"
    )


def render_how_it_works():
    st.markdown("### ⚙️ How it works")

    st.markdown(
        """
        1. **You ask a question** about a threat, sector, or incident.  
        2. **Perplexity API** searches the live web and returns a concise threat‑intel style summary with links.  
        3. **OpenAI** turns those notes into a structured, audience‑aware briefing.  
        4. The UI shows a **risk level**, the **final briefing**, and the **underlying web context**.  
        """
    )

    st.caption(
        "Important: this app is for educational and research purposes. "
        "Always validate findings against your own sources and internal telemetry."
    )
