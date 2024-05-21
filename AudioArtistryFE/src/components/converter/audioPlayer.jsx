import React from 'react';
import './audioPlayer.css';

const AudioPlayer = ({ audioSrc }) => {
    // Function to handle download button click
    const handleDownload = () => {
        if (!audioSrc) return;

        // Create an anchor element
        const link = document.createElement('a');
        link.href = audioSrc;
        link.download = 'audio.mp3';
        
        // Simulate a click on the anchor element
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        
            <div className="audio-player-inner-container">
                <div className="audio-player">
                    {audioSrc ? (
                        <audio controls>
                            <source src={audioSrc} type="audio/mpeg" />
                            Your browser does not support the audio element.
                        </audio>
                    ) : (
                        <p>No audio source available</p>
                    )}
                </div>
                <button className="download-button" onClick={handleDownload}>
                    Download
                </button>
            </div>
        
    );
};

export default AudioPlayer;
