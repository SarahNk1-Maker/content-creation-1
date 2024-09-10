import json
import os
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('intfloat/multilingual-e5-large')

#from knowledge_base.load_knowledge_base import load_knowledge_base # Import the function


def create_knowledge_base():
    knowledge_base_dir = 'knowledge_base'
    if not os.path.exists(knowledge_base_dir):
        os.makedirs(knowledge_base_dir)

    # Grade 2: Addition
    create_json_file(knowledge_base_dir, 'addition_grade2.json', "Addition (Grade 2)", 
                     "Addition is finding the total or sum by combining two or more numbers. We use the plus sign (+) for addition. For example, 3 + 5 = 8.")

    # Grade 3: Subtraction
    create_json_file(knowledge_base_dir, 'subtraction_grade3.json', "Subtraction (Grade 3)", 
                     "Subtraction is taking one number away from another. We use the minus sign (-) for subtraction. For example, 7 - 3 = 4.")

    # Grade 4: Multiplication
    create_json_file(knowledge_base_dir, 'multiplication_grade4.json', "Multiplication (Grade 4)", 
                     "Multiplication is repeated addition. We use the times sign (x) or asterisk (*) for multiplication. For example, 4 x 3 = 12, which is the same as 4 + 4 + 4.")

    # Grade 5: Division
    create_json_file(knowledge_base_dir, 'division_grade5.json', "Division (Grade 5)",
                     "Division is splitting into equal parts or groups. We use the division sign (÷) or slash (/) for division. For example, 12 ÷ 3 = 4, which means 12 can be divided into 3 groups of 4 each.")

    # Grade 6: Fractions
    create_json_file(knowledge_base_dir, 'fractions_grade6.json', "Fractions (Grade 6)",
                     "A fraction represents a part of a whole. It has a numerator (top number) and a denominator (bottom number). For example, 3/4 means 3 out of 4 equal parts.")

    # Grade 7: Decimals
    create_json_file(knowledge_base_dir, 'decimals_grade7.json', "Decimals (Grade 7)",
                     "Decimals are a way to represent parts of a whole using a decimal point. For example, 0.5 is equivalent to 1/2 or half.")

    # Grade 8: Percentages
    create_json_file(knowledge_base_dir, 'percentages_grade8.json', "Percentages (Grade 8)",
                     "Percentages are a way to express a number as a fraction of 100. The symbol for percent is %. For example, 50% is equivalent to 50/100 or 1/2.")

    # Grade 9: Algebra
    create_json_file(knowledge_base_dir, 'algebra_grade9.json', "Algebra (Grade 9)",
                     "Algebra involves using letters (variables) to represent unknown numbers and solving equations to find their values. For example, in the equation x + 3 = 7, we solve for x to find that x = 4.")

    # Grade 10: Geometry
    create_json_file(knowledge_base_dir, 'geometry_grade10.json', "Geometry (Grade 10)",
                     "Geometry is the study of shapes, sizes, and properties of figures in space. It involves concepts like points, lines, angles, triangles, circles, and more.")

def create_json_file(directory, filename, topic, content):
    data = {
        "topic": topic,
        "content": content
    }
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_knowledge_base():
    documents = []
    for filename in os.listdir('knowledge_base'):
        if filename.endswith('.json'):
            with open(os.path.join('knowledge_base', filename)) as f:
                data = json.load(f)
                documents.append({
                    'id': len(documents),  
                    'content': data['content'],
                    'topic': data['topic']
                })

    # Embed documents
    embeddings = model.encode([doc['content'] for doc in documents])

    return documents, embeddings 

if __name__ == '__main__':
    create_knowledge_base()