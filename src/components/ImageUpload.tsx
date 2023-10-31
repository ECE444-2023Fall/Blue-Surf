// ImageUploadComponent.js
import React, { useState } from 'react';
import "../styles/PostCreation.css";

interface ImageUploadProps {
  onImageUpload: (imageUrl: string) => void;
}

const ImageUploadComponent: React.FC<ImageUploadProps> = ({ onImageUpload }) => {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0];

    if (file) {
      // Use a FileReader to read the uploaded file as a data URL
      const reader = new FileReader();

      reader.onload = (e) => {
        const dataURL = e.target?.result as string;
        setUploadedImage(dataURL);
        onImageUpload(dataURL); // Call the callback to update the parent component
      };

      reader.readAsDataURL(file);
    }
  };

  return (
    <div>
      {/* Input for image upload */}
      <input className="image-upload-button right" type="file" accept="image/*" onChange={handleImageUpload} />

      {/* Display the uploaded image if available */}
      {/*{uploadedImage && (
        <div className="uploaded-image">
          <img src={uploadedImage} alt="Uploaded" style={{ width: '400px', height: '500px' }} />
        </div>
      )}*/}
    </div>
  );
};

export default ImageUploadComponent;
