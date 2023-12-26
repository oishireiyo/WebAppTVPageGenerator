import React from "react";
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import LaptopChromebookIcon from '@mui/icons-material/LaptopChromebook';
import AssistantIcon from '@mui/icons-material/Assistant';
import FaceIcon from '@mui/icons-material/Face';
import Axios from 'axios'

export default function LLMPayloadShower() {
  const [messages, setMessages] = React.useState([])

  function handleClick() {
    Axios.get('http://127.0.0.1:5432/get_llm_payload')
    .then(function(response) {
      console.log(response.data.payload.messages)
      setMessages(response.data.payload.messages)
    })
    .catch(function(error) {
      console.error(error)
    })
  }

  function MakeChip(message) {
    let color = 'default'
    let icon = <HelpOutlineIcon />
    if (message.role === 'system') {
      color = 'primary'
      icon = <LaptopChromebookIcon />
    } else if (message.role === 'assistant') {
      color = 'success'
      icon = <AssistantIcon />
    } else if (message.role === 'user') {
      color = 'warning'
      icon = <FaceIcon />
    }

    return (
      <Chip
        sx={{
          height: 'auto',
          '& .MuiChip-label': {
            display: 'block',
            whiteSpace: 'normal',
          },
        }}
        color={color}
        icon={icon}
        label={message.content[0].text}
      />
    )
  }

  return (
    <>
      <Button
        color="primary"
        variant="contained"
        onClick={handleClick}
      >
        ペイロードの取得
      </Button>
      <div className="flex flex-col space-y-4 bg-gray-200">
        {
          messages.map(function(message, i) {
            return (
              <div key={`chip-id-${i}`}>
                {MakeChip(message=message)}
              </div>
            )
          })
        }
      </div>
    </>
  )
}