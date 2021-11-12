from fastapi import FastAPI

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd



# GOOGLE SPREEDSHEET Authorization
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive']
                
GOOGLE_APPLICATION_CREDENTIALS = 'google-credentials.json'


credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_APPLICATION_CREDENTIALS, SCOPES)

#-----------------------------
table_name = 'Positions'
sheet = gs.create(table_name)

# Make it visible to other guys
sheet.share('ggguncha@gmail.com', perm_type='user', role='writer')

worksheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1-0aU-aiRv1KoA2gs6J8X93ZuhidFAp61aVpRTwxt0wU/edit?usp=sharing')
sheet = worksheet.worksheet("Sheet1")
values_list = sheet.col_values(2)[1:]

listed = []
all_keys_places = []
def main():
    driver = webdriver.Chrome('C:\\Users\\gggun\\PositionChecker\\chromedriver.exe')
    driver.get(f"https://yandex.ru/search/?lr=43")
    for key in values_list:
        search_form = driver.find_element(By.TAG_NAME, "form")
        search_box = search_form.find_element(By.NAME, "text")
        search_box.send_keys(f"{key}")


        search_button = search_form.find_element_by_css_selector(".websearch-button")
        search_button.click()

        search = driver.find_elements_by_class_name("serp-item")

        count = 0
        place = 0
        for i in search:
            i = i.text
            count = count + 1
            if "Реклама" in i and "toyota.kanavto.ru" in i:
                place = count
                break

        listed = [key, place]
        all_keys_places.append(listed)

        search_form = driver.find_element(By.TAG_NAME, "form")
        search_form.find_element(By.NAME, "text").clear()



    df = pd.DataFrame(all_keys_places)
    sheet = 'Sheet1'
    d2g.upload(df, table_name, sheet, credentials=credentials, row_names=True)



@app.get("/")
def root():
    main()
    return {"message": "Done"}

if __name__ == "__main__":
    main()