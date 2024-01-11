import React from "react";
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Axios from 'axios'

export default function TitleField() {
  const [title, setTitle] = React.useState('')

  function handleChange(event) {
    setTitle(event.target.value)
  }

  function handleClick() {
    Axios.post('http://127.0.0.1:5432/set_title', {'title': title})
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <div className="flex flex-row space-x-4">
      <div className="flex-none w-96">
        <TextField
          color="primary"
          variant="outlined"
          label="タイトル名の指定"
          defaultValue={title}
          fullWidth
          onChange={handleChange}
        />
      </div>
      <div className="flex-none">
        <Button
          color="primary"
          variant="contained"
          onClick={handleClick}
        >
          タイトル設定
        </Button>
      </div>
    </div>
  )
}