import os
from dataclasses import dataclass
from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI
import textwrap

load_dotenv()


class MissingAPIKeyError(RuntimeError):
    pass


@dataclass
class BriefingResult:
    answer: str
    web_context: str
    risk_score: str
    audience: str
    sources_hint: str


class CyberGuardRAG:
    """
    Simple web‑RAG style pipeline that:
    1. Uses Perplexity's web‑grounded models to gather fresh context.
    2. Uses OpenAI to turn that context into a structured, executive‑ready briefing.
    """

    def __init__(self):
        openai_key = os.getenv("OPENAI_API_KEY")
        pplx_key = os.getenv("PERPLEXITY_API_KEY")

        if not openai_key:
            raise MissingAPIKeyError(
                "OPENAI_API_KEY is not set. Add it to your .env file."
            )
        if not pplx_key:
            raise MissingAPIKeyError(
                "PERPLEXITY_API_KEY is not set. Add it to your .env file."
            )

        # Standard OpenAI client for reasoning / formatting
        self.openai_client = OpenAI(api_key=openai_key)

        # Perplexity is OpenAI‑compatible – we just change base_url
        self.perplexity_client = OpenAI(
            api_key=pplx_key,
            base_url="https://api.perplexity.ai",
        )

    @staticmethod
    def _build_focus_hint(focus_area: str) -> str:
        if focus_area == "Ransomware":
            return "Focus on ransomware campaigns, double‑extortion, data leaks, and impact on operations."
        if focus_area == "Cloud & SaaS security":
            return "Emphasize cloud misconfigurations, SaaS abuse, and identity‑based attacks in cloud environments."
        if focus_area == "Supply‑chain / third‑party risk":
            return "Highlight attacks via suppliers, managed service providers, CI/CD, and software dependencies."
        if focus_area == "AI & LLM security":
            return "Highlight prompt injection, data exfiltration via LLMs, model supply‑chain risks, and AI governance."
        if focus_area == "Identity & access (IAM)":
            return "Emphasize credential theft, phishing, MFA bypass, and privileged access abuse."
        return "Consider the overall threat landscape and pick the most relevant details."

    def _call_perplexity(self, query: str, focus_area: str, detail_level: str) -> str:
        """
        Ask Perplexity to research the live web. We treat its answer
        as 'retrieved context' for the second-stage OpenAI call.

        Note: This uses Perplexity's OpenAI‑compatible chat completions API.
        """
        focus_hint = self._build_focus_hint(focus_area)

        depth_hint = {
            "High-level summary": "Keep it concise (250–350 words).",
            "Balanced": "Write a balanced briefing (400–600 words).",
            "Deep dive": "Go deep (700–900 words) with rich technical detail.",
        }.get(detail_level, "Write a balanced briefing (400–600 words).")

        prompt = textwrap.dedent(
            f"""
            You are a senior cybersecurity analyst.

            Task:
            • Research the very latest, credible, public information from the web.
            • Focus on: {focus_area}.
            • User question: {query}

            Instructions:
            • Start with a short paragraph summarizing what is happening.
            • Then provide 3–7 concise bullet points with key facts and statistics.
            • End with a section called "Sources" that lists numbered links, for example:
              Sources:
              1. https://example.com/article‑1
              2. https://example.com/article‑2

            {focus_hint}
            {depth_hint}
            """
        ).strip()

        completion = self.perplexity_client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": "You are a cybersecurity threat‑intel assistant that always cites sources at the end.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content

    def _call_openai(self, query: str, web_context: str, detail_level: str) -> str:
        """
        Use OpenAI to transform Perplexity's web‑grounded context into
        a polished, structured briefing tailored to security audiences.
        """
        completion = self.openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": textwrap.dedent(
                        """
                        You are "CyberGuard AI", a senior cybersecurity advisor.
                        You turn raw research notes into executive‑ready threat briefings.

                        Requirements:
                        • Be accurate and avoid exaggeration.
                        • If something is uncertain or early‑stage, say so.
                        • Write as if for a CISO or security lead in a mid‑size company.
                        • Use clear section headings and bullet points.
                        """
                    ).strip(),
                },
                {
                    "role": "user",
                    "content": textwrap.dedent(
                        f"""
                        User question:
                        {query}

                        Web research notes (may include numbered Sources at the end):
                        ---
                        {web_context}
                        ---

                        Using ONLY the information above (plus common security best practices),
                        produce a structured briefing with this format:

                        1. Executive Summary (2–4 short bullet points)
                        2. What We Know So Far
                        3. Who Is Most At Risk
                        4. Technical Details (only if available)
                        5. Recommended Actions in the Next 30–90 Days
                        6. One‑Paragraph Brief for Non‑Technical Leadership
                        7. Sources (reuse or clean up the numbered links, do not invent URLs)

                        Depth level requested by the user: {detail_level}
                        """
                    ).strip(),
                },
            ],
        )
        return completion.choices[0].message.content

    @staticmethod
    def _heuristic_risk_score(web_context: str) -> str:
        """
        Very rough heuristic risk scoring just to make the UI more interesting.
        """
        ctx_lower = web_context.lower()
        score = 3  # medium by default

        high_terms = ["active exploitation", "critical", "ransomware", "zero‑day", "nation‑state"]
        low_terms = ["proof of concept", "theoretical", "no active exploits"]

        for term in high_terms:
            if term in ctx_lower:
                score += 1

        for term in low_terms:
            if term in ctx_lower:
                score -= 1

        score = max(1, min(5, score))

        labels = {
            1: "1/5 – Low (monitor only)",
            2: "2/5 – Low‑Medium (monitor + basic hardening)",
            3: "3/5 – Medium (prioritize in backlog)",
            4: "4/5 – High (treat as active program item)",
            5: "5/5 – Critical (urgent response likely needed)",
        }
        return labels.get(score, "3/5 – Medium (prioritize in backlog)")

    def generate_briefing(
        self,
        query: str,
        focus_area: str = "All threats",
        detail_level: str = "Balanced",
    ) -> BriefingResult:
        """
        Full two‑stage pipeline: Perplexity (web search) -> OpenAI (reasoning & formatting).
        """
        web_context = self._call_perplexity(query=query, focus_area=focus_area, detail_level=detail_level)
        answer = self._call_openai(query=query, web_context=web_context, detail_level=detail_level)

        risk_score = self._heuristic_risk_score(web_context)
        audience = "Designed for CISOs, security leads, and engineering managers who need fast, reliable context."
        sources_hint = (
            "Links at the bottom of the briefing come from live web research via Perplexity. "
            "Always click through and verify before acting on them in production environments."
        )

        return BriefingResult(
            answer=answer,
            web_context=web_context,
            risk_score=risk_score,
            audience=audience,
            sources_hint=sources_hint,
        )
