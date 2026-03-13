# CreatorChain (Initia Appchain)

CreatorChain is a production-grade monetization platform for creators and communities built on the Initia stack. It enables creators to launch revenue-generating mini-platforms in minutes while keeping fees low and routing all value to creator vaults.

**Highlights**
- Appchain-based monetization primitives (subscriptions, micro-payments, pay-per-content, tipping, marketplace fees)
- Social login wallets with frictionless onboarding
- Cross-ecosystem users without manual bridging
- Real-time analytics and revenue dashboards

## Repository Layout
```
creatorchain
├ frontend
├ backend
├ contracts
├ infra
├ scripts
├ docker
└ docs
```

## Quick Start (Local)
1. `cp .env.example .env`
2. `docker compose up --build`
3. Open `http://localhost:3000` for the frontend

All data services run in containers (Postgres, Redis, RabbitMQ) via Docker Compose.

## Docs
- Architecture: `docs/architecture.md`
- Demo walkthrough: `docs/demo.md`
- Deployment notes: `docs/deployment.md`

## What’s Included
- Initia Move contracts (core monetization primitives)
- FastAPI microservices (auth, creator, payment, analytics, indexer)
- Next.js 14 frontend with Tailwind + Shadcn-style components
- Docker Compose for local stack
