import numpy as np
import matplotlib.pyplot as plt
zip_to_prec_file = open("ziptoprec.csv", "r").read().splitlines()
ztp_pairs = [(line.split(",")[1], line.split(",")[3]) for line in zip_to_prec_file]
zip_to_prec = {}
for prec, zip in ztp_pairs:
    if int(zip) in zip_to_prec: zip_to_prec[int(zip)].append(int(prec))
    else: zip_to_prec[int(zip)] = [int(prec)]

zips = [22201, 22202, 22203, 22204, 22205, 22206, 22207, 22209, 22213]
demos_by_zip = {}
dem_by_prec = {1: 0.798951048951049, 2: 0.8292929292929293, 3: 0.727051177904143, 4: 0.801226366888094, 5: 0.8026394721055788, 6: 0.7769404672192917, 7: 0.7863729508196722, 8: 0.7573200992555831, 9: 0.8171342685370742, 10: 0.7993786063027075, 11: 0.7750865051903114, 12: 0.7966197183098591, 13: 0.7739910313901345, 14: 0.8143800440205429, 15: 0.8020100502512563, 16: 0.7873704982733103, 17: 0.7999071494893222, 18: 0.806234502302515, 19: 0.8154733301297453, 20: 0.7422027290448343, 21: 0.7581187010078387, 22: 0.8052805280528053, 23: 0.8111587982832618, 24: 0.8152946092770581, 25: 0.8018539976825029, 26: 0.80413555427915, 27: 0.8043243243243243, 28: 0.81941431670282, 29: 0.8031376518218624, 30: 0.8207485226526592, 31: 0.798582995951417, 32: 0.7049180327868853, 33: 0.7277992277992278, 34: 0.7641921397379913, 35: 0.6770925110132159, 36: 0.7675988428158148, 37: 0.7745474492594624, 38: 0.8466819221967964, 39: 0.8172635445362718, 40: 0.7832558139534884, 41: 0.809299587992937, 42: 0.829153605015674, 43: 0.8032967032967033, 44: 0.8168193172356369, 45: 0.8061674008810573, 46: 0.7873443983402489, 47: 0.8266228430566968, 48: 0.768904593639576, 49: 0.8045234248788369, 50: 0.758257203092059, 51: 0.811088295687885, 52: 0.7859358841778697, 53: 0.7759197324414716, 54: 0.8154269972451791}
turnout_by_prec = {1: 0.4057598338046635, 2: 0.6013879434951335, 3: 0.6681884489936366, 4: 0.5550268797463707, 5: 0.6102175753277357, 6: 0.5172697024961369, 7: 0.6416266060915553, 8: 0.5237689642287707, 9: 0.5200141429555055, 10: 0.5102510853674073, 11: 0.6779774621926188, 12: 0.6877274551316644, 13: 0.5291861770875267, 14: 0.5753959578750575, 15: 0.57212385064405, 16: 0.6051101077355282, 17: 0.6801734491916794, 18: 0.507558573526933, 19: 0.4754892660346449, 20: 0.7039990197730162, 21: 0.5400694418195269, 22: 0.6472753628716932, 23: 0.6588588759179834, 24: 0.6089307541657011, 25: 0.6098709034236462, 26: 0.48545927576462977, 27: 0.5877914134794869, 28: 0.4929116268413064, 29: 0.7241031815623814, 30: 0.4742174033917153, 31: 0.686172801994227, 32: 0.5522369963221921, 33: 0.70126071242944, 34: 0.704499258364006, 35: 0.7076690122027257, 36: 0.6407343862920444, 37: 0.7168673218241889, 38: 0.42575302427539174, 39: 0.6343381389252949, 40: 0.5509162872634926, 41: 0.5136103171197142, 42: 0.4956972650491667, 43: 0.3498113997604314, 44: 0.5012408797203736, 45: 0.46575021250403026, 46: 0.49551381195184746, 47: 0.5258601399680559, 48: 0.5628900325700504, 49: 0.4963220423314136, 50: 0.4377739932978081, 51: 0.6255045871559634, 52: 0.39011177027839916, 53: 0.472369861313292, 54: 0.47788702842802483}
# [median income, average income], [white, black, native, hispanic, asian, hawaiian, two or more, other],[master
# bachelors, other degree, hs diploma, dropout], unemployment, median age. 
strs = "median income", "average income", "white", "black", "native", "hispanic", "asian", "hawaiian", "two or more", "other","master", "bachelors", "other degree", "hs diploma", "dropout", "unemployment", "median age"
for zip in zips:
    
    marker =  "This text never appears and functions as a marker"
    demo_file = open(f"zips/{zip}.txt", "r").read().splitlines()
    full_text = marker.join(demo_file)
    index_median_inc = full_text.count(marker, 0, full_text.find("the median household income"))
    index_avg_inc = full_text.count(marker, 0, full_text.find("The average (or mean) household income in"))
    index_race = full_text.count(marker, 0, full_text.find("% White"))
    index_edu = full_text.count(marker, 0, full_text.find("Master's degree or higher")) + 1
    index_unemp = full_text.count(marker, 0, full_text.find("The unemployment rate in"))
    index_age = full_text.count(marker, 0, full_text.find("The median age in"))
    demos_by_zip[zip] = [[], [], [], 0, 0]

    # income
    demos_by_zip[zip][0].append(float((line:=demo_file[index_median_inc])[line.find("$")+1:-1].replace(",", "")))
    demos_by_zip[zip][0].append(float((line:=demo_file[index_avg_inc])[line.find("$")+1:-1].replace(",", "")))

    # race
    for i in range(8):
        index = index_race + i * 2
        demos_by_zip[zip][1].append(float((line:=demo_file[index])[:line.find("%")]))

    # education
    for i in range(5):
        index = index_edu + i * 2
        demos_by_zip[zip][2].append(float((line:=demo_file[index])[:line.find("%")]))

    # unemployment
    demos_by_zip[zip][3] = float((line:=demo_file[index_unemp])[line.find("%")-4:line.find("%")])

    # age 
    demos_by_zip[zip][4] = float((line:=demo_file[index_age])[line.find(str(zip))+9:line.find("y")-1])

