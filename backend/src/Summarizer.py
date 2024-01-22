import os
import sys
import pprint
import json
from typing import Union

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
sys.path.append(os.path.dirname(os.pardir))
from OpenAI.src.TextGeneration import TextGeneration
from OpenAI.utils.textCosmetics import TextCosmetics
from OpenAI.utils.textEmbedding import TextEmbedding, CosSimilarities
from OpenAI.utils.textFromCSV import ParseSubtitleCSVreader, ParseSubtitleCSV
from DeepLAPI.src.translator import DeepLTranslator

class Summarizer(object):
  def __init__(
    self,
    title: str='「座りっぱなし」は寿命が縮む',
    csvfile: str='../assets/helth.csv',
    n_summary_texts: int=5,
    max_tokens_per_call: int=500,
  ) -> None:
    self.llm = TextGeneration(max_tokens_per_call=max_tokens_per_call)
    self.translator = DeepLTranslator()

    self.title = title
    self.csvfile = csvfile
    self.subtitle = None
    self.n_summary_texts = n_summary_texts

  def set_title(self, title: str) -> None:
    self.title = title

  def set_csvfile(self, csvfile: str) -> None:
    self.csvfile = csvfile

  def set_subtitle(self, csvreader: Union[list, None]) -> None:
    self.subtitle = ParseSubtitleCSVreader(csvreader=csvreader) \
      if not csvreader is None else ParseSubtitleCSV(csvfile=self.csvfile)

  def set_n_summary_texts(self, n_summary_texts: int) -> None:
    self.n_summary_texts = n_summary_texts

  def check_openai_api_key_valid(self, api_key: str) -> None:
    self.llm.set_api_key(api_key=api_key)

  def check_deepl_api_key_valid(self, api_key: str) -> None:
    self.translator.set_api_key(api_key=api_key)

  def get_similar_text_startsecs(self, texts: list[str], startsecs: list[int], subject: str, nreturns: int=1) -> list[str]:
    emb_texts = TextEmbedding(texts=texts)
    emb_subject = TextEmbedding(texts=subject)
    cosines = CosSimilarities(vec1s=emb_texts, vec2=emb_subject[-1])

    information = [info for info in zip(texts, startsecs, cosines)]
    information = sorted(information, key=lambda x: x[2], reverse=True)

    return information[:nreturns]

  def set_system_character(self, text: str) -> None:
    self.llm.add_message_entry_as_specified_role_with_text_content(
      role='system',
      text=self.translator.translate(
        text=text, source_lang='JA', target_lang='EN-US',
      )
    )

  def set_subtitle_texts(self) -> None:
    self.llm.add_message_entry_as_specified_role_with_text_content(
      role='user',
      text=self.translator.translate(
        text=TextCosmetics(
          text=f'''
            以下に続く文章は"{self.title}"というタイトルのニュース番組を文字起こししたものです。\
            動画の内容を{self.n_summary_texts}個の文章に要約し、文章の配列として出力してください。\
            "{''.join(self.subtitle['texts'])}"
          '''
        ),
        source_lang='JA',
        target_lang='EN-US',
      ),
    )

  def set_function_tool(self) -> None:
    def dummy_function(responses: list[str]):
      for response in responses:
        logger.info(response)

    self.llm.add_tool_entry_as_function(
      tools={
        'type': 'function',
        'function': {
          'name': dummy_function.__name__,
          'description': 'Dummy function for controling the GPT output format.',
          'parameters': {
            'type': 'object',
            'properties': {
              'responses': {'type': 'array', 'items': {'type': 'string'}},
            },
            'required': ['responses'],
          },
        },
      },
    )

  def get_llm_payload(self):
    return self.llm.get_payload()

  def print_llm_payload(self):
    for line in pprint.pformat(self.llm.get_payload(), width=150).split('\n'):
      logger.info(line)

  def execute(self):
    llmresponse = self.llm.execute()
    llmresponse = json.loads(llmresponse.choices[0].message.tool_calls[0].function.arguments)['responses']

    self.llm.add_message_entry_as_specified_role(role='assistant')
    self.llm.add_text_content(text='\n'.join(llmresponse))

    allgoodsubtitles = []
    for llmres in llmresponse:
      llmres = self.translator.translate(
        text=llmres, source_lang='EN', target_lang='JA',
      )
      goodsubtitles = self.get_similar_text_startsecs(
        texts=self.subtitle['texts'],
        startsecs=self.subtitle['startsecs'],
        subject=llmres,
        nreturns=1,
      )

      logger.info(f'*  {llmres}')
      logger.info(f'-> {goodsubtitles[0]}')

      allgoodsubtitles.append(goodsubtitles)

    return llmresponse, allgoodsubtitles

if __name__ == '__main__':
  obj = Summarizer()
  obj.check_openai_api_key_valid(
    api_key=os.environ['OPENAI_API_KEY']
  )
  obj.check_deepl_api_key_valid(
    api_key=os.environ['DEEPL_API_KEY']
  )
  obj.set_title(title='「座りっぱなし」は寿命が縮む')
  obj.set_csvfile(csvfile='../assets/helth.csv')
  obj.set_subtitle(csvreader=None)
  obj.set_n_summary_texts(n_summary_texts=5)
  obj.set_system_character(
    text='あなたは質問に対してカジュアルかつ簡潔に回答するアシスタントです。'
  )
  obj.set_subtitle_texts()
  obj.set_function_tool()
  obj.print_llm_payload()
  llmresponse, allgoodsubtitles = obj.execute()

  from FrameExtractor import FrameExtractor
  from PageGenerator import PageGenerator
  import cv2

  frame_extractor = FrameExtractor()
  frame_extractor.set_video_name(video_name='../assets/helth.mp4')
  frame_extractor.set_video()

  frames = frame_extractor.extract_with_millisecs(millisecs=[int(goodsubtitles[0][1]) for goodsubtitles in allgoodsubtitles])

  imagepaths = []
  for i, frame in enumerate(frames):
    cv2.imwrite(f'helth_{i}.png', frame)
    imagepaths.append(f'helth_{i}.png')

  page_generator = PageGenerator(
    title='「座りっぱなし」は寿命が縮む',
    output_html_name='hoge.html',
  )
  page_generator.generate(
    paragraphs=llmresponse,
    imagepaths=imagepaths,
  )