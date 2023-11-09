import React, { useEffect, useRef, useState, ChangeEvent } from "react";
import "../styles/AutoSizeTextArea.css";
interface AutoSizeTextAreaProps {
  content: string;
  onChange: (value: string) => void;
  placeholderWord?: string;
}

const AutoSizeTextArea: React.FC<AutoSizeTextAreaProps> = ({
  content,
  onChange,
  placeholderWord,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [textareaHeight, setTextAreaHeight] = useState<string>("auto");

  const setInitialTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  const updateTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  useEffect(() => {
    setInitialTextareaHeight();
    updateTextareaHeight();
  }, [content]);

  const handleTextAreaChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e.target.value);
    updateTextareaHeight();
  };

  return (
    <textarea
      ref={textareaRef}
      className="edit-text-input"
      value={content}
      onChange={handleTextAreaChange}
      style={{ height: textareaHeight }}
      placeholder={placeholderWord}
    />
  );
};

export default AutoSizeTextArea;
