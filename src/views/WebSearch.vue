<script setup>
import { ref, inject } from 'vue';
import axios from 'axios';

// Access shared state passed from parent
const API_BASE_URL = inject('API_BASE_URL');
const loading = inject('loading');
const error = inject('error');

// Web search
const webSearchPrompt = ref('What are the latest developments in AI?');
const webSearchResponse = ref('');
const webSearchResults = ref([]);

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
</script>

<template>
  <div>
    <h3 class="text-h6 mb-2">Web Search Tool</h3>
    <p class="mb-4">
      The Responses API can use OpenAI's web search tool to find information online.
    </p>
    
    <v-textarea
      v-model="webSearchPrompt"
      label="Ask a question that requires current information"
      rows="3"
      auto-grow
      variant="outlined"
      class="mb-4"
      :disabled="loading"
    ></v-textarea>
    
    <div class="d-flex justify-end mb-6">
      <v-btn
        color="primary"
        size="large"
        :loading="loading"
        @click="sendWebSearchPrompt"
        min-width="120"
      >
        Search
      </v-btn>
    </div>
    
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
  </div>
</template> 