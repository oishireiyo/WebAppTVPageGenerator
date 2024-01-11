import React from 'react';
import Button from '@mui/material/Button'
import Axios from 'axios'

export default function CallButton() {
  async function handleClick() {
    await Axios.get('http://127.0.0.1:5432/set_function_tool')
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })

    await Axios.get('http://127.0.0.1:5432/execute')
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <Button
      color='primary'
      variant='contained'
      onClick={handleClick}
    >
      処理実行
    </Button>
  )
}