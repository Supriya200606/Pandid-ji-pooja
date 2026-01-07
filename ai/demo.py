from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai.config import load_settings
from ai.llm import build_llm
from ai.models import QueryContext
from ai.rag import PoojaRecommender


def main() -> None:
    parser = argparse.ArgumentParser(description="Try the Pandit Ji recommender")
    parser.add_argument("query", help="User need, e.g., 'health and peace' or Hindi text")
    parser.add_argument("--city", help="City to filter availability", default=None)
    parser.add_argument("--lang", help="Language hint (en/hi)", default="en")
    args = parser.parse_args()

    settings = load_settings()
    llm = build_llm(settings.llm_provider, settings.llm_model)
    rec = PoojaRecommender(settings, llm=llm)
    rec.load_data()

    ctx = QueryContext(user_issue=args.query, city=args.city, language=args.lang)
    recommendations = rec.recommend(ctx)

    for idx, item in enumerate(recommendations, 1):
        print(f"\nOption {idx}: {item.pooja.name} (score: {item.score})")
        print(f"Reason: {item.reason}")
        print(f"Benefits: {', '.join(item.pooja.benefits)}")
        print(f"Duration: {item.pooja.duration_minutes} minutes | Price: INR {item.pooja.price_inr}")
        print(f"Cities: {', '.join(item.pooja.cities)}")

    print("\nJSON output (for integrations):")
    print(json.dumps(rec.to_jsonable(recommendations), indent=2))


if __name__ == "__main__":
    main()
