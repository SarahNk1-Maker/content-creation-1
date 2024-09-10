"use client";

import { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Header from './components/header';
const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3', 
    },
  },
});

export default function Home() {
  const [query, setQuery] = useState('');
  const [quiz, setQuiz] = useState(null); 
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [feedback, setFeedback] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const getProblem = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/api/get_quiz', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),  // Send the query string directly
      });

      if (response.ok) {
        const quizData = await response.json();
        setQuiz(quizData);
        setSelectedAnswers({});  // Reset selected answers for the new quiz
        setFeedback([]);  // Clear feedback from previous quizzes
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Error fetching quiz. Please try again.');
      }
    } catch (error) {
      console.error('Fetch error:', error);
      setError('Error fetching quiz. Please check your connection.');
    } finally {
      setIsLoading(false);
    }
  };

  const checkAnswer = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const responses = await Promise.all(quiz.questions.map(async (question) => {
        const response = await fetch('http://localhost:5000/api/check_answer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question_id: question.id, user_answer: selectedAnswers[question.id] }),
        });
        const result = await response.json();
        return result;
      }));

      // Ensure responses contain the feedback correctly
      setFeedback(responses.map(data => data.result || 'No feedback received'));
    } catch (error) {
      console.error('Fetch error:', error);
      setError('Error checking answers. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswerChange = (questionId, event) => {
    setSelectedAnswers({ ...selectedAnswers, [questionId]: event.target.value });
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="sm">
      <Header/>
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            AI Math Teacher
          </Typography>
          <TextField
            fullWidth
            label="Enter a math topic and grade level (e.g., 'algebra 9')"
            variant="outlined"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            margin="normal"
          />
          {error && <Typography color="error">{error}</Typography>}
          <Button variant="contained" onClick={getProblem} sx={{ mt: 2 }} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Get Quiz'}
          </Button>

          {quiz && quiz.questions && (
            <Box sx={{ mt: 4 }}>
              {quiz.questions.map((question) => (
                <Box key={question.id} sx={{ mb: 3 }}>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {question.question}
                  </Typography>
                  <RadioGroup
                    aria-labelledby={`question-${question.id}`}
                    name={`question-${question.id}`}
                    value={selectedAnswers[question.id] || ''}
                    onChange={(event) => handleAnswerChange(question.id, event)}
                  >
                    {question.options.map((option, index) => (
                      <FormControlLabel key={index} value={option} control={<Radio />} label={option} />
                    ))}
                  </RadioGroup>
                </Box>
              ))}
              <Button variant="contained" onClick={checkAnswer} sx={{ mt: 2 }} disabled={isLoading}>
                {isLoading ? 'Checking...' : 'Check Answers'}
              </Button>
              {feedback.length > 0 && (
                <Box sx={{ mt: 4 }}>
                  {feedback.map((fb, index) => (
                    <Typography 
                      key={index} 
                      variant="body1" 
                      sx={{ mt: 2 }} 
                      color={fb.startsWith("Correct") ? 'green' : 'red'}
                    >
                      {fb}
                    </Typography>
                  ))}
                </Box>
              )}
            </Box>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}
