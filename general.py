import regex as re
precinct_code_to_reg = {}
p_file = open("precincts.txt", "r").read().splitlines()
def get_num_from_string(str):
    if "\"" in str:
        return int(str[1:-1].replace(",", ""))
    else: return int(str)

def get_2022_extrap():
    file = open("2022extrap.txt", "r").read().splitlines()
    prec_to_dems = {}
    for ind, line in enumerate(file[13::12]):
        
        l = [int(i.replace(",", "")) for i in line.split("\t")[1:]]
        
        prec_to_dems[ind+1] = l[-1]
    prec_to_rebs = {}
    for ind, line in enumerate(file[15::12]):
        l = [int(i.replace(",", "")) for i in line.split("\t")[1:] if i]
        prec_to_rebs[ind+1] = l[-1]
    perc_abs_by_prec, perc_dem_by_prec, perc_reb_by_prec = {}, {}, {}
    for (prec, val) in prec_to_dems.items():
        perc_dem_by_prec[prec] = val/(val+prec_to_rebs[prec])
        perc_reb_by_prec[prec] = prec_to_rebs[prec]/(val+prec_to_rebs[prec])

    total_AB = [int(i.replace(",", "")) for i in file[3].split("\t")[1:] if i][-1] + [int(i.replace(",", "")) for i in file[5].split("\t")[1:] if i][-1]
    for (prec, val) in prec_to_dems.items():
        perc_abs_by_prec[prec] = (val+prec_to_rebs[prec])/total_AB
    return perc_dem_by_prec, perc_reb_by_prec, perc_abs_by_prec, prec_to_dems, prec_to_rebs
    
    
perc_dem_by_prec, perc_reb_by_prec, perc_abs_by_prec, abs_dem_by_prec, abs_reb_by_prec = get_2022_extrap()




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

# for 2022

for i in range(1, 55):
    precinct_code_to_votes_dem[i][5] += abs_dem_by_prec[i]
    precinct_code_to_votes_rep[i][5] += abs_reb_by_prec[i]


for i in range(5):
    reg_file = open(f"votes/vot{2017+i}.csv", "r").read().splitlines()
    v = 0
    for line in reg_file:
        if "ARLINGTON" in line and "DARLINGTON" not in line:
            if "ABSENTEE" in line.upper():
                for person in dems[i]:
                
                    if person.upper() in line.upper():                    
                        
                        spl = line.split("\",\"")
                        v += int(spl[5])
                        for prec in perc_abs_by_prec.keys():
                            precinct_code_to_votes_dem[prec][i] += int(spl[5])*perc_abs_by_prec[prec] 
                for person in reps[i]:
                
                    if person.upper() in line.upper():                    
                        
                        spl = line.split("\",\"")
                        v += int(spl[5])
    # for prec in perc_abs_by_prec.keys():
    #     precinct_code_to_votes_dem[prec][i] += v*perc_dem_by_prec[prec]*perc_abs_by_prec[prec] 
    #     precinct_code_to_votes_rep[prec][i] += v*perc_reb_by_prec[prec]*perc_abs_by_prec[prec] 
real_turnouts = [0.59, 0.71, 0.37, 0.79, 0.62, 0.56] 
fake_turnouts = [0.56, 0.66, 0.33, 0.68, 0.56, 0.545] 


prec_turnouts = {}        
for yr in range(6):                                           

    vots = 0
    reg_vot = 0
    for p in range(1, 55):
        vots = (precinct_code_to_votes_dem[p][yr]+precinct_code_to_votes_rep[p][yr])
        reg_vot = precinct_code_to_reg[p][yr][0]
        
        
        
        
        if p not in prec_turnouts: prec_turnouts[p] = [(vots/reg_vot)*real_turnouts[yr]/fake_turnouts[yr]]
        else: prec_turnouts[p].append((vots/reg_vot)*real_turnouts[yr]/fake_turnouts[yr])
    #print(vots/reg_vot)





perc_arl_dem = []
for i in range(6):
    d = sum([de[i] for de in precinct_code_to_votes_dem.values()])
    r = sum([de[i] for de in precinct_code_to_votes_rep.values()])
    perc_arl_dem.append(d/(d+r))

# for y in range(6):
#     tot = 0
#     reg_vot = 0
#     for p in precinct_code_to_reg:
#         tot += prec_turnouts[p][y]*precinct_code_to_reg[p][y][0]
#         reg_vot += precinct_code_to_reg[p][y][0]

#     print(tot/reg_vot)
# exit()
        
# import docx
# import matplotlib.pyplot as plt

