import React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';

export default function APIKeySetting(props) {
  const {tool} = props

  const [text, setText] = React.useState('')
  const [valid, setValid] = React.useState(true)

  function handleChange(event) {
    setText(event.target.value)
  }

  function handleClick() {
    console.log(text)
  }

  return (
    <div className='m-4 space-y-4'>
      <Typography>
        {tool}のAPI鍵を入力してください。
      </Typography>
      <TextField
        color='primary'
        variant='outlined'
        label={`${tool}のAPI鍵を入力してください。`}
        fullWidth
        onChange={handleChange}
      />
      <div className='flex flex-row space-x-4 items-center'>
        <div className='flex-none'>
          <Button
            color='primary'
            variant='conteined'
            onClick={handleClick}
          >
            設定の反映
          </Button>
        </div>
        <div>
          {valid ?
            <CheckCircleOutlineIcon
              fontSize='large'
              color='primary'
            /> :
            <HighlightOffIcon
              fontSize='large'
              color='primary'
            />
          }
        </div>
      </div>
    </div>
  )
}