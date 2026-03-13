# CreatorChain Architecture

## System Diagram
```mermaid
flowchart LR
  subgraph UX[Frontend - Next.js 14]
    UI[Landing + Dashboard + Community + Analytics]
  end

  subgraph API[Backend Services - FastAPI]
    AUTH[auth-service]
    CREATOR[creator-service]
    PAYMENT[payment-service]
    ANALYTICS[analytics-service]
    INDEXER[indexer]
  end

  subgraph DATA[Data Layer]
    PG[(PostgreSQL)]
    REDIS[(Redis Cache)]
    MQ[(RabbitMQ)]
  end

  subgraph CHAIN[Initia Appchain]
    REG[CreatorRegistry]
    SUB[SubscriptionManager]
    REV[RevenueRouter]
    CAC[ContentAccessControl]
    MKT[MarketplaceEngine]
  end

  UI --> AUTH
  UI --> CREATOR
  UI --> PAYMENT
  UI --> ANALYTICS

  AUTH --> REDIS
  CREATOR --> PG
  PAYMENT --> PG
  PAYMENT --> MQ
  ANALYTICS --> PG
  INDEXER --> PG

  PAYMENT --> CHAIN
  INDEXER --> CHAIN
  CHAIN --> INDEXER

  CHAIN --> REV
  CHAIN --> SUB
  CHAIN --> REG
  CHAIN --> CAC
  CHAIN --> MKT
```

## Key Flows
- Creator onboarding: UI -> auth-service -> creator-service -> CreatorRegistry
- Subscription: UI -> payment-service -> SubscriptionManager -> RevenueRouter
- Analytics: indexer writes chain events to Postgres -> analytics-service queries

