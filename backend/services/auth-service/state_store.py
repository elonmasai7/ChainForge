import time
import uuid
import json
from typing import Any
import redis
from shared.config import REDIS_HOST, REDIS_PORT

class StateStore:
    def __init__(self) -> None:
        self._fallback: dict[str, tuple[float, dict[str, Any]]] = {}
        try:
            self._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            self._redis.ping()
        except Exception:
            self._redis = None

    def put(self, payload: dict[str, Any], ttl_seconds: int = 600) -> str:
        state = uuid.uuid4().hex
        if self._redis:
            self._redis.setex(f"oauth_state:{state}", ttl_seconds, json.dumps(payload))
        else:
            self._fallback[state] = (time.time() + ttl_seconds, payload)
        return state

    def get(self, state: str) -> dict[str, Any] | None:
        if self._redis:
            raw = self._redis.get(f"oauth_state:{state}")
            if not raw:
                return None
            try:
                return json.loads(raw)
            except Exception:
                return None
        if state not in self._fallback:
            return None
        expires_at, payload = self._fallback[state]
        if time.time() > expires_at:
            del self._fallback[state]
            return None
        return payload

    def delete(self, state: str) -> None:
        if self._redis:
            self._redis.delete(f"oauth_state:{state}")
        else:
            self._fallback.pop(state, None)
