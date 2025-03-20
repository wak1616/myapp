<script setup>
import { ref } from 'vue';
import { useTheme } from 'vuetify';

const theme = useTheme();
const title = ref('Vue Vuetify Template');
const darkMode = ref(false);

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark';
  darkMode.value = !darkMode.value;
}
</script>

<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar height="72">
      <v-container>
        <div class="d-flex align-center py-2">
          <v-app-bar-title class="app-title">{{ title }}</v-app-bar-title>
          <v-spacer></v-spacer>
          
          <!-- Theme Toggle -->
          <v-btn icon @click="toggleTheme">
            <v-icon>{{ darkMode ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
          </v-btn>
        </div>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container class="py-8">
        <v-card class="mx-auto">
          <v-card-title class="text-h5">Welcome to Your Vue Project</v-card-title>
          <v-card-text>
            <p>
              This is a clean starter template using Vue 3 and Vuetify 3.
              Simply modify this template to begin building your application.
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary">
              Get Started
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer class="bg-surface-variant">
      <v-container>
        <div class="text-center">
          &copy; {{ new Date().getFullYear() }} — <strong>{{ title }}</strong>
        </div>
      </v-container>
    </v-footer>
  </v-app>
</template>

<style scoped>
.app-title {
  font-family: 'Inter', sans-serif;
  font-size: 1.8rem;
  font-weight: 600;
  letter-spacing: -0.5px;
  line-height: 1.5; /* Improved line height */
  padding: 4px 0; /* Add vertical padding to prevent text cut-off */
}

@media (max-width: 600px) {
  .app-title {
    font-size: 1.2rem;
    line-height: 1.8rem;
  }
}

.v-app-bar-title {
  font-family: 'Inter', sans-serif;
  font-size: 1.8rem !important;
  font-weight: 600;
  letter-spacing: -0.5px;
}

/* Add a bit more style to our card */
.v-card {
  border-radius: 12px;
  overflow: hidden;
}

/* Make buttons more vibrant */
.v-btn {
  font-weight: 500;
  letter-spacing: 0.5px;
}

.v-container {
  max-width: 1200px; /* Adjust this value to control the overall page width */
}
</style>
