<script setup>
import { ref, inject } from 'vue';
import axios from 'axios';

// Access shared state passed from parent
const API_BASE_URL = inject('API_BASE_URL');
const loading = inject('loading');
const error = inject('error');
const conversationHistory = inject('conversationHistory');
const responseId = inject('responseId');

// Simple prompt
const simplePrompt = ref('Tell me a joke about programming');
const simpleResponse = ref('');

// Models
const models = inject('models');
const selectedModel = inject('selectedModel');

async function sendSimplePrompt() {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await axios.post(`${API_BASE_URL}/simple-prompt`, {
      prompt: simplePrompt.value,
      model: selectedModel.value
    });
    
    simpleResponse.value = response.data.text;
    console.log('Response from API:', response.data);
    responseId.value = response.data.id || 'temp-id-' + Date.now();
    
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
</script>

<template>
  <div>
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
    
    <div class="d-flex justify-end mb-6">
      <v-btn
        color="primary"
        size="large"
        :loading="loading"
        @click="sendSimplePrompt"
        min-width="120"
      >
        Send
      </v-btn>
    </div>
    
    <v-divider class="mb-4"></v-divider>
    
    <div v-if="simpleResponse" class="response-container">
      <h4 class="text-subtitle-1 font-weight-bold mb-2">Response:</h4>
      <div class="response-text pa-4">
        <p style="white-space: pre-line">{{ simpleResponse }}</p>
      </div>
    </div>
  </div>
</template> 