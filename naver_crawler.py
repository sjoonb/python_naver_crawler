import json_parsing
import requests
import time
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class ClickButton():
    def __init__(self, key):
        self.key = key

    def get_button_by_class(self):
        return self.driver.find_element_by_class_name(self.key)

    def run(self, driver):
        self.driver = driver
        
        button = self.get_button_by_class()
        time.sleep(0.4)
        button.send_keys(Keys.ENTER)

        return self.driver

class FindDynamicData():
    def __init__(self, key):
        self.key = key

    def run(self, driver):
        self.driver = driver

        try:
            self.driver.find_element_by_class_name(self.key)

        except NoSuchElementException:
            pass

        return self.driver

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

class Metro():
    def __init__(self, station_name):
        self.station_name = station_name
        self.departure_list = []

    def insert_departure(self, departure):
        self.departure_list.append(departure)

    def get(self):
        return [self.station_name, self.departure_list]

    def print(self):
        print("[현재역]")
        print(self.station_name)
        print()
        print("[도착역 리스트]")

        for i, departure in enumerate(self.departure_list):
            print("#{}".format(i+1))
            departure.print()

class Departure():
    def __init__(self, station_name, line, departure_time, time_weight):
        self.station_name = station_name
        self.line = line
        self.departure_time = departure_time
        self.time_weight = time_weight

    def get(self):
        return [self.station_name, self.line, self.departure_time, self.time_weight]

    def print(self):
        print("station_name:", self.station_name)
        print("line:", self.line)
        print("departure_time:", self.departure_time)
        print("time_weight: ", self.time_weight)
        print()

class FindingStation():
    def __init__(self, station_line, line, curr_station, final_station):
        self.station_line = station_line
        self.line = line
        self.curr_station = curr_station
        self.final_station = final_station

    def get_instance_variables(self):
        return [self.station_line, self.line , self.curr_station, self.final_station]

class Driver():
    set_of_operator = dict()
    driver = 0

    def __init__(self):
        self.driver = webdriver.Safari()
        self.driver.implicitly_wait(1)

    @classmethod
    def set_operation(cls, key, operation):
        Driver.set_of_operator[key] = operation

    def set_html(self, url, action_list=[]):
        self.driver.get(url)

        for operator in action_list:
            if operator in Driver.set_of_operator.keys():
                self.driver = Driver.set_of_operator[operator].run(self.driver)

        html = self.driver.page_source
        self.soup = BeautifulSoup(html, "html.parser")


    def get_elements(self, find_type=[], attrs_list=[]):
        curr_soup = self.soup

        for idx, operator in enumerate(find_type):
            if operator in Driver.set_of_operator.keys():
                curr_soup = Driver.set_of_operator[operator].run(curr_soup, attrs_list[idx])

        if curr_soup == None:
            return None

        else:
            if isinstance(curr_soup, Tag):
                return curr_soup.get_text()

            else:
                elements = []

                for element in curr_soup:
                    elements.append(element.get_text())
                    
                return elements

    def quit(self):
        self.driver.quit()


myClickButton = ClickButton("_ft_search")
myFind = Find()
myFindAll = FindAll()
myFindDynamicData = FindDynamicData("info_detail")

Driver.set_operation("click_find_road_button", myClickButton)
Driver.set_operation("find_dynamic_data", myFindDynamicData)
Driver.set_operation("find", myFind)
Driver.set_operation("find_all", myFindAll)


def get_station_info(station):
    station_line, line, curr_station, final_station = station.get_instance_variables()

    driver = Driver()
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query="

    def get_weight_between_station(src_station, dest_station):
        temp_driver = driver
        
        src_station = src_station[:-1] + src_station[-1].replace("역","") + "역"
        dest_station = dest_station[:-1] + dest_station[-1].replace("역","") + "역"

        #print("# 다음역: ", dest_station)

        query = '+'.join([src_station, station_line]) + "에서+" + '+'.join([dest_station, station_line])


        temp_driver.set_html(url + query, action_list=["click_find_road_button", "find_dynamic_data"]) 

        info_detail = temp_driver.get_elements(find_type=["find_all"], attrs_list=[['em',{}]])
        #print(info_detail)
        if len(info_detail) == 14 or len(info_detail) == 13:
            weight = info_detail[11]

        else:
            weight = 5

        return weight

    def get_departure_list(hour_list, min_list):
        departure_list = []

        for idx in range(1, len(hour_list)-1):
            h = hour_list[idx]
            for m in min_list[idx-1].split():
                if m != '-':
                    departure_list.append(int(h+m))

        return departure_list

    while(True):
        query = '+'.join([station_line, curr_station, "열차시간표"])
        driver.set_html(url+query)

        hour_list = driver.get_elements(find_type=["find", "find", "find_all"], attrs_list=[["div", {"id":"timetable_weekend"}], ["tbody", {}], ["td", {"class":"mid"}]])

        next_station = driver.get_elements(find_type=["find", "find"], attrs_list=[["div", {"class":"nav_next"}], ["a", {}]])
        next_minute_list = driver.get_elements(find_type=["find", "find", "find_all"], attrs_list=[["div", {"id":"timetable_weekend"}], ["tbody", {}], ["td", {"class":"rc"}]])

        prev_station = driver.get_elements(find_type=["find", "find"], attrs_list=[["div", {"class":"nav_prev"}], ["a", {}]])
        prev_minute_list = driver.get_elements(find_type=["find", "find", "find_all"], attrs_list=[["div", {"id":"timetable_weekend"}], ["tbody", {}], ["td", {"class":"lc"}]])
        

        if curr_station in metro_dict:
            metro = metro_dict[curr_station]
        else:
            metro = Metro(curr_station)
            metro_dict[curr_station] = metro

        for dest_station_info in ([prev_station, prev_minute_list], [next_station, next_minute_list]):
            dest_station = dest_station_info[0]
            min_list = dest_station_info[1]

            if dest_station is not None:
                departure_list = get_departure_list(hour_list, min_list)

                time_weight = get_weight_between_station(curr_station, dest_station)
                departure = Departure(dest_station, line, departure_list, time_weight)

                metro.insert_departure(departure)


        if(next_station == None or curr_station == final_station):
            print("{station} is the last station".format(station = curr_station))
            break

        else:
            curr_station = next_station

    driver.quit()

metro_dict = dict()

if __name__ == "__main__":
    station_list = []

    station_line_1 = FindingStation("1호선", 1, "동묘앞", "대방")
    station_line_2 = FindingStation("2호선", 2, "홍대입구", "신당")
    station_line_3 = FindingStation("3호선", 3, "경복궁", "압구정")
    station_line_4 = FindingStation("4호선", 4, "혜화", "동작")
    station_line_5 = FindingStation("5호선", 5, "애오개", "행당")

    station_list.append(station_line_1)
    station_list.append(station_line_2)
    station_list.append(station_line_3)
    station_list.append(station_line_4)
    station_list.append(station_line_5)

    
    for station in station_list:
        get_station_info(station)

    json_parsing.write_to_json_file(metro_dict, "test.json")
    
#    for i in metro_dict:
#        metro_dict[i].print()

