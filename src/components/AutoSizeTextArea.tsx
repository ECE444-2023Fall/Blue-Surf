import React, { useEffect, useRef, useState, ChangeEvent } from "react";

interface AutoSizeTextAreaProps {
  content: string;
  onChange: (value: string) => void;
}

const AutoSizeTextArea: React.FC<AutoSizeTextAreaProps> = ({
  content,
  onChange,
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
    />
  );
};

export default AutoSizeTextArea;
