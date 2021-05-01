import React from 'react';

const MovieList = (props) => {
    const IMG_API = "https://image.tmdb.org/t/p/w1280";
	return (
		<>
            { 
                props.movies.map((movie) => (
                    <div tabIndex="1" className="movie-container d-flex justify-content-start m-3">
                        <img src={movie.Poster} alt={movie.Title} />
                        <div className="movie-overlay">
                            <h2>Overview:</h2>
                            <p>{movie.Overview}</p>
                        </div>
                    </div>                    
                )) 
            }
		</>
	);
};

export default MovieList;