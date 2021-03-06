import requests
import time
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver import ActionChains

class ClickButton():
    name = ""

    def __init__(self, name):
        self.name = name

    def get_button_by_class(self):
        return self.driver.find_element_by_class_name(self.name)

    def run(self, driver):
        self.driver = driver
        
        button = self.get_button_by_class()
        ActionChains(driver).click(button).perform()

class Find():
    def run(self, soup, attrs):
        tag = attrs[0]
        curr_attrs = attrs[1]
        try:
            soup = soup.find(tag, attrs=curr_attrs)
        except:
            return None

        return soup

class FindAll():
    def run(self, soup, attrs):
        tag = attrs[0]
        curr_attrs = attrs[1]
        try:
            soup = soup.find_all(tag, attrs=curr_attrs)
        except:
            return None

        return soup
        

class Driver():
    set_of_operator = dict()

    def __init__(self):
        self.driver = webdriver.Safari()
        self.driver.implicitly_wait(1)

    @classmethod
    def set_operation(cls, key, operation):
        Driver.set_of_operator[key] = operation

    def init_soup(self, url, action_list=[]):
        self.driver.get(url)

        for operator in action_list:
            if operator in Driver.set_of_operator.keys():
                Driver.set_of_operator[operator].run(self.driver)

        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")


    def get_elements(self, url, find_type=[], attrs_list=[]):
        curr_soup = self.soup

        for idx, operator in enumerate(find_type):
            if operator in Driver.set_of_operator.keys():
                curr_soup = Driver.set_of_operator[operator].run(curr_soup, attrs_list[idx])

        if curr_soup == None:
            return None

        else:
            elements = []

            if isinstance(curr_soup, Tag):
                curr_soup = [curr_soup]

            for element in curr_soup:
                elements.append(element.get_text())
                
            return elements

    def quit(self):
        self.driver.quit()


myClickButton = ClickButton("_ft_search")
myFind = Find()
myFindAll = FindAll()

Driver.set_operation("click_find_road_button", myClickButton)
Driver.set_operation("find", myFind)
Driver.set_operation("find_all", myFindAll)

if __name__ == "__main__":
    driver = Driver()

    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&"

    station_line = "서울3호선"
    data = "열차시간표"
    curr_station = "정발산"

    while(True):
        query = "query=" + '+'.join([station_line, curr_station, data])

        driver.init_soup(url+query)

        next_station = driver.get_elements(url + query, find_type=["find", "find"], attrs_list=[["div", {"class":"nav_next"}], ["a", {}]])
        prev_station = driver.get_elements(url + query, find_type=["find", "find"], attrs_list=[["div", {"class":"nav_prev"}], ["a", {}]])
        hour_list = driver.get_elements(url + query, find_type=["find", "find", "find_all"], attrs_list=[["div", {"id":"timetable_weekend"}], ["tbody", {}], ["td", {"class":"mid"}]])
        prev_minute_list = driver.get_elements(url + query, find_type=["find", "find", "find_all"], attrs_list=[["div", {"id":"timetable_weekend"}], ["tbody", {}], ["td", {"class":"lc"}]])
        #print(time_table[0].get_text())
        
        print(next_station)
        print(prev_station)
        print(hour_list)
        print(prev_minute_list)

        if(next_station == None):
            print("curr_station {station} is last station".format(station = curr_station))
            break
        else:
            curr_station = next_station[0]

    driver.quit()
