import React, {useCallback, useState} from 'react';
import {useDropzone} from 'react-dropzone';
import "./App.css"
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const onDrop = useCallback(acceptedFiles => {
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', acceptedFiles[0]);
    axios.post('http://localhost:5000/upload', formData)
      .then(response => {
        setIsProcessing(false);
        console.log(response.data);
        setMessage({success:'File uploaded successfully'});
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
    <div className='progress-bar'>
    {message.success && !isProcessing && <p style={{color:'green'}}>{message.success}</p>}
    {message.error && !isProcessing && <p style={{color:'red'}}>{message.error}</p>}
    {isProcessing && <div class="loader"></div>}
    </div>
    </>
  )
}

export default App;