// For right now, all this does is display the old home page, which has been converted to the login screen. 
// To be done: make a button in App.css that goes to this either this or a different page.
import logo from './logo.svg';
import './App.css';
import Message from './components/Message';

function Listing_Page() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        Rent4Hire
        <Message/>
        
        
        
        <form method="POST">
          <input name="text">
          </input>
          <input type="submit">
          </input>
        
        
        
        </form>
      </header>
    </div>
  );
}

export default Listing_Page;