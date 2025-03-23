import './assets/main.css'

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
          primary: '#6750a4',   // MD3 default primary
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
          primary: '#d0bcff',   // MD3 dark mode primary
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
  .mount('#app')
