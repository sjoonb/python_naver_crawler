#def write_to_json_file(metro_dict, file_name):
#    data = []
#
#    for key in metro_dict:
#        metro_obj = dict()
#        station_name, departure_list = metro_dict[key].get()
#        metro_obj["station_name"] = station_name
#    
#        departure_obj_list = []
#
#        for departure in departure_list:
#            departure_obj = dict()
#            station_name, line, departure_time, time_weight = departure.get()
#            departure_obj["station_name"] = station_name
#            departure_obj["line"] = line
#            departure_obj["departure_time"] = departure_time
#            departure_obj["time_weight"] = time_weight
#
#            departure_obj_list.append(departure_obj)
#
#        metro_obj["departure_list"] = departure_obj_list
#
#    with open(file_name, 'w') as json_file:
#        json.dump(metro_obj, json_file, indent=4)

def write_to_json_file(metro_dict, filename):
    ret = ""
    indent = 4

    ret += "[" + "\n"

    isFirst = True
    for key in metro_dict:
        if isFirst:
            isFirst = False
        else:
            ret += "," + "\n"

        ret += " "*indent + "{" + "\n"

        station_name, departure_list = metro_dict[key].get()

        ret += " "*indent*2 + '"station_name":"{}",'.format(station_name) + "\n"
        ret += " "*indent*2 + '"departure_list":['.format(station_name) + "\n"

        isFirstNet = True
        for departure in departure_list:
            if isFirstNet:
                isFirstNet = False
            else:
                ret += "," + "\n"

            ret += " "*indent*3 + "{" + "\n"
            station_name, line, departure_time, time_weight = departure.get()

            ret += " "*indent*4 + '"station_name":"{}",'.format(station_name) + "\n"
            ret += " "*indent*4 + '"line":{},'.format(line) + "\n"
            ret += " "*indent*4 + '"departure_time":{},'.format(departure_time) + "\n"
            ret += " "*indent*4 + '"time_weight":{}'.format(time_weight) + "\n"
            ret += " "*indent*3 + "}"

        ret += "\n"
        ret += " "*indent*2 + "]".format(station_name) + "\n"
        ret += " "*indent + "}"

    ret += "\n"
    ret += "]"

    f = open(filename, "w")
    f.write(ret)
    f.close()
        
