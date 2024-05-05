// import logo from './logo.svg';
// import './App.css';
//
// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
//
// export default App;
//
import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');

  const handleChange = (event) => {
    setPrompt(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
               <p>
          Enter your prompt below:
        </p>
        <input
          type="text"
          value={prompt}
          onChange={handleChange}
          placeholder="Type something..."
          className="App-input"
        />
        <p className="App-display">
          {prompt ? `Your prompt: ${prompt}` : "Your entered prompt will appear here..."}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

