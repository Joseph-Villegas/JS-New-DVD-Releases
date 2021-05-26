# JS-New-DVD-Releases

**JS-New-DVD-Releases** is a containerized web application that provides a weekly schedule for DVD releases.
The front end is dynamically rendered using React.js and styled using Bootstrap and CSS. The backend is a REST API which follows the Python Flask framework.
When the server first loads a web scrape is performed to retrieve DVD release information by week from this [source](https://www.dvdsreleasedates.com). From this scrape all the movies IMDb IDs are provided and more information on the movies are gathered by making several HTTP request to the TMDB API at once using the Python modules asyncio and aiohttp. These results are then stored in a MySQL database (MariaDB) through the SQL Alchemy ORM. The backend provides several endpoints to retrieve all movies by week or the movies released for a specific week.

## How to run the app using Docker
- Ensure you set the environment variables for the database URI and the TMDB API key
- Alse, make sure you have docker installed on your local machine.
- Run `docker-compose up` in the root directory
- Navigate to `http://localhost:3000` in the browser to view the client.
- Navigate to `http://localhost:80` in the browser to view the server.

## Backend/Python Modules Used
- Flask
- Requests
- Beautiful Soup
- SQLAlchemy
- Flask SQLAlchemy
- AsyncIO
- AIOHTTP
- APScheduler

## Frontend/Javascript (Node.js) Packages Used
- Bootstrap Library
- React.js
- Fetch API

 
