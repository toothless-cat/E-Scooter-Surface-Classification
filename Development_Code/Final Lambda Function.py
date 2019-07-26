from __future__ import print_function
#import matplotlib.pyplot as plt
#import numpy as np
#import json
import base64
import time

#geofence for parking lot with sidewalk in back
new_dx_sidewalk_poly = [(35.305198, -120.672091),(35.305214, -120.672063),(35.305217, -120.671829),(35.305217, -120.671760),(35.305220, -120.671577),(35.305211, -120.671576),(35.305217, -120.671355),(35.305187, -120.671356),(35.305188, -120.671242),(35.305210, -120.671248),(35.305207, -120.671328),(35.305243, -120.671330),(35.305237, -120.671540),(35.305254, -120.671540),(35.305397, -120.671543),(35.305398, -120.671498),(35.305470, -120.671501),(35.305467, -120.671567),(35.305418, -120.671563),(35.305248, -120.671561),(35.305241, -120.671768),(35.305235, -120.672070),(35.305218, -120.672102)]
cal_poly_geofence_new = [(35.302391, -120.663555),(35.302373, -120.663646),(35.302741, -120.663748),(35.302852, -120.663793),(35.302976, -120.663838),(35.303074, -120.663885),(35.303190, -120.663978),(35.303330, -120.664148),(35.303315, -120.664191),(35.303216, -120.664046),(35.303114, -120.663953),(35.302943, -120.663854),(35.302822, -120.663815),(35.302728, -120.663773),(35.302473, -120.663696),(35.302335, -120.663657)]
fences = [new_dx_sidewalk_poly,cal_poly_geofence_new]

def parser(data_in):
    x_vals = []
    y_vals = []
    z_vals = []
    lat_vals = []
    lon_vals = []
    mag_vals = []
    data_list = [x_vals,y_vals,z_vals,lat_vals,lon_vals,mag_vals]
    #tbrdl = [data_list[0],data_list[1],data_list[2],data_list[5]]
    index = 0 #0 = x, 1 = y, 2 = z, 3 = mag
    dummy_string = ""
    for char in data_in:
        if char == ",":
            data_list[index].append(float(dummy_string))
            index+=1
            dummy_string = ""
        elif char == ";":
            data_list[index].append(float(dummy_string))
            index = 0
            dummy_string = ""
        else:
            dummy_string+=char
    #creating magnitude values from x,y,z
    #subtracting 9.8 from z values to get unbiased magnitude
    for i in range(0,len(x_vals)-1):
        mag_vals.append(pow((pow(x_vals[i],2)+pow(y_vals[i],2)+pow(z_vals[i]-9.8,2)),.5))
    
    return data_list

#input a single list
#function finds amount of peaks per window

def bounder(point,shapes):
    position = "Outside"
    for shape in shapes:
        #starting point of ray (ray will be straight down from origin to point)
        origin = (point[0],point[1]+1000)
        crosscount = 0
        seglist = []
        #iterate through pairs of coordinates and build list of segments
        for i in range(len(shape)):
            seglist.append((shape[i],shape[i-1]))
        #iterate through list of line segments
        for segment in seglist:
            #print(segment)
            #create a dummy segment to get around tuple immutability
            dummysegment = list(segment)
            #check if ray will intersect a vertex, and move that vertext slightly to the left
            if (point[0] == segment[0][0]):
                dummysegment[0] = (segment[0][0] -.001, segment[0][1])
            if (point[0] == segment[1][0]):
                dummysegment[1] = (segment[1][0] -.001, segment[1][1])
            #replace original segment tuple with modified dummysegment tuple
            segment = dummysegment
            #if the segment lies on the path of the ray from origin to point
            if (min(segment[0][0],segment[1][0]) < point[0] < max(segment[0][0],segment[1][0])):
                #if the segment is not vertical (removing division by zero in slope calculation)
                if (segment[0][0] != segment[1][0]):
                    #print("Valid segment")
                    #calculate slope
                    slope = (segment[1][1]-segment[0][1])/(segment[1][0]-segment[0][0])
                    deltax = point[0] - segment[0][0]
                    #find the y value at which the ray will intersect the segment
                    y_extrapolated = segment[0][1]+slope*deltax
                    #if the point of intersection is above the point (and thus before it along the ray's path from origin)
                    if (origin[1] > y_extrapolated > point[1]):
                        crosscount+=1
                        #print("Ray crosses segment")
                    
            #if the cross count is odd, the point lays inside the polygon
            if(crosscount%2 !=0):
                position = "Inside"
                
    return position

