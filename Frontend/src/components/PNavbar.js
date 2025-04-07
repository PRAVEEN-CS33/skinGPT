import React, { useState } from 'react';
import './PNavbar.css';
import img1 from '../assets/image.png';
import logo from '../assets/logo.png';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faVolumeHigh, faVolumeMute } from "@fortawesome/free-solid-svg-icons";

const PNavbar = () => {
  const [voiceAssist, setVoiceAssist] = useState(true);
  const handleVoiceAssist = () => {
    setVoiceAssist(!voiceAssist);
  };
  return (
    <div className='nav'>
      <nav className="unique-navbar">
        <div className="logo">
        <img src={logo} alt="Logo" />
          <h3>MediBot</h3>
        </div>
        <div className='row'>
          <div className='speak'>
            <button onClick={handleVoiceAssist}>
              {voiceAssist ? (
                <FontAwesomeIcon icon={faVolumeHigh} />
              ) : (
                <FontAwesomeIcon icon={faVolumeMute} />
              )}
            </button>
          </div>
          <div className="avatar">
            <Link to='components/login'>
              <img src={img1} alt="User Avatar" />
            </Link>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default PNavbar;