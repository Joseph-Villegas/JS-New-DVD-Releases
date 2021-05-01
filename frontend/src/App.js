// Import React elements
import React, { useState, useEffect } from 'react';

// Import stylesheets
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'; 

// Import functional components
import MovieList from './components/MovieList';
import WeekHeading from './components/WeekHeading';

// Temporary mock data
const SAMPLE_MOVIES = [
  {
    "Title": "Star Wars: The Last Jedi",
    "Poster": "https://m.media-amazon.com/images/M/MV5BMjQ1MzcxNjg4N15BMl5BanBnXkFtZTgwNzgwMjY4MzI@._V1_SX300.jpg",
    "IMDbID": "1",
    "Overview": "This is a movie. This is the overview of said movie.",
    "Vote_Avg": "2"
  },
  {
    "Title": "Star Wars: The Last Jedi",
    "Poster": "https://m.media-amazon.com/images/M/MV5BMjQ1MzcxNjg4N15BMl5BanBnXkFtZTgwNzgwMjY4MzI@._V1_SX300.jpg",
    "IMDbID": "1",
    "Overview": "This is a movie. This is the overview of said movie.",
    "Vote_Avg": "2"
  },
  {
    "Title": "Star Wars: The Last Jedi",
    "Poster": "https://m.media-amazon.com/images/M/MV5BMjQ1MzcxNjg4N15BMl5BanBnXkFtZTgwNzgwMjY4MzI@._V1_SX300.jpg",
    "IMDbID": "1",
    "Overview": "This is a movie. This is the overview of said movie.",
    "Vote_Avg": "2"
  },
  {
    "Title": "Star Wars: The Last Jedi",
    "Poster": "https://m.media-amazon.com/images/M/MV5BMjQ1MzcxNjg4N15BMl5BanBnXkFtZTgwNzgwMjY4MzI@._V1_SX300.jpg",
    "IMDbID": "1",
    "Overview": "This is a movie. This is the overview of said movie.",
    "Vote_Avg": "2"
  },
  {
    "Title": "Star Wars: The Last Jedi",
    "Poster": "https://m.media-amazon.com/images/M/MV5BMjQ1MzcxNjg4N15BMl5BanBnXkFtZTgwNzgwMjY4MzI@._V1_SX300.jpg",
    "IMDbID": "1",
    "Overview": "This is a movie. This is the overview of said movie.",
    "Vote_Avg": "2"
  }
];

const App = () => {
	const [movies, setMovies] = useState([]);

	const getWeeklyReleases= async () => {
    /* 
      TODO: Retreive actual weekly release info. from backend
      const url = ``;
      const response = await fetch(url);
      const data = await response.json();
      setMovies(data);
    */
    setMovies(SAMPLE_MOVIES);
	};

  // Retrieves weekly releases on page load
	useEffect(() => {
		getWeeklyReleases();
	}, []);

  // Render components on the page
	return (
		<div className='container-fluid releases-container'>
      <div className='row d-flex align-items-center justify-content-center mt-4 mb-4'>
				<h1>Weekly DVD Releases</h1>
			</div>
			<div className='row d-flex align-items-center mt-4 mb-4'>
				<WeekHeading week='This Week' />
			</div>
			<div className='row'>
				<MovieList movies={movies} />
			</div>
			<div className='row d-flex align-items-center mt-4 mb-4'>
				<WeekHeading week='Next Week' />
			</div>
			<div className='row'>
				<MovieList movies={movies} />
			</div>
		</div>
	);
};

export default App;