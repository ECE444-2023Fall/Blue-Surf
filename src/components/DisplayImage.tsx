import React from 'react';

const DisplayImageComponent: React.FC<{ uploadedImage: string | null }> = ({ uploadedImage }) => {
  return (
    <div>
      {/* Display the uploaded image if available */}
      {uploadedImage && (
        <div className="uploaded-image">
          <img src={uploadedImage} alt="Uploaded" style={{ maxWidth: '100%' }} />
        </div>
      )}
    </div>
  );
};

export default DisplayImageComponent;
