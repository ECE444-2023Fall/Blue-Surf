import React, { useState } from 'react';
import Autosuggest, { ChangeEvent, InputProps } from 'react-autosuggest';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import '../styles/SearchBar.css';
import API_URL from '../config';

export interface SearchBarProps {
  onDataReceived: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onDataReceived }) => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const getSuggestions = async (value: string) => {
    try {
      const response = await fetch(`${API_URL}/api/autosuggest?query=${value}`);
      if (!response || !response.ok) {
        throw new Error('Network response was not ok.');
      }
      const data = await response.json();
      setSuggestions(data);
      setShowSuggestions(data.length > 0);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const onSuggestionsFetchRequested = ({ value }: { value: string }) => {
    getSuggestions(value);
  };

  const onSuggestionsClearRequested = () => {
    setShowSuggestions(false);
    setSuggestions([]);
  };

  const onSuggestionSelected = (_event: React.FormEvent, { suggestion }: { suggestion: string }) => {
    setSearchQuery(suggestion);
    onSearch(suggestion);
  };

  const onSearch = async (query: string) => {
    onDataReceived(query);
  };

  const handleInputChange = (event: React.FormEvent<HTMLElement>, { newValue }: ChangeEvent) => {
    setSearchQuery(newValue);
  };
  
  const handleInputKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      setShowSuggestions(false);
      onSearch(searchQuery);
    }
  };

  const inputClassName = showSuggestions
    ? 'react-autosuggest__input react-autosuggest__input--suggestions'
    : 'react-autosuggest__input';

  const inputProps: InputProps<string> = {
    placeholder: 'Search',
    value: searchQuery,
    onChange: handleInputChange,
    onKeyPress: handleInputKeyPress,
    className: inputClassName,
  };

  return (
    <div className="search-input-container">
      <FontAwesomeIcon icon={faSearch} className="search-icon" />
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
