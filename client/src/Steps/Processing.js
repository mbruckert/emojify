import react, { useState, useEffect, useCallback } from "react";
import UploadImage from "../Assets/upload.png";
import DropImage from "../Assets/drop.png";
import Rocket from "../Assets/rocket.png";
import { useDropzone } from "react-dropzone";

function Processing(props) {
  useEffect(() => {
    setTimeout(() => {
      props.changeStep(2);
    }, 5000);
  }, []);

  return (
    <div style={{ paddingTop: "50px", paddingBottom: "50px" }}>
      <img src={Rocket} className="rocket" alt="rocket" />
      <h1 className="upload-text">Processing...</h1>
      <h4 className="upload-subtext">
        Please be patient, this can take up to a minute.
      </h4>
    </div>
  );
}

export default Processing;
