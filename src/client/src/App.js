import axios from 'axios';
import './App.css';

const apiCall = () => {
  axios.get('http://localhost:8080').then((data) => {
    console.log(data)
  })
}

const App = () => {
  return (
      <div className="App">
        <header className="App-header">

          <button onClick={apiCall}>Testing Make API Call</button>

        </header>
      </div>
  );
}

export default App