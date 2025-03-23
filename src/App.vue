<script setup>
import { ref, computed, provide } from 'vue';
import { useTheme } from 'vuetify';
import { useRouter } from 'vue-router';
import axios from 'axios';

// Router
const router = useRouter();

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Theme settings
const theme = useTheme();
const title = ref('De Rojas App');
const darkMode = ref(true);

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark';
  darkMode.value = !darkMode.value;
}

// Set initial theme to dark
theme.global.name.value = 'dark';

// Shared state
const loading = ref(false);
const error = ref(null);

// Conversation state
const responseId = ref('');
const conversationHistory = ref([]);

// Models
const models = [
  { value: 'gpt-4o-mini', title: 'GPT-4o Mini' },
  { value: 'gpt-4o', title: 'GPT-4o' },
];
const selectedModel = ref('gpt-4o-mini');

// Computed properties
const isConversationStarted = computed(() => responseId.value !== '');

// Provide shared state to child components
provide('API_BASE_URL', API_BASE_URL);
provide('loading', loading);
provide('error', error);
provide('responseId', responseId);
provide('conversationHistory', conversationHistory);
provide('models', models);
provide('selectedModel', selectedModel);

// Navigation items
const navItems = [
  { title: 'Simple Prompt', to: '/', icon: 'mdi-message-text' },
  { 
    title: 'Continue Conversation', 
    to: '/continue', 
    icon: 'mdi-message-reply-text',
    disabled: computed(() => !isConversationStarted.value)
  },
  { title: 'Web Search', to: '/websearch', icon: 'mdi-web' },
  { title: 'Multimodal', to: '/multimodal', icon: 'mdi-image-text' },
];

// Demo state
const activeTab = ref(0);

// Simple prompt
const simplePrompt = ref('Tell me a joke about programming');
const simpleResponse = ref('');

// Continue conversation
const continuePrompt = ref('');
const continueResponse = ref('');

// Web search
const webSearchPrompt = ref('What are the latest developments in AI?');
const webSearchResponse = ref('');
const webSearchResults = ref([]);

// Multimodal
const multimodalPrompt = ref('What do you see in this image?');
const multimodalResponse = ref('');
const imageUrl = ref('');
const imageFile = ref(null);
const useWebSearch = ref(false);
const previewUrl = ref('');

