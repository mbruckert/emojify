import react, { useState, useEffect, useCallback } from "react";
import UploadImage from "../Assets/upload.png";
import DropImage from "../Assets/drop.png";
import { useDropzone } from "react-dropzone";

function Upload(props) {
  const onDrop = useCallback((acceptedFiles) => {
    props.changeUploaded();
    props.changeStep(1);
  }, 2000);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <div>
          <img src={DropImage} alt="Upload" className="upload-image" />
          <h1 className="upload-text">Drop the files here</h1>
        </div>
      ) : (
        <div>
          <img src={UploadImage} alt="Upload" className="upload-image" />
          <h1 className="upload-text">
            Please Drop an Image or Click to Upload
          </h1>
        </div>
      )}
    </div>
  );
}

export default Upload;
