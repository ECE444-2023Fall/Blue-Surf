import React, { useState } from 'react';
import Autosuggest from 'react-autosuggest';
import axios from 'axios';

function App() {
    const [value, setValue] = useState('');
    const [suggestions, setSuggestions] = useState([]);

    const onChange = (event, { newValue }) => {
        setValue(newValue);
    };

    const onSuggestionsFetchRequested = async ({ value }) => {
        try {
            const response = await axios.get(`http://localhost:5000/search?q=${value}`);
            setSuggestions(response.data);
        } catch (error) {
            console.error('Failed to fetch suggestions', error);
        }
    };

    const onSuggestionsClearRequested = () => {
        setSuggestions([]);
    };

    const inputProps = {
        placeholder: 'Type a fruit name',
        value,
        onChange: onChange
    };

    return (
        <div className="App">
            <Autosuggest
                suggestions={suggestions}
                onSuggestionsFetchRequested={onSuggestionsFetchRequested}
                onSuggestionsClearRequested={onSuggestionsClearRequested}
                getSuggestionValue={(suggestion) => suggestion}
                renderSuggestion={(suggestion) => <div>{suggestion}</div>}
                inputProps={inputProps}
            />
        </div>
    );
}

export default App;
