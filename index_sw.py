import pandas

genes = pandas.read_csv("C:\\Users\\Arie\\Desktop\\sw_genes.csv")

ids = " ".join(genes['x']).split(" ")
index = 0
for id in ids:
  ids[index] = id.split('.')[0]
  index+=1

#ids = ["P0C9F0"]

print("ids loaded")

rows = []

with open("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\uniprot_sprot.xml") as file:
#with open("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\test.xml") as file:
    j = 0
    print("starting to process file")
    while line := file.readline():
        if("<entry" in line):
            start = file.tell()-len(line)-1
            #counter to keep track of how many newlines there are. We need to subtract these from the end counter because they count as two bytes in the file but are only read in as one
            i = 1
            line = file.readline()
            i+=1
            acc = line.replace("<accession>", "").replace("</accession>", "").strip()
            if(acc in ids):
                #counter of how many entries we've processed
                j += 1
                entry = True
                while entry == True:
                    e = file.readline()
                    i += 1
                    if("</entry>" in e):
                        end = file.tell()
#                        end = file.tell()-i
                        row = [acc, start, end]
                        rows.append(row)
                        entry = False
                        if(j%1000 == 0):
                            print("processed " + str(j) + " entries (" + str(j/len(ids)*100) + "%)")
print("finished!")

#with open("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\uniprot_sprot.xml") as file:
#with open("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\test.xml") as file:
#  start = rows[0][1]
#  print(start)
#  print(type(start))
#  file.seek(start)
#  print(file.read(rows[0][2]-rows[0][1]))

index = pandas.DataFrame(rows, columns = ['accession', 'start', 'end'])
index.to_csv("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\sw_index.csv")
