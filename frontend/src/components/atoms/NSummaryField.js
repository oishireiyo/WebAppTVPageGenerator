import React from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Axios from 'axios'

export default function NSummaryFiled() {
  const [nSummary, setNSummary] = React.useState(5)

  function handleChange(event) {
    setNSummary(event.target.value)
  }

  function handleClick() {
    Axios.post('http://127.0.0.1:5432/set_n_summary_texts', {'n_summary_texts': nSummary})
    .then(function(response) {
      console.log(response)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  return (
    <div className='flex flex-row space-x-4'>
      <div className='flex-none w-48'>
        <TextField
          color='primary'
          variant='outlined'
          label='段落の数'
          defaultValue={nSummary}
          onChange={handleChange}
        />
      </div>
      <div className='flex-none'>
        <Button
          color='primary'
          variant='contained'
          onClick={handleClick}
        >
          段落数の設定
        </Button>
      </div>
    </div>
  )
}