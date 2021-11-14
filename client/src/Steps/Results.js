import react, { useState, useEffect, useCallback } from "react";
import UploadImage from "../Assets/upload.png";
import DropImage from "../Assets/drop.png";
import Rocket from "../Assets/rocket.png";
import Arrow from "../Assets/arrow.png";
import { useDropzone } from "react-dropzone";
import useWindowSize from "react-use/lib/useWindowSize";
import Confetti from "react-confetti";

function Results(props) {
  const [isConfetti, setIsConfetti] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setIsConfetti(false);
    }, 8000);
  }, []);

  function downloadResult() {
    var a = document.createElement("a");
    a.href = props.processedImage.replace(/(\r\n|\n|\r)/gm, "");
    a.download = "Emojify.png";
    a.click();
  }

  return (
    <div>
      <div className="results-container">
        <div
          className="start-image"
          style={{
            backgroundImage:
              "url('" +
              props.uploadedImage.replace(/(\r\n|\n|\r)/gm, "") +
              "')",
            backgroundSize: "contain",
            backgroundClip: "content-box",
            backgroundRepeat: "no-repeat",
            backgroundPosition: "center",
          }}
        />
        <img src={Arrow} className="arrow" alt="arrow" />
        <div
          className="result-image"
          style={{
            backgroundImage:
              "url('" +
              props.processedImage.replace(/(\r\n|\n|\r)/gm, "") +
              "')",
            backgroundSize: "contain",
            backgroundClip: "content-box",
            backgroundRepeat: "no-repeat",
            backgroundPosition: "center",
          }}
        ></div>
      </div>
      <button className="download-button" onClick={downloadResult}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          style={{ width: "20px", height: "20px" }}
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
            clip-rule="evenodd"
          />
        </svg>
        <span style={{ paddingLeft: "20px" }}>Download Image</span>
      </button>
      <Confetti
        run={isConfetti}
        recycle={false}
        style={{ display: isConfetti ? "block" : "none" }}
        numberOfPieces={100}
        drawShape={(ctx) => {
          ctx.font = "30px Arial";
          ctx.fillText("🎉", 0, 0);
        }}
      />
    </div>
  );
}

export default Results;
