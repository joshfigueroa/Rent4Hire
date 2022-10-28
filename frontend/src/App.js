// Matthew Walter - basically converted this into the login screen. That should be the first thing you see anyway.
// To do: add a button that can take you to another page.
// this is technically a change
import logo from './logo.svg';
import './App.css';
import './Listing_Page.js'
import Listing_Page from './Listing_Page.js';
import ReactDOM from 'react-dom/client';
import React, { useState } from "react";

const root = ReactDOM.createRoot(document.getElementById('root'));


function App() {
    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    function validateForm() {

        return email.length > 0 && password.length > 0;

    }

    function handleSubmit(event) {

        event.preventDefault();
        root.render(

            <React.StrictMode>
                <Listing_Page />
            </React.StrictMode>

        );

    }

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                Rent4Hire



                <form method="POST" onSubmit={handleSubmit}>

                    <input name="text" className="App-text-field">
                    </input>


                    <input type="password" name="text" className="App-text-field">
                    </input>


                    <button className="App-button">
                        Submit
                    </button>





                </form>

            </header>

        </div>


    );
}

export default App;