# getting turnout/democratic averages by zip code
zip_to_dem = {}
zip_to_turnout = {}
for zip in zips:
    precincts = zip_to_prec[zip]
    total_dem, total_turn = 0, 0
    for p in precincts:
        total_dem += dem_by_prec[p]
        total_turn += turnout_by_prec[p]
    dem, turn = total_dem/len(precincts), total_turn/len(precincts)
    zip_to_dem[zip] = dem
    zip_to_turnout[zip] = turn

demos = []
turns = []
pstve = []
for key, val in demos_by_zip.items():
    arr = []
    for v in val:
        if isinstance(v, list):
            arr.extend(v)
        else: arr.append(v)
    demos.append(arr)
    turns.append(zip_to_turnout[key])
    pstve.append(zip_to_dem[key])

demos = np.asarray(demos)
turns = np.asarray(turns)
pstve = np.asarray(pstve)

for var in range(demos.shape[1]):
    
    print(strs[var]+" turnout", end = ": ")
    print(r:=np.corrcoef(demos[:, var], turns)[1][0])
    plt.scatter(demos[:, var], turns)
    m,b = np.polyfit(demos[:, var], turns, 1)
    plt.plot(demos[:, var], m*demos[:, var]+b)
    plt.suptitle(f"The effect of {strs[var]} on turnout".title())
    plt.xlabel(strs[var].title())
    plt.ylabel("Turnout")
    plt.savefig(f"images/img{var}t")
    
    plt.clf()
    print(strs[var]+" positive", end = ": ")
    print(np.corrcoef(demos[:, var], pstve)[1][0])
    plt.scatter(demos[:, var], pstve)
    m,b = np.polyfit(demos[:, var], pstve, 1)
    plt.plot(demos[:, var], m*demos[:, var]+b)
    plt.suptitle(f"The effect of {strs[var]} on voting for Democrats".title())
    plt.xlabel(strs[var].title())
    plt.ylabel("Percent Dem")
    plt.savefig(f"images/img{var}p")
    
    plt.clf()


    

