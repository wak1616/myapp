<script setup>
import { ref, inject, computed } from 'vue';
import axios from 'axios';

// Access shared state passed from parent
const API_BASE_URL = inject('API_BASE_URL');
const loading = inject('loading');
const error = inject('error');
const conversationHistory = inject('conversationHistory');
const responseId = inject('responseId');

// Continue conversation
const continuePrompt = ref('');
const continueResponse = ref('');

// Models
const models = inject('models');
const selectedModel = inject('selectedModel');

// Computed properties
const isConversationStarted = computed(() => responseId.value !== '');

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
</script>

<template>
  <div>
    <h3 class="text-h6 mb-2">Continue the Conversation</h3>
    <p class="mb-4">
      The API maintains conversation state, so you can continue where you left off.
    </p>
    
    <!-- Warning if no conversation started -->
    <v-alert
      v-if="!isConversationStarted"
      type="info"
      class="mb-4"
    >
      Please start a conversation in the Simple Prompt section first.
    </v-alert>
    
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
      :disabled="loading || !isConversationStarted"
    ></v-textarea>
    
    <v-btn
      color="primary"
      block
      :loading="loading"
      @click="sendContinuePrompt"
      :disabled="!isConversationStarted"
    >
      Continue Conversation
    </v-btn>
  </div>
</template> 