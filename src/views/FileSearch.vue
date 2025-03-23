<script setup>
import { ref, inject, computed } from 'vue';
import axios from 'axios';

// Access shared state passed from parent
const API_BASE_URL = inject('API_BASE_URL');
const loading = inject('loading');
const error = inject('error');

// File Search State
const pdfsUploaded = ref(false);
const vectorStoreId = ref('');
const vectorStoreName = ref('');
const selectedFiles = ref([]);
const filesList = ref([]);
const searchQuery = ref('');
const searchResponse = ref('');
const retrievedFiles = ref([]);

// Upload file to backend
async function handleFileUpload(event) {
  const files = event.target.files;
  if (!files || files.length === 0) return;
  
  selectedFiles.value = Array.from(files);
  
  try {
    loading.value = true;
    error.value = null;
    
    // Create a vector store if not already created
    if (!vectorStoreId.value) {
      const storeResponse = await axios.post(`${API_BASE_URL}/create-vector-store`, {
        name: 'user_files_store'
      });
      
      vectorStoreId.value = storeResponse.data.id;
      vectorStoreName.value = storeResponse.data.name;
    }
    
    // Upload files one by one
    for (const file of selectedFiles.value) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('vector_store_id', vectorStoreId.value);
      
      const uploadResponse = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      // Add to list of uploaded files
      filesList.value.push({
        name: file.name,
        size: formatFileSize(file.size),
        status: 'Uploaded',
        id: uploadResponse.data.file_id
      });
    }
    
    pdfsUploaded.value = true;
    selectedFiles.value = [];
    
  } catch (err) {
    error.value = err.message || 'Failed to upload PDFs';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

// Format file size
function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' bytes';
  else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  else return (bytes / 1048576).toFixed(1) + ' MB';
}

// Send search query to backend
async function sendSearchQuery() {
  if (!searchQuery.value) {
    error.value = 'Please enter a search query';
    return;
  }
  
  if (!vectorStoreId.value) {
    error.value = 'Please upload PDF files first';
    return;
  }
  
  try {
    loading.value = true;
    error.value = null;
    
    const response = await axios.post(`${API_BASE_URL}/file-search`, {
      prompt: searchQuery.value,
      vector_store_id: vectorStoreId.value,
      model: 'gpt-4o' // File search requires gpt-4o
    });
    
    searchResponse.value = response.data.text;
    retrievedFiles.value = response.data.retrieved_files || [];
    
  } catch (err) {
    error.value = err.message || 'An error occurred';
    console.error(err);
  } finally {
    loading.value = false;
  }
}

// Reset the component state
function resetState() {
  searchQuery.value = '';
  searchResponse.value = '';
  selectedFiles.value = [];
  retrievedFiles.value = [];
  error.value = null;
}
</script>

<template>
  <div>
    <h3 class="text-h6 mb-2">File Search (RAG)</h3>
    <p class="mb-4">
      Upload PDF files and ask questions about their content using OpenAI's Retrieval-Augmented Generation.
    </p>
    
    <v-card class="mb-6 pa-4">
      <v-card-title>1. Upload PDF Files</v-card-title>
      <v-card-text>
        <div class="mb-4">
          <label for="pdf-upload" class="d-block mb-2">Upload PDF files:</label>
          <input 
            type="file" 
            id="pdf-upload" 
            accept="application/pdf"
            multiple
            @change="handleFileUpload"
            :disabled="loading"
            class="d-none"
          >
          <v-btn
            color="primary" 
            @click="$refs.fileInput.click()"
            :disabled="loading"
            prepend-icon="mdi-file-pdf-box"
          >
            Choose PDF Files
          </v-btn>
          <input
            ref="fileInput"
            type="file"
            @change="handleFileUpload"
            accept="application/pdf"
            multiple
            class="d-none"
          >
        </div>
        
        <div v-if="filesList.length > 0" class="mb-4">
          <h4 class="text-subtitle-1 mb-2">Uploaded Files:</h4>
          <v-list density="compact">
            <v-list-item v-for="(file, index) in filesList" :key="index">
              <v-list-item-title>
                {{ file.name }} ({{ file.size }})
              </v-list-item-title>
              <v-list-item-subtitle>
                Status: {{ file.status }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </div>
        
        <v-alert
          v-if="pdfsUploaded"
          type="success"
          density="compact"
          class="mb-4"
        >
          Vector store created: {{ vectorStoreName }}
        </v-alert>
      </v-card-text>
    </v-card>
    
    <v-card class="mb-6 pa-4">
      <v-card-title>2. Ask Questions About Your Documents</v-card-title>
      <v-card-text>
        <v-textarea
          v-model="searchQuery"
          label="What would you like to ask about these PDFs?"
          rows="3"
          auto-grow
          variant="outlined"
          class="mb-4"
          :disabled="loading || !pdfsUploaded"
        ></v-textarea>
        
        <div class="d-flex justify-end mb-4">
          <v-btn
            color="primary"
            size="large"
            :loading="loading"
            @click="sendSearchQuery"
            :disabled="!pdfsUploaded || !searchQuery"
            min-width="120"
            class="mr-2"
          >
            Search
          </v-btn>
          <v-btn
            variant="outlined"
            size="large"
            @click="resetState"
            min-width="120"
          >
            Reset
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    
    <v-divider class="mb-4"></v-divider>
    
    <div v-if="searchResponse" class="response-container">
      <h4 class="text-subtitle-1 font-weight-bold mb-2">Response:</h4>
      <div class="response-text pa-4 mb-4">
        <p style="white-space: pre-line">{{ searchResponse }}</p>
      </div>
      
      <div v-if="retrievedFiles.length > 0">
        <h4 class="text-subtitle-1 font-weight-bold mb-2">Retrieved From:</h4>
        <v-list density="compact">
          <v-list-item v-for="(file, index) in retrievedFiles" :key="index">
            <v-list-item-title>
              {{ file.filename }}
            </v-list-item-title>
            <v-list-item-subtitle v-if="file.score">
              Relevance: {{ (file.score * 100).toFixed(1) }}%
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </div>
    </div>
  </div>
</template>

<style scoped>
.response-text {
  background-color: rgba(var(--v-theme-surface-variant), 0.4);
  border-radius: 8px;
  line-height: 1.6;
}
</style> 