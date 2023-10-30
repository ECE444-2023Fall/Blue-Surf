{/*import React from 'react';

const ImageUploadButton: React.FC = ({ onImageUpload = () => {} }) => {}
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0];

    if (file) {
      // Use a FileReader to read the uploaded file as a data URL
      const reader = new FileReader();

      reader.onload = (e) => {
        const dataURL = e.target?.result as string;
        onImageUpload(dataURL);
      };

      reader.readAsDataURL(file);
    }
  };

  return (
    <input className="image-upload-button right" type="file" accept="image/*" onChange={handleImageUpload} />
  );
};

export default ImageUploadButton;*/}
