"""
Script to calculate average surface current direction and 
average current velocity from the buoy Stena Skåne Ferrybox
for every April of 2019 - 2022, both seperately and all years together.


Written for the B.Sc. thesis:
"Identification of Gas Seeps Associated with Fracture Zones in the 
Southwestern Baltic Sea Using Open-Source Software"

by Victor Bäcklin
Department of Geological Sciences, Stockholm University
2025-05-16
"""
import math
import numpy as np

def mean(vector):
    s = sum(vector)
    n = len(vector)
    
    return s/n

def calculate_average_direction(d_vector):
    radians = [math.radians(d) for d in d_vector]
    sin_dir = [math.sin(r) for r in radians]
    cos_dir = [math.cos(r) for r in radians]
    
    sin_mean = mean(sin_dir)
    cos_mean = mean(cos_dir)
    
    rad_avg = math.atan2(sin_mean, cos_mean)
    deg_avg = math.degrees(rad_avg) % 360
    
    return deg_avg

def calculate_average_scaled_direction(vd_vector):
    sin_dir = [v*math.sin(math.radians(d)) for (v, d) in vd_vector]
    cos_dir = [v*math.cos(math.radians(d)) for (v, d) in vd_vector]
    
    sin_mean = mean(sin_dir)
    cos_mean = mean(cos_dir)
    
    rad_avg = math.atan2(sin_mean, cos_mean)
    deg_avg = math.degrees(rad_avg) % 360
    
    return deg_avg

filename = "current_data.csv"

with open(filename, 'r') as f:
    
    lines = f.readlines()
    
    directions = {"April, 2019": [], 
                  "April, 2020": [], 
                  "April, 2021": [], 
                  "April, 2022": [], 
                  "April, 2019 - 2022": []}
    
    velocities = {"April, 2019": [], 
                  "April, 2020": [], 
                  "April, 2021": [], 
                  "April, 2022": [], 
                  "April, 2019 - 2022": []}
    
    both = {"April, 2019": [], 
            "April, 2020": [], 
            "April, 2021": [], 
            "April, 2022": [], 
            "April, 2019 - 2022": []}
    
    buffer = True
    for line in lines:
        cells = line.split(';')
        
        if buffer:
            if cells[0] == "Datum Tid (UTC)":
                buffer = False
        else:
            month = cells[0].split('-')[1]
            year = cells[0].split('-')[0]
            if cells[1]:
                
                direction = float(cells[1])
                if month == '04':
                    directions[f'April, {year}'].append(direction)
                    directions['April, 2019 - 2022'].append(direction)
                    
            if cells[6]:
                velocity = float(cells[6])
                if month == '04':
                    velocities[f'April, {year}'].append(velocity)
                    velocities['April, 2019 - 2022'].append(velocity)
            
            if cells[6] and cells[1]:
                if month == '04':
                    both[f'April, {year}'].append((velocity, direction))
                    both['April, 2019 - 2022'].append((velocity, direction))


for key in directions.keys():
        avg_dir = calculate_average_direction(directions[key])
        avg_vel = mean(velocities[key])
        median_vel = np.median(velocities[key])
        max_vel = np.max(velocities[key])
        scaled_dir = calculate_average_scaled_direction(both[key])
        print(f'\n{key}')
        print(f'Avg. direction: {round(avg_dir)}')
        print(f'Avg. velocity: {round(avg_vel)}')
        print(f'Velocity median: {round(median_vel)}')
        print(f'Velocity maximum: {round(max_vel)}')
        print(f'Velocity scaled vector direction: {round(scaled_dir)}')


