import { useState, useEffect } from 'react';
// import reactLogo from './assets/react.svg';
// import viteLogo from '/vite.svg';
import './App.css';
import axios from 'axios';


function App() {

  const [libri, setLibri] = useState([]);

  const fetchAPI = async (parola_chiave) => {
    const response = await axios.post("http://localhost:5000/cercaLibro/",{"parola_chiave":parola_chiave});
    setLibri(response.data.response);
    return
  };
  useEffect(()=>{
    fetchAPI("a")
    console.log(libri)
  },[])
  return (
    <>
      <h1>Cerca Libri</h1>
      
    </>
  );
}

export default App;
