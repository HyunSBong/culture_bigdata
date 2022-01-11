from logging import exception
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os


# --------------------------------
# 크롤링 사용자 설정 부분
ChromeDriver = "/Users/hyunsubong/Developer/chromedriver" # 크롬 드라이버 경로
search_keyword = "겨울 여행지 추천"
search_option = 0 # 0 : 정확도순, 1 : 기간설정
startDate = "2021-05-30" # 기간 시작일
endDate = "2021-07-26" # 기간 종료일
count_goal = 4000 # 크롤링할 게시물 수
# --------------------------------


page_count = count_goal//7
if page_count < 1 or count_goal%7 != 0:
  page_count += 1
postUrls = []
blogDataSet = []
search_count = 1
status = False

# selenium
postDataPath = ".se-component.se-text.se-l-default"

# search
# 네이버는 페이지당 7개의 게시물이 표시됨
print("---- search start!...--------------------------------------------------") 
print("크롤링 데이터수 : ", count_goal)
print("페이지수 : ", page_count)
driver = wd.Chrome(ChromeDriver)
driver.get("https://www.naver.com")

try:
  for i in range(1, page_count+1):
    if status == True:
      break
    if search_option == 0:
      URL = f"https://section.blog.naver.com/Search/Post.nhn?pageNo={str(i)}&rangeType=ALL&orderBy=sim&keyword=" + search_keyword
    else:
      URL = f"https://section.blog.naver.com/Search/Post.naver?pageNo={str(i)}&rangeType=PERIOD&orderBy=sim&startDate={startDate}&endDate={endDate}&keyword=" + search_keyword
    driver.get(URL)
    time.sleep(1)
    for j in range(1,8):
      if search_count > count_goal:
        status = True
        break
      postUrl = driver.find_element_by_xpath(f"/html/body/ui-view/div/main/div/div/section/div[2]/div[{str(j)}]/div/div[1]/div[1]/a[1]")
      postUrl = postUrl.get_attribute("href")
      postUrls.append(postUrl)
      search_count += 1

except:
  print("---- 더이상 찾을 게시물이 없습니다.")
  pass

print("---- get posts success!!!--------------------------------------------------") 

for post in postUrls:
  print(f"{count_goal}개 남음")
  contents = ""
  driver.get(post)
  driver.switch_to.frame('mainFrame')
  postContents = driver.find_elements_by_css_selector(postDataPath)
  for e in postContents:
    contents += e.text
  blogDataSet.append(contents)
  print(contents)
  count_goal -= 1

print("---- All success!! start save.....--------------------------------------------------") 
try:
    naverBlog_df = pd.DataFrame({"네이버 블로그": blogDataSet})
    naverBlog_df.to_csv(f"naverBlog_{search_keyword}.csv", index=False)
    print("---- save csv success! at", os.path.realpath(__file__))
except:
    print("---- fail to save..")
try:
    naverBlog_df = pd.DataFrame({"네이버 블로그": blogDataSet})
    naverBlog_df.to_excel(f"naverBlog_{search_keyword}.xlsx", index=False)
    print("---- save xlsx success! at", os.path.realpath(__file__))
except:
    print("---- fail to save..")

print("---- 분석이 모두 끝났습니다......--------------------------------------------------") 
driver.close()
driver.quit()
