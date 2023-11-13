import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../styles/FilterField.css";
import "../styles/CalanderDatePicker.css";

interface CalendarDatePickerProps {
  onDateChange: (startDate: Date | null, endDate: Date | null) => void;
}

const CalanderDatePicker: React.FC<CalendarDatePickerProps> = ({
  onDateChange,
}) => {
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const onChange = (dates: [Date | null, Date | null] | null) => {
    if (dates) {
      const [start, end] = dates;
      setStartDate(start);
      setEndDate(end);
      onDateChange(start, end);
    }
  };

  const clearDates = () => {
    setStartDate(null);
    setEndDate(null);
    onDateChange(null, null);
    setDropdownOpen(false);
  };

  return (
    <div>
      <button onClick={toggleDropdown} className="custom-button">
        <span className="select-date-text">
          {startDate && endDate && startDate !== endDate
            ? `${startDate.toLocaleDateString()} - ${endDate.toLocaleDateString()}`
            : startDate
            ? startDate.toLocaleDateString()
            : "Select Date"}
        </span>
      </button>
      {dropdownOpen && (
        <div className="calendar-container">
          <DatePicker
            selected={startDate}
            onChange={onChange}
            startDate={startDate}
            endDate={endDate}
            selectsRange
            inline
          />
          <button onClick={clearDates} className="clear-button">
            Clear
          </button>
        </div>
      )}
    </div>
  );
};

export default CalanderDatePicker;
