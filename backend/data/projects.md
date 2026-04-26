# Projects

## Featured Open-Source Projects

### VideoBrief — AI-Powered YouTube Summarizer with LangGraph Agent
Full-Stack AI Developer — Day 3 of 5-Day AI Developer Challenge

Paste any YouTube URL and get a structured markdown report with key takeaways, clickable timestamps, and video-type-specific insights. Built with a 5-stage LangGraph agent that autonomously decides which specialized tools to run based on video content (tutorials trigger code extraction, interviews trigger quote extraction, etc.).

**Key achievements:**
- Multi-stage LangGraph agent with conditional routing based on content type
- 137 tests (63 backend + 74 frontend), full CI/CD with GitHub Actions
- Glassmorphism UI with Hero, Feature Cards, Video Preview, and Staged Loader
- Adaptive reports: tutorial vs. interview vs. educational content get different structures

**Tech stack:** Python, FastAPI, LangGraph, Groq (Llama 3.3 70B), youtube-transcript-api, React 18, Vite, TailwindCSS, Framer Motion, Docker

**Repository:** https://github.com/stefanpesovic/VideoBrief

### AskStefan — Multi-Document RAG Chatbot (LIVE DEPLOYMENT)
Full-Stack AI Developer — Day 2 of 5-Day AI Developer Challenge

The chatbot you're currently talking to. A production RAG (Retrieval-Augmented Generation) chatbot that answers questions about me based on my CV, project descriptions, and personal documents. Features a glassmorphism split-layout UI with highlighted source citations, cold-start loader, and dismissible welcome banner.

**Key achievements:**
- LIVE demo: askstefan.onrender.com — anyone can interact with it
- Multi-document ingestion (PDF + Markdown) with SHA-256 hash deduplication
- 88 tests (67 backend + 21 frontend), Docker Compose, GitHub Actions CI
- Citation-aware retrieval: every answer shows exact source chunks with highlighted keywords

**Tech stack:** FastAPI, LangChain, ChromaDB, Cohere Embed v3 (embeddings), Groq + Llama 3.3 70B (generation), React, TailwindCSS, Docker Compose

**Live Demo:** https://askstefan.onrender.com

**Repository:** https://github.com/stefanpesovic/AskStefan

### AIJobRadar — Real-Time AI/ML Job Scraper REST API
Backend Developer — Day 1 of 5-Day AI Developer Challenge

A production-grade REST API that scrapes real-time AI/ML job listings from RemoteOK, WeWorkRemotely, and Hacker News, normalizes them into a unified schema, and serves them via a FastAPI backend.

**Key achievements:**
- 72 tests, 89% code coverage
- Async scraping with httpx — 3 sites scraped in 1.4 seconds
- Word-boundary regex filter solving substring false-positive bug (reduced 201 raw jobs to 39 genuinely AI-relevant listings)
- Docker containerized with GitHub Actions CI
- JSON cache with TTL for efficient re-querying

**Tech stack:** Python 3.11, FastAPI, httpx, BeautifulSoup, Pydantic v2, pytest, Docker

**Repository:** https://github.com/stefanpesovic/AIJobRadar

---

## Commercial & Private Projects

The following projects are in private repositories because they are either commercial products or under active development for paying clients or personal ventures. Full code access available upon request via direct contact.

### Best Guest — AI Waiter Platform for Restaurants (Active Development)
A restaurant platform where guests scan a QR code at their table and interact with an AI agent acting as a waiter. The agent knows the full menu, ingredients, allergens, can recommend dishes, answer questions about the restaurant, and process orders and payments directly through chat. Currently under active development.

**Tech stack:** Python, FastAPI, React, AI agents, payment integration, real-time chat

### Kitchen Flow — Multilingual Recipe SaaS (In Sales)
A SaaS web application solving a real hospitality problem: foreign kitchen staff who don't know local dish preparation standards. Restaurants subscribe and get a digital recipe book with ingredients, plating techniques, and step-by-step images, all translated across multiple languages. New staff can be onboarded in days instead of weeks. Built and tested; currently in sales conversations with restaurants.

**Tech stack:** TypeScript, React, backend API, multi-language translation

### PolymarketBTCbot — Autonomous Trading System (Paper Testing)
An algorithmic trading bot for 5-minute binary prediction markets on Polymarket (BTC/ETH/SOL up-down). Uses an 11-strategy ensemble voting system with 3 mathematical risk gates (microstructure, execution feasibility, Kelly sizing) and full SQLite persistence. Currently in paper-testing phase.

**Architecture highlights:**
- Async Python pipeline with market discovery, timing gates, and orderbook analysis
- TIER_1/TIER_2/INFO_ONLY strategy classification with weighted voting
- Asymmetric Kelly criterion for binary payouts
- Break-even WR mathematical framework with safety margins
- 120+ tests covering strategy logic and risk gates

**Tech stack:** Python 3.11, async/await, py-clob-client, Binance WebSockets, pandas, SQLite, pytest

### Apex Fitness — Personal Training Platform (Delivered to Client)
A web application where users purchase customized training and nutrition plans, receiving daily workouts and meals adapted to their goals. Project delivered and sold to a private client; currently in production.

**Tech stack:** TypeScript, React, backend API, payment integration

### Local AI Server — RTX 5080 Infrastructure
Built a dedicated AI server around an RTX 5080 GPU for running local models with full data privacy and zero recurring API costs. Hosts multiple custom agents:
- Marketing content generator (Instagram, TikTok)
- Coding assistant
- Image generation without cloud dependencies
- Task-specific agents for various personal workflows

**Tech stack:** Local LLM deployment, CUDA, Python agents, custom integrations

---

## Development Philosophy

I learn by building. Whenever I encounter a new tool or concept, my first instinct is to drop it into a project and see where it breaks. Explaining things to others is how I end up understanding them better myself. Every project listed above taught me something specific — the AIJobRadar substring bug taught me the importance of regex boundaries, the PolymarketBTCbot taught me mathematical rigor in financial systems, AskStefan taught me the full RAG pipeline from embeddings to citation UI, and VideoBrief taught me multi-stage LangGraph agent design with conditional routing.