// app/api/get_quiz/route.js

export async function POST(req) {
  try {
    const { query } = await req.json(); // Parse the request body

    // Make a request to your Flask backend to get the quiz
    const backendResponse = await fetch(' http://localhost:5000/api/get_quiz', { // Replace with the actual URL of your Flask backend
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (backendResponse.ok) {
      const quizData = await backendResponse.json();
      return new Response(JSON.stringify(quizData), { status: 200 });
    } else {
      console.error('Error fetching quiz from backend:', backendResponse.statusText);
      return new Response(JSON.stringify({ error: 'Internal Server Error' }), { status: 500 });
    }
  } catch (error) {
    console.error('Error fetching quiz:', error);
    return new Response(JSON.stringify({ error: 'Internal Server Error' }), { status: 500 });
  }
}

export async function GET() {
  return new Response('GET method is not allowed', { status: 405 });
}
