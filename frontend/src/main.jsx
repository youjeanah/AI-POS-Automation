import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import POSApp from './POSApp.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <POSApp />
  </StrictMode>,
)
