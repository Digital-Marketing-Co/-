#!/usr/bin/env python3
"""Deterministic inactivity deadline calculation for ConversationSync.

eligible_at = last_activity_at + 6000 seconds (UTC).
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

INACTIVITY_SECONDS = 6000

def calculate_eligible_at(last_activity_at: datetime, estimated: bool = False) -> dict:
    """Return eligible_at and metadata.
    
    Args:
        last_activity_at: Verified or estimated activity timestamp (aware UTC).
        estimated: True if timing is based on first durable observation.
    """
    if last_activity_at.tzinfo is None:
        last_activity_at = last_activity_at.replace(tzinfo=timezone.utc)
    else:
        last_activity_at = last_activity_at.astimezone(timezone.utc)
    
    eligible = last_activity_at + timedelta(seconds=INACTIVITY_SECONDS)
    return {
        "eligible_at": eligible.isoformat(),
        "last_activity_at": last_activity_at.isoformat(),
        "inactivity_seconds": INACTIVITY_SECONDS,
        "timing": "estimated" if estimated else "verified",
        "is_eligible_now": datetime.now(timezone.utc) >= eligible,
    }

def is_eligible(eligible_at_iso: str, now: Optional[datetime] = None) -> bool:
    """Exact comparison: eligible at 6000 seconds, ineligible at 5999."""
    if now is None:
        now = datetime.now(timezone.utc)
    eligible = datetime.fromisoformat(eligible_at_iso.replace("Z", "+00:00"))
    return now >= eligible

if __name__ == "__main__":
    # Example
    now = datetime.now(timezone.utc)
    result = calculate_eligible_at(now - timedelta(seconds=5999))
    print(result)
    print("Eligible?", is_eligible(result["eligible_at"]))
