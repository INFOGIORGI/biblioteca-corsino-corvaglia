import { useState } from 'react';
import './App.css';
import axios from 'axios';

const postAPI = async (e, route, args) => {
  e.preventDefault(); // Prevent the default form submission
  try {
    const response = await axios.post("http://localhost:5000" + route, args);
    return response.data;  // Return the complete response data
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

function App() {
  const [libri, setLibri] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [ordinamento, setOrdinamento] = useState("");
  const [attributo, setAttributo] = useState("");

  const cercaLibro = async (e) => {
    e.preventDefault();
    const data = await postAPI(e, "/cercaLibro/", { "parola_chiave": keyword });
    console.log("response:", data);
    setLibri(data);
  };

  const ordinaLibro = async (e) => {
    e.preventDefault();
    // Send the payload as a single JSON object
    const data = await postAPI(e, "/ordinaLibro/", { "attributo": attributo, "ordinamento": ordinamento });
    console.log("ordinaLibro response:", data);
    setLibri(data);
  };

  return (
    <div className="App">
      <h1>Cerca Libri</h1>
      <form onSubmit={cercaLibro}>
        <input
          type="text"
          name="parola_chiave"
          placeholder="Inserisci la parola chiave"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
      <div>
        {Array.isArray(libri) && libri.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Titolo</th>
                <th>ISBN</th>
                <th>Genere</th>
                <th>ID Autore</th>
              </tr>
            </thead>
            <tbody>
              {libri.map((libro, index) => (
                <tr key={index}>
                  <td>{libro.title}</td>
                  <td>{libro.isbn}</td>
                  <td>{libro.genre}</td>
                  <td>{libro.id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No books found.</p>
        )}
      </div>

      <h1>Ordina Libri</h1>
      <form onSubmit={ordinaLibro}>
        <input
          type="text"
          name="attributo"
          placeholder="Inserisci per quale valore si vuole ordinare (titolo, isbn)"
          value={attributo}
          onChange={(e) => setAttributo(e.target.value)}
        />
        <input
          type="text"
          name="ordinamento"
          placeholder="Inserisci l'ordinamento (asc, desc)"
          value={ordinamento}
          onChange={(e) => setOrdinamento(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
      <div>
        {Array.isArray(libri) && libri.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Titolo</th>
                <th>ISBN</th>
                <th>Genere</th>
                <th>ID Autore</th>
              </tr>
            </thead>
            <tbody>
              {libri.map((libro, index) => (
                <tr key={index}>
                  <td>{libro.title}</td>
                  <td>{libro.isbn}</td>
                  <td>{libro.genre}</td>
                  <td>{libro.id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No books found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
