# Deployment

## Local (Docker Compose)
1. `cp .env.example .env`
2. `docker compose up --build`
3. Frontend: `http://localhost:3000`
4. Auth service: `http://localhost:8001/health`
5. Creator service: `http://localhost:8002/health`
6. Payment service: `http://localhost:8003/health`
7. Analytics service: `http://localhost:8004/health`
8. Realtime stream: `http://localhost:8004/revenue/stream?platform_id=demo-platform`

## Initia Appchain Integration
1. Deploy Move modules in `contracts/` to the CreatorChain appchain.
2. Update `INITIA_RPC_URL` and `INITIA_CHAIN_ID` in `.env`.
3. Set `INITIA_CLI_COMMAND` to a valid Initia CLI broadcast command that returns JSON with `txhash`.
4. Configure indexer with `INITIA_TX_SEARCH_QUERY` to pull recent on-chain events.
5. Wire payment-service to invoke `SubscriptionManager` and `RevenueRouter` entry functions.
6. Configure indexer to poll chain events and store in Postgres.

## Production Checklist
- Replace stub auth with Initia social login wallet SDK
- Enable chain event streaming for analytics
- Add signature verification for all chain-triggering endpoints
- Apply rate limiting and WAF
