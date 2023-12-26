import React from "react";
import Button from "@mui/material/Button";
import FileUploadIcon from '@mui/icons-material/FileUpload';
import Axios from 'axios'

export default function CSVUploader() {
  const [file, setFile] = React.useState(null)

  const inputRef = React.useRef(null)

  function handleClick() {
    console.log('CSVファイルの選択')
    inputRef.current.click()
  }

  function handleChange(event) {
    const files = event.target.files
    if (files && files[0]) {
      setFile(files[0])
    }
  }

  async function handleClickSubmit() {
    let formData = new FormData()
    formData.append('csvfile', file)

    await Axios.post('http://127.0.0.1:5432/set_subtitle', formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "Access-Control-Allow-Origin": "*",
      }
    })
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })

    await Axios.post('http://127.0.0.1:5432/set_title', {'title': '「座りっぱなし」は寿命が縮む'})
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })

    await Axios.post('http://127.0.0.1:5432/set_system_character', {
      'text': 'あなたは質問に対してカジュアルかつ簡潔に回答するアシスタントです。'
    })
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })

    await Axios.get('http://127.0.0.1:5432/set_subtitle_texts')
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <div>
      <Button
        color='primary'
        variant='contained'
        endIcon={<FileUploadIcon />}
        onClick={handleClick}
      >
        CSVファイルの選択
      </Button>
      <input
        type="file"
        accept="text/csv"
        hidden
        onChange={handleChange}
        ref={inputRef}
      />
      <p>{file && file.name}</p>
      <Button
        color="primary"
        variant="contained"
        endIcon={<FileUploadIcon />}
        onClick={handleClickSubmit}
      >
        CSVファイルの送信
      </Button>
    </div>
  )
}