import React from "react";
import "../styles/FilterField.css";
import CalanderDatePicker from "./CalanderDatePicker";

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

  return (
    <div
      className="form-group mt-3 mb-3 select-container"
      style={{ textAlign: "center" }}
    >
      <label className="filter-title d-flex justify-content-center">
        {FilterOptionProps.title}{" "}
      </label>
      {FilterOptionProps.title === "Date" ? (
        <CalanderDatePicker />
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
