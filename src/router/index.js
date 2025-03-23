import { createRouter, createWebHistory } from 'vue-router'

// Create component imports for each route
// These will be lazy-loaded when the route is visited
const SimplePrompt = () => import('../views/SimplePrompt.vue')
const ContinueConversation = () => import('../views/ContinueConversation.vue')
const WebSearch = () => import('../views/WebSearch.vue')
const Multimodal = () => import('../views/Multimodal.vue')

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    {
      path: '/',
      name: 'simple-prompt',
      component: SimplePrompt
    },
    {
      path: '/continue',
      name: 'continue-conversation',
      component: ContinueConversation
    },
    {
      path: '/websearch',
      name: 'web-search',
      component: WebSearch
    },
    {
      path: '/multimodal',
      name: 'multimodal',
      component: Multimodal
    },
    // Redirect any unknown routes to home
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

export default router 