#Assignment 2 participants list
# Shraddha Machchhar
# Shruti S. Sankolli

from pygeodesy import ellipsoidalVincenty as ev
from datetime import datetime

#Intitialize global variables
date_pos = 0
time_pos=1
storm_name_pos = 2
landFall_count=0
landFall_pos=2
wind_pos=6
dict_wind={}
data_set_lon_list=[]
data_set_lat_list=[]
data_set_cur_time_list=[]
data_set_speed_list=[]
lon_pos=4
lat_pos=5
dict_strom_per_year={}
dict_hurricane_per_year={}
dict_storm_info={}
hurricane_pos=3
hurricane_count=0
hurricane_found_flag=False

def mean(real_num_list: list)-> float:
    '''
    This function calculates the mean speed of a particular storm
    :param real_num_list: Inputs a list of speeds observed during the path for a particular storm
    :return: The mean speed for that storm
    '''
    sum = 0
    for each in real_num_list:
        sum += each
    return sum/len(real_num_list)

def findMaxWindAndDate(dict_wind: dict):
    '''
    This functions calculates the maximum speed observed for a partiuclar storm and the date/time at which that occured.
    :param dict_wind: Inputs a dictionary having the dates and times observed for the different tracks for a particular storm
    :return: the max speed obsrved for the storm and the date and time at which the max speed was observed.
    '''
    max_wind_speed = 0
    max_wind_date=""
    max_wind_time=""
    FMT = '%Y%m%d %H%M'
    for key, value in dict_wind.items():
        if int(value) > int(max_wind_speed):
            max_wind_speed = int(value)
            max_wind_date=key[0]
            max_wind_time=key[1]
    print("Date/Time when the highest maximum sustained wind was observed:", max_wind_date,max_wind_time)
    return max_wind_date,max_wind_speed

def calulate_distance_and_speed(lat_list:list, lon_list:list, data_set_cur_time_list:list):
    '''
    Calculates the maximum and mean speed the storm centre has moved. Also calculates the total distance the storm has moved.
    :param lat_list: Inputs a list of latitudes
    :param lon_list: Inputs a list of latitudes
    :param data_set_cur_time_list: Inputs a list of times
    :return:
    '''
    dist_meters=0
    tot_dist_meters =0
    for i in range(len(lon_list)-1):
        ini_pos = ev.LatLon(lat_list[i], lon_list[i])
        fin_pos = ev.LatLon(lat_list[i+1], lon_list[i+1])
        try:
            dist_meters = ini_pos.distanceTo(fin_pos)/1852 #Convert to nautical miles
        except ev.VincentyError:
            dist_meters =0
        tot_dist_meters = tot_dist_meters + dist_meters
        time_diff = calc_time_diff(data_set_cur_time_list[i],data_set_cur_time_list[i+1])
        data_set_speed_list.append(dist_meters/time_diff)
    if not data_set_speed_list :
        data_set_speed_list.append(0.0)
    print("Max speed is: ",round(max(data_set_speed_list),5)," Nautical Miles/Minute")
    print("Mean speed is: ",round(mean(data_set_speed_list),5)," Nautical Miles/Minute")
    print("Total distance the storm was tracked",round((tot_dist_meters),5)," Nautical Miles")
    return tot_dist_meters

def calc_time_diff(date1:str,date2:str):
    '''
    This function calculates the time lag for a particular storm
    :param date1: Inputs a date the storm started
    :param date2: Inputs the date the storm ended
    :return: The time lag for the storm in seconds
    '''
    FMT = '%Y%m%d %H%M'
    tdelta = datetime.strptime(date2, FMT) - datetime.strptime(date1, FMT)
    return tdelta.total_seconds()/60

def calc_storm_per_year(start_date:str,end_date:str):
    '''
    This function calculates the number of storms per year and stores them in a dictionary with key being the year and value being the storm count
    :param start_date: Inputs the date the storm started
    :param end_date: Inouts the date the storm ended
    '''
    storm_start_year = str(start_date[:4])
    storm_end_year = str(end_date[:4])
    if storm_start_year in dict_strom_per_year:
        dict_strom_per_year[storm_start_year] +=1
    else:
        dict_strom_per_year[storm_start_year] = 1
    if storm_start_year!= storm_end_year:
        if storm_end_year in dict_strom_per_year:
            dict_strom_per_year[storm_end_year] += 1
        else:
            dict_strom_per_year[storm_end_year] = 1

