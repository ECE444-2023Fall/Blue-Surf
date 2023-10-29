import React, { useState } from 'react';
import Autosuggest from 'react-autosuggest';

const SearchBar = ({ onDataReceived }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const getSuggestions = async (value) => {
    try {
      const response = await fetch(`/autosuggest?query=${value}`);
      if (!response ||!response.ok) {
        throw new Error('Network response was not ok.');
      }
      const data = await response.json();
      setSuggestions(data);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const onSuggestionsFetchRequested = ({ value }) => {
    getSuggestions(value);
  };

  const onSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

  const onSuggestionSelected = (event, { suggestion }) => {
    setSearchQuery(suggestion);
    onSearch(suggestion);
  };

  const onSearch = async (query) => {
    try {
      const response = await fetch(`/search?query=${query}`);
      if (!response || !response.ok) {
        throw new Error('Network response was not ok.');
      }
      const data = await response.json();
      onDataReceived(data);
    } catch (error) {
      console.error('Error performing search:', error);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      onSearch(searchQuery);
    }
  };

  const inputProps = {
    placeholder: 'Search...',
    value: searchQuery,
    onChange: (e, { newValue }) => setSearchQuery(newValue),
    onKeyPress: handleKeyPress
  };

  return (
    <div>
      <Autosuggest
        suggestions={suggestions}
        onSuggestionsFetchRequested={onSuggestionsFetchRequested}
        onSuggestionsClearRequested={onSuggestionsClearRequested}
        onSuggestionSelected={onSuggestionSelected}
        getSuggestionValue={(suggestion) => suggestion}
        renderSuggestion={(suggestion) => <div>{suggestion}</div>}
        inputProps={inputProps}
      />
    </div>
  );
};

export default SearchBar;
