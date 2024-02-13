import os
import sys

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

# Handmade modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from facilitator.Summarizer import Summarizer
from facilitator.FrameExtractor import FrameExtractor
from facilitator.PageGenerator import PageGenerator

class TVPageGenerator(object):
  def __init__(
    self,
    max_tokens_per_call: int=500,
    title: str='「座りっぱなし」は寿命が縮む',
    video_path: str='../assets/helth.mp4',
    csvfile: str='../assets/helth.csv',
    n_summary_texts: int=5,
    do_translate: bool=False,
    output_html_dir: str='outputs',
    output_html_name: str='output.html',
  ) -> None:
    self.summarizer = Summarizer(
      max_tokens_per_call=max_tokens_per_call,
      title=title,
      csvfile=csvfile,
      n_summary_texts=n_summary_texts,
      do_translate=do_translate,
    )
    self.frame_extractor = FrameExtractor(
      video_name = video_path,
    )
    self.page_generator = PageGenerator(
      title=title,
      output_html_name=f'{output_html_dir}/{output_html_name}',
    )
    self.output_html_dir = output_html_dir

  def execute(self):
    ### Summarizer ###
    self.summarizer.check_openai_api_key_valid(api_key=os.environ['OPENAI_API_KEY'])
    self.summarizer.check_deepl_api_key_valid(api_key=os.environ['DEEPL_API_KEY'])
    self.summarizer.set_subtitle(csvreader=None)

    # OpenAIのPromtを設定する。
    self.summarizer.set_system_character()
    self.summarizer.set_subtitle_texts()
    self.summarizer.set_function_tool()

    # Promtの設定確認
    self.summarizer.print_llm_payload()

    # OpenAIのサーバーにPostリクエストを投げ、結果を取得する
    llmresponse, allgoodsubtitles = self.summarizer.execute()

    ### Frame extractor ###
    self.frame_extractor.set_video()

    # ビデオから適切なフレームを取得する
    frames = self.frame_extractor.extract_with_centisecs(
      centisecs=[int(goodsubtitles[0][1]) for goodsubtitles in allgoodsubtitles]
    )

    # フレームを画像として保存
    imagepaths = self.frame_extractor.save_frames(frames=frames, dirname=self.output_html_dir)
    imagepaths = [os.path.basename(imagepath) for imagepath in imagepaths]

    ### Page generator ###
    self.page_generator.generate(
      paragraphs=llmresponse,
      imagepaths=imagepaths,
    )

if __name__ == '__main__':
  obj = TVPageGenerator(
    title='アメリカ主導のウクライナ支援 曲がり角?議会で予算が通らず年末までに予算枯渇の可能性',
    video_path='../assets/Ukraine.mp4',
    csvfile='../assets/Ukraine.csv',
    output_html_dir='Ukrain',
    output_html_name='Ukurain.html',
  )
  # obj = TVPageGenerator(
  #   title='学校に行かない子供が増加 問われ始めた学校教育のあり方とは 学校の未来 不登校30万人から考える',
  #   video_path='../assets/Tuant.mp4',
  #   csvfile='../assets/Tuant.csv',
  #   output_html_dir='Tuant',
  #   output_html_name='Tuant.html',
  # )
  # obj = TVPageGenerator()
  obj.execute()