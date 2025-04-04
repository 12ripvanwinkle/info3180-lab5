<template>
    <div class="container mt-4">
        <h2>Add A Movie</h2>
        <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data">

            <div class="form-group mb-3">
                <label for="title" class="form-label">Movie Title</label>
                <input type="text" id="title" v-model="movie.title" class="form-control" required>  
            </div>

            <div class="form-group mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea id="description" v-model="movie.description" class="form-control" required></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="poster" class="form-label">Movie Poster</label>
                <input type="file" id="poster" @change="handleFileUpload" class="form-control" required>
            </div>

            <button type="submit" class="btn btn-primary">Submit</button>

            <div v-if="errorMessage" class="alert alert-danger mt-3">
                {{ errorMessage }}
            </div>

            <div v-if="successMessage" class="alert alert-success mt-3">
                {{ successMessage }}
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const movie = ref({
    title: "",
    description: "",
    poster: null
});

const errorMessage = ref("");
const successMessage = ref("");

// this handles file inputs
const handleFileUpload = (event) =>{
    movie.value.poster = event.target.files[0];
};

// Function to submit the movie data
const saveMovie = async () => {
    const formData = new FormData();
    formData.append("title", movie.value.title);
    formData.append("description", movie.value.description);
    formData.append("poster", movie.value.poster);

    try{
        const response = await fetch("/api/v1/movies",{
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
      successMessage.value = data.message;
      errorMessage.value = "";
      movie.value.title = "";
      movie.value.description = "";
      movie.value.poster = null;
    } else {
      errorMessage.value = data.errors.join(", ");
      successMessage.value = "";
    }
  } catch (error) {
    console.error("Error:", error);
    errorMessage.value = "An error occurred while submitting the form.";
    successMessage.value = "";
  }

};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
