import React from "react";
import VideoUploader from '../molecules/VideoUploader'
import VideoPlayer from "../molecules/VideoPlayer";

export default function GivenVideoPlayer() {
  const [file, setFile] = React.useState(null)

  const videoRef = React.useRef(null)

  return (
    <div>
      <VideoUploader file={file} setFile={setFile} />
      <VideoPlayer file={file} videoRef={videoRef} />
    </div>
  )
}