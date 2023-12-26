import React from "react";
import Button from '@mui/material/Button';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export default function VideoUploader(props) {
  const {file, setFile} = props

  const inputRef = React.useRef(null)

  function handleClick() {
    console.log('動画ファイルの選択')
    inputRef.current.click()
  }

  function handleChange(event) {
    const files = event.target.files
    if (files && files[0]) {
      setFile(files[0])
    }
  }

  return (
    <div>
      <Button
        color="primary"
        variant="contained"
        endIcon={<FileUploadIcon />}
        onClick={handleClick}
      >
        動画ファイルの選択
      </Button>
      <input
        type="file"
        accept="video/mp4"
        hidden
        onChange={handleChange}
        ref={inputRef}
      />
    </div>
  )
}