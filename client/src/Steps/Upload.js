import react, { useState, useEffect, useCallback } from "react";
import UploadImage from "../Assets/upload.png";
import DropImage from "../Assets/drop.png";
import { useDropzone } from "react-dropzone";

function Upload(props) {
  function getBase64(file) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      console.log(reader.result);
    };
    reader.onerror = function (error) {
      console.log("Error: ", error);
    };
  }

  const onDrop = useCallback((acceptedFiles) => {
    getBase64(acceptedFiles[0]);

    props.changeUploaded();
    props.changeStep(1);

    console.log(acceptedFiles);
  }, 2000);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div
      {...getRootProps()}
      style={{ paddingTop: "50px", paddingBottom: "50px" }}
    >
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
