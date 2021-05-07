import React from 'react';

const MovieList = (props) => {
	return (
		<>
            { 
                props.movies.map((movie) => (
                    <div tabIndex="1" className="movie-container d-flex justify-content-start m-3">
                        <img src={movie.poster} alt={movie.title} />
                        <div className="movie-overlay">
                            <h2>Title: {movie.title}</h2>
                            <h2>Overview:</h2>
                            <p>{movie.overview}</p>
                            <h2>Rating: {movie.rating}/10</h2>
                        </div>
                    </div>                    
                )) 
            }
		</>
	);
};

export default MovieList;