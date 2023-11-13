import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../styles/FilterField.css";

interface CalendarDatePickerProps {
  onDateChange: (startDate: Date, endDate: Date | null) => void;
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
      if(start && end) {
        setStartDate(start);
        setEndDate(end);
        onDateChange(start, end);
      }
    }
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
        </div>
      )}
    </div>
  );
};

export default CalanderDatePicker;
