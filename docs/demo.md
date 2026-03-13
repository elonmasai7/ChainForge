# Demo Walkthrough: Paid AI Coding Community

## Scenario
A developer creates a paid AI coding community with a monthly subscription.

## Steps
1. Creator signs in with social login.
2. Creator registers a platform with subscription pricing.
3. Users join via social login.
4. Users pay subscription.
5. Creator receives routed revenue.

## Sample API Calls
1. Auth login
```
POST http://localhost:8001/login
{ "provider": "google", "email": "dev@creator.com" }
```

2. Create creator
```
POST http://localhost:8002/creators
{ "name": "AI Guild", "handle": "ai-guild", "wallet_address": "initia1creator" }
```

3. Create platform
```
POST http://localhost:8002/platforms
{ "creator_id": "<creator_id>", "name": "AI Coding Guild", "monetization_type": "subscription", "pricing_model": { "price": 29, "denom": "INIT" } }
```

4. User subscribes
```
POST http://localhost:8003/subscriptions
{ "platform_id": "<platform_id>", "user_id": "<user_id>", "price_amount": 29, "price_denom": "INIT" }
```

5. Payment recorded
```
POST http://localhost:8003/payments
{ "platform_id": "<platform_id>", "user_id": "<user_id>", "amount": 29, "denom": "INIT", "tx_hash": "<chain_tx>" }
```

6. Analytics
```
GET http://localhost:8004/revenue/summary?platform_id=<platform_id>
```

