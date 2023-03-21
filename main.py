import regex as re
precinct_code_to_reg = {}
p_file = open("precincts.txt", "r").read().splitlines()
def get_num_from_string(str):
    if "\"" in str:
        return int(str[1:-1].replace(",", ""))
    else: return int(str)

for l in p_file[1:]:
    lg = l.split(",")
    precinct_code_to_reg[int(lg[2])] = []

for i in range(6):

    reg_file = open(f"registrated/regvot{2017+i}.csv", "r").read().splitlines()
    
    hit = False
    for line in reg_file[1:]:
        
        
        if "ARLINGTON" in line and "DARLINGTON" not in line:
            g = re.findall(r",(\d+|\"\d+,\d+\")(?=,)", line)
            active, inactive, total = get_num_from_string(g[1]), get_num_from_string(g[2]), get_num_from_string(g[3])            
            precinct_code_to_reg[int(g[0])%100].append((active, inactive, total))

precinct_code_to_votes_dem = {}
precinct_code_to_votes_rep = {}
for l in p_file[1:]:
    lg = l.split(",")
    precinct_code_to_votes_dem[int(lg[2])] = [0]*6
for l in p_file[1:]:
    lg = l.split(",")
    precinct_code_to_votes_rep[int(lg[2])] = [0]*6




people_file = open("people.txt", "r").read().splitlines()
dems = list()
reps = list()
for line in people_file[:6]:
    dems.append(line.split(", "))
for line in people_file[7:]:
    reps.append(line.split(", "))


print(dems, reps)


for i in range(6):

    reg_file = open(f"votes/vot{2017+i}.csv", "r").read().splitlines()
    
    hit = False
    for line in reg_file[1:]:
        
        
        if "ARLINGTON" in line and "DARLINGTON" not in line:
            if "ABSENTEE" in line.upper() or "PROVISIONAL" in line.upper(): continue
            for person in dems[i]:
                
                if person.upper() in line.upper():
                    
                    
                    spl = line.split("\",\"")
                    v, prec = int(spl[5]), int(spl[12][:3])
                    precinct_code_to_votes_dem[prec%100][i] += v
                    
            for person in reps[i]:
                
                if person.upper() in line.upper():
                    
                    
                    spl = line.split("\",\"")
                    v, prec = int(spl[5]), int(spl[12][:3])                   
                    
                    precinct_code_to_votes_rep[prec%100][i] += v
    
for p in range(1, 55):
    print(f"Precinct: {p}")
    for yr in range(6):
        print(f"Year: {yr}: {(precinct_code_to_votes_dem[p][yr]+precinct_code_to_votes_rep[p][yr])/precinct_code_to_reg[p][yr][0]}")


    