import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import vuetify from 'vite-plugin-vuetify'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    vuetify({
      autoImport: true,
      styles: { configFile: 'src/settings.scss' }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // Configure fs.allow to include node_modules for @mdi/font
  server: {
    fs: {
      // Allow serving files from these directories
      allow: ['..', 'node_modules'],
    },
  },
  // Build configuration for production
  build: {
    // Generate source maps for better debugging
    sourcemap: true,
    // Rollup options
    rollupOptions: {
      // Make sure to exclude these dependencies from the bundle
      external: [],
      output: {
        // Chunk naming and organization
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router'],
          'vuetify-vendor': ['vuetify']
        }
      }
    }
  },
  // Ensure Vue Router is pre-bundled
  optimizeDeps: {
    include: ['vue-router']
  }
})
