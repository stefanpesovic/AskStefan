# Technical Skills — Detailed Breakdown

## Languages

**Python (daily, 3+ years)** — My primary language. Comfortable with async/await, type hints, dataclasses and Pydantic models, context managers, decorators, and modern Python 3.11+ features. Use it for backend services, AI pipelines, trading algorithms, and automation scripts.

**JavaScript / TypeScript (daily)** — Frontend work in React, some Angular. Comfortable with modern ES6+, React hooks, state management, and TypeScript type systems.

**Java (academic)** — From university coursework and a structured Java course.

## AI & Machine Learning

**LLM APIs** — Production experience with:
- Anthropic Claude (API and via Claude Code)
- OpenAI (ChatGPT API)
- Groq (Llama 3.3 70B — used in AskStefan and VideoBrief)
- Cohere (embeddings — used in AskStefan)

**RAG Systems** — End-to-end pipeline experience (AskStefan project):
- Document loading (PDF via pypdf, Markdown via python-frontmatter)
- Chunking strategies (LangChain RecursiveCharacterTextSplitter, chunk_size/overlap tuning)
- Embeddings (Cohere embed-english-v3.0, 1024-dimensional vectors)
- Vector storage (ChromaDB with persistent client and metadata filtering)
- Retrieval with top-k similarity search
- Citation-aware prompt engineering

**LangGraph** — Multi-stage agent design with conditional routing (VideoBrief project):
- 5-stage agent pipeline that autonomously decides which tools to run
- Content-type-specific routing (tutorials, interviews, educational content)
- Tool calling and specialized tool execution

**AI Agents & Automation** — Multiple agents in production for personal use:
- Marketing content generation (Instagram, TikTok)
- Coding assistance
- Trading signal analysis
- Local-hosted agents with privacy constraints

**Prompt Engineering & Tool Calling** — Designing structured prompts for LLMs, implementing tool calling patterns for agent systems, and building citation-aware retrieval prompts.

**Vector Databases** — ChromaDB with persistent storage, metadata filtering, and similarity search.

**Local AI Infrastructure** — Built and operate a dedicated AI server with RTX 5080 for running local LLMs, image generation, and custom agents without cloud dependencies.

## Backend Development

**FastAPI (daily)** — My go-to framework for Python APIs. Comfortable with:
- Async endpoints and lifespan handlers
- Pydantic v2 schemas for request/response validation
- Dependency injection
- Middleware and CORS
- Background tasks
- OpenAPI auto-documentation
- Error handling with custom HTTPException responses

**API Integrations** — Real-world experience with Coinglass, Polymarket CLOB, Binance WebSockets, OpenAI, Anthropic, Groq, Cohere, payment gateways. I know how to connect systems and what to do when docs don't match reality.

**Testing** — pytest with pytest-asyncio and respx for HTTP mocking. I write tests because they catch bugs before users do. Portfolio total: 274+ tests across 3 production projects (137 in VideoBrief, 88 in AskStefan, 72 in AIJobRadar at 89% coverage).

## Frontend Development

**React 18 (daily)** — Functional components, hooks (useState, useEffect, useCallback, useMemo, custom hooks), context API, React Router.

**Angular (working knowledge)** — For projects that require it.

**Styling** — TailwindCSS daily, glassmorphism UI patterns, responsive layouts (mobile-first when needed).

**Animation & UI Libraries** — Framer Motion for animations, Lucide React for icons.

**Build tools** — Vite (primary), some webpack experience.

## Databases

**MongoDB (daily)** — Document modeling, aggregation pipelines, indexing.

**ChromaDB (vector)** — Vector storage with persistent client, metadata filtering, and similarity search for RAG systems.

**SQLite** — For embedded persistence (used in PolymarketBTCbot for trade history and dynamic strategy weights).

**SQL (basic)** — Comfortable with standard queries; could go deeper if a role requires it.

## DevOps & Deployment

**Docker** — Multi-stage Dockerfiles, docker-compose for multi-service apps, volume management for persistent data, .dockerignore optimization.

**CI/CD** — GitHub Actions for automated testing, linting, and deployment pipelines. Recent setup: ruff + black + pytest running on every push.

**Deployment platforms** — Render (primary, live deployment at askstefan.onrender.com), familiar with the platform's quirks around environment variables, build commands, and service limits.

**Version control** — Git daily, comfortable with branching strategies, rebasing, resolving merge conflicts, writing clean commit histories.

## AI Development Tools

**Claude Code (daily driver)** — Primary tool for architecture, implementation, and testing workflows.

**Other tools** — Cursor, ChatGPT, local models on own GPU server.

## Rapid Prototyping

**Streamlit, Gradio, FastAPI + Swagger UI** — For fast AI demos and internal tools. I use these when I need to validate an idea quickly before committing to a full production stack.

## Methodology

**PSM I Certified (Professional Scrum Master I, Scrum.org)** — Formal Agile training. I work in sprints naturally because when you're shipping an MVP in a week, there's no other way.

**Architect-first development** — I design the system before writing code. Define the contracts, data models, and interfaces; then the implementation falls out naturally.

**Test-driven mindset** — 274+ tests across portfolio projects. Every project ships with comprehensive test suites covering backend logic, API endpoints, and frontend components.

## What I'm Learning Next

- Production-grade observability (Prometheus, Grafana)
- Kubernetes basics (currently comfortable with Docker Compose; K8s is the logical next step)
- Czech language (for potential relocation)