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
sys.path.append(os.path.dirname(os.pardir))
from OpenAI.src.TextGeneration import TextGeneration
from OpenAI.utils.checkOpenAIAPIKeyValid import CheckAPIKeyValid
from OpenAI.utils.payloadParsor import PayloadParsor
from OpenAI.utils.textCosmetics import TextCosmetics
from OpenAI.utils.textEmbedding import TextEmbedding, CosSimilarity, CosSimilarities
from OpenAI.utils.textFromCSV import TextFromCSV, ParseSubtitleCSV
from DeepLAPI.src.translator import DeepLTranslator