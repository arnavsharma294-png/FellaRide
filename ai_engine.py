"""OpenAI-powered persona and outreach helpers for FellaRide."""

import json
import os
from typing import Tuple

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PERSONAS = ("Potential Driver", "Potential Passenger", "Connector", "Neutral")


def _fallback_persona(post_text: str) -> Tuple[str, str]:
    """Keep the demo usable when no API key is configured."""
    text = post_text.lower()
    if any(term in text for term in ("group chats", "organize", "spread the word", "student org", "club", "tag me")):
        return "Connector", "This post signals influence over groups and willingness to coordinate other students."
    if any(term in text for term in ("open seats", "i drive", "my car", "has a car", "driver")):
        return "Potential Driver", "This post indicates access to a car and openness to sharing rides."
    if any(term in text for term in ("need a ride", "looking for a carpool", "ride with someone", "split rides", "chip in")):
        return "Potential Passenger", "This post expresses an immediate need for a ride or carpool."
    return "Neutral", "This post describes a commuting pain point without a clear ride-sharing role."


def categorize_persona(post_text: str) -> Tuple[str, str]:
    """Assign a FellaRide persona and a one-sentence explanation to a post."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return _fallback_persona(post_text)

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You classify university community posts for a carpooling product. "
                "Choose exactly one persona: Potential Driver, Potential Passenger, Connector, or Neutral. "
                "Return strict JSON with keys persona and reasoning; reasoning must be one sentence."
            ),
            input=f"Post: {post_text}",
            text={"format": {"type": "json_object"}},
            max_output_tokens=100,
            store=False,
        )
        result = json.loads(response.output_text)
        persona = result.get("persona", "Neutral")
        reasoning = result.get("reasoning", "The post does not provide enough signal for a more specific persona.")
        if persona not in PERSONAS:
            persona = "Neutral"
        return persona, reasoning
    except Exception:
        return _fallback_persona(post_text)


def generate_outreach(event_name: str, connectors: list[str], locations: list[str]) -> str:
    """Draft contextual outreach for community connectors, with an offline fallback."""
    api_key = os.getenv("OPENAI_API_KEY")
    connector_list = ", ".join(connectors) or "community leaders"
    location_list = ", ".join(locations) or "nearby neighborhoods"
    if not api_key or api_key == "your_openai_api_key_here":
        return (
            f"Hi {connector_list}! You’re already helping people connect around campus. "
            f"For {event_name}, could you share a quick FellaRide carpool callout with your groups? "
            f"We’re matching students from {location_list} so they can skip parking stress and transit delays."
        )

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "Write one warm, concise outreach message (70 words or fewer) for university community connectors. "
                "Mention FellaRide, carpooling, the event, and the local commuting friction. Do not invent incentives."
            ),
            input=(f"Event: {event_name}\nConnectors: {connector_list}\n"
                   f"Relevant locations: {location_list}"),
            max_output_tokens=160,
            store=False,
        )
        return response.output_text.strip()
    except Exception:
        return generate_outreach_fallback(event_name, connector_list, location_list)


def generate_outreach_fallback(event_name: str, connector_list: str, location_list: str) -> str:
    return (
        f"Hi {connector_list}! Could you help bring FellaRide to {event_name}? "
        f"Share a carpool callout with students in {location_list} so they can avoid parking and transit headaches together."
    )
