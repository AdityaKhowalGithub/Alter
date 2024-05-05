import axios from 'axios';
import './App.css';
import validator from 'validator/es';
import { useState } from 'react';

const testApiCall = () => {
    axios.get('http://localhost:8080').then((data) => {
        console.log(data)
    });
}

const App = () => {
    const [errorMessage, setErrorMessage] = useState('');

    const validate = (value) => {
        if (!validator.isURL(value)) {
            setErrorMessage('Invalid URL');
            return false;
        } else {
            setErrorMessage('');
            return true;
        }
    }

    const submitURL = (e) => {
        e.preventDefault();
        const inputElement = document.getElementById('user-input');
        const inputValue = inputElement.value;

        if (validate(inputValue)) {
            axios.get(inputValue)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    }

    const clearErrorMessage = () => {
        setErrorMessage('');
    }

    return (
        <div className="App">
            <div className={"input-content-wrapper"}>
                <p className={"page-header"}>Generate Alt text for website</p>

                <div className={"input-and-submit"}>
                    <div className={"user-input-field"}>
                        <input type="input" id={"user-input"} placeholder={"Add your URL here"} name={"Website URL"}
                               required onChange={clearErrorMessage}/>
                        <label htmlFor={"Website URL"} className={"user-input-label"}>Website URL</label>
                    </div>

                    <button id={"submit-user-input-button"} role={"button"} onClick={submitURL}>Submit</button>
                    {errorMessage && <span id={"url-error"}>{errorMessage}</span>}
                    {/*  the fact that this moves bothers me so much  */}
                </div>

            </div>

            {/*<button onClick={testApiCall}>Testing Make API Call</button>*/}

        </div>
    );
}

export default App;