import React from "react";
import "../styles/SortBy.css";

interface SortByOptions {
  options: string[];
}

const SortBy: React.FC<SortByOptions> = (SortByOptions: any) => {
  return (
    <div className="d-flex justify-content-end align-items-center SortBy">
      <label className="sort-title">Sort by</label>
      <select className="sort-dropdown" id="sort-by">
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
