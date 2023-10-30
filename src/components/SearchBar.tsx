import React, { useState } from 'react';
import Autosuggest, { ChangeEvent, InputProps } from 'react-autosuggest';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import '../styles/SearchBar.css';

export interface SearchBarProps {
  onDataReceived: (data: any) => void; // Change 'any' to the expected data type
}

const SearchBar: React.FC<SearchBarProps> = ({ onDataReceived }) => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  const getSuggestions = async (value: string) => {
    try {
      const response = await fetch(`/api/autosuggest?query=${value}`);
      if (!response || !response.ok) {
        throw new Error('Network response was not ok.');
      }
      const data = await response.json();
      setSuggestions(data);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const onSuggestionsFetchRequested = ({ value }: { value: string }) => {
    setShowSuggestions(true);
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
    try {
      const response = await fetch(`/api/search?query=${query}`);
      if (!response || !response.ok) {
        throw new Error('Network response was not ok.');
      }
      const data = await response.json();
      onDataReceived(data);
    } catch (error) {
      console.error('Error performing search:', error);
    }
  };

  const handleInputChange = (event: React.FormEvent<HTMLElement>, { newValue }: ChangeEvent) => {
    setSearchQuery(newValue);
  };
  
  const handleInputKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
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
