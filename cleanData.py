import wget
import os
from os import path

print("===========STARTING TO CLEAN CASES CSV===========")

url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
if path.exists("datasets/us-counties.csv"):
    os.remove("datasets/us-counties.csv")

#download from NYT github repo, keeping data as up to date as possible
filename = wget.download(url, out="datasets")

print() #wget doesnt include newline char for some reason

#store tuples w/ date, county + state, cases
entries = []
#csv format: date,county,state,fips,cases,deaths
with open("datasets/us-counties.csv", 'r') as f:
    #advance to skip format row
    f.readline()
    for line in f:
        line = line.strip()
        elems = line.split(',')
        loc = elems[1] + ',' + elems[2]
        if "Hawaii" in loc or "Alaska" in loc:
            continue
        currTot = int(elems[4])
        entries.append((elems[0], loc, currTot))


print("===========DONE CLEANING CASES CSV===========")

print("===========STARTING TO BUILD COUNTIES DICT===========")
#this could be added to txt to make cleaner
#translate fullname to abbrev to synchronize datasets
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))


countiesToCoords = {}
with open("datasets/counties.csv", 'r') as f:
    for line in f:
        line.strip()
        elems = line.split(',')
        #lat, long   #mult by neg 1 to match convention
        coords = float(elems[3]), float(elems[4]) * -1
        #counties, state abbrev
        if elems[5] == '' or elems[5] == "AE":
            continue
        countiesWState = elems[5]+','+abbrev_us_state[elems[2]]
        if countiesWState not in countiesToCoords:
            countiesToCoords[countiesWState] = coords


print("===========DONE CREATING COUNTIES DICT===========")

print("===========ADDING LAT, LONG===========")

invalids = {}  #dict to help track all counties not present in both datasets
correct = {
    #this could be added to txt to make cleaner
    #dict to account for counties with conflicting names across both datasets
        #e.g: New York City instead of New York
    "New York City,New York": (40.713, 74.006),
    "Orleans,Louisiana": (29.951, 90.072),
    "Jefferson,Louisiana": (29.951, 90.072),
    "Unknown, New Jersey": (40.058, 74.406),
    "DuPage,Illinois": (41.824, 88.090),
    "Baltimore city,Maryland": (39.290, 76.612),

    'DeKalb,Georgia': (33.796, 84.228),
    'East Baton Rouge,Louisiana': (30.569, 91.097),
    'Caddo,Louisiana': (32.614, 93.866),
    'Unknown,Rhode Island': (41.580, 71.477),
    'St. Tammany,Louisiana': (30.436, 89.925),
    'Unknown,Michigan': (44.315, 85.602),
    'St. Louis city,Missouri': (38.627, 90.199),
    'Unknown,Massachusetts': (42.407, 71.382),
    'St. John the Baptist,Louisiana': (30.112, 90.488),
    'Lafourche,Louisiana': (29.695, 90.526),
    'Ouachita,Louisiana': (32.427, 92.224),
    'Unknown,Georgia': (32.166, 82.900),
    'Alexandria city,Virginia': (38.805, 77.047),
    'Unknown,New Jersey': (40.058, 74.406),
    'Ascension,Louisiana': (30.202, 90.944),
    'St. Charles,Louisiana': (30.227, 93.217),
    'Tangipahoa,Louisiana': (30.876, 90.512),
    'Unknown,Connecticut': (41.603, 73.088),
    'Kansas City,Missouri': (39.099, 94.579),
    'St. Bernard,Louisiana': (29.880, 89.323),
    'Lafayette,Louisiana': (30.224, 92.020),
    'Iberville,Louisiana': (30.290, 91.405),
    'Harrisonburg city,Virginia': (38.450, 78.869),
    'Terrebonne,Louisiana': (29.230, 90.753),
    'Calcasieu,Louisiana': (30.209, 93.339),
    'Virginia Beach city,Virginia': (36.853, 75.978),
    'Richmond city,Virginia': (37.541, 77.436),
    'Unknown,Illinois': (40.633, 89.399)
}

includeLoc = [] #list<tuples (date, "county,state", cases, lat, long)
#countiesToCoords: key = "county,state"; val = (lat, long)
#entries: list<tuples (date, "county,state", cases)>
for i in range(len(entries)):
    key = entries[i][1]; lat, long = 0, 0;
    if key not in countiesToCoords:
        if key in correct:
            coords = correct[key]
            lat, long = coords[0], coords[1]
        else:
            if key in invalids:
                invalids[key] += entries[i][2]
            else:
                invalids[key] = entries[i][2]
            continue
    else:
        lat, long = countiesToCoords[key]
    includeLoc.append(entries[i] + (lat, long))
