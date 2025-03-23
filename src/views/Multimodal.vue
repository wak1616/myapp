<script setup>
import { ref, inject } from 'vue';
import axios from 'axios';

// Access shared state passed from parent
const API_BASE_URL = inject('API_BASE_URL');
const loading = inject('loading');
const error = inject('error');

// Multimodal
const multimodalPrompt = ref('What do you see in this image?');
const multimodalResponse = ref('');
const imageUrl = ref('');
const imageFile = ref(null);
const useWebSearch = ref(false);
const previewUrl = ref('');

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
  <div>
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
      label="What would you like to ask about this image?"
      rows="3"
      auto-grow
      variant="outlined"
      class="mb-4"
      :disabled="loading || !previewUrl"
    ></v-textarea>
    
    <v-checkbox
      v-model="useWebSearch"
      label="Use web search alongside image analysis"
      class="mb-4"
    ></v-checkbox>
    
    <div class="d-flex justify-end mb-6">
      <v-btn
        color="primary"
        size="large"
        :loading="loading"
        @click="sendMultimodalPrompt"
        :disabled="!previewUrl"
        min-width="120"
      >
        Analyze
      </v-btn>
    </div>
    
    <v-divider class="mb-4"></v-divider>
    
    <div v-if="multimodalResponse" class="response-container">
      <h4 class="text-subtitle-1 font-weight-bold mb-2">Response:</h4>
      <div class="response-text pa-4">
        <p style="white-space: pre-line">{{ multimodalResponse }}</p>
      </div>
    </div>
  </div>
</template> 