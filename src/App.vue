<script setup>
import { ref, computed, onMounted } from 'vue';
import { useTheme } from 'vuetify';
import axios from 'axios';

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Theme settings
const theme = useTheme();
const title = ref('OpenAI Responses API Demo');
const darkMode = ref(false);

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark';
  darkMode.value = !darkMode.value;
}

// Demo state
const activeTab = ref(0);
const loading = ref(false);
const error = ref(null);

// Simple prompt
const simplePrompt = ref('Tell me a joke about programming');
const simpleResponse = ref('');
const responseId = ref('');

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

// Models
const models = [
  { value: 'gpt-4o-mini', title: 'GPT-4o Mini' },
  { value: 'gpt-4o', title: 'GPT-4o' },
];
const selectedModel = ref('gpt-4o-mini');

// Conversation history
const conversationHistory = ref([]);

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

// Computed properties
const isConversationStarted = computed(() => responseId.value !== '');
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
        <v-card class="mx-auto mb-6">
          <v-card-title class="text-h5">
            Explore the OpenAI Responses API
          </v-card-title>
          <v-card-text>
            <p>
              This demo app showcases the capabilities of the OpenAI Responses API. 
              Try out different features using the tabs below.
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
        
        <!-- API Demo Tabs -->
        <v-card>
          <v-tabs
            v-model="activeTab"
            bg-color="primary"
          >
            <v-tab value="0">Simple Prompt</v-tab>
            <v-tab value="1" :disabled="!isConversationStarted">Continue Conversation</v-tab>
            <v-tab value="2">Web Search</v-tab>
            <v-tab value="3">Multimodal</v-tab>
          </v-tabs>
          
          <v-window v-model="activeTab">
            <!-- Simple Prompt Tab -->
            <v-window-item value="0">
              <v-card-text>
                <h3 class="text-h6 mb-2">Basic Text Prompt</h3>
                <p class="mb-4">
                  Try a simple text prompt with the Responses API.
                </p>
                
                <v-select
                  v-model="selectedModel"
                  :items="models"
                  label="Model"
                  density="compact"
                  class="mb-4"
                ></v-select>
                
                <v-textarea
                  v-model="simplePrompt"
                  label="Your prompt"
                  rows="3"
                  auto-grow
                  variant="outlined"
                  class="mb-4"
                  :disabled="loading"
                ></v-textarea>
                
                <v-btn
                  color="primary"
                  block
                  :loading="loading"
                  @click="sendSimplePrompt"
                  class="mb-6"
                >
                  Send
                </v-btn>
                
                <v-divider class="mb-4"></v-divider>
                
                <div v-if="simpleResponse" class="response-container">
                  <h4 class="text-subtitle-1 font-weight-bold mb-2">Response:</h4>
                  <div class="response-text pa-4">
                    <p style="white-space: pre-line">{{ simpleResponse }}</p>
                  </div>
                </div>
              </v-card-text>
            </v-window-item>
            
            <!-- Continue Conversation Tab -->
            <v-window-item value="1">
              <v-card-text>
                <h3 class="text-h6 mb-2">Continue the Conversation</h3>
                <p class="mb-4">
                  The API maintains conversation state, so you can continue where you left off.
                </p>
                
                <!-- Conversation History -->
                <div class="conversation-container mb-4">
                  <div
                    v-for="(message, index) in conversationHistory"
                    :key="index"
                    :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']"
                  >
                    <div class="message-content">
                      <p style="white-space: pre-line">{{ message.content }}</p>
                    </div>
                  </div>
                </div>
                
                <v-textarea
                  v-model="continuePrompt"
                  label="Your next message"
                  rows="3"
                  auto-grow
                  variant="outlined"
                  class="mb-4"
                  :disabled="loading"
                ></v-textarea>
                
                <v-btn
                  color="primary"
                  block
                  :loading="loading"
                  @click="sendContinuePrompt"
                >
                  Continue Conversation
                </v-btn>
              </v-card-text>
            </v-window-item>
            
            <!-- Web Search Tab -->
            <v-window-item value="2">
              <v-card-text>
                <h3 class="text-h6 mb-2">Web Search Tool</h3>
                <p class="mb-4">
                  The Responses API can use OpenAI's web search tool to find information online.
                </p>
                
                <v-textarea
                  v-model="webSearchPrompt"
                  label="Ask a question that requires web search"
                  rows="3"
                  auto-grow
                  variant="outlined"
                  class="mb-4"
                  :disabled="loading"
                ></v-textarea>
                
                <v-btn
                  color="primary"
                  block
                  :loading="loading"
                  @click="sendWebSearchPrompt"
                  class="mb-6"
                >
                  Search & Answer
                </v-btn>
                
                <v-divider class="mb-4"></v-divider>
                
                <div v-if="webSearchResponse" class="response-container">
                  <h4 class="text-subtitle-1 font-weight-bold mb-2">Response:</h4>
                  <div class="response-text pa-4">
                    <p style="white-space: pre-line">{{ webSearchResponse }}</p>
                  </div>
                  
                  <div v-if="webSearchResults.length" class="mt-4">
                    <h4 class="text-subtitle-1 font-weight-bold mb-2">Sources:</h4>
                    <ul>
                      <li v-for="(result, index) in webSearchResults" :key="index" class="mb-2">
                        <template v-if="result.url">
                          <a :href="result.url" target="_blank" class="source-link">
                            {{ result.title || result.url }}
                          </a>
                        </template>
                      </li>
                    </ul>
                  </div>
                </div>
              </v-card-text>
            </v-window-item>
            
            <!-- Multimodal Tab -->
            <v-window-item value="3">
              <v-card-text>
                <h3 class="text-h6 mb-2">Multimodal (Text + Image)</h3>
                <p class="mb-4">
                  The Responses API can process both text and images in a single request.
                </p>
                
                <div class="mb-4">
                  <label for="image-upload" class="d-block mb-2">Upload an image:</label>
                  <input 
                    type="file" 
                    id="image-upload" 
                    accept="image/*"
                    @change="handleImageUpload"
                    :disabled="loading"
                    class="d-none"
                  >
                  <v-btn
                    color="primary" 
                    @click="$refs.fileInput.click()"
                    :disabled="loading"
                    prepend-icon="mdi-image"
                  >
                    Choose Image
                  </v-btn>
                  <input
                    ref="fileInput"
                    type="file"
                    @change="handleImageUpload"
                    accept="image/*"
                    class="d-none"
                  >
                </div>
                
                <div v-if="previewUrl" class="image-preview mb-4">
                  <img :src="previewUrl" alt="Preview" class="preview-image">
                </div>
                
                <v-textarea
                  v-model="multimodalPrompt"
                  label="Ask about the image"
                  rows="3"
                  auto-grow
                  variant="outlined"
                  class="mb-4"
                  :disabled="loading || !imageUrl"
                ></v-textarea>
                
                <v-checkbox
                  v-model="useWebSearch"
                  label="Use web search alongside image analysis"
                  class="mb-4"
                ></v-checkbox>
                
                <v-btn
                  color="primary"
                  block
                  :loading="loading"
                  @click="sendMultimodalPrompt"
                  :disabled="!imageUrl"
                  class="mb-6"
                >
                  Analyze Image
                </v-btn>
                
                <v-divider class="mb-4"></v-divider>
                
                <div v-if="multimodalResponse" class="response-container">
                  <h4 class="text-subtitle-1 font-weight-bold mb-2">Response:</h4>
                  <div class="response-text pa-4">
                    <p style="white-space: pre-line">{{ multimodalResponse }}</p>
                  </div>
                </div>
              </v-card-text>
            </v-window-item>
          </v-window>
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
.app-title {
  font-family: 'Inter', sans-serif;
  font-size: 1.8rem;
  font-weight: 600;
  letter-spacing: -0.5px;
  line-height: 1.5;
  padding: 4px 0;
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
