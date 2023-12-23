import os
import sys
import pprint

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
from OpenAI.utils.checkOpenAIAPIKeyValid import CheckAPIKeyValid as CheckOpenAIAPIKeyValid
from OpenAI.utils.payloadParsor import PayloadParsor
from OpenAI.utils.textCosmetics import TextCosmetics
from OpenAI.utils.textEmbedding import TextEmbedding, CosSimilarities
from OpenAI.utils.textFromCSV import ParseSubtitleCSV
from DeepLAPI.src.translator import DeepLTranslator
from DeepLAPI.utils.checkDeepLAPIKeyValid import CheckAPIKeyValid as CheckDeepLAPIKeyValid

def GetSimilarTextsAndStartFrames(texts: list[str], startframes: list[int], subject: str, nreturn: int=1):
  emb_texts = TextEmbedding(texts=texts)
  emb_subject = TextEmbedding(texts=subject)
  cosines = CosSimilarities(vec1s=emb_texts, vec2=emb_subject[-1])

  information = [[text, startframe, cosine] for text, startframe, cosine in zip(texts, startframes, cosines)]
  information = sorted(information, key=lambda x: x[2], reverse=True)
  return information[:nreturn]

llm = TextGeneration()
translator = DeepLTranslator()

CheckDeepLAPIKeyValid(api_key=os.environ['DEEPL_API_KEY'])
CheckOpenAIAPIKeyValid(api_key=os.environ['OPENAI_API_KEY'])

# sys.exit(1)

llm.add_message_entry_as_specified_role_with_text_content(
  role='system',
  text=translator.translate(
    text='あなたは質問に対してカジュアルかつ簡潔に回答するアシスタントです。',
    source_lang='JA',
    target_lang='EN-US',
  )
)

csvfile = '../assets/helth.csv'
title = '「座りっぱなし」は寿命が縮む'
subtitle = ParseSubtitleCSV(csvfile=csvfile)
llm.add_message_entry_as_specified_role_with_text_content(
  role='user',
  text=translator.translate(
    text=TextCosmetics(
      text=f'''\
        以下に続く文章は"{title}"というタイトルのニュース番組を文字起こししたものです。\
        動画の内容を要約してください。\
        "{''.join(subtitle['texts'])}"\
      '''
    ),
    source_lang='JA',
    target_lang='EN-US',
  )
)

payload = llm.get_payload()
for line in pprint.pformat(PayloadParsor(payload=payload), width=150).split('\n'):
  logger.info(line)

llmresponse = llm.execute()
llmresponse = llmresponse.choices[0].message.content.replace('\n', '')
llmresponse = translator.translate(
  text=llmresponse,
  source_lang='EN',
  target_lang='JA',
)

for llmres in llmresponse.split('。'):
  if len(llmres) > 0:
    goodsubtitles = GetSimilarTextsAndStartFrames(
      texts=subtitle['texts'],
      startframes=subtitle['startframes'],
      subject=llmres,
      nreturn=1,
    )

    print(f'*  {llmres}')
    print(f'-> {goodsubtitles[0]}')