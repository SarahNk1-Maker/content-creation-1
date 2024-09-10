import os
import json
import time
import uuid

from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from knowledge_base.load_knowledge_base import load_knowledge_base  # Import the function

# Load environment variables from .env.local
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env.local'))

# Initialize SentenceTransformer model
model = SentenceTransformer("intfloat/multilingual-e5-large")

# Initialize Pinecone using the new method
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index_name = "content-2"

# Create a serverless index (if it doesn't exist)
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index(index_name)

def load_and_upsert_knowledge_base():
    # Call the load_knowledge_base function from knowledge_base module
    documents, embeddings = load_knowledge_base()  

    vectors = []
    for d, e in zip(documents, embeddings):
        vectors.append({
            "id": str(d['id']),
            "values": e.tolist(),
            "metadata": {'topic': d['topic'], 'content': d['content']}
        })

    # Upsert into Pinecone index
    index.upsert(vectors=vectors, namespace="ns1")

# Call this function during initialization or after loading documents
load_and_upsert_knowledge_base()

# Wait for the index to be ready
while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

# Retrieve documents from Pinecone based on the user's query
def retrieve_documents(query, k=3):
    # Embed the query using the SentenceTransformer model
    query_embedding = model.encode([query]).tolist()  # Wrap query in a list

    # Query Pinecone index for top k most similar documents
    result = index.query(query_embedding, top_k=k, include_metadata=True, namespace="ns1")

    # Return the retrieved documents along with their IDs, content, and topics
    return [
        {'id': match['id'], 'content': match['metadata']['content'], 'topic': match['metadata']['topic']}
        for match in result['matches']
    ]

# Example of generating a quiz with explanations from Pinecone
def generate_quiz_with_explanations(query):
    # Generate quiz (existing logic)

    # Retrieve relevant explanations from Pinecone
    explanations = retrieve_documents(query)

    # Attach explanations to quiz questions
    questions = []  # Replace this with your quiz generation logic
    for i, question in enumerate(questions):
        if i < len(explanations):
            question['explanation'] = explanations[i]['content']
        else:
            question['explanation'] = "No additional explanation available."

    return {
        'id': str(uuid.uuid4()),  # Generate a unique quiz ID
        'questions': questions
    }
