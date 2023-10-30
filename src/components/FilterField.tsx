import React from "react";
import "../styles/FilterField.css";

interface FilterOptionProps {
  title: string;
  values: string[];
}

const FilterField: React.FC<FilterOptionProps> = (FilterOptionProps: any) => {
  return (
    <div
      className="form-group mt-3 mb-3 select-container"
      style={{ textAlign: "center" }}
    >
      <label className="filter-title d-flex justify-content-center">
        {FilterOptionProps.title}
      </label>
      <select
        className="custom-select custom-border-primary"
        id={FilterOptionProps.title}
      >
        {FilterOptionProps.values.map((tag: string, index: number) => (
          <option key={index} value={tag}>
            {tag}
          </option>
        ))}
      </select>
    </div>
  );
};

export default FilterField;
