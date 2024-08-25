from flask import Flask, request, jsonify, render_template
import json
import sys
from db import db_insert, db_query, add_one_inasra_word_please
import CrystalizeByCoords  # Assuming this is where regex logic exists

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Global variables to store IPUZ data and lexicon
ipuz_data = None
lexicon = []


@app.route('/')
def home():
    global ipuz_data
    # Ensure ipuz_data is already loaded
    if ipuz_data is None:
        return jsonify(success=False, message="No IPUZ data loaded"), 404

    # Pass the puzzle to the template
    puzzle = ipuz_data.get('solution', [])
    return render_template('crossword.html', puzzle=puzzle)


@app.route('/click', methods=['GET'])
def handle_click():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    return jsonify(success=True, x=x, y=y)


@app.route('/hover', methods=['GET'])
def handle_hover():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    global ipuz_data, lexicon

    # Call the function from CrystalizeByCoords.py to get possible words
    possible_words = CrystalizeByCoords.calculate_possible_words(ipuz_data, lexicon, x, y)

    # Return the possible words and updated puzzle state for preview
    return jsonify(possible_words=possible_words)


@app.route('/start', methods=['GET'])
def start_with_data():
    global ipuz_data, lexicon
    if ipuz_data:
        return jsonify(success=True, message="Crossword session started with provided data", ipuz=ipuz_data)
    else:
        return jsonify(success=False, message="Failed to start session with provided data"), 404


@app.route('/process', methods=['POST'])
def process():
    global ipuz_data, lexicon
    position = request.json['position']
    
    possible_words = get_possible_words(position, ipuz_data, lexicon)
    
    return jsonify(possible_words=possible_words)


@app.route('/place_word', methods=['POST'])
def place_word():
    global ipuz_data
    word = request.json['word']
    position = request.json['position']
    orientation = request.json['orientation']
    
    updated_ipuz, new_coords = place_word_in_ipuz(word, position, orientation, ipuz_data)
    
    # Update global IPUZ data
    ipuz_data = updated_ipuz
    
    new_uuid = str(uuid.uuid4())
    
    return jsonify(success=True, message="Word placed successfully", ipuz=updated_ipuz, new_uuid=new_uuid)


def get_possible_words(position, ipuz_data, lexicon):
    return [word for word in lexicon if word.startswith('A')]  # Example filter


def place_word_in_ipuz(word, position, orientation, ipuz_data):
    new_coords = (position[0], position[1])
    return ipuz_data, new_coords


def run_without_database(ipuz_file, word_list):
    global ipuz_data, lexicon
    with open(ipuz_file, 'r') as f:
        ipuz_data = json.load(f)
    
    lexicon = word_list
    
    # Start the Flask server
    print("Starting Flask server with provided IPUZ file and word list...")
    app.run(port=9000, debug=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        ipuz_file = sys.argv[1]
        word_list = sys.argv[2:]
        run_without_database(ipuz_file, word_list)
    else:
        app.run(port=9000, debug=True)

