// Matthew Walter - basically converted this into the login screen. That should be the first thing you see anyway.
// To do: add a button that can take you to another page.
import logo from './logo.svg';
import './App.css';
import Message from './components/Message';
import './Listing_Page'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        Rent4Hire

        
        <Message/>
        <form method="POST">

          <input name="text" className="App-text-field">
          </input>
          

          <input type="password" name="text" className="App-text-field">
          </input>
          

          <button className="App-button" >
          Submit
          </button>


        </form>

      </header>
      
    </div>
    
  );
}

export default App;
