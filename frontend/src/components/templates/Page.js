import React from "react";
import ApplicationBar from "../organisms/ApplicationBar";
import GivenVideoPlayer from "../organisms/GivenVideoPlayer";
import ArgumentsSetting from "../molecules/ArgumentsSetting";
import CSVUploader from "../molecules/CSVUploader";
import LLMPayloadShower from "../organisms/LLMPayloadShower";
import CallButton from "../atoms/CallButton";

export default function Page() {
  return (
    <div>
      <ApplicationBar />
      <div className="h-screen grid grid-cols-6 divide-x-2 divide-gray-300">
        <div className="col-span-2 space-y-8 m-2">
          <GivenVideoPlayer />
          <ArgumentsSetting />
          <CSVUploader />
        </div>
        <div className="col-span-2 space-y-8 m-2">
          <LLMPayloadShower />
        </div>
        <div className="col-span-2 space-y-8 m-2">
          <CallButton />
        </div>
      </div>
    </div>
  )
}