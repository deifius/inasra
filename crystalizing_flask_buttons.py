# crystalizing_flask.py

from flask import Flask, request, jsonify, render_template_string
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
    if ipuz_data:
        html = render_crossword(ipuz_data)
        return render_template_string(html)
    return "No crossword data available."

@app.route('/click', methods=['GET'])
def handle_click():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    return jsonify(success=True, x=x, y=y)


@app.route('/hover', methods=['GET'])
def handle_hover():
    x = int(request.args.get('x')) - 1  # Adjust for zero-based index
    y = int(request.args.get('y')) - 1  # Adjust for zero-based index
    
    print(f"Adjusted hover coordinates: x={x}, y={y}")
    
    global ipuz_data, lexicon

    # Assuming the corrected interpretation (x = col, y = row) after adjusting for zero-indexing
    possible_words = CrystalizeByCoords.calculate_possible_words(ipuz_data, lexicon, y, x)

    return jsonify(possible_words=possible_words)


def render_crossword(ipuz_data):
    puzzle = ipuz_data.get('solution', [])
    table_html = '<table id="crossword">'
    for row in puzzle:
        table_html += '<tr>'
        for cell in row:
            table_html += f'''
            <td>
                <div class="dropdown">
                    <button class="dropbtn" onmouseover="handleHover(this)" onclick="toggleDropdown(this)">
                        {cell if cell != " " else "&nbsp;"}
                    </button>
                    <div class="dropdown-content">
                        <!-- Words will be populated here by JS -->
                    </div>
                </div>
            </td>'''
        table_html += '</tr>'
    table_html += '</table>'
    
    html = f'''
    <html>
    <head>
        <style>
            .dropdown {{
                position: relative;
                display: inline-block;
            }}
            .dropbtn {{
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px 10px;
                cursor: pointer;
                width: 100%;
            }}
            .dropdown-content {{
                display: none;
                position: absolute;
                background-color: #f1f1f1;
                min-width: 200px;
                max-height: 200px;
                overflow-y: auto;
                box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                z-index: 1;
            }}
            .dropdown-content button {{
                width: 100%;
                color: black;
                padding: 10px;
                text-align: left;
                border: none;
                background: none;
                cursor: pointer;
            }}
            .dropdown-content button:hover {{
                background-color: #ddd;
            }}
            .highlight {{
                color: red;
            }}
        </style>
    </head>
    <body>
        <script>
        function siblingCount(node) {{
            return [...node.parentElement.childNodes].indexOf(node);
        }}

        function handleHover(btn) {{
            const x = siblingCount(btn.parentElement.parentElement.parentElement);
            const y = siblingCount(btn.parentElement.parentElement);
            fetch(`/hover?x=` + x + `&y=` + y)
                .then(response => response.json())
                .then(data => {{
                    let dropdownContent = btn.nextElementSibling;
                    dropdownContent.innerHTML = '';  // Clear previous content
                    data.possible_words.forEach(word => {{
                        let wordButton = document.createElement('button');
                        wordButton.textContent = word[0];
                        wordButton.onclick = () => updateBoard(word[0], word[1], x, y, word[2]);
                        dropdownContent.appendChild(wordButton);
                    }});
                }});
        }}

        function toggleDropdown(btn) {{
            let dropdownContent = btn.nextElementSibling;
            dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
        }}

        function updateBoard(word, position, startX, startY, orientation) {{
            let table = document.getElementById('crossword');
            let cells = table.getElementsByTagName('td');
            let index = 0;
            let x = startX;
            let y = startY;

            if (orientation === 'horiz') {{
                for (let i = y; i < y + word.length; i++) {{
                    cells[x * table.rows[0].cells.length + i].firstChild.textContent = word[index++];
                    cells[x * table.rows[0].cells.length + i].firstChild.classList.add('highlight');
                }}
            }} else if (orientation === 'vert') {{
                for (let i = x; i < x + word.length; i++) {{
                    cells[i * table.rows[0].cells.length + y].firstChild.textContent = word[index++];
                    cells[i * table.rows[0].cells.length + y].firstChild.classList.add('highlight');
                }}
            }}
        }}
        </script>
        {table_html}
    </body>
    </html>
    '''
    return html

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



