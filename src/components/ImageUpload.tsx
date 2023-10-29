import React, { useState } from 'react';
import "../styles/PostCreation.css";

const ImageUploadComponent: React.FC = () => {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0];

    if (file) {
      // Use a FileReader to read the uploaded file as a data URL
      const reader = new FileReader();

      reader.onload = (e) => {
        const dataURL = e.target?.result as string;
        setUploadedImage(dataURL);
      };

      reader.readAsDataURL(file);
    }
  };

  return (
    <div>
      {/* Input for image upload */}
      <input className="image-upload-button right" type="file" accept="image/*" onChange={handleImageUpload} />

      {/* Display the uploaded image if available */}
      {uploadedImage && (
        <div className="uploaded-image">
          <img src={uploadedImage} alt="Uploaded" style={{ maxWidth: '100%' }} />
        </div>
      )}
    </div>
  );
};

export default ImageUploadComponent;