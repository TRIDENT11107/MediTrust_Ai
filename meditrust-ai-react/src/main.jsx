import React, { useEffect } from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'
import './theme-overrides.css'

function Root(){
  useEffect(()=>{
    try{ window.AOS && window.AOS.init({ duration:800, easing:'ease-in-out', once:true }); }catch(e){}
    try{ window.feather && window.feather.replace(); }catch(e){}
  },[])
  return <App />
}

ReactDOM.createRoot(document.getElementById('root')).render(<React.StrictMode><Root /></React.StrictMode>)
