from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS
import uuid
import random

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)

from utils.math_utils import generate_quiz, check_answer, is_valid_topic
from utils.nlp_utils import generate_explanation

@app.route('/')
def index():
    return "Welcome to the AI Math Buddy backend!"

quiz_data = {}

def generate_question(topic, grade_level):
    if topic == 'algebra':
        coefficient = random.randint(1, 5)
        constant = random.randint(1, 10)
        solution = random.randint(1, 10)
        question = f"Solve for x: {coefficient}x + {constant} = {coefficient * solution + constant}"
        correct_answer = str(solution)
        options = [correct_answer] + [str(random.randint(1, 10)) for _ in range(3)]
        random.shuffle(options)
        return question, options, correct_answer

    elif topic == 'geometry':
        if grade_level in range(1, 5):
            shapes = ['circle', 'triangle', 'square']
            shape = random.choice(shapes)
            if shape == 'circle':
                radius = random.randint(1, 10)
                question = f"Calculate the area of a circle with radius {radius}."
                correct_answer = round(3.14 * radius * radius, 2)
            elif shape == 'triangle':
                base = random.randint(1, 10)
                height = random.randint(1, 10)
                question = f"Calculate the area of a triangle with base {base} and height {height}."
                correct_answer = round(0.5 * base * height, 2)
            elif shape == 'square':
                side = random.randint(1, 10)
                question = f"Calculate the area of a square with side length {side}."
                correct_answer = round(side * side, 2)
            options = [str(correct_answer)] + [str(round(random.uniform(1, 100), 2)) for _ in range(3)]
            random.shuffle(options)
            return question, options, str(correct_answer)

    elif topic == 'fractions':
        if grade_level in range(1, 5):
            numerator = random.randint(1, 10)
            denominator = random.randint(2, 10)  # Avoid zero denominator
            question = f"What is {numerator}/{denominator} simplified?"
            correct_answer = str(round(numerator / denominator, 2))
            options = [correct_answer] + [str(round(random.uniform(0, 5), 2)) for _ in range(3)]
            random.shuffle(options)
            return question, options, correct_answer

    elif topic == 'percentages':
        if grade_level in range(1, 5):
            base = random.randint(50, 200)
            percentage = random.randint(5, 50)
            question = f"What is {percentage}% of {base}?"
            correct_answer = round((percentage / 100) * base, 2)
            options = [str(correct_answer)] + [str(round(random.uniform(0, 100), 2)) for _ in range(3)]
            random.shuffle(options)
            return question, options, str(correct_answer)

    elif topic == 'statistics':
        if grade_level in range(1, 5):
            numbers = [random.randint(1, 10) for _ in range(5)]
            mean = round(sum(numbers) / len(numbers), 2)
            question = f"What is the mean of the numbers {', '.join(map(str, numbers))}?"
            options = [str(mean)] + [str(round(random.uniform(1, 10), 2)) for _ in range(3)]
            random.shuffle(options)
            return question, options, str(mean)

    elif topic == 'trigonometry':
        if grade_level in range(5, 10):
            angle = random.choice([30, 45, 60])
            if angle == 30:
                question = "What is the sine of 30 degrees?"
                correct_answer = round(0.5, 2)
            elif angle == 45:
                question = "What is the cosine of 45 degrees?"
                correct_answer = round(0.707, 3)
            elif angle == 60:
                question = "What is the tangent of 60 degrees?"
                correct_answer = round(1.732, 3)
            options = [str(correct_answer)] + [str(round(random.uniform(0, 2), 3)) for _ in range(3)]
            random.shuffle(options)
            return question, options, str(correct_answer)

    elif topic == 'calculus':
        if grade_level in range(10, 12):
            function = random.choice(['x^2', 'x^3', 'sin(x)', 'cos(x)'])
            if function == 'x^2':
                question = "What is the derivative of x^2?"
                correct_answer = '2x'
            elif function == 'x^3':
                question = "What is the integral of x^3?"
                correct_answer = 'x^4 / 4'
            elif function == 'sin(x)':
                question = "What is the derivative of sin(x)?"
                correct_answer = 'cos(x)'
            elif function == 'cos(x)':
                question = "What is the integral of cos(x)?"
                correct_answer = 'sin(x)'
            options = [correct_answer] + [f'{random.choice(["2x", "x^2", "x^3 / 3", "cos(x)"])}' for _ in range(3)]
            random.shuffle(options)
            return question, options, correct_answer

    elif topic == 'linear algebra':
        if grade_level in range(9, 12):
            matrix = [[random.randint(1, 5) for _ in range(2)] for _ in range(2)]
            question = f"Find the determinant of the matrix: {matrix}"
            correct_answer = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            options = [str(correct_answer)] + [str(random.randint(-10, 10)) for _ in range(3)]
            random.shuffle(options)
            return question, options, str(correct_answer)

    elif topic == 'complex numbers':
        if grade_level in range(11, 12):
            real1 = random.randint(1, 5)
            imag1 = random.randint(1, 5)
            real2 = random.randint(1, 5)
            imag2 = random.randint(1, 5)
            question = f"Add the complex numbers: ({real1} + {imag1}i) and ({real2} + {imag2}i)."
            correct_answer = f"{real1 + real2} + {imag1 + imag2}i"
            options = [correct_answer] + [f"{random.randint(-10, 10)} + {random.randint(-10, 10)}i" for _ in range(3)]
            random.shuffle(options)
            return question, options, correct_answer

    elif topic == 'matrices':
        if grade_level in range(10, 12):
            matrix1 = [[random.randint(1, 5) for _ in range(2)] for _ in range(2)]
            matrix2 = [[random.randint(1, 5) for _ in range(2)] for _ in range(2)]
            result = [[matrix1[i][j] + matrix2[i][j] for j in range(2)] for i in range(2)]
            question = f"Add the matrices:\nMatrix A: {matrix1}\nMatrix B: {matrix2}"
            correct_answer = result
            options = [str(correct_answer)] + [str([[random.randint(1, 5) for _ in range(2)] for _ in range(2)]) for _ in range(3)]
            random.shuffle(options)
            return question, options, str(correct_answer)

    else:
        return "Invalid topic", [], ""

