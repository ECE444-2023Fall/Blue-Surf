import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import SearchBar from './components/SearchBar.js';

function App() {
  const [searchResults, setSearchResults] = useState(null);

  const handleSearchData = (data) => {
    setSearchResults(data);
  };

  return (
    <div className="App">
      <header className="App-header">
        <SearchBar onDataReceived={handleSearchData} />
        <img src={logo} className="App-logo" alt="logo" />
        <div className="SearchResults">
          {searchResults && searchResults.map(result => (
            <div>
              <p>Title: {result.title}</p>
              <p>Description: {result.description}</p>
              <p>Location: {result.location}</p>
              <p>Start Time: {result.start_time}</p>
              <p>End Time: {result.end_time}</p>
              <p>Like Count: {result.like_count}</p>
            </div>
          ))}
          {!searchResults && (
            <p>No search results available.</p>
          )}
        </div>
        <p>
          Edit <code>src/App.js</code> and save to reload.
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
