import os
import sys
import math

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

import numpy as np
import cv2

class FrameExtractor(object):
  def __init__(self, video_name: str='video') -> None:
    self.video_name = video_name
    self.video = None

  def set_video_name(self, video_name: str) -> None:
    self.video_name = video_name

  def set_video(self, video=None) -> None:
    self.video = video if video else cv2.VideoCapture(self.video_name)

  def get_video_information(self) -> dict[str, int]:
    return {
      'nframes': self.video.get(cv2.CAP_PROP_FRAME_COUNT),
      'width': self.video.get(cv2.CAP_PROP_FRAME_WIDTH),
      'height': self.video.get(cv2.CAP_PROP_FRAME_HEIGHT),
      'fps': self.video.get(cv2.CAP_PROP_FPS),
    }

  def convert_sec_to_frame(self, sec):
    return math.ceil(self.video.get(cv2.CAP_PROP_FPS) * sec)

  def convert_centisec_to_frame(self, centisec):
    return self.convert_sec_to_frame(sec=centisec/1e2)

  def convert_millisec_to_frame(self, millisec):
    return self.convert_sec_to_frame(sec=millisec/1e3)

  def get_frame(self, video, frame_number):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video.read()
    logger.info(f'フレーム番号: {frame_number}, 読み出し結果: {ret}')
    if ret:
      return frame
    else:
      return None

  def extract_with_frame_numbers(self, frame_numbers: list[int]) -> list[np.ndarray]:
    frames = []
    for frame_number in frame_numbers:
      frame = self.get_frame(video=self.video, frame_number=frame_number)
      if not frame is None: frames.append(frame)

    return frames

  def extract_with_centisecs(self, centisecs: list[int]) -> list[np.ndarray]:
    frame_numbers = [self.convert_centisec_to_frame(centisec=centisec) for centisec in centisecs]
    frames = self.extract_with_frame_numbers(frame_numbers=frame_numbers)

    return frames

  def save_frames(self, frames: list[np.ndarray], dirname: str) -> list[str]:
    imagepaths = []
    for i, frame in enumerate(frames):
      imagename = f'{dirname}/{i}.png'
      cv2.imwrite(imagename, frame)
      imagepaths.append(imagename)

    return imagepaths

if __name__ == '__main__':
  import pprint

  obj = FrameExtractor()
  obj.set_video_name(video_name='../assets/helth.mp4')
  obj.set_video()
  _ = obj.get_video_information()
  pprint.pprint(_)
  frames = obj.extract_with_millisecs([0, 11427, 64909, 53906, 155603])

  for i, frame in enumerate(frames):
    cv2.imwrite(f'helth_{i}.png', frame)