def generate_quiz(query):
    parts = query.split()
    if len(parts) < 2:
        return {"error": "Invalid query format. Please provide both topic and grade level."}

    topic = parts[0].lower()
    try:
        grade_level = int(parts[-1])
    except ValueError:
        return {"error": "Invalid grade level. Please provide an integer."}

    questions = []
    for i in range(10):  # Generate 10 questions
        result = generate_question(topic, grade_level)
        if result[0] == "Invalid topic":
            return {"error": "Invalid topic provided"}
        question, options, correct_answer = result
        question_id = f"q{i+1}"
        questions.append({
            'id': question_id,
            'question': question,
            'options': options,
            'correct_answer': correct_answer
        })
        quiz_data[question_id] = correct_answer

    return {
        'id': str(uuid.uuid4()),  # Generate a unique quiz ID
        'questions': questions
    }

@app.route('/api/get_quiz', methods=['POST'])
def get_quiz():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query not provided'}), 400

    quiz = generate_quiz(query)
    if 'error' in quiz:
        return jsonify(quiz), 400

    return jsonify(quiz)

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')

    if not question_id or not user_answer:
        return jsonify({'error': 'Missing question_id or user_answer'}), 400

    correct_answer = quiz_data.get(question_id)
    if correct_answer is None:
        return jsonify({'error': 'Invalid question_id'}), 400

    if user_answer == correct_answer:
        return jsonify({'result': 'Correct'})
    else:
        return jsonify({'result': 'Incorrect', 'correct_answer': correct_answer})

if __name__ == '__main__':
    app.run(debug=True)
