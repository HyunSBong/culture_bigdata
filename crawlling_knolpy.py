import pandas as pd
from konlpy.tag import Okt
from nltk import Text
from collections import Counter
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import re
okt = Okt()
file_path = "./크롤링데이터/각지역 계절별 크롤링"
token_list = []


# normalize
def normalizer(text):
  hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')
  result = hangul.sub('', text)
  return result

def text_preprocessing(text):
  stopWords = [line.rstrip('\n') for line in open('불용어리스트.txt', 'r')]
  token = okt.morphs(text)
  token = [t for t in token if t not in stopWords]

  return token
  
# Konlpy - Okt
def funcOkt(season, file):
  # font
  rc('font', family='AppleGothic')
  plt.rcParams['axes.unicode_minus'] = False
  plt.rcParams["figure.figsize"] = (8,6)

  processing_data = text_preprocessing(file)
  okt_process = okt.pos(" ".join(processing_data), norm=True, stem=True)
  filter = [x for x, y in okt_process if y in ['Noun']]
 
  Okt = Text(filter, name="Okt") 
  
  plt.xlabel("명사")
  plt.ylabel("빈도")

  wordInfo = dict()
  for tags, counts in Okt.vocab().most_common(50):
    if(len(str(tags)) > 1):
        wordInfo[tags] = counts
 
  values = sorted(wordInfo.values(), reverse=True)
  keys = sorted(wordInfo, key=wordInfo.get, reverse=True)

  # # 그래프 값 설정
  plt.bar(range(len(wordInfo)), values, align='center')
  plt.xticks(range(len(wordInfo)), list(keys), rotation='70')
  plt.savefig(f"{season}_형태소 분석.png", dpi = 600)
  
  print(f"---- 분석 완료 --------------------------------------------------") 
  




# # 계절별 형태소 분석
# 봄
# df = pd.read_excel(f"{file_path}/봄_전체.xlsx")
# analysis_list = df["네이버 블로그"].tolist()
# analysis_text = " ".join(analysis_list)
# funcOkt("봄", analysis_text)
# print("---- 봄 데이터 끝 --------------------------------------------------") 

# # 여름
# df = pd.read_excel(f"{file_path}/여름_전체.xlsx")
# analysis_list = df["네이버 블로그"].tolist()
# analysis_text = " ".join(analysis_list)
# normalizer(analysis_text)
# funcOkt("여름", analysis_text)
# print("---- 여름 데이터 끝 --------------------------------------------------") 

# # # 가을
df = pd.read_excel(f"{file_path}/가을_전체.xlsx")
analysis_list = df["네이버 블로그"].tolist()
analysis_text = " ".join(analysis_list)
normalizer(analysis_text)
funcOkt("가을", analysis_text)
print("---- 가을 데이터 끝 --------------------------------------------------") 

# # # 겨울
# df = pd.read_excel(f"{file_path}/겨울_전체.xlsx")
# analysis_list = df["네이버 블로그"].tolist()
# analysis_text = " ".join(analysis_list)
# normalizer(analysis_text)
# funcOkt("겨울", analysis_text)
# print("---- 겨울 데이터 끝 --------------------------------------------------") 
