<template>
    <div>
        <h1>All Movies</h1>
        <div v-if="movies.length === 0"> No Movies Found.</div>
        <div v-else class="movie-grid">
            <div v-for="movie in movies" :key="movie.id" class="movie-card">
                <img :src="movie.poster" alt="Movie Poster" class="poster" />
                <h2>{{ movie.title }}</h2>
                <p>{{ movie.description }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

// Define fetchMovies() function
const fetchMovies = async () => {
  try {
    const response = await fetch("/api/v1/movies");
    const data = await response.json();
    movies.value = data.movies;
  } catch (error) {
    console.error("Failed to fetch movies:", error);
  }
};

// Run fetchMovies() on page load
onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
.container {
  padding: 2rem;
}

.movie-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.movie-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 1rem;
  width: 250px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background: #fff;
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: scale(1.02);
}

.poster {
  width: 100%;
  height: auto;
  border-radius: 8px;
}
</style>