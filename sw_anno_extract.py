import xmltodict
import pandas

index = pandas.read_csv("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\sw_index.csv")
index.drop(index.columns[[0]], axis = 1, inplace = True)

def process(i, start, end):
    with open("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\uniprot_sprot.xml", 'r') as file:
        file.seek(start)
        xml = file.read(end-start)
        entry = xmltodict.parse(xml)
        entry = entry["entry"]
        row = []
        row.append(i)
        row.append(entry["name"])
        if(isinstance(entry["protein"]["recommendedName"]["fullName"], str)):
            row.append(entry["protein"]["recommendedName"]["fullName"])
        else:
            row.append(entry["protein"]["recommendedName"]["fullName"]["#text"])
        #check if comments exist
        temp = ""
        if("comment" in entry.keys()):
            #check if there is more than one comment entry
            if(isinstance(entry["comment"], list)):
                for cc in entry["comment"]:
                    if(cc["@type"] == "function"):
                        #the structure here isn't always the same, so try one way and do the other if it fails
                        temp = cc["text"]
                        if(not isinstance(temp,str)):
                            temp = temp["#text"]
            else:
                if(entry["comment"]["@type"] == "function"):
                    temp = entry["comment"]["text"]
        row.append(temp)
        temp = ""
        #check if more than one name exists
        if(isinstance(entry["organism"]["name"], dict)):
            if(entry["organism"]["name"]["@type"] == "scientific"):
                row.append(entry["organism"]["name"]["#text"])
            else:
                row.append("")
                temp = entry["organism"]["name"]["#text"]
        else:
            #we have both scientific and common names available
            for org in entry["organism"]["name"]:
                if(org["@type"] == "scientific"):
                    row.append(org["#text"])
                elif(org["@type"] == "common"):
                    temp = org["#text"]
        row.append(temp)
        temp = []
        if("keyword" in entry.keys()):
            if(isinstance(entry["keyword"], dict)):
                temp = entry["keyword"]["#text"]
            else:
                for kw in entry["keyword"]:
                    temp.append(kw["#text"])
        row.append(temp)
        p = []
        c = []
        f = []
        for dbr in entry["dbReference"]:
            if(dbr["@type"] == "GO"):
                for val in  dbr["property"]:
                    if(val["@type"] == "term"):
                        val = val["@value"].split(":")
                        if(val[0] == "P"):
                            p.append(val[1])
                        elif(val[0] == "C"):
                            c.append(val[1])
                        elif(val[0] == "F"):
                            f.append(val[1])
        row.append(p)
        row.append(c)
        row.append(f)
    return(row)    
        

rows = [process(i, start, end) for i, start, end in zip(index["accession"], index["start"], index["end"])]


sw_gene_info = pandas.DataFrame(rows, columns = ['id', 'Gene Names (primary)', 'Protein names', 'Function', 'Organism (scientific)', 'Organism (common)', 'Keywords', 'Gene Ontology (biological process)', 'Gene Ontology (cellular component)', 'Gene Ontology (molecular function)'])
sw_gene_info.to_csv("C:\\Users\\Arie\\Documents\\MLML_Class_Materials\\Logan_Lab\\Thesis_data\\annotation\\sw_gene_info.csv")


