// Import React elements
import React, { useState, useEffect } from 'react';

// Import stylesheets
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'; 

// Import functional components
import MovieList from './components/MovieList';
import WeekHeading from './components/WeekHeading';

const App = () => {
	const [moviesByWeek, setMoviesByWeek] = useState([]);

	const getWeeklyReleases= async () => {
      const response = await fetch("/api/all-releases");
      const data = await response.json();

      let moviesByWeek = data.query_results.reduce((hash, obj) => ({...hash, [obj.release_week]:( hash[obj.release_week] || [] ).concat(obj)}), {});
      console.log(Object.entries(moviesByWeek));
      setMoviesByWeek(Object.entries(moviesByWeek));
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
      <>
        {
          moviesByWeek.map((week) => (
            <>
              <div key={week[0]} className='row d-flex align-items-center mt-4 mb-4'>
                <WeekHeading week={week[0]} />
              </div>
              <div className='row'>
                <MovieList movies={week[1]} />
              </div>
            </>
          ))
        }
      </>
		</div>
	);
};

export default App;