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

class PageGenerator(object):
  def __init__(self, title: str, output_html_name: str):
    self.title = title
    self.output_html_name = output_html_name

  def get_paragraph_element(self, paragraph: str):
    return f'<p>{paragraph}</p>\n'

  def get_img_element(self, imagepath: str):
    return f'<img src="{imagepath}" alt="{imagepath}" />\n'

  def get_contents(self, paragraphs: list[str], imagepaths: list[str]):
    contents = ''
    for paragraph, imagepath in zip(paragraphs, imagepaths):
      contents += self.get_paragraph_element(paragraph=paragraph)
      contents += self.get_img_element(imagepath=imagepath)

    return contents

  def generate(self, paragraphs: list[str], imagepaths: list[str]):
    template = f'''
<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<meta http-equiv='X-UA-Compatible' content='IE=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>{self.title}</title>
</head>
<body>
<h1>{self.title}</h1>
  {self.get_contents(
    paragraphs = paragraphs,
    imagepaths = imagepaths,
  )}
</body>
</html>
'''

    with open(self.output_html_name, 'w') as f:
      f.write(template)

if __name__ == '__main__':
  generator = PageGenerator(
    title='「座りっぱなし」は寿命が縮む',
    output_html_name='hoge.html'
  )

  paragraphs = [
    '厚生労働省が健康維持のために必要な運動量の目安を発表しました。',
    '成人は、１日60分以上のｳｫｰｷﾝｸﾞと週に23回のﾄﾚｰﾆﾝｸﾞを行うのが望ましいとされています。',
    'さらに座りっぱなしの時間が長いと死亡ﾘｽｸが高まるとも指摘されました｡',
    '厚生労働省の調査では、運動量が多い人は、少ない人と比べ、生活習慣病や死亡ﾘｽｸが低いことが報告されています｡',
    '関西ﾃﾚﾋﾞﾆｭｰｽYouTubeﾁｬﾝﾈﾙをご覧いただき、ありがとうございます｡',
  ]
  imagepaths = [
    'helth_0.png',
    'helth_1.png',
    'helth_2.png',
    'helth_3.png',
    'helth_4.png',
  ]

  generator.generate(
    paragraphs=paragraphs,
    imagepaths=imagepaths,
  )