def calc_hurricane_per_year(start_date:str,end_date:str,hurricane_found_flag:bool):
    '''
    This function calculates the number of hurricanes per year and stores them in a dictionary with key being the year and value being the hurricane count.
    :param start_date:
    :param end_date:
    :param hurricane_found_flag:
    :return:
    '''
    if hurricane_found_flag:
        storm_start_year = str(start_date[:4])
        storm_end_year = str(end_date[:4])
        if storm_start_year in dict_hurricane_per_year:
            dict_hurricane_per_year[storm_start_year] +=1
        else:
            dict_hurricane_per_year[storm_start_year] = 1
        if storm_start_year!= storm_end_year:
            if storm_end_year in dict_hurricane_per_year:
                dict_hurricane_per_year[storm_end_year] += 1
            else:
                dict_hurricane_per_year[storm_end_year] = 1

# We take the file name as input from the user
file_name=input("Enter the data file name :")

with open(file_name, 'r',buffering=1000) as input_file:
    list_data = input_file.readlines()
    file_size = list_data.__len__()
    i=0
    if list_data[file_size-1] == '\n':
        file_size = file_size - 1
    while(i< file_size):

        #Clean the data sets before each iteration
        data_set_lon_list = []
        data_set_lat_list = []
        data_set_cur_time_list = []
        data_set_speed_list=[]
        dict_wind={}

        #Initialize a flag to check if hurricane for a year is alraedy present. If True, that year is ignored.
        hurricane_found_flag=False

        #Iterate over each row as set of columns separated by ','
        header_data = list_data[i].split(",")

        #Get the Storm Name
        storm_name = header_data[1]

        #Counter to keep track of the no of records available for each storm
        data_set_len = int(header_data[storm_name_pos])

        #Counter to keep track of no of landfalls observed
        landFall_count = 0

        i=j=i+1
        while(j < i+data_set_len):
            data_row = list_data[j].split(",")
            if(j==i):
                start_date = data_row[date_pos]
                start_time = data_row[time_pos]
            if(j==i+data_set_len-1):
                end_date = data_row[date_pos]
                end_time = data_row[time_pos]

            #Check to see if Landfall observed. If yes, then the counter is incremented by 1
            if("L" == data_row[landFall_pos].strip()):
                landFall_count=landFall_count+1

            dict_wind[data_row[0],data_row[1]] = data_row[wind_pos]
            data_set_lat_list.append(data_row[4])
            data_set_lon_list.append(data_row[5])
            data_set_cur_time_list.append(data_row[date_pos]+data_row[time_pos])

            #Check to see if hurricane observed. If yes, flag is set to True
            if(hurricane_found_flag == False and data_row[hurricane_pos].strip() == 'HU'):
                hurricane_found_flag = True
            j=j+1

        #Print summary information for each storm
        print("Storm Name: ",storm_name.strip())
        print("Date Range for the Storm: ",datetime.strptime(str(start_date+" "+start_time),'%Y%m%d %H%M'),"-",datetime.strptime(str(end_date+" "+end_time),'%Y%m%d %H%M'))
        print("Highest Maximum Sustained Wind :",max(list(dict_wind.values()))," knots")
        str(findMaxWindAndDate(dict_wind))
        print("No of times Landfalls observed:",landFall_count)


        #Get the total no of storms observed per year
        calc_storm_per_year(start_date, end_date)

        #Get the total no of hurricanes observed per year
        calc_hurricane_per_year(start_date, end_date, hurricane_found_flag)

        # get the maximum and mean speed the storm centre moved
        calulate_distance_and_speed(data_set_lat_list,data_set_lon_list, data_set_cur_time_list)
        print("--------------------------------------------------")
        i=j #reference to new dataset

    print("\n No of Storms observed per year:")
    print("\n",dict_strom_per_year)
    print("------------------------------------------------")
    print("\n No of Hurricanes observed per year:")
    print("\n", dict_hurricane_per_year)



