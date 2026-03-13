CREATE TABLE IF NOT EXISTS creators (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  handle TEXT UNIQUE NOT NULL,
  wallet_address TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS platforms (
  id UUID PRIMARY KEY,
  creator_id UUID REFERENCES creators(id),
  name TEXT NOT NULL,
  monetization_type TEXT NOT NULL,
  pricing_model JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id UUID PRIMARY KEY,
  platform_id UUID REFERENCES platforms(id),
  user_id UUID NOT NULL,
  status TEXT NOT NULL,
  price_amount NUMERIC NOT NULL,
  price_denom TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
  id UUID PRIMARY KEY,
  platform_id UUID REFERENCES platforms(id),
  user_id UUID NOT NULL,
  amount NUMERIC NOT NULL,
  denom TEXT NOT NULL,
  tx_hash TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events (
  id UUID PRIMARY KEY,
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
