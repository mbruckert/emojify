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
        <div className="result-image"></div>
      </div>
      <button className="download-button">Download Image</button>
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
