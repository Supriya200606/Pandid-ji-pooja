import json
import os

def load_poojas():
    try:
        # Try multiple possible paths
        possible_paths = [
            'sample_data/poojas.json',
            '../sample_data/poojas.json',
            'e:/POOJAI/ai/sample_data/poojas.json',
            os.path.join(os.path.dirname(__file__), 'sample_data', 'poojas.json')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        print(f"Warning: poojas.json not found in any expected location")
        return []
    except Exception as e:
        print(f"Error loading poojas: {e}")
        return []

def pandit_ji_reply(user_msg):
    msg = user_msg.lower()
    poojas = load_poojas()

    # Greetings
    if any(word in msg for word in ["hi", "hello", "hey", "namaste"]):
        return (
            "🙏 Namaste! I'm Pandit Ji 😊\n"
            "I'm here to listen and help you.\n"
            "Please tell me what's on your mind."
        )

    # How are you
    elif "how are you" in msg:
        return (
            "By God's grace, I'm doing well 😊\n"
            "Thank you for asking.\n"
            "How may I help you today?"
        )

    # Search for matching poojas
    else:
        matching_poojas = find_matching_poojas(msg, poojas)
        
        if matching_poojas:
            response = f"✨ Found {len(matching_poojas)} recommendation(s) for you:\n\n"
            for pooja in matching_poojas[:3]:  # Show top 3
                response += f"🕉️ {pooja['name']}\n"
                response += f"   {pooja['description']}\n"
                response += f"   💰 ₹{pooja['price_inr']}\n\n"
            return response
        else:
            return (
                "🙏 I'm listening.\n"
                "You can tell me about health, career, marriage, or any concern."
            )

def find_matching_poojas(user_msg, poojas):
    msg_lower = user_msg.lower()
    msg_words = set(msg_lower.split())
    matches = []
    
    for pooja in poojas:
        score = 0
        
        # Check intents - exact substring match
        for intent in pooja.get('intents', []):
            intent_lower = intent.lower()
            if intent_lower in msg_lower or any(word in intent_lower for word in msg_words):
                score += 2
                break
        
        # Check tags - exact substring match
        if score == 0:
            for tag in pooja.get('tags', []):
                tag_lower = tag.lower()
                if tag_lower in msg_lower or any(word in tag_lower for word in msg_words):
                    score += 1
                    break
        
        # Check description keywords
        if score == 0:
            description_lower = pooja.get('description', '').lower()
            for word in msg_words:
                if len(word) > 2 and word in description_lower:
                    score += 0.5
        
        if score > 0:
            matches.append((pooja, score))
    
    # Sort by score (highest first) and return just the poojas
    matches.sort(key=lambda x: x[1], reverse=True)
    return [pooja for pooja, score in matches]
