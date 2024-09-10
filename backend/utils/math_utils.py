#backend/utils/math_utils.py
import random
import uuid  # For generating unique quiz IDs
import math   # For mathematical calculations

# Valid topics for quizzes
valid_topics = [
    'algebra', 'geometry', 'fractions', 'percentages', 'statistics', 
    'trigonometry', 'calculus', 'linear algebra', 'complex numbers', 'matrices'
]

def is_valid_topic(topic):
    """
    Checks if the provided topic is valid.

    Args:
        topic (str): The topic to check.

    Returns:
        bool: True if the topic is valid, False otherwise.
    """
    return topic.lower() in valid_topics

# Global variable to store quiz data
quiz_data = {}

def generate_quiz(query):
    """
    Generates a math quiz based on the given query.

    Args:
        query (str): The query specifying the topic and grade level (e.g., "algebra 9").

    Returns:
        dict: A dictionary containing the quiz ID and a list of questions,
              or an error message if the query is invalid.
    """
    parts = query.split()
    if len(parts) < 2:
        return {"error": "Invalid query format. Please provide both topic and grade level."}

    topic = parts[0].lower()  # Convert to lowercase for consistency
    try:
        grade_level = int(parts[-1])
    except ValueError:
        return {"error": "Invalid grade level. Please provide an integer."}

    if not is_valid_topic(topic):
        return {"error": "Invalid topic provided"}

    questions = []
    for i in range(10):  # Generate 10 questions
        question, options, correct_answer = generate_question(topic, grade_level)
        if question == "Invalid topic":
            return {"error": "Invalid topic provided"}
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

