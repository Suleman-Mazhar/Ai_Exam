from flask import Flask, render_template, request, jsonify
import plotly
import json
from AI_Test_Analyser_V2 import analyze_test_answers

app = Flask(__name__)

# Sample questions (you can modify these or load from a database)
QUESTIONS = [
    "What is a binary search tree?",
    "Explain the difference between a stack and a queue.",
    "What is the time complexity of accessing an element in an array?",
    "Describe how a hash table works.",
    "What is the purpose of a linked list?",
    "Explain the concept of recursion.",
    "What is a graph data structure?",
    "Describe the difference between depth-first search (DFS) and breadth-first search (BFS).",
    "What is the time complexity of sorting an array using merge sort?",
    "Explain the difference between a balanced and unbalanced binary search tree."
]

@app.route('/')
def index():
    return render_template('index.html', questions=QUESTIONS)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    student_answers = data.get('answers', [])
    
    if len(student_answers) != len(QUESTIONS):
        return jsonify({'error': 'Number of answers does not match number of questions'}), 400
    
    percentages, analysis = analyze_test_answers(QUESTIONS, student_answers)
    
    # Create a bar chart using Plotly
    fig = {
        'data': [{
            'x': [f'Q{i+1}' for i in range(len(QUESTIONS))],
            'y': percentages,
            'type': 'bar',
            'marker': {
                'color': percentages,
                'colorscale': 'RdYlGn',
                'colorbar': {'title': 'Understanding %'}
            }
        }],
        'layout': {
            'title': 'Understanding Analysis by Question',
            'xaxis': {'title': 'Questions'},
            'yaxis': {'title': 'Understanding Percentage'},
            'height': 500
        }
    }
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'percentages': percentages,
        'analysis': analysis,
        'graph': graphJSON
    })

if __name__ == '__main__':
    app.run(debug=True) 