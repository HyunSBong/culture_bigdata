#-*- coding:utf-8 -*-

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json
import pandas as pd


def extract_insta_data(user_id="id", user_passwd="passwd", wish_num=10,
                       login_option="facebook",
                       driver_path="~/chromedriver", keyword="마블", 
                       instagram_id_name="username", instagram_pw_name="password",
                       instagram_login_btn=".sqdOP.L3NKy.y3zKF     ",
                       facebook_login_page_css=".sqdOP.L3NKy.y3zKF     ",
                       facebook_login_page_css2=".sqdOP.yWX7d.y3zKF     ", 
                       facebook_id_form_name="email",
                       facebook_pw_form_name="pass",
                       facebook_login_btn_name="login",
                       first_img_css="div.v1Nh3.kIKUG._bz0w",
                       location_object_css="div.o-MQd.z8cbW > div.M30cS > div.JF9hh > a.O4GlU",
                       upload_id_object_css="div.e1e1d > span.Jv7Aj.MqpiF  > a.sqdOP.yWX7d._8A5w5.ZIAjV ",
                       date_object_css="div.k_Q0X.NnvRN > a.c-Yi7 > time._1o9PC.Nzb55",
                       main_text_object_css="div.C7I1f.X7jCj > div.C4VMK > span",
                       tag_css=".C7I1f.X7jCj",
                       comment_more_btn="button.dCJp8.afkep",
                       comment_ids_objects_css="ul.Mr508 > div.ZyFrc > li.gElp9.rUo9f > div.P9YgZ > div.C7I1f > div.C4VMK > h3",
                       comment_texts_objects_css="ul.Mr508 > div.ZyFrc > li.gElp9.rUo9f > div.P9YgZ > div.C7I1f > div.C4VMK > span",
                       print_flag=False,
                       next_arrow_btn_css1="._65Bje.coreSpriteRightPaginationArrow",
                       next_arrow_btn_css2="._65Bje.coreSpriteRightPaginationArrow",
                       save_file_name="instagram_extract",
                       save_file_name_tag="instagram_tag"):
    driver = wd.Chrome(driver_path)
    
    print(f"login start - option {login_option}")
    
    login_url = "https://www.instagram.com/accounts/login/"
    driver.get(login_url)
    time.sleep(10)
    
    is_login_success = False
    
    if login_option == "instagram":
        try:
            instagram_id_form = driver.find_element_by_name(instagram_id_name)
            instagram_id_form.send_keys(user_id)
            time.sleep(5)

            instagram_pw_form = driver.find_element_by_name(instagram_pw_name)
            instagram_pw_form.send_keys(user_passwd)
            time.sleep(7)
            
            login_ok_button = driver.find_element_by_css_selector(instagram_login_btn)
            login_ok_button.click()
            is_login_success = True
        except:
            print("instagram login fail")
            is_login_success = False

        time.sleep(10)
    elif login_option == "facebook":
        is_facebook_btn_click = False
        try:
            print("try click facebook login button 1")
            facebook_login_btn = driver.find_element_by_css_selector(facebook_login_page_css)
            time.sleep(5)
            facebook_login_btn.click()
            is_facebook_btn_click = True
            is_login_success = True
        except:
            print("click facebook login button 1 fail")
            is_facebook_btn_click = False
            is_login_success = False
            
        time.sleep(10)
        
        if not is_facebook_btn_click:
            print("try click facebook login button 2")
            try:
                facebook_login_btn = driver.find_element_by_css_selector(facebook_login_page_css2)
                time.sleep(5)
                facebook_login_btn.click()
                is_facebook_btn_click = True
                is_login_success = True
            except:
                print("click facebook login button 2 fail")
                is_login_success = False
                
        time.sleep(10)
        
        if is_facebook_btn_click:
            id_input_form = driver.find_element_by_name(facebook_id_form_name)
            time.sleep(5)
            id_input_form.send_keys(user_id)
            
            time.sleep(7)
            
            pw_input_form = driver.find_element_by_name(facebook_pw_form_name)
            time.sleep(5)
            pw_input_form.send_keys(user_passwd)
            
            time.sleep(7)
            
            login_btn = driver.find_element_by_name(facebook_login_btn_name)
            time.sleep(5)
            login_btn.click()
        time.sleep(10)
        
    if is_login_success:
        print(f"login {login_option} success")
        print(f"Start {keyword} Extract")

        url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

        instagram_tags = []
        instagram_tag_dates = []

        driver.get(url)
        time.sleep(10)


        print("login success")

        # 첫번째 게시물
        driver.find_element_by_css_selector(first_img_css).click()


        # data lists
        location_infos = []
        location_hrefs = []

        upload_ids = []

        date_texts = []
        date_times = []
        date_titles = []

        main_texts = []

        instagram_tags = []

        comments = []

        check_arrow = True

        count_extract = 0

        while True:
            if count_extract > wish_num:
                break
            time.sleep(5.0)
            # 위치정보

            if check_arrow == False:
                break

            try:
                location_object = driver.find_element_by_css_selector(location_object_css)
                location_info = location_object.text
                location_href = location_object.get_attribute("href")
            except:
                location_info = None
                location_href = None

            # 올린사람 ID
            try:
                upload_id_object = driver.find_element_by_css_selector(upload_id_object_css)
                upload_id = upload_id_object.text
            except:
                upload_id = None


            # 날짜
            try:
                date_object = driver.find_element_by_css_selector(date_object_css)
                date_text = date_object.text
                date_time = date_object.get_attribute("datetime")
                date_title = date_object.get_attribute("title")
            except:
                date_text = None
                date_time = None
                date_title = None


            # 본문
            try:
                main_text_object = driver.find_element_by_css_selector(main_text_object_css)
                main_text = main_text_object.text
            except:
                main_text = None


            ## 본문 속 태그
            try:
                data = driver.find_element_by_css_selector(tag_css) # C7I1f X7jCj
                tag_raw = data.text
                tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw) 
                tag = ''.join(tags).replace("#"," ") # "#" 제거

                tag_data = tag.split()

                for tag_one in tag_data:
                    instagram_tags.append(tag_one)
            except:
                continue


            # 댓글
            ## 더보기 버튼 클릭
            try:
                while True:
                    try:
                        more_btn = driver.find_element_by_css_selector(comment_more_btn)
                        more_btn.click()
                    except:
                        break
            except:
                print("----------------------fail to click more btn----------------------------------")
                continue

            ## 댓글 데이터
            try:
                comment_data = {}

                comment_ids_objects = driver.find_elements_by_css_selector(comment_ids_objects_css)

                comment_texts_objects = driver.find_elements_by_css_selector(comment_texts_objects_css)



                try:
                    for i in range(len(comment_ids_objects)):
                        comment_data[str((i+1))] = {"comment_id":comment_ids_objects[i].text, "comment_text":comment_texts_objects[i].text} 
                except:
                    print("fail")



            except:
                comment_id = None
                comment_text = None
                comment_data = {}


            try:
                if comment_data != {}:
                    keys = list(comment_data.keys())

                    for key in keys:
                        if comment_data[key]['comment_id'] == upload_id:
                            tags = re.findall('#[A-Za-z0-9가-힣]+', comment_data[key]['comment_text']) 
                            tag = ''.join(tags).replace("#"," ") # "#" 제거

                            tag_data = tag.split()

                            for tag_one in tag_data:
                                instagram_tags.append(tag_one)
            except:
                continue



            location_infos.append(location_info)
            location_hrefs.append(location_href)

            upload_ids.append(upload_id)

            date_texts.append(date_text)
            date_times.append(date_time)
            date_titles.append(date_title)

            main_texts.append(main_text)

            comment_json = json.dumps(comment_data, ensure_ascii=False)

            comments.append(comment_json)

            if print_flag:
                print("location_info : ", location_info)
                print("location_href : ", location_href)
                print("upload id : ", upload_id)
                print("date : {} {} {}".format(date_text, date_time, date_title))
                print("main : ", main_text)
                print("comment : ", comment_data)

                print("insta tags : ", instagram_tags)

            try:
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, next_arrow_btn_css1)))
                driver.find_element_by_css_selector(next_arrow_btn_css2).click()
            except:
                check_arrow = False

            count_extract += 1

        try:
            insta_info_df = pd.DataFrame({"location_info":location_infos, "location_href":location_hrefs, "upload_id":upload_ids, "date_text":date_texts, "date_time":date_times, "date_title":date_titles, "main_text":main_texts, "comment":comments})
            insta_info_df.to_csv("{}.csv".format(save_file_name), index=False)
        except:
            print("fail to save data")


        try:
            insta_tag_df = pd.DataFrame({"tag":instagram_tags})
            insta_tag_df.to_csv("{}.csv".format(save_file_name_tag), index=False)
        except:
            print("fail to save tag data")        
    elif not is_login_success:
        print(f"login {login_option} fail")
    
    driver.close()
    driver.quit()

    if __name__ == "__main__":
    extract_insta_data(user_id="id", user_passwd="passwd", wish_num=10,
                       login_option="facebook",
                       driver_path="~/chromedriver", keyword="마블", 
                       instagram_id_name="username", instagram_pw_name="password",
                       instagram_login_btn=".sqdOP.L3NKy.y3zKF     ",
                       facebook_login_page_css=".sqdOP.L3NKy.y3zKF     ",
                       facebook_login_page_css2=".sqdOP.yWX7d.y3zKF     ", 
                       facebook_id_form_name="email",
                       facebook_pw_form_name="pass",
                       facebook_login_btn_name="login",
                       first_img_css="div.v1Nh3.kIKUG._bz0w",
                       location_object_css="div.o-MQd.z8cbW > div.M30cS > div.JF9hh > a.O4GlU",
                       upload_id_object_css="div.e1e1d > span.Jv7Aj.MqpiF  > a.sqdOP.yWX7d._8A5w5.ZIAjV ",
                       date_object_css="div.k_Q0X.NnvRN > a.c-Yi7 > time._1o9PC.Nzb55",
                       main_text_object_css="div.C7I1f.X7jCj > div.C4VMK > span",
                       tag_css=".C7I1f.X7jCj",
                       comment_more_btn="button.dCJp8.afkep",
                       comment_ids_objects_css="ul.Mr508 > div.ZyFrc > li.gElp9.rUo9f > div.P9YgZ > div.C7I1f > div.C4VMK > h3",
                       comment_texts_objects_css="ul.Mr508 > div.ZyFrc > li.gElp9.rUo9f > div.P9YgZ > div.C7I1f > div.C4VMK > span",
                       print_flag=False,
                       next_arrow_btn_css1="._65Bje.coreSpriteRightPaginationArrow",
                       next_arrow_btn_css2="._65Bje.coreSpriteRightPaginationArrow",
                       save_file_name="instagram_extract",
                       save_file_name_tag="instagram_tag")