import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'

const rootEl = document.getElementById('root')
try {
  createRoot(rootEl).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
} catch (err) {
  rootEl.innerHTML = `
    <div style="padding: 2rem; font-family: sans-serif; background: #1a1a1a; color: #fff; min-height: 100vh;">
      <h1 style="color: #f87171;">App failed to load</h1>
      <pre style="background: #333; padding: 1rem; overflow: auto;">${err.message}\n\n${err.stack || ''}</pre>
    </div>
  `
}