# for p in range(1, 55):
#     print(p)
#     doc = docx.Document()
#     head = p_file[p]
#     head = head.split(",")
#     doc.add_heading(f"Information Sheet", 0)
#     doc.add_heading(f"Precinct: {head[0]} with code {head[2]}", 2)
#     doc.add_heading("Voting Registration Statistics", 4)
#     doc_para1 = doc.add_paragraph(f"As of November 2022, there are {precinct_code_to_reg[p][5][0]} registered and active voters and  {precinct_code_to_reg[p][5][2]} total voters")
    

   
#     doc_para2 = doc.add_paragraph("Summary of Precinct Data")
#     table = doc.add_table(rows=8, cols=7)
#     table.style = "Table Grid"
#     cells = table.rows[0].cells
#     cells[0].text = "Year:"
#     for i in range(6): cells[i+1].text = str(2017+i)
#     cells = table.rows[1].cells
#     cells[0].text = "Total registered voters"
#     for i in range(6): cells[i+1].text = str( [v[0] for v in precinct_code_to_reg[p]][i])

#     cells = table.rows[2].cells
#     races = ["Governor", "US Senate", "VA Senate", "President", "Governor", "House"]
#     cells[0].text = "Election"    
#     for i in range(6): cells[i+1].text = f"{races[i]}"

#     cells = table.rows[3].cells    
#     cells[0].text = "Candidate"    
#     for i in range(6): cells[i+1].text = f"{str(dems[i][0])}"

    

#     cells = table.rows[4].cells
#     cells[0].text = "Precinct Turnout"
#     for i in range(6): cells[i+1].text = str( int(round(prec_turnouts[p][i], 2)*100))+"%"
#     cells = table.rows[5].cells
#     cells[0].text = "County Turnout"
#     for i in range(6): cells[i+1].text = str( int(real_turnouts[i]*100))+"%"
#     cells = table.rows[6].cells
#     cells[0].text = "Precinct Dem"
#     for i in range(6): cells[i+1].text = str(int(round(precinct_code_to_votes_dem[p][i]/(precinct_code_to_votes_dem[p][i]+precinct_code_to_votes_rep[p][i]), 2)*100))+"%"
#     cells = table.rows[7].cells
#     cells[0].text = "County Dem"
#     for i in range(6): cells[i+1].text = str(int(round(perc_arl_dem[i], 2)*100))+"%"
#     plt.plot([2017, 2018, 2019, 2020, 2021, 2022], [v[0] for v in precinct_code_to_reg[p]])
#     plt.title("Voter Registration over Time in Your Precinct")
#     plt.xticks([2017, 2018, 2019, 2020, 2021, 2022])
#     plt.xlabel("Year")
#     plt.ylabel("Number of voters registered")
#     plt.ylim([0, max([v[0] for v in precinct_code_to_reg[p]])+1000])
#     plt.savefig("temp.png")
#     doc.add_page_break()
#     doc.add_picture("temp.png", height =docx.shared.Inches(4))
#     plt.clf()
#     plt.plot([2017, 2018, 2019, 2020, 2021, 2022], [prec_turnouts[p][i]*100 for i in range(6)], label = "Precinct Turnout")
#     plt.plot([2017, 2018, 2019, 2020, 2021, 2022], [real_turnouts[i]*100 for i in range(6)], label = "County Turnout")
#     plt.plot([2017, 2018, 2019, 2020, 2021, 2022], [precinct_code_to_votes_dem[p][i]/(precinct_code_to_votes_dem[p][i]+precinct_code_to_votes_rep[p][i])*100 for i in range(6)], label = "Precinct Dem")
#     plt.plot([2017, 2018, 2019, 2020, 2021, 2022], [perc_arl_dem[i]*100 for i in range(6)], label = "County Dem")

#     plt.title("Voting over Time in Your Precinct")
#     plt.xticks([2017, 2018, 2019, 2020, 2021, 2022])
#     plt.xlabel("Year")
#     plt.ylabel("Percent")
#     plt.ylim([0,100])
#     leg = plt.legend(loc = "upper right")

#     plt.savefig("temp.png")
#     doc.add_picture("temp.png", height = docx.shared.Inches(4))
#     plt.clf()
#     doc.save(f"docs/p{p}.docx")
import sys
all_file = open("all.csv", "w")
sys.stdout = all_file
races = ["Governor", "US Senate", "VA Senate", "President", "Governor", "House"]
print("PRECINCT,YEAR,RACE,PRECINCT_TURNOUT,PRECINCT_DEM,ALL_TURNOUT,ALL_DEM")
for p in range(1,55):
    for y in range(6):
        print(f"{p},{y+2017},{races[y]},{prec_turnouts[p][y]},{precinct_code_to_votes_dem[p][y]/(precinct_code_to_votes_dem[p][y]+precinct_code_to_votes_rep[p][y])},{real_turnouts[y]},{perc_arl_dem[y]}")
    









# for p in range(1, 55):
#     print(f"Precinct: {p}")
#     for yr in range(6):
#         print(f"Year: {yr}: {(precinct_code_to_votes_dem[p][yr]+precinct_code_to_votes_rep[p][yr])/precinct_code_to_reg[p][yr][0]}")


    