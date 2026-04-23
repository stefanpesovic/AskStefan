# Projects

## Featured Open-Source Projects

### AIJobRadar
A production-grade REST API that scrapes real-time AI/ML job listings from RemoteOK, WeWorkRemotely, and Hacker News, normalizes them into a unified schema, and serves them via a FastAPI backend.

**Key achievements:**
- 89% test coverage with 72 tests
- Async scraping with httpx — 3 sites scraped in 1.4 seconds
- Word-boundary regex filter solving substring false-positive bug (reduced 201 raw jobs to 39 genuinely AI-relevant listings)
- Docker containerized with GitHub Actions CI
- JSON cache with TTL for efficient re-querying

**Tech stack:** Python 3.11, FastAPI, httpx, BeautifulSoup, Pydantic v2, pytest, Docker

**Repository:** https://github.com/stefanpesovic/AIJobRadar

### AskStefan
The chatbot you're currently talking to. A multi-document RAG (Retrieval-Augmented Generation) system that answers questions about me based on my CV, project descriptions, and personal documents.

**Key achievements:**
- Multi-document architecture — drop any PDF or Markdown into the data folder and the system knows about it
- Idempotent ingestion using SHA-256 file hashes
- 88 tests total (67 backend + 21 frontend)
- Glassmorphism split-layout UI with highlighted source citations
- Source cards show exactly where each answer came from

**Tech stack:** FastAPI, LangChain, ChromaDB, Cohere Embed v3 (embeddings), Groq + Llama 3.3 70B (generation), React, Vite, TailwindCSS, Docker Compose

**Repository:** https://github.com/stefanpesovic/AskStefan

---

## Commercial & Private Projects

The following projects are in private repositories because they are either commercial products or under active development for paying clients or personal ventures. Full code access available upon request via direct contact.

### Best Guest — AI Waiter Platform
A restaurant platform where guests scan a QR code at their table and interact with an AI agent acting as a waiter. The agent knows the full menu, ingredients, allergens, can recommend dishes, answer questions about the restaurant, and process orders and payments directly through chat. Currently under active development.

**Tech stack:** Python, FastAPI, React, AI agents, payment integration, real-time chat

### Kitchen Flow — Multilingual Recipe SaaS
A SaaS web application solving a real hospitality problem: foreign kitchen staff who don't know local dish preparation standards. Restaurants subscribe and get a digital recipe book with ingredients, plating techniques, and step-by-step images, all translated across multiple languages. New staff can be onboarded in days instead of weeks. Built and tested; currently in sales conversations with restaurants.

**Tech stack:** TypeScript, React, backend API, multi-language translation

### PolymarketBTCbot — Autonomous Trading System
An algorithmic trading bot for 5-minute binary prediction markets on Polymarket (BTC/ETH/SOL up-down). Uses an 11-strategy ensemble voting system with 3 mathematical risk gates (microstructure, execution feasibility, Kelly sizing) and full SQLite persistence. Currently in paper-testing phase; not deployed for live trading without further validation.

**Architecture highlights:**
- Async Python pipeline with market discovery, timing gates, and orderbook analysis
- TIER_1/TIER_2/INFO_ONLY strategy classification with weighted voting
- Asymmetric Kelly criterion for binary payouts
- Break-even WR mathematical framework with safety margins
- 120+ tests covering strategy logic and risk gates

**Tech stack:** Python 3.11, async/await, py-clob-client, Binance WebSockets, pandas, SQLite, pytest

### Apex Fitness — Personal Training Platform
A web application where users purchase customized training and nutrition plans, receiving daily workouts and meals adapted to their goals. Delivered and sold to a client.

**Tech stack:** TypeScript, React, backend API, payment integration

### Local AI Server — RTX 5080 Infrastructure
Built a dedicated AI server around an RTX 5080 GPU for running local models with full data privacy and zero recurring API costs. Hosts multiple custom agents:
- Marketing content generator (Instagram, TikTok)
- Coding assistant
- Image generation without cloud dependencies
- Task-specific agents for various personal workflows

**Tech stack:** Local LLM deployment, CUDA, Python agents, custom integrations

### AI Nutrition & Calorie App (Early Stage)
An AI agent that helps users make food choices based on their goals, calorie targets, and nutritional values. Extensive pre-development research into existing apps to identify and avoid their common UX frustrations.

**Status:** Early stage development

---

## Development Philosophy

I learn by building. Whenever I encounter a new tool or concept, my first instinct is to drop it into a project and see where it breaks. Explaining things to others is how I end up understanding them better myself. Every project listed above taught me something specific — the AIJobRadar substring bug taught me the importance of regex boundaries, the PolymarketBTCbot taught me mathematical rigor in financial systems, and AskStefan taught me the full RAG pipeline from embeddings to citation UI.