import React, { useState } from 'react';
import Autosuggest from 'react-autosuggest';

const SearchBar = () => {
  const [value, setValue] = useState('');
  const [suggestions, setSuggestions] = useState([]); 
  
  const getSuggestions = async (value) => {
    const response = await fetch(`/autosuggest?query=${value}`);
    const data = await response.json();
    setSuggestions(data);
  };
  
  const onSuggestionsFetchRequested = ({ value }) => {
    getSuggestions(value);
  };

  const onSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

  const onSuggestionSelected = (event, { suggestion }) => {
    setValue(suggestion);
  };

  const inputProps = {
    placeholder: 'Search...',
    value,
    onChange: (e, { newValue }) => setValue(newValue),
  };

  return (
    <Autosuggest
      suggestions={suggestions}
      onSuggestionsFetchRequested={onSuggestionsFetchRequested}
      onSuggestionsClearRequested={onSuggestionsClearRequested}
      onSuggestionSelected={onSuggestionSelected}
      getSuggestionValue={(suggestion) => suggestion}
      renderSuggestion={(suggestion) => <div>{suggestion}</div>}
      inputProps={inputProps}
    />
  );
};

export default SearchBar;
