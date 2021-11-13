import react, { useState, useEffect } from "react";
import "./App.css";
import Logo from "./Assets/logo.png";
import Thought from "./Assets/thought.png";
import Processing from "./Steps/Processing";
import Results from "./Steps/Results";
import Upload from "./Steps/Upload";
import Check from "./Assets/check.png";

function App() {
  const [step, setStep] = useState(0);
  const [uploaded, setUploaded] = useState(false);

  function changeStep(step) {
    setStep(step);
  }

  function changeUploaded() {
    setUploaded(!uploaded);
  }

  return (
    <div className="App">
      <img src={Logo} className="logo" alt="logo" />
      {step === 0 && (
        <div className="speech-bubble">
          <img src={Thought} className="thought" alt="thought" />
          <div>
            <div className="bubble-container">
              <div className="bubble"></div>
              <div className="bubble2"></div>
              <div className="bubble3"></div>
            </div>
          </div>
        </div>
      )}
      <div className="upload-box">
        {step == 0 && (
          <Upload changeStep={changeStep} changeUploaded={changeUploaded} />
        )}
        {step == 1 && <Processing changeStep={changeStep} />}
        {step == 2 && <Results changeStep={changeStep} />}
      </div>
    </div>
  );
}

export default App;
