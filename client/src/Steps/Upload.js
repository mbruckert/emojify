import react, { useState, useEffect, useCallback } from "react";
import UploadImage from "../Assets/upload.png";
import DropImage from "../Assets/drop.png";
import { useDropzone } from "react-dropzone";
import toast, { Toaster } from "react-hot-toast";

function Upload(props) {
  function getBase64(file) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      props.changeUploadedImage(reader.result);
    };
    reader.onerror = function (error) {
      console.log("Error: ", error);
    };
  }

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (acceptedFiles.length > 0) {
      getBase64(acceptedFiles[0]);

      props.changeUploaded();
      props.changeStep(1);

      console.log(acceptedFiles);
    }

    if (rejectedFiles.length > 0) {
      console.log(rejectedFiles[0].errors[0].code);
      if (rejectedFiles[0].errors[0].code === "too-many-files") {
        toast.error("Please upload only one photo");
      } else if (rejectedFiles[0].errors[0].code === "file-invalid-type") {
        toast.error("Please upload a photo (jpeg and png only)");
      } else {
        toast.error("Error uploading photo, please try again.");
      }
    }
  }, 2000);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: "image/jpeg, image/png",
    maxFiles: 1,
  });

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
      <Toaster />
    </div>
  );
}

export default Upload;
