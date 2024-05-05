import axios from 'axios';
import './App.css';

const testApiCall = () => {
    axios.get('http://localhost:8080').then((data) => {
        console.log(data)
    });
}

const App = () => {
    return (
        <div className="App">
            <div className={"input-content-wrapper"}>
                <p className={"page-header"}>Generate Alt text for website</p>

                <div className={"input-and-submit"}>
                    <div className="user-input-field">
                        <input type="input" className="user-input" placeholder="Add your URL here" name="Website URL"
                               required/>
                        <label htmlFor={"Website URL"} className="user-input-label">Website URL</label>
                    </div>

                    <button id={"submit-user-input-button"} role={"button"}>Submit</button>
                </div>

            </div>

            {/*<button onClick={testApiCall}>Testing Make API Call</button>*/}

        </div>
    );
}

export default App;