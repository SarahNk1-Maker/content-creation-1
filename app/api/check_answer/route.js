//api/check_answer/route.js
export default async function handler(req, res) {
    if (req.method === 'POST') {
      const { question_id, answer } = req.body;
  
      try {
        // Make a request to your Flask backend to check the answer
        const backendResponse = await fetch('http://localhost:5000/api/check_answer', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question_id, answer }),
        });
  
        if (backendResponse.ok) {
          const feedbackData = await backendResponse.json();
          res.status(200).json(feedbackData);
        } else {
          console.error('Error checking answer on backend:', backendResponse.statusText);
          res.status(500).json({ error: 'Internal Server Error' });
        }
      } catch (error) {
        console.error('Error checking answer:', error);
        res.status(500).json({ error: 'Internal Server Error' });
      }
    } else {
      res.status(405).end(); // Method Not Allowed
    }
  }