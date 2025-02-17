import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

function App() {
  const [parolaChiave, setParolaChiave] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    const response = await fetch('http://localhost:5000/cercaLibro/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ parola_chiave: parolaChiave }),
    });

    const data = await response.json();
    setResponse(data);
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <input
          name="parola_chiave"
          type="text"
          value={parolaChiave}
          onChange={(e) => setParolaChiave(e.target.value)}
        />
        <input type="submit" value="Cerca Libro" />
      </form>
      {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
    </>
  );
}

export default App;