// Methods
async function sendSimplePrompt() {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await axios.post(`${API_BASE_URL}/simple-prompt`, {
      prompt: simplePrompt.value,
      model: selectedModel.value
    });
    
    simpleResponse.value = response.data.text;
    responseId.value = response.data.id;
    
    // Add to conversation history
    conversationHistory.value.push({
      role: 'user',
      content: simplePrompt.value
    });
    conversationHistory.value.push({
      role: 'assistant',
      content: simpleResponse.value
    });
    
  } catch (err) {
    error.value = err.message || 'An error occurred';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function sendContinuePrompt() {
  if (!responseId.value) {
    error.value = 'You need to send a simple prompt first';
    return;
  }
  
  try {
    loading.value = true;
    error.value = null;
    
    const response = await axios.post(`${API_BASE_URL}/continue-conversation`, {
      prompt: continuePrompt.value,
      response_id: responseId.value,
      model: selectedModel.value
    });
    
    continueResponse.value = response.data.text;
    responseId.value = response.data.id; // Update to the new response ID
    
    // Add to conversation history
    conversationHistory.value.push({
      role: 'user',
      content: continuePrompt.value
    });
    conversationHistory.value.push({
      role: 'assistant',
      content: continueResponse.value
    });
    
    // Clear input
    continuePrompt.value = '';
    
  } catch (err) {
    error.value = err.message || 'An error occurred';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function sendWebSearchPrompt() {
  try {
    loading.value = true;
    error.value = null;
    webSearchResults.value = [];
    
    const response = await axios.post(`${API_BASE_URL}/web-search`, {
      prompt: webSearchPrompt.value,
      model: 'gpt-4o' // Web search requires gpt-4o
    });
    
    webSearchResponse.value = response.data.text;
    webSearchResults.value = response.data.web_search_results;
    
  } catch (err) {
    error.value = err.message || 'An error occurred';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  imageFile.value = file;
  
  // Create a preview
  previewUrl.value = URL.createObjectURL(file);
  
  // Upload the file
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    loading.value = true;
    const response = await axios.post(`${API_BASE_URL}/upload-image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // Store the base64 data from the server response
    imageUrl.value = `data:image/${file.type.split('/')[1]};base64,${response.data.base64}`;
    
  } catch (err) {
    error.value = err.message || 'Failed to upload image';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

async function sendMultimodalPrompt() {
  if (!imageUrl.value) {
    error.value = 'Please upload an image first';
    return;
  }
  
  try {
    loading.value = true;
    error.value = null;
    
    const response = await axios.post(`${API_BASE_URL}/multimodal`, {
      prompt: multimodalPrompt.value,
      image_url: imageUrl.value,
      model: 'gpt-4o', // Multimodal requires gpt-4o
      use_web_search: useWebSearch.value
    });
    
    multimodalResponse.value = response.data.text;
    
  } catch (err) {
    error.value = err.message || 'An error occurred';
    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <v-app>
    <!-- App Bar -->
    <v-app-bar height="auto">
      <v-container class="py-3">
        <div class="d-flex flex-column w-100">
          <div class="d-flex align-center mb-2">
            <div class="app-title-container">
              <img src="/logo.png" alt="Logo" class="app-logo mr-2" />
              <span class="app-title">{{ title }}</span>
            </div>
            <v-spacer></v-spacer>
            <v-btn icon size="small" class="mt-1" @click="toggleTheme">
              <v-icon>{{ darkMode ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
            </v-btn>
          </div>
          
          <!-- Navigation -->
          <v-tabs 
            color="primary"
            hide-slider
            density="comfortable"
            class="mb-1"
            show-arrows
            slider-color="primary"
          >
            <v-tab
              v-for="item in navItems"
              :key="item.title"
              :to="item.to"
              :disabled="item.disabled"
              :prepend-icon="item.icon"
              rounded
              exact
              density="compact"
            >
              {{ item.title }}
            </v-tab>
          </v-tabs>
        </div>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container class="py-8">
        <v-card class="mx-auto mb-6">
          <v-card-title class="text-h5">
            Explore the OpenAI Responses API
          </v-card-title>
          <v-card-text>
            <p>
              This demo app showcases the capabilities of the OpenAI Responses API. 
              Use the navigation bar above to explore different features.
            </p>
          </v-card-text>
        </v-card>
        
        <!-- Error Alert -->
        <v-alert
          v-if="error"
          type="error"
          closable
          class="mb-4"
          @click:close="error = null"
        >
          {{ error }}
        </v-alert>
        
        <!-- Router View -->
        <v-card>
          <v-card-text>
            <router-view></router-view>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer class="bg-surface-variant" dense height="40">
      <v-container class="py-1">
        <div class="text-center">
          &copy; {{ new Date().getFullYear() }} — <strong>{{ title }}</strong>
        </div>
      </v-container>
    </v-footer>
  </v-app>
</template>

<style scoped>
.app-title-container {
  padding: 12px 0;
  display: flex;
  align-items: center;
}

.app-logo {
  height: 36px;
  width: 36px;
  object-fit: contain;
  background-color: transparent;
}

.app-title {
  font-family: 'Inter', sans-serif;
  font-size: 1.6rem;
  font-weight: 600;
  letter-spacing: -0.5px;
  line-height: 1.4;
}

@media (max-width: 600px) {
  .app-title {
    font-size: 1.3rem;
  }
}

.v-app-bar {
  padding: 8px 0;
}

.v-tabs {
  min-height: 48px;
}

.v-card {
  border-radius: 12px;
  overflow: hidden;
}

.v-btn {
  font-weight: 500;
  letter-spacing: 0.5px;
}

.v-container {
  max-width: 1200px;
  padding-left: 16px !important;
  padding-right: 16px !important;
  width: 100%;
}

.response-container {
  border-radius: 8px;
  overflow: hidden;
}

.response-text {
  background-color: rgba(var(--v-theme-surface-variant), 0.4);
  border-radius: 8px;
  line-height: 1.6;
}

.conversation-container {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
  border-radius: 8px;
  padding: 16px;
}

.message {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.user-message {
  align-items: flex-end;
}

.assistant-message {
  align-items: flex-start;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.4;
}

.user-message .message-content {
  background-color: rgb(var(--v-theme-primary));
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant-message .message-content {
  background-color: rgba(var(--v-theme-surface-variant), 0.6);
  border-bottom-left-radius: 4px;
}

.image-preview {
  width: 100%;
  max-height: 300px;
  overflow: hidden;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  border: 1px solid rgba(var(--v-theme-on-surface), 0.1);
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}

.source-link {
  color: rgb(var(--v-theme-primary));
  text-decoration: none;
}

.source-link:hover {
  text-decoration: underline;
}

.v-footer {
  min-height: 40px !important;
  max-height: 40px !important;
}

.v-footer .v-container {
  padding-top: 4px !important;
  padding-bottom: 4px !important;
}
</style>
