import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import axios from "axios"
axios.defaults.baseURL = import.meta.env.VITE_APP_API_ENDPOINT
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';


createApp(App).mount('#app')
