import React from "react";
import "../styles/FilterField.css";
import CalanderDatePicker from "./CalanderDatePicker";
import moment from "moment-timezone";

interface FilterOptionProps {
  title: string;
  values: string[];
  onFilterChange: (filterTitle: string, selectedValue: string) => void;
}

const FilterField: React.FC<FilterOptionProps> = (FilterOptionProps: any) => {
  const handleFilterChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = event.target.value;
    FilterOptionProps.onFilterChange(FilterOptionProps.title, selectedValue);
  };

  const handleDateChange = (startDate: Date | null, endDate: Date | null) => {
    const formattedStartDate = moment(startDate)
      .tz("America/New_York")
      .format("YYYY-MM-DD");

    const formattedEndDate = moment(endDate)
      .tz("America/New_York")
      .format("YYYY-MM-DD");

    if (startDate) {
      FilterOptionProps.onFilterChange("start_time", formattedStartDate);
    } else {
      FilterOptionProps.onFilterChange("start_time", "no_start_time");
    }

    if (endDate) {
      FilterOptionProps.onFilterChange("end_time", formattedEndDate);
    } else {
      FilterOptionProps.onFilterChange("end_time", "no_end_time");
    }
  };

  return (
    <div
      className="form-group mt-3 mb-3 select-container"
      style={{ textAlign: "center" }}
    >
      <label className="filter-title d-flex justify-content-center">
        {FilterOptionProps.title}{" "}
      </label>
      {FilterOptionProps.title === "Date" ? (
        <CalanderDatePicker onDateChange={handleDateChange} />
      ) : (
        <select
          className="custom-select custom-border-primary"
          id={FilterOptionProps.title}
          onChange={handleFilterChange}
        >
          {FilterOptionProps.values.map((tag: string, index: number) => (
            <option key={index} value={tag}>
              {tag}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};

export default FilterField;
