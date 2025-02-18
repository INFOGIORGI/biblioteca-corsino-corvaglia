import { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [libri, setLibri] = useState([]);
  const [keyword, setKeyword] = useState("");

  const fetchAPI = async (e) => {
    e.preventDefault(); // Prevent the default form submission
    try {
      const response = await axios.post("http://localhost:5000/cercaLibro/", {
        parola_chiave: keyword
      });
      setLibri(response.data.response);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <>
      <h1>Cerca Libri</h1>
      <form onSubmit={fetchAPI}>
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
        {libri.length > 0 ? (
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
    </>
  );
}

export default App;
