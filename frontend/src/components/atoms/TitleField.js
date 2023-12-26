import React from "react";
import TextField from '@mui/material/TextField'

export default function TitleField() {
  const [title, setTitle] = React.useState('')

  function handleChange(event) {
    setTitle(event.target.value)
  }

  return (
    <TextField
      color="primary"
      variant="outlined"
      label="タイトル名の指定"
      defaultValue={title}
      fullWidth
      onChange={handleChange}
    />
  )
}