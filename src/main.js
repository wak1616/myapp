import './assets/main.css'

// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import { createApp } from 'vue'
import App from './App.vue'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#3f51b5',   // Indigo
          secondary: '#673ab7', // Deep Purple
          accent: '#2196f3',    // Blue
          error: '#f44336',     // Red
          info: '#00bcd4',      // Cyan
          success: '#4caf50',   // Green
          warning: '#ff9800',   // Orange
          background: '#f5f5f5' // Light gray background
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#7986cb',    // Lighter Indigo for dark mode
          secondary: '#9575cd',  // Lighter Deep Purple
          accent: '#64b5f6',     // Lighter Blue
          error: '#e57373',      // Lighter Red
          info: '#4dd0e1',       // Lighter Cyan
          success: '#81c784',    // Lighter Green
          warning: '#ffb74d',    // Lighter Orange
          background: '#121212'  // Dark background
        }
      }
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

createApp(App)
  .use(vuetify)
  .mount('#app')
