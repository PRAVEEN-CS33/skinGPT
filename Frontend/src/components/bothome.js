import './bothome.css';
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMicrophone, faPaperPlane, faVolumeHigh, faVolumeMute } from "@fortawesome/free-solid-svg-icons";
import { useSpeechSynthesis } from "react-speech-kit";
import SpeechRecognition from "react-speech-recognition";
import { useEffect, useState, useRef } from "react";
import axios from "axios";
import lottie from 'lottie-web';
import { defineElement } from 'lord-icon-element';
import ReactMarkdown from 'react-markdown';

defineElement(lottie.loadAnimation);
const BHome = () => {
  const [listen, setListen] = useState(true);
  const [input, setInput] = useState("");
  const [queryInfo, setQueryInfo] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedImg, setSelectedImg] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [voiceAssist, setVoiceAssist] = useState(true);

  const { speak } = useSpeechSynthesis();
  const fileInputRef = useRef(null);
  const chatContainerRef = useRef(null); // Ref for chat container

  const {
    transcript,
    listening,
    browserSupportsSpeechRecognition,
    startListening,
    stopListening,
  } = SpeechRecognition;

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setSelectedImage(URL.createObjectURL(selectedFile));
      setSelectedImg(selectedFile);
      setShowPreview(true);
    }
  };

  useEffect(() => {
    setInput(transcript);
  }, [transcript]);

  const handleVoiceAssist = () => {
    setVoiceAssist(!voiceAssist);
  };

  const handleInput = (event) => {
    setInput(event.target.value);
  };

  const handleSend = async () => {
    if (!input.trim()) return; // Prevent empty inputs

    const formData = new FormData();
    formData.append('text', input);

    const newQuery = {
      input: input,
      output: "Loading...", // Display loading buffer
      image: selectedImage,
      rimg: null,
    };

    setQueryInfo([...queryInfo, newQuery]);
    setInput(""); // Clear the input box
    setShowPreview(false); // Hide the image preview

    try {
      let response;
      if (selectedImage) {
        formData.append('image', selectedImg);
        response = await axios.post("http://127.0.0.1:5001/botimg", formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        const updatedQuery = {
          input: input,
          output: response.data.result,
          image: selectedImage,
          rimg: `data:image/jpeg;base64,${response.data.image_data}`,
        };

        setQueryInfo((prevQueries) => {
          const updatedQueries = [...prevQueries];
          updatedQueries[updatedQueries.length - 1] = updatedQuery;
          return updatedQueries;
        });

        setSelectedImage(null);
        setSelectedImg(null);
      } else {
        response = await axios.post("http://127.0.0.1:5001/bot", formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        const updatedQuery = {
          input: input,
          output: response.data.response,
          image: null,
          rimg: null,
        };

        setQueryInfo((prevQueries) => {
          const updatedQueries = [...prevQueries];
          updatedQueries[updatedQueries.length - 1] = updatedQuery; // Replace the last query with the final response
          return updatedQueries;
        });
      }
    } catch (error) {
      console.error(error);

      setQueryInfo((prevQueries) => {
        const updatedQueries = [...prevQueries];
        updatedQueries[updatedQueries.length - 1].output = "Something went wrong. Please try again.";
        return updatedQueries;
      });
    }
  };

  // Scroll to the bottom of the chat container whenever queryInfo updates
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [queryInfo]);

  const handleMic = () => {
    setListen(!listen);
    if (listen) startListening();
    else stopListening();
  };

  return (
    <div className="home-parent">
      <div className="animate_animated animate_zoomInDown">
        <div className="chat-response" ref={chatContainerRef} style={{ overflowY: "auto", maxHeight: "75vh" }}>
          {queryInfo.map((query, index) => (
            <React.Fragment key={index}>
              {/* User message */}
              <div className="request">
                <div className="input">
                  <p>
                    {query.image &&
                      <>
                        <img src={query.image} alt="Uploaded" style={{ width: '200px', height: '200px' }} />
                        <br />
                      </>
                    }
                    {query.input}
                  </p>
                </div>
              </div>

              {/* AI Response */}
              <div className="response">
                <div className="output">
                  <p>
                    {query.rimg && (
                      <>
                        <img
                          src={query.rimg}
                          alt="Predicted"
                          className="predicted-image"
                          style={{ width: '200px', height: '200px' }}
                        />
                        <br />
                      </>
                    )}
                    {query.output === "Loading..." ? (
                      <span className="loading-indicator">⏳ Analysing...</span>
                    ) : (
                      <ReactMarkdown>{query.output}</ReactMarkdown>
                    )}
                  </p>
                </div>
              </div>
            </React.Fragment>
          ))}

          {showPreview && (
            <div className="image-preview">
              <img src={selectedImage} alt="Preview" />
              <button className="close-preview" onClick={() => { setShowPreview(false); setSelectedImage(null) }}>
                X
              </button>
            </div>
          )}
          {queryInfo.length === 0 && (
            <div className='empty'>
              <h1>What can I help with?</h1>
            </div>
          )}
        </div>
        
        <div className='input-box'>
          <div className="input-area">
            <div className="chat-input">
              <input
                type="text"
                value={input}
                onChange={handleInput}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
              />
            </div>
            <div className='row2'>
              <div className="file-input">
                <div onClick={handleUploadClick}>
                  <lord-icon
                    src="https://cdn.lordicon.com/mecwbjnp.json"
                    trigger="hover"
                    colors="primary:#121331,secondary:#08a88a"
                    style={{ width: 50, height: 50 }}>
                  </lord-icon>
                </div>
                <input
                  type="file"
                  ref={fileInputRef}
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                />
              </div>
              <div className="send-mic-speek">
                {input && input.length > 0 ? (
                  <button onClick={handleSend}>
                    <FontAwesomeIcon icon={faPaperPlane} />
                  </button>
                ) : (
                  <button onClick={handleMic}>
                    <FontAwesomeIcon icon={faMicrophone} />
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      <script src="https://cdn.lordicon.com/bhenfmcm.js"></script>
    </div>
  );
};

export default BHome;
