from typing import Optional


class CasualChatHandler:
    """Handle casual greetings and small talk."""

    GREETINGS = {
        "hi": "Hello! 🙏 I'm Pandit Ji, your spiritual guide. How can I help you today?",
        "hello": "Namaste! Welcome to Pandit Ji. I'm here to help with pooja recommendations and spiritual guidance. What brings you here?",
        "hey": "Hey there! 👋 I'm Pandit Ji. Ask me about poojas or spiritual practices.",
        "hola": "Hola! I'm Pandit Ji. How can I assist you spiritually today?",
    }

    WHO_ARE_YOU = {
        "who are you": "I'm Pandit Ji, an AI spiritual guide. I help you find the perfect poojas for your needs, answer questions about Hindu rituals and practices, and guide you on your spiritual journey. Ask me anything! 🙏",
        "what are you": "I'm Pandit Ji, your AI assistant for all things spiritual. I recommend poojas, explain rituals, and answer questions about Hindu practices and philosophy.",
        "tell me about yourself": "I'm Pandit Ji—an intelligent spiritual guide. I offer: pooja recommendations based on your needs, answers to spiritual questions, guidance on rituals and practices. Let me help you find peace and prosperity! 🙏",
    }

    GOODBYES = {
        "bye": "Namaste! May you find peace, prosperity, and spiritual growth. 🙏 Goodbye!",
        "goodbye": "Goodbye! May your spiritual journey be blessed. 🙏",
        "thanks": "You're welcome! Feel free to return anytime. 🙏",
        "thank you": "You're very welcome! Wishing you all the best. 🙏",
    }

    @staticmethod
    def is_casual_chat(query: str) -> bool:
        """Check if query is a casual greeting or small talk."""
        query_lower = query.lower().strip()
        return (
            query_lower in CasualChatHandler.GREETINGS
            or query_lower in CasualChatHandler.WHO_ARE_YOU
            or query_lower in CasualChatHandler.GOODBYES
        )

    @staticmethod
    def respond(query: str) -> Optional[str]:
        """Get response for casual chat."""
        query_lower = query.lower().strip()

        # Check greetings
        if query_lower in CasualChatHandler.GREETINGS:
            return CasualChatHandler.GREETINGS[query_lower]

        # Check "who are you"
        if query_lower in CasualChatHandler.WHO_ARE_YOU:
            return CasualChatHandler.WHO_ARE_YOU[query_lower]

        # Check goodbyes
        if query_lower in CasualChatHandler.GOODBYES:
            return CasualChatHandler.GOODBYES[query_lower]

        return None