#function assumes dat_list_in is parsed raw data
#window_size is the size of window to be used in peak filtering, 100 is recommended
#factor is the divisor to be used in data filtering, 4 is recommended
#max_count is the cutoff value for a peak to be considered, 21 is recommended
def new_peak_isolator(data_list_in,window_size,factor,min_avg,max_count,geofences,full):
    #timing purposes
    start_time = time.clock()
    #initialization and lists
    #data_in is accelerometer magnitude
    data_in = data_list_in[5]
    #lats is latitude
    lats = data_list_in[3]
    #lons is longitude
    lons = data_list_in[4]
    #count list is where measure of peak frequency is stored
    count_list = []
    #evaluator list is where surface classification values are stored
    evaluator_list = []
    #initializing count as 0 to avoid error for first loop of iteration
    count=0
    #initializing avg_val as 0 to avoid error for first loop of iteration
    avg_val = 0
    csv_output = "Acceleration_classification, geotag_classification, composite_score, latitude, longitude \r\n"
    #iterate across data input
    for i in range(len(data_in)):
        #if 0 or multiple of window size is reached
        if i%window_size == 0: 
            #if the average acceleration value exceeds the stationary threshold, indicates movement
            if avg_val > min_avg:
                #if the peak count is less than the maximum, indicates sidewalk
                if count <= max_count:
                    evaluator_list.append(2)
                #if the peak count is more than the maximum, indicates pavement
                else:
                    evaluator_list.append(1)
            #if the average acceleration value does not exceed stationary threshold, indicates no movement
            else:
                evaluator_list.append(0)
            #append count to count_list and reset value of count
            count_list.append(count)
            count = 0
            
            #if full == True, do geofencing and full analysis
            if full ==True:
                #get geofence data
                bounder_score = str(bounder((lats[i],lons[i]),geofences))
                #get composite data
                score = 0
                classification = "Not Sidewalk"
                if evaluator_list[-1] == 2:
                    score+=2
                if bounder_score == "Inside":
                    score+=1
                if(len(evaluator_list) >=2):
                    if evaluator_list[-2] == 2:
                        score +=1
                if score >=2:
                    classification = "Sidewalk"
                #append csv_data
                csv_output+= str(evaluator_list[-1]) + "," + bounder_score + "," + classification + "," + str(lats[i]) + "," + str(lons[i]) + "\r\n"
           
            #creating the bounding values for the upcoming window of data
            if len(data_in) > i+window_size:
                max_val = max(data_in[i:i+window_size])
                max_val = sum(sorted(data_in[i:i+window_size],reverse=True)[0:4])/5
                avg_val = sum(data_in[i:i+window_size])/window_size
            #if the index called would be out of range of the data list, keep the current values
            else:
                #do not change max_val or avg_val
                max_val,avg_val = max_val,avg_val
        #everything above covers cases where a multiple of window size is met
        #now we compare the incoming data to our thresholds to determine if a peak is made
        if data_in[i] > ((avg_val+max_val)/factor):
            count+=1
    millis_elapsed = ((time.clock()-start_time)*1000)
    #print("Milliseconds to run: ",millis_elapsed)
    return (count_list,evaluator_list,csv_output,millis_elapsed)


def lambda_handler(event, context):
       data_string_form = str(base64.b64decode(event['Records'][0]["kinesis"]["data"]))[3:-2]
       print(data_string_form)
       parsed_data = parser(data_string_form)
       evaluated_data = new_peak_isolator(parsed_data,100,6,4,35,fences,True)
       print("Milliseconds to process data: ",evaluated_data[3])
       print(evaluated_data[2])
       return None
       
      