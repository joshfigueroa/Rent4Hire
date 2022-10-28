// For right now, all this does is display the old home page, which has been converted to the login screen.
// To be done: make a button in App.css that goes to this either this or a different page.
import logo from './logo.svg';
import './App.css';
import Message from './components/Message';
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));

function Listing_Page() {
    function handleSubmit(event) {

        event.preventDefault();
        root.render(
            <React.StrictMode>
                <App />
            </React.StrictMode> );

    }
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                Rent4Hire
                <Message/>



                <form method="POST" onSubmit={handleSubmit}>
                    <input name="text" className="App-text-field">
                    </input>
                    <input name="text" className="App-text-field">
                    </input>

                    <button className="App-button" onClick={handleSubmit}>
                        Back
                    </button>

                </form>
            </header>
        </div>
    );
}

export default Listing_Page;