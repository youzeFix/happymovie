<template>
  <div class="home">
    <MovieLibrary/>
  </div>
</template>

<script>
// @ is an alias to /src
import MovieLibrary from '@/components/MovieLibrary.vue'

export default {
  name: 'Home',
  components: {
    MovieLibrary
  }
}
</script>
