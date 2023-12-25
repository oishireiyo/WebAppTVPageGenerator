import os
import sys
import pprint
import json

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
from OpenAI.utils.textFromCSV import ParseSubtitleCSV
from DeepLAPI.src.translator import DeepLTranslator

class PageGenerator(object):
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
    self.subtitle = ParseSubtitleCSV(csvfile=csvfile)
    self.n_summary_texts = n_summary_texts

  def set_title(self, title: str) -> None:
    self.title = title

  def set_csvfile(self, csvfile: str) -> None:
    self.csvfile = csvfile
    self.subtitle = ParseSubtitleCSV(csvfile=csvfile)

  def set_n_summary_texts(self, n_summary_texts: int) -> None:
    self.n_summary_texts = n_summary_texts

  def check_openai_api_key_valid(self, api_key: str) -> None:
    self.llm.set_api_key(api_key=api_key)

  def check_deepl_api_key_valid(self, api_key: str) -> None:
    self.translator.set_api_key(api_key=api_key)

  def get_similar_text_startframes(self, texts: list[str], startframes: list[int], subject: str, nreturns: int=1) -> list[str]:
    emb_texts = TextEmbedding(texts=texts)
    emb_subject = TextEmbedding(texts=subject)
    cosines = CosSimilarities(vec1s=emb_texts, vec2=emb_subject[-1])

    information = [info for info in zip(texts, startframes, cosines)]
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
            動画の内容を{self.n_summary_texts}つの文章に要約し、文章の配列として出力してください。\
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

  def print_llm_payload(self):
    payload = self.llm.get_payload()
    for line in pprint.pformat(payload, width=150).split('\n'):
      logger.info(line)

  def execute(self):
    llmresponse = self.llm.execute()
    llmresponse = json.loads(llmresponse.choices[0].message.tool_calls[0].function.arguments)['responses']
    for llmres in llmresponse:
      llmres = self.translator.translate(
        text=llmres, source_lang='EN', target_lang='JA',
      )

      goodsubtitles = self.get_similar_text_startframes(
        texts=self.subtitle['texts'],
        startframes=self.subtitle['startframes'],
        subject=llmres,
        nreturns=1,
      )

      logger.info(f'*  {llmres}')
      logger.info(f'-> {goodsubtitles[0]}')

if __name__ == '__main__':
  obj = PageGenerator()
  obj.check_openai_api_key_valid(
    api_key=os.environ['OPENAI_API_KEY']
  )
  obj.check_deepl_api_key_valid(
    api_key=os.environ['DEEPL_API_KEY']
  )
  obj.set_system_character(
    text='あなたは質問に対してカジュアルかつ簡潔に回答するアシスタントです。'
  )
  obj.set_subtitle_texts()
  obj.set_function_tool()
  obj.print_llm_payload()
  obj.execute()