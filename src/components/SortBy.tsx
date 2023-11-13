import React from "react";
import "../styles/SortBy.css";

interface SortByOptions {
  options: string[];
  onSortChange: (selectedValue: string) => void;
}

const SortBy: React.FC<SortByOptions> = (SortByOptions: any) => {
  const handleSortChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = event.target.value;
    SortByOptions.onSortChange(selectedValue);
  };

  return (
    <div className="d-flex justify-content-end align-items-center SortBy">
      <label className="sort-title">Sort by</label>
      <select
        className="sort-dropdown"
        id="sort-by"
        onChange={handleSortChange}
      >
        {SortByOptions.options.map((tag: string, index: number) => (
          <option key={index} value={tag}>
            {tag}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SortBy;
