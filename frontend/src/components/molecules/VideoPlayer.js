import React from "react";
import PlayPauseButtons from "../atoms/PlayPauseButtons";
import Seekbar from "../atoms/Seekbar";

export default function VideoPlayer(props) {
  const {file, videoRef} = props

  const [videourl, setVideourl] = React.useState(null)
  const [isPlaying, setIsPlaying] = React.useState(false)
  const [currentInSec, setCurrentInSec] = React.useState(0)
  const [durationInSec, setDurationInSec] = React.useState(0)

  function handlePlayPause() {
    isPlaying ? videoRef.current.pause() : videoRef.current.play()
    setIsPlaying(!isPlaying)
  }

  function handleLoadedMetadata() {
    if (videoRef.current) {
      console.log(`ビデオの長さ: ${videoRef.current.duration} 秒`)
      setDurationInSec(videoRef.current.duration)
    } else {
      console.error('ビデオのメタデータ取得不能。')
    }
  }

  function handleSeekbarValue(event) {
    setCurrentInSec(event.target.value)
    videoRef.current.currentTime = event.target.value
  }

  React.useEffect(function() {
    if (isPlaying) {
      const interval = setInterval(function() {
        setCurrentInSec(videoRef.current.currentTime)
      }, 200)
      return function() {clearInterval(interval)}
    }
  }, [isPlaying])

  React.useEffect(function() {
    const videourl = URL.createObjectURL(new Blob([file], {file: "video/mp4"}))
    setVideourl(videourl)
  }, [file])

  return (
    <div>
      <video
        ref={videoRef}
        src={videourl}
        width="90%"
        loop
        onClick={handlePlayPause}
        onLoadedMetadata={handleLoadedMetadata}
      />
      <PlayPauseButtons
        file={file}
        isPlaying={isPlaying}
        handlePlayPause={handlePlayPause}
      />
      <Seekbar
        file={file}
        currentInSec={currentInSec}
        handleSeekbarValue={handleSeekbarValue}
        durationInSec={durationInSec}
      />
    </div>
  )
}