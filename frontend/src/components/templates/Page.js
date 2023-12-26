import React from "react";
import ApplicationBar from "../organisms/ApplicationBar";
import GivenVideoPlayer from "../organisms/GivenVideoPlayer";
import CSVUploader from "../molecules/CSVUploader";
import LLMPayloadShower from "../organisms/LLMPayloadShower";

export default function Page() {
  return (
    <div>
      <ApplicationBar />
      <div className="h-screen grid grid-cols-6 divide-x-2 divide-gray-300">
        <div className="col-span-2 space-y-8 m-2">
          <GivenVideoPlayer />
          <CSVUploader />
        </div>
        <div className="col-span-2 space-y-8 m-2">
          <LLMPayloadShower />
        </div>
        <div className="col-span-2 space-y-8 m-2">
          <p>piyo</p>
        </div>
      </div>
    </div>
  )
}