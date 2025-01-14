import math

# static data

# location numbers mapped to on-screen position coordinates
locs = {
    0 : (-100, -100), 1 : (50, 40), 2 : (70, 155), 3 : (100, 250), 4 : (140, 385), 5 : (210, 500), 6 : (431, 520), 7 : (479, 440),
    8 : (479, 290), 9 : (460, 155), 10 : (489, 110), 11 : (590, 110), 12 : (675, 110), 13 : (695, 165), 14 : (710, 190), 15 : (690, 235),
    16 : (680, 320), 17 : (680, 420), 18 : (680, 480), 19 : (590, 480), 20 : (587, 435), 21 : (587, 340), 22 : (587, 165),
    23 : (587, 35), 24 : (590, -100), 25 : (40, 160), 26 : (40, 80), 27 : (120, 80), 28 : (120, 160)
}

# degrees in radians of airplane in each location
loc_radians = {
    0 : 0, 1 : (11 * math.pi / 12), 2 : (11 * math.pi / 12), 3 : (5 * math.pi / 6), 4 : (5 * math.pi / 6),
    5 : (math.pi / 2), 6 : (math.pi / 4), 7 : 0, 8 : 0, 9 : 0, 10 : (2* math.pi) / 5,
    11 : math.pi / 2, 12 : (3 * math.pi / 4), 13 : (9 * math.pi / 10), 14 : math.pi, 15 : (5 * math.pi) / 4,
    16 : math.pi, 17 : math.pi, 18 : (5 * math.pi / 4), 19 : (7 * math.pi / 4), 20 : 0,
    21 : 0, 22 : 0, 23 : 0, 24 : 0, 25 : (7 * math.pi / 4),
    26 : math.pi / 4, 27 : (3 * math.pi / 4), 28 : (5 * math.pi / 4)
}

# voice file number mapped to name of mp3 file and 
voice_files = {
    '0.0' : "airplane-landing-6732.mp3", '1.0' : "1.0.wav", '2.0' : "2.0.wav",
    '3.0' : "3.0.wav", '4.0' : "4.0.wav", '5.0' : "5.0.wav",
    '6.0' : "6.0.wav", '7.0' : "7.0.wav", '8.0' : "8.0.wav",
    '9.0' : "9.0.wav", '10.0' : "10.0.wav", '11.0' : "11.0.wav",
    '12.0' : "12.0.wav", '13.0' : "13.0.wav", '14.0' : "14.0.wav", '15.0' : "15.0.wav",
    '16.0' : "16.0.wav", '17.0' : "17.0.wav", '18.0' : "18.0.wav",
    '20.0' : "20.0.wav", '21.0' : "21.0.wav", '22.0' : "22.0.wav",
    '23.0' : "23.0.wav", '24.0' : "24.0.wav", '25.0' : "25.0.wav", '26.0' : "26.0.wav"
}


light_off_color = "Light Grey"
light_on_color = "Yellow"

flight_num_day_color = "Black"
flight_num_off_color = "Yellow"

#lights coordinates
RW6L_positions = [
    (458, 420), (458, 400), (458, 380), (458, 360), (458, 340), (458, 320),
    (458, 300), (458, 280), (458, 260), (458, 240), (458, 220), (458, 200), 
    (458, 180), (458, 160), (458, 140),
    (500, 420), (500, 400), (500, 380), (500, 360), (500, 340), (500, 320),
    (500, 300), (500, 280), (500, 260), (500, 240), (500, 220), (500, 200), 
    (500, 180), (500, 160), (500, 140)
]

#RW6R (RW6L translated 99 units to the right)
RW6R_positions = []
for coord in RW6L_positions:
    x, y = coord
    x += 109
    RW6R_positions.append((x, y))

#taxiway
taxiway_positions = [(514, 94), (534, 94), (554, 94),
                     (514, 124), (534, 124), (554, 124),
                     (622, 94), (642, 94), (662, 94),
                     (622, 124), (642, 124), (662, 124),
                     
                    (716, 272), (716, 297), (716, 322),
                    (716, 347), (716, 372), (716, 397), (716, 422),
                    (716, 447), (716, 472), (716, 497),
                    (694, 515), (669, 515), (644, 515),
                    (619, 515), (594, 515), (569, 515)]

# vasi
RW6L_vasi_positions = [(451, 440), (507, 440)]

# approach lights
RW6L_apch_positions = [(480, 485), (480, 495), (470, 495), (490, 495)]

# ramp lights
ramp_positions = [(727, 94), (710, 108), (710, 137), (727, 151), (756, 151), (783, 151), (810, 151),
                  (820, 163), (820, 183), (800, 189), (780, 204), (755, 207), (728, 207), (707, 214),
                  (800, 238), (780, 225), (755, 220), (728, 220), (805, 247), (805, 261),
                  (795, 267), (775, 267), (755, 272)]

# fuel depot light
fuel_depot_light_position = (444, 165)
# beacon gw
beacon_gw_position = [(390, 510)]


#simulation data

records = [
    "0,0,11111111,1,0.0,N123",
    "1,1,11111111,1,1.0,N123",
    "2,2,11111111,1,0.0,N123",
    "3,3,11111111,1,2.0,N123",
    "4,4,11111111,1,0.0,N123",
    "5,5,11111111,1,3.0,N123",
    "6,6,11111111,1,0.0,N123",
    "7,7,11111111,1,4.0,N123",
    "8,8,11111111,1,0.0,N123",
    "9,9,11111111,1,5.0,N123",
    "10,10,11111111,1,0.0,N123",
    "11,11,11111111,1,6.0,N123",
    "12,12,11111111,1,0.0,N123",
    "13,13,11111111,1,7.0,N123",
    "14,14,11111111,1,0.0,N123",
    "15,15,11111111,1,8.0,N123",
    "16,16,11111111,1,0.0,N123",
    "17,17,11111111,1,9.0,N123",
    "18,18,11111111,1,0.0,N123",
    "19,19,11111111,1,10.0,N123",
    "20,20,11111111,1,0.0,N123",
    "21,21,11111111,1,11.0,N123",
    "22,22,11111111,1,0.0,N123",
    "23,23,11111111,1,12.0,N123",
    "24,24,11111111,1,0.0,N123"
]

record2 = [
    "0,0,11111111,0,0.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "1,1,11111111,0,1.0,AIR22",
    "2,2,11111111,0,0.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "3,3,11111111,0,2.0,AIR22",
    "4,4,11111111,0,0.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "5,5,11111111,0,3.0,AIR22",
    "6,6,11111111,0,0.0,AIR22",
    "7,7,10011111,0,4.0,AIR22",
    "8,8,10011111,0,0.0,AIR22",
    "9,9,10011111,0,5.0,AIR22",
    "10,10,10011111,0,0.0,AIR22",
    "11,11,10011111,0,6.0,AIR22",
    "12,12,10011111,0,0.0,AIR22",
    "13,13,10011111,0,7.0,AIR22",
    "14,14,10011111,0,0.0,AIR22",
    "15,15,10011111,0,8.0,AIR22",
    "16,16,10011111,0,0.0,AIR22",
    "17,17,10011111,0,9.0,AIR22",
    "18,18,10011111,0,0.0,AIR22",
    "19,19,10011111,0,10.0,AIR22",
    "20,20,11011111,0,0.0,AIR22",
    "21,21,11011111,0,11.0,AIR22",
    "22,22,11011111,0,0.0,AIR22",
    "23,23,11011111,0,12.0,AIR22",
    "24,24,11011111,0,0.0,AIR22",
]
