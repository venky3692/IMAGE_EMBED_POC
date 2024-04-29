import React, {useCallback} from 'react';
import {useDropzone} from 'react-dropzone';
import "./App.css"

function App() {
  const onDrop = useCallback(acceptedFiles => {
    // Do something with the files
  }, [])
  const {getRootProps, getInputProps, isDragActive} = useDropzone({onDrop})

  return (
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
  )
}

export default App;