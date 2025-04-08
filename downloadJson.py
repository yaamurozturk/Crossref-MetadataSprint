# Given a list of doi, fetch the json

import json
import requests
import os
import sys
import re

# Crossref query
# https://github.com/CrossRef/rest-api-doc#resource-components
# https://api.crossref.org/journals/{issn}/works
# https://api.crossref.org/journals/1422-0067/works

#try_url = "https://api.crossref.org/works?query=gun+violence+school&facet=category-name:5&rows=5&filter=has-abstract:true"
root = "https://api.crossref.org/works?"

In_file = "wakefield-citations-test-OpenCitations.csv"
Out_dir = "OutDirOC"
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filename = In_file
    with open(filename, 'r') as file:
        for line in file:
            print("\n ------ "+line.strip()+"\n")
            d = line.strip()
            doi_files = d.split('/')
            #doi_file = Out_dir + "/" + doi_file
            doi_file = Out_dir + "/" + d
            print("\n ------ doi_file: " + doi_file + "--- doi dir:" + str(doi_files) + "\n")
            if (not os.path.isfile(doi_file+".json")):
                doi_dir = Out_dir
                for i in range(0, len(doi_files)-1):
                    doi_dir = doi_dir + "/" + doi_files[i].strip()
                    print("doi_dir:"+str(doi_dir))
                    if not os.path.exists(doi_dir):
                        os.makedirs(doi_dir)
                print(f"file {doi_file} does not exists: quering Crossref")
                req = requests.get("http://api.crossref.org/works/" + d)
                #print("Quering http://api.crossref.org/works/" + d)
                # error of connection
                if req.status_code != 200:
                    print(f"http get went wrong: http://api.crossref.org/works/{d}")
                    print(req.status_code)
                    #break
                else:
                    doi_data = req.json()
                    with open(doi_file+".json", mode='w', encoding='utf-8') as file:
                        json.dump(doi_data, file, indent=4, ensure_ascii=False)  # `indent=4` for pretty formatting
                        print(f"JSON data has been written to {doi_file}")
                    doi_data = doi_data['message']
            else:
                print(f"file {doi_file} exists")

print("All Done")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
