from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai'))
from pandit_ji_chatbot import pandit_ji_reply, load_poojas, find_matching_poojas

app = Flask(__name__)
CORS(app)

@app.route('/greeting', methods=['GET'])
def greeting():
    """Send initial greeting message"""
    return jsonify({
        'message': '🙏 Namaste! Welcome to Pandit Ji. I\'m here to help you find the perfect pooja for your spiritual needs, answer questions about Hindu rituals and practices, or guide you on your spiritual journey.\n\nYou can ask me:\n• "Health and peace" - for wellness poojas\n• "Business success" - for prosperity\n• "What is a mantra?" - for spiritual knowledge\n• "How to prepare for pooja?" - for guidance\n\nWhat brings you here today?'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return pooja recommendations"""
    data = request.json
    user_msg = data.get('message', '')
    user_id = data.get('user_id', 'unknown')
    
    if not user_msg:
        return jsonify({'error': 'No message provided'}), 400
    
    msg_lower = user_msg.lower()
    
    try:
        # Check for greetings first
        greeting_words = ["hi", "hello", "hey", "namaste", "how are you", "how's it going"]
        if any(word in msg_lower for word in greeting_words):
            return jsonify({
                'status': 'greeting',
                'message': '🙏 Namaste! I\'m Pandit Ji 😊\n\nI\'m here to listen and help you find the perfect pooja for your needs.\n\nPlease tell me what spiritual guidance you\'re seeking. You can ask about:\n• Health and wellness\n• Career and business\n• Marriage and relationships\n• Family prosperity\n• Education\n• Or any other spiritual concern',
                'is_general_qa': True,
                'recommendations': []
            })
        
        # Get poojas data
        poojas = load_poojas()
        
        if not poojas:
            return jsonify({
                'status': 'error',
                'message': 'Unable to load pooja database.',
                'is_general_qa': False,
                'recommendations': []
            })
        
        # Find matching poojas
        matching_poojas = find_matching_poojas(msg_lower, poojas)
        
        if matching_poojas:
            # Format recommendations with scores and reasons
            recommendations = []
            for pooja in matching_poojas[:3]:  # Top 3
                recommendations.append({
                    'pooja': pooja,
                    'score': 0.95,
                    'reason': f"This pooja addresses {', '.join(pooja['intents'])} needs"
                })
            
            return jsonify({
                'status': 'success',
                'is_general_qa': False,
                'recommendations': recommendations
            })
        else:
            return jsonify({
                'status': 'no_match',
                'message': '🤔 I didn\'t find specific pooja recommendations for that query.\n\nTry asking about:\n• Health issues\n• Career goals\n• Marriage concerns\n• Business success\n• Family well-being\n\nOr browse our complete catalog to explore all available poojas.',
                'is_general_qa': False,
                'recommendations': []
            })
    
    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}',
            'is_general_qa': False,
            'recommendations': []
        }), 500

@app.route('/poojas', methods=['GET'])
def get_poojas():
    """Return all poojas for the catalog"""
    poojas = load_poojas()
    return jsonify({'poojas': poojas})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("🙏 Starting Pandit Ji Backend Server...")
    print("Running on http://127.0.0.1:8000")
    print("Press CTRL+C to quit\n")
    app.run(debug=True, port=8000)
