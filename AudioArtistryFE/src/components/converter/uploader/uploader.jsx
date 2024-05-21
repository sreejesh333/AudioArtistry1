import React, { useRef, useState } from 'react';
import { MdCloudUpload, MdDelete } from 'react-icons/md';
import { AiFillFileImage } from 'react-icons/ai';
import './uploader.css';
import exifr from 'exifr';
import axios from '../../../api/axios';
import AudioPlayer from '../audioPlayer'; 

export default function TemplateDemo() {
    const [image, setImage] = useState("");
    const [audioSrc, setAudioSrc] = useState(null);
    const [fileName, setFileName] = useState("No Selected File");
    const [isActive, setIsActive] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [uploading, setUploading] = useState(false);
    const [selectedStyle, setSelectedStyle] = useState("");
    const audioRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);

    const handleFileChange = ({ target: { files } }) => {
        if (files && files[0]) {
            setFileName(files[0].name);
            setImage(files[0]);

            // Check for GEO Location data in EXIF
            checkForGeoLocation(files[0]);
        }
    };

    const checkForGeoLocation = async (file) => {
        try {
            const exifData = await exifr.parse(file);
            if (exifData && exifData.latitude && exifData.longitude) {
                setIsActive(true);
                setErrorMessage("");
            } else {
                setIsActive(false);
                setErrorMessage("Uploaded image doesn't have location information.");
            }
        } catch (error) {
            console.error('Error parsing EXIF data:', error);
            setIsActive(false);
            setErrorMessage("Error parsing EXIF data. Please try again.");
        }
    };

    const handleSubmit = async () => {
        setUploading(true);
        try {
            const formData = new FormData();
            formData.append('image', image);
            formData.append('type', selectedStyle);

            const response = await axios.post('api/music/saveimage/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data], { type: 'audio/mpeg' }));
            setAudioSrc(url);
            audioRef.current = new Audio(url);
            audioRef.current.onended = () => setIsPlaying(false);

            if (response) {
                console.log('Image uploaded successfully');
            } else {
                console.error('Image upload failed:', response.statusText);
            }
        } catch (error) {
            console.error('Error uploading image:', error);
        } finally {
            setUploading(false);
        }
    };

    const playAudio = () => {
        if (audioRef.current) {
            audioRef.current.play();
            setIsPlaying(true);
        }
    };

    const pauseAudio = () => {
        if (audioRef.current) {
            audioRef.current.pause();
            setIsPlaying(false);
        }
    };

    const stopAudio = () => {
        if (audioRef.current) {
            audioRef.current.pause();
            audioRef.current.currentTime = 0;
            setIsPlaying(false);
        }
    };

    return (<div className="main-container">
        <div className="upload-container">

        
        <div className="upload-inner-container">
            <form action='' onClick={() => document.querySelector(".input-field").click()}>
                <input
                    type="file"
                    accept="image/*"
                    className="input-field"
                    hidden
                    onChange={handleFileChange}
                />
                {image ? (
                    <img src={URL.createObjectURL(image)} className="uploaded-image" alt="Uploaded" />
                ) : (
                    <>
                        <MdCloudUpload color="#1475cf" size={60} />
                        <p>Browse file to upload.</p>
                    </>
                )}
            </form>
            <div className="file-name-section">
                <div className="file-name-container">
                    <AiFillFileImage className="file-icon" />
                    <span className="file-name-container-rightbox">
                        {fileName}
                        <MdDelete
                            className="delete-icon"
                            onClick={() => {
                                setFileName("No selected file");
                                setImage(null);
                                setIsActive(false);
                                setErrorMessage("");
                            }}
                        />
                    </span>
                </div>
            </div>
            <div className="button-convert-container">
                {errorMessage && <p className="error-message">{errorMessage}</p>}
                <div className="music-style-selection-section">
                    <p>Choose a music style</p>
                    <div className="music-selection-btn-container">
                        {['Single', 'Interval', 'Chord_one', 'Chord_two'].map((style) => (
                            <button
                                key={style}
                                className={`music-selection-btn ${selectedStyle === style ? 'active' : ''}`}
                                onClick={() => setSelectedStyle(style)}
                            >
                                {style}
                            </button>
                        ))}
                    </div>
                </div>
                <button
                    className="button-convert"
                    style={{ backgroundColor: isActive ? 'green' : 'gray', color: 'white', padding: '12px 20px', border: 'none', cursor: 'pointer' }}
                    disabled={!isActive || uploading || !selectedStyle}
                    onClick={handleSubmit}
                >
                    {uploading ? 'Uploading...' : 'Convert my pic to music'}
                </button>
                {/* {audioSrc && (
                    <div className="audio-controls">
                        <button onClick={playAudio} disabled={isPlaying}>Play</button>
                        <button onClick={pauseAudio} disabled={!isPlaying}>Pause</button>
                        <button onClick={stopAudio}>Stop</button>
                    </div>
                )} */}
                
            </div>
        </div>
        </div>
        <div className="audio-player-container">
        {<AudioPlayer audioSrc={audioSrc} />}
        </div>
        
        </div>
          );
}