def generate_question(topic, grade_level):
    """
    Generates a single question based on the topic and grade level.

    Args:
        topic (str): The topic of the question (e.g., 'addition', 'fractions').
        grade_level (int): The grade level for which to generate the question.

    Returns:
        tuple: A tuple containing the question, a list of options, and the correct answer.
    """
    question = ""
    options = []
    correct_answer = ""

    if topic == 'addition':
        if grade_level <= 5:
            a = random.randint(1, 50)
            b = random.randint(1, 50)
        else:
            a = random.randint(50, 500)
            b = random.randint(50, 500)
        question = f"What is {a} + {b}?"
        correct_answer = str(a + b)
        options = [correct_answer] + [str(random.randint(a + b - 10, a + b + 10)) for _ in range(3)]
        random.shuffle(options)

    elif topic == 'subtraction':
        if grade_level <= 5:
            a = random.randint(20, 100)
            b = random.randint(1, 20)
        else:
            a = random.randint(100, 500)
            b = random.randint(50, 200)
        question = f"What is {a} - {b}?"
        correct_answer = str(a - b)
        options = [correct_answer] + [str(random.randint(a - b - 10, a - b + 10)) for _ in range(3)]
        random.shuffle(options)

    elif topic == 'multiplication':
        if grade_level <= 5:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        else:
            a = random.randint(10, 50)
            b = random.randint(10, 50)
        question = f"What is {a} * {b}?"
        correct_answer = str(a * b)
        options = [correct_answer] + [str(random.randint(a * b - 20, a * b + 20)) for _ in range(3)]
        random.shuffle(options)

    elif topic == 'division':
        if grade_level <= 5:
            a = random.randint(1, 10) * random.randint(1, 10)
            b = random.randint(1, 10)
        else:
            a = random.randint(50, 500)
            b = random.randint(10, 50)
        question = f"What is {a} ÷ {b}?"
        correct_answer = str(a // b)
        options = [correct_answer] + [str(random.randint(a // b - 5, a // b + 5)) for _ in range(3)]
        random.shuffle(options)

    elif topic == 'fractions':
        numerator = random.randint(1, 10)
        denominator = random.randint(1, 10)
        if grade_level <= 5:
            question = f"What is {numerator}/{denominator} as a decimal?"
            correct_answer = str(round(numerator / denominator, 2))
        else:
            mixed_num = random.randint(1, 5)
            question = f"Convert the mixed fraction {mixed_num} {numerator}/{denominator} to an improper fraction."
            correct_answer = str(mixed_num * denominator + numerator) + "/" + str(denominator)
        options = [correct_answer] + [str(random.randint(1, 20)) + "/" + str(random.randint(1, 20)) for _ in range(3)]
        random.shuffle(options)

    elif topic == 'percentages':
        if grade_level <= 5:
            value = random.randint(1, 100)
            question = f"What is {value}% of 100?"
            correct_answer = str(value)
        else:
            base = random.randint(100, 1000)
            percentage = random.randint(1, 100)
            question = f"What is {percentage}% of {base}?"
            correct_answer = str(round((percentage / 100) * base, 2))
        options = [correct_answer] + [str(random.randint(1, 1000)) for _ in range(3)]
        random.shuffle(options)

    elif topic == 'geometry':
        if grade_level >= 8:
            shapes = ['circle', 'triangle', 'square']
            shape = random.choice(shapes)
            if shape == 'circle':
                radius = random.randint(1, 10)
                area = round(math.pi * radius ** 2, 2)
                question = f"Calculate the area of a circle with radius {radius}."
                correct_answer = str(area)
                options = [correct_answer] + [str(round(random.uniform(0.5, 2) * area, 2)) for _ in range(3)]
                random.shuffle(options)
            elif shape == 'triangle':
                base = random.randint(1, 10)
                height = random.randint(1, 10)
                area = round(0.5 * base * height, 2)
                question = f"Calculate the area of a triangle with base {base} and height {height}."
                correct_answer = str(area)
                options = [correct_answer] + [str(round(random.uniform(0.5, 2) * area, 2)) for _ in range(3)]
                random.shuffle(options)
            elif shape == 'square':
                side = random.randint(1, 10)
                area = side ** 2
                question = f"Calculate the area of a square with side length {side}."
                correct_answer = str(area)
                options = [correct_answer] + [str(random.randint(1, 100)) for _ in range(3)]
                random.shuffle(options)
        else:
            return "Geometry questions are only available for grade level 8 or higher.", [], ""

    elif topic == 'trigonometry':
        if grade_level >= 9:
            angle = random.randint(0, 90)
            question = f"What is sin({angle})?"
            correct_answer = str(round(math.sin(math.radians(angle)), 2))
            options = [correct_answer] + [str(round(random.uniform(0, 1), 2)) for _ in range(3)]
            random.shuffle(options)
        else:
            return "Trigonometry questions are only available for grade level 9 or higher.", [], ""

    elif topic == 'calculus':
        if grade_level >= 11:
            a = random.randint(1, 5)
            question = f"What is the derivative of {a}x^2 with respect to x?"
            correct_answer = f"{2*a}x"
            options = [correct_answer] + [str(random.randint(1, 10)) + "x" for _ in range(3)]
            random.shuffle(options)
        else:
            return "Calculus questions are only available for grade level 11 or higher.", [], ""

    else:
        return "Invalid topic. Please choose from: addition, subtraction, multiplication, division, fractions, percentages, algebra, geometry, trigonometry, calculus", [], ""

    return question, options, correct_answer

def check_answer(question_id, user_answer):
    """
    Checks if the given answer is correct for the specified question.

    Args:
        question_id (str): The ID of the question.
        answer (str): The user's answer.

    Returns:
        tuple: A tuple containing a boolean indicating if the answer is correct and feedback.
    """
    correct_answer = quiz_data.get(question_id)
    if correct_answer is None:
        return False, "Invalid question ID."

    is_correct = (user_answer == correct_answer)
    if is_correct:
        feedback = "Correct!"
    else:
        feedback = f"Incorrect. The correct answer is {correct_answer}."

    return is_correct, feedback
