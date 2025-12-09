# 🛡️ CyberGuard AI – Real‑Time Threat Briefings

A **GenAI‑powered, web‑RAG Streamlit application** that turns *live* cybersecurity news and research into **executive‑ready threat briefings**.

Built with:

- **Streamlit** for a fast, modern UI  
- **Perplexity Sonar models** for live, web‑grounded research  
- **OpenAI models** for structured reasoning and clear communication  
- **Docker** for easy deployment to platforms like Render  

---

## 🌍 Why this project exists

Security leaders and engineers are drowning in feeds, alerts, and headlines.  
**CyberGuard AI** helps you:

- Turn *unstructured* web information into **actionable threat briefings** in minutes  
- Quickly understand **what’s happening, who’s at risk, and what to do next**  
- Re‑use the code as a **template for production‑grade web‑RAG apps** using Perplexity + OpenAI + Streamlit  

This project is also designed to showcase end‑to‑end skills for a **GenAI / AI Engineer** role:
RAG design, prompt engineering, API orchestration, observability hooks, and deployability.

---

## 🧱 Architecture (high level)

1. **User query** + optional threat focus (e.g., *Ransomware*, *Cloud & SaaS*, *AI & LLM security*)  
2. **Perplexity Sonar (web‑grounded LLM)**  
   - Searches the live web  
   - Returns a compact threat‑intel style summary with links  
3. **OpenAI model (e.g., `gpt-4.1-mini`)**  
   - Consumes the Perplexity output as **retrieval context**  
   - Produces a **structured briefing** tailored to security leadership  
4. **Streamlit UI**  
   - Shows a heuristic risk score, the final briefing, and the underlying web context  

> There is **no local `/data` folder**. All context is fetched from live websites via Perplexity, so you don’t need to maintain a document store.

---

## ⚙️ Local setup (macOS + PyCharm friendly)

### 1. Clone the repo

```bash
git clone <YOUR_REPO_URL>.git
cd cyberguard_ai_streamlit
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API keys

Copy the example environment file and fill in your keys:

```bash
cp .env .env
```

Edit `.env`:

```text
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=pplx-...
```

> `.env` is already added to **.gitignore**, so it will **never** be committed.

### 5. Run the app (locally)

```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501).

---

## 🐳 Docker support

### Build the image

```bash
docker build -t cyberguard-ai .
```

### Run the container

```bash
docker run -p 8501:8501 --env-file .env cyberguard-ai
```

If you see an error like `port is already allocated`, it means something else is using port `8501`:

- Stop any existing container using that port, or
- Run on a different host port, for example:

```bash
docker run -p 8502:8501 --env-file .env cyberguard-ai
```

---

## ☁️ Deploying to Render

You can deploy this app to **Render** either with the Dockerfile or using Render’s native Python environment.

### Option A – Deploy with Dockerfile

1. Push this project to a public GitHub repo.  
2. In Render, click **New ➜ Web Service**.  
3. Connect your GitHub repo.  
4. Render will detect the `Dockerfile` automatically.  
5. Set **environment variables** in Render:
   - `OPENAI_API_KEY`
   - `PERPLEXITY_API_KEY`
6. Choose a suitable instance type and deploy.  

The service will listen on port `8501` inside the container; Render maps it to a public URL.

### Option B – Deploy as a Python web service (no Docker)

1. In Render, click **New ➜ Web Service**.  
2. Use **Build Command**:

   ```bash
   pip install -r requirements.txt
   ```

3. Use **Start Command**:

   ```bash
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

4. Add environment variables (`OPENAI_API_KEY`, `PERPLEXITY_API_KEY`).  
5. Deploy.

---

## 🔐 How `.env` and `.gitignore` protect your secrets

### Ignoring `.env` in Git

The `.gitignore` file already contains:

```gitignore
.env
.env.*
```

That means any file named `.env` (or matching `.env.*`) is **never tracked** by Git or pushed to GitHub.

> You **should commit** your `.gitignore` file, so collaborators get the same protection rules.

If you accidentally committed a `.env` in the past, you’d need to:

```bash
git rm --cached .env
git commit -m "Remove .env from repo history"
```

---

## 🧪 Example usage

Ask questions like:

- *“Give me a 1‑page briefing on recent ransomware activity targeting healthcare in the US.”*  
- *“What’s the current state of supply‑chain attacks via CI/CD pipelines?”*  
- *“How are attackers abusing AI and LLM‑enabled internal tools in 2025?”*  

The app will:

1. Use **Perplexity** to research the live web.  
2. Use **OpenAI** to build a structured briefing with:
   - Executive summary  
   - Technical details (when available)  
   - Who is most at risk  
   - Recommended actions for the next 30–90 days  
   - Source links you can click and verify  

---

## 👤 About the author

This project was built by **Bhavesh Kalluru**:

- GitHub: https://github.com/bhavesh-kalluru  
- LinkedIn: https://www.linkedin.com/in/bhaveshkalluru/  
- Portfolio: https://kbhavesh.com  

> Bhavesh has **5+ years of experience** and is actively looking for **full‑time Generative AI / AI Engineer roles** in the US.
> If this project resonates with the kind of systems you want to build, feel free to reach out.

---