'''
#testing invalids bc some counties present in NYT arent in usgov counties
#sorted order to prioritize highest num cases
sorted = []
for key in invalids:
    sorted.append((invalids[key], key))
sorted.sort(reverse=True)
for elem in sorted:
    print(elem)
'''

print("===========DONE ADDING LAT, LONG===========")


class Region:
    def __init__(self, xPixLocs, yPixLocs, longLocs, latLocs):
        self.pxMin = xPixLocs[0]; self.pxMax = xPixLocs[1];
        self.pyMin = yPixLocs[0]; self.pyMax = yPixLocs[1];
        self.longMin = longLocs[0]; self.longMax = longLocs[1];
        self.latMin = latLocs[0]; self.latMax = latLocs[1];

#Starting map: pixels = (72, 2029, 75, 1105); coords = (49, 25, 125, 67)
REGIONS = [
    #       pixX,       pixY        longLocs        latLocs
    Region((74, 718), (75, 431), (105.938, 125), (41.587, 49)), #Idaho
    Region((74, 718), (431, 688), (105.938, 125), (35.687, 41,587)),    #Nevada
    Region((74, 718), (688, 1105), (105.938, 125), (25, 35.687)),      #Arizona

    Region((718, 1134), (75, 431), (93.625, 105.938), (41.587, 49)),    #Dakotas
    Region((718, 1134), (431, 688), (93.625, 105.938), (35.687, 41,587)),#Kansas
    Region((718, 1134), (688, 1105), (93.625, 105.938), (25, 35.687)),   #TX

    Region((1134, 1593), (75, 431), (79.996, 93.625), (41.587, 49)),#Great Lakes
    Region((1134, 1593), (431, 688), (79.996, 93.625), (35.687, 41,587)),  #IL
    Region((1134, 1593), (688, 1105), (79.996, 93.625), (25, 35.687)), #Alabama

    Region((1593, 2029), (75, 431), (67, 79.996), (41.587, 49)), #New York
    Region((1593, 2029), (431, 688), (67, 79.996), (35.687, 41,587)),#East Coast
    Region((1593, 2029), (688, 1105), (67, 79.996), (25, 35.687))#North Carolina
]

def regionBounds(lat, long):
    #locate which Region these lat and long correspond to
    for region in REGIONS:
        if (lat >= region.latMin and lat <= region.latMax and
            long >= region.longMin and long <= region.longMax):
            pixels = region.pxMin, region.pxMax, region.pyMin, region.pyMax
            coords = region.latMin, region.latMax, region.longMin,region.longMax
            return pixels, coords

'''
keys are "county,state", vals:
                            (pxMin, pxMax, pyMin, pyMax)
                            (latMin, latMax, longMin, longMax)
'''

countiesToRegions = {}
for each in includeLoc:
    key = each[1]
    countiesToRegions[key] = (regionBounds(each[3], each[4]))

def getPixels(lat, long, regionTup):
    #use ratio to determine mapping of lat/long to pixX/pixY
    def mapVal(input, inputLow, inputHigh, outputLow, outputHigh):
        return ((input - inputLow) / (inputHigh - inputLow)) \
            * (outputHigh - outputLow) + outputLow
    pixels, coords = regionTup[0], regionTup[1]
    pixX = mapVal(long, coords[3], coords[2], pixels[0], pixels[1])
    pixY = mapVal(lat, coords[1], coords[0], pixels[2], pixels[3])
    return int(pixX), int(pixY)

print("===========DONE GETTING REGION BOUNDS===========")
#loop over entries and map its long lat to correct pixel based on region bounds
resLst = [] #list<tuples (date, "county,state", cases, lat, long, pixX, pixY)
for each in includeLoc:
    key = each[1]; regionTup = countiesToRegions[key];
    if not regionTup:
        if key == "Cameron,Texas":
            resLst.append(each + (970, 940))
        elif key == "Monroe,Florida":
            resLst.append(each + (1645, 1107))
        elif key == "Houghton,Michigan":
            resLst.append(each + (1212, 174))
        continue
    lat, long = each[3], each[4]
    pixX, pixY = getPixels(lat, long, regionTup)
    resLst.append(each + (pixX, pixY))

print("===========DONE MAPPING PIXELS===========")
with open("clean.csv", 'w') as f:
    for entry in resLst:
        f.write(entry[0] + ',' + str(entry[2]) + ',' + str(entry[5]) \
            + ',' + str(entry[6]) + '\n')

#write entire resLst to file to make debugging easier
with open("debugging.csv", 'w') as f:
    for entry in resLst:
        f.write(str(entry) + '\n')

print("===========SCRIPT DONE===========")
