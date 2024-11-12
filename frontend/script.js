document.addEventListener("DOMContentLoaded", function () {
    // Fetch and display movies when the page loads
    fetchMovies();

    // Handle form submission to add a movie
    const form = document.getElementById('add-movie-form');
    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        
        const name = document.getElementById('name').value;
        const plot = document.getElementById('plot').value;
        const genres = document.getElementById('genres').value.split(',').map(genre => genre.trim());
        const casts = document.getElementById('casts').value.split(',').map(cast => cast.trim());

        const newMovie = {
            name: name,
            plot: plot,
            genres: genres,
            casts: casts
        };
        
        // POST the new movie to the backend
        const response = await fetch('http://localhost:8000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newMovie)
        });

        if (response.ok) {
            fetchMovies(); // Refresh the movie list after adding a new movie
            form.reset();  // Reset the form
        } else {
            alert('Failed to add movie');
        }
    });
});

async function fetchMovies() {
    const response = await fetch('http://localhost:8000/');
    const movies = await response.json();
    const moviesContainer = document.getElementById('movies-container');
    moviesContainer.innerHTML = ''; // Clear previous content

    movies.forEach(movie => {
        const movieElement = document.createElement('div');
        movieElement.innerHTML = `<h3>${movie.name}</h3><p>${movie.plot}</p><p><strong>Genres:</strong> ${movie.genres.join(', ')}</p><p><strong>Casts:</strong> ${movie.casts.join(', ')}</p>`;
        moviesContainer.appendChild(movieElement);
    });
}
