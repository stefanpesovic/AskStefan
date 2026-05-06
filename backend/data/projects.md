# Projects

## Commercial Project Delivery

### LingoDish — Multilingual Recipe SaaS Platform (LIVE — 50+ active restaurants)
Full-Stack Founder & Engineer — Live commercial SaaS

Built and launched a production SaaS web application solving a real hospitality problem: foreign kitchen staff who don't know local dish preparation standards. Restaurants subscribe and get a digital recipe book with ingredients, plating techniques, and step-by-step images translated across 12+ languages. Currently serving 50+ active restaurants across Europe (Czech Republic, Austria, Serbia, and more) with multiple subscription tiers and 24-hour onboarding time.

**Key achievements:**
- End-to-end ownership: product, architecture, frontend, backend, deployment, marketing site, sales
- 12+ languages supported (English, Hindi, Nepali, Czech, German, Romanian, Vietnamese, etc.)
- Tiered subscription plans (Starter, Pro, Enterprise) with proportional upgrades
- Kiosk-style interface optimized for kitchen monitors — no scrolling required

**Tech stack:** TypeScript, React, FastAPI backend, multi-language translation, kiosk-optimized UI, subscription management, marketing site

**Live Site:** www.lingodish.com

### Apex Fitness — Full-Stack Web Platform (Delivered to Client)
Full-Stack Developer — Commercial project, delivered and paid

Built and delivered a complete full-stack web platform for a private fitness business. The platform handles member management, workout scheduling, and business operations. Delivered as a paid commercial engagement.

**Key achievements:**
- End-to-end delivery: requirements gathering, architecture, implementation, deployment
- Worked directly with the client to refine features through multiple iterations
- Successfully deployed and handed over to client for ongoing operation

**Tech stack:** TypeScript, React, modern frontend tooling, REST API backend, deployed for production use

---

## AI Portfolio Projects

### VideoBrief — AI-Powered YouTube Summarizer with LangGraph Agent
Full-Stack AI Developer — Day 3 of 5-Day AI Developer Challenge

Paste any YouTube URL and get a structured markdown report with key takeaways, clickable timestamps, and video-type-specific insights. Built with a 5-stage LangGraph agent that autonomously decides which specialized tools to run based on video content (tutorials trigger code extraction, interviews trigger quote extraction, etc.).

**Key achievements:**
- Multi-stage LangGraph agent with conditional routing based on content type
- 137 tests (63 backend + 74 frontend), full CI/CD with GitHub Actions
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

A production-grade REST API that scrapes real-time AI/ML job listings from RemoteOK, WeWorkRemotely, and Hacker News, normalizes them into a unified schema, and serves them via a FastAPI backend. Async scraping completes all 3 sites in 1.4 seconds.

**Key achievements:**
- 72 tests, 89% code coverage
- Async scraping with httpx — 3 sites scraped in 1.4 seconds
- JSON cache with TTL for efficient re-querying

**Tech stack:** Python 3.11, FastAPI, httpx (async), BeautifulSoup, Pydantic v2, pytest, Docker, GitHub Actions

**Repository:** https://github.com/stefanpesovic/AIJobRadar

---

## Additional Projects

### Best Guest — AI Waiter Platform (Active Development)
Restaurant platform where guests scan a QR code at their table and interact with an AI agent acting as a waiter. The agent knows the menu, ingredients, allergens, recommends dishes, and processes orders and payments directly through chat.

**Tech stack:** Python, FastAPI, React, AI agents, payment integration, real-time chat

### Local AI Server — RTX 5080 Infrastructure
Built a dedicated AI server around an RTX 5080 GPU for running local models with full data privacy and zero recurring API costs. Hosts multiple custom agents: marketing content generator, coding assistant, image generation, and task-specific agents.

**Tech stack:** Local LLM deployment, CUDA, Python agents, custom integrations

---

## Development Philosophy

I learn by building. Whenever I encounter a new tool or concept, my first instinct is to drop it into a project and see where it breaks. Every project listed above taught me something specific — AIJobRadar taught me async scraping patterns, AskStefan taught me the full RAG pipeline from embeddings to citation UI, and VideoBrief taught me multi-stage LangGraph agent design with conditional routing.