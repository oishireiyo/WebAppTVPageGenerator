import React from "react"
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import PauseIcon from '@mui/icons-material/Pause';

export default function PlayPauseButtons(props) {
  const {file, isPlaying, handlePlayPause} = props

  return (
    <Stack direction="row" alignItems="center">
      <IconButton color="primary" disabled={!file}><SkipNextIcon /></IconButton>
      {isPlaying ?
        <IconButton color="primary" onClick={handlePlayPause} disabled={!file}><PauseIcon /></IconButton> :
        <IconButton color="primary" onClick={handlePlayPause} disabled={!file}><PlayArrowIcon /></IconButton>
      }
      <IconButton color="primary" disabled={!file}><SkipPreviousIcon /></IconButton>
    </Stack>
  )
}