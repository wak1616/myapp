import './assets/main.css'
import './settings.scss'

// Vuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import { md3 } from 'vuetify/blueprints'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const vuetify = createVuetify({
  blueprint: md3,
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1565C0',   // Lightened royal blue
          secondary: '#625b71', // MD3 secondary
          tertiary: '#7d5260',  // MD3 tertiary
          error: '#b3261e',     // MD3 error
          surface: '#fffbff',   // MD3 surface
          background: '#fffbff' // MD3 background
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#5B7CE2',   // Lightened royal blue for dark mode
          secondary: '#ccc2dc', // MD3 dark mode secondary
          tertiary: '#efb8c8',  // MD3 dark mode tertiary
          error: '#f2b8b5',     // MD3 dark mode error
          surface: '#141218',   // MD3 dark mode surface
          background: '#141218' // MD3 dark mode background
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
  .use(router)
  .mount('#app')
