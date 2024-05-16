import React, {useCallback, useState} from 'react';
import {useDropzone} from 'react-dropzone';
import "./App.css"
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [imageUploaded, setImageData] = useState(null);
  const onDrop = useCallback(acceptedFiles => {
    console.log(URL.createObjectURL(acceptedFiles[0]))
    setImageData(URL.createObjectURL(acceptedFiles[0]))
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', acceptedFiles[0]);
    axios.post('http://localhost:5000/upload', formData)
      .then(response => {
        setIsProcessing(false);
        console.log(response.data);
        setMessage({success: `Similarity score: ${response.data.similarity_score}%`, matching_image: response.data.imageData, matching_colors: response.data.matching_colors, dominating_color_similarity: response.data.dominating_color_similarity});
      })
      .catch(error => {
        setIsProcessing(false);
        console.error('Error uploading file: ', error);
        setMessage({error:'Error uploading file'});
      });
  }, [])
  const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

  return (
    <>
    <div className='title-bar'>
      <img src="/photo-icons.png" alt="App Logo" className="logo" />
      <h1 className="app-name">Trademark Infringement Detection</h1>
    </div>
    <div class="container">
    <div className='dropbox-container'>
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      {
        isDragActive ?
          <p>Drop the image here ...</p> :
          <p>Drag 'n' drop your images here, or click to select files</p>
      }
    </div>
    </div>
    <div className='result-container'>
    {!isProcessing && <div>
        <p>Uploaded logo:</p>
      </div>}
      {!isProcessing && <div id="image-card" class="image-card">
        <img id="image" class="result-image" src={imageUploaded} alt=""></img>
      </div>}
    <p>Result</p>
    <div className='progress-bar'>
    {message.success && !isProcessing && <p style={{color:'green'}}>{message.success}</p>}
    {message.success && !isProcessing && <p style={{color:'green'}}>Similarity of color combination: {message.dominating_color_similarity}</p>}
    {message.error && !isProcessing && <p style={{color:'red'}}>{message.error}</p>}
    {isProcessing && <div class="loader"></div>}
    </div>
      {!isProcessing && <div>
        <p>Matching logo:</p>
      </div>}
      {!isProcessing && <div id="image-card" class="image-card">
        <img id="image" class="result-image" src={`data:image/jpeg;base64, ${message.matching_image}`} alt=""></img>
        <div><p>Common dominating colors:</p></div>
        <div className="color-list">
      {message.matching_colors && message.matching_colors.map((rgb, index) => (
        <div
          key={index}
          className="color-box"
          style={{ backgroundColor: `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})` }}
        ></div>
      ))}
    </div>
      </div>}
    </div>
    </div>
    </>
  )
}

export default App;