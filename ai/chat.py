#!/usr/bin/env python3
"""Interactive chat with Pandit Ji AI recommender."""

from ai.config import load_settings
from ai.context import ConversationManager, IntentExtractor
from ai.guardrails import SafetyChecker
from ai.llm import build_llm
from ai.models import QueryContext
from ai.rag import PoojaRecommender


def main():
    print("🙏 Welcome to Pandit Ji AI Assistant 🙏")
    print("=" * 60)
    print("Ask about poojas, rituals, and spiritual practices.")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    settings = load_settings()
    llm = build_llm(settings.llm_provider, settings.llm_model)
    rec = PoojaRecommender(settings, llm=llm)
    rec.load_data()

    conv_mgr = ConversationManager(max_history=10)
    user_id = "cli_user"

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            print("Assistant: Namaste! May you find peace and prosperity. 🙏")
            break

        # Safety check
        is_safe, safety_msg = SafetyChecker.check_query(user_input)
        if not is_safe:
            print(f"Assistant: {safety_msg}\n")
            conv_mgr.add_turn(user_id, "user", user_input)
            conv_mgr.add_turn(user_id, "assistant", safety_msg)
            continue

        # Extract intent and city
        intents = IntentExtractor.extract(user_input)
        city = IntentExtractor.extract_city(user_input)

        # Build query context
        ctx = QueryContext(
            user_issue=user_input,
            city=city,
            language="en",
        )
        ctx = conv_mgr.enrich_context(ctx, user_id)

        # Get recommendations
        recommendations = rec.recommend(ctx)

        if not recommendations:
            print("Assistant: I couldn't find matching poojas. Please try a different query.\n")
            conv_mgr.add_turn(user_id, "user", user_input)
            conv_mgr.add_turn(user_id, "assistant", "No matches found.")
            continue

        # Display results
        print("\nAssistant:")
        for idx, rec_item in enumerate(recommendations, 1):
            print(f"\n  Option {idx}: {rec_item.pooja.name}")
            print(f"  Relevance: {rec_item.score * 100:.0f}%")
            print(f"  📝 {rec_item.reason}")
            print(f"  ✨ Benefits: {', '.join(rec_item.pooja.benefits)}")
            print(f"  ⏱️  Duration: {rec_item.pooja.duration_minutes} min | 💰 Price: ₹{rec_item.pooja.price_inr}")
            print(f"  📍 Cities: {', '.join(rec_item.pooja.cities)}")
            if rec_item.pooja.scriptural_refs:
                print(f"  📚 References: {', '.join(rec_item.pooja.scriptural_refs)}")

        print("\n" + "=" * 60 + "\n")

        # Add to history
        conv_mgr.add_turn(user_id, "user", user_input)
        response_summary = f"Recommended {len(recommendations)} pooja(s) for intents: {intents}"
        conv_mgr.add_turn(user_id, "assistant", response_summary)


if __name__ == "__main__":
    main()
