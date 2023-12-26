import React, { useState } from "react";
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

export default function RoleRadio() {
  const [role, setRole] = useState('user')

  function handleChange(event) {
    setRole(event.target.value)
  }

  return (
    <FormControl>
      <FormLabel>Roleの選択</FormLabel>
      <RadioGroup
        row
        value={role}
        onChange={handleChange}
      >
        {['user', 'system', 'assistant'].map(function(role) {
          return (
            <div key={role}>
              <FormControlLabel value={role} control={<Radio />} label={role} />
            </div>
          )
        })}
      </RadioGroup>
    </FormControl>
  )
}