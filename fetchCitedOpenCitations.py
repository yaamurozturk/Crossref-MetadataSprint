# Given a list of doi, query open citations to get the list of cited.

import json
import os
import csv
import requests

if __name__ == '__main__':
    fileOC = "OpenCitationsLevel1.csv"
    first = True
    with open("outputOpenCitationsLevel2.csv", "w", newline="", encoding="utf-8") as csvfileOut:
        with open(fileOC, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                seedPaper = row['cited doi']
                if int(row['is-referenced-by-count']) > 0:
                    #https://opencitations.net/index/api/v1/citations/10.1016/s0140-6736(97)11096-0?format=csv
                    #print(row['citing doi'], row['is-referenced-by-count'])
                    d=row['citing doi']
                    req = requests.get("https://opencitations.net/index/api/v1/citations/" + d + "?format=csv")
                    if req.status_code != 200:
                        print(f"http get went wrong:https://opencitations.net/index/api/v1/citations/{d}?format=csv")
                        print(req.status_code)
                        break
                    else:
                        decoded_content = req.content.decode('utf-8')
                        cr = csv.DictReader(decoded_content.splitlines(), delimiter=',')
                        #next(cr)
                        for rowb in cr:
                            if rowb['citing']:
                                print(f"{rowb['citing']}, {rowb['cited']}, {seedPaper}")
                                rowout = {
                                    "layer2": rowb['citing'],
                                    "layer1": rowb['cited'],
                                    "seed": seedPaper,
                                }
                                writer = csv.DictWriter(csvfileOut, fieldnames=rowout.keys())
                                if first:
                                    writer.writeheader()
                                    writer.writerow(rowout)
                                    first = False
                                else:
                                    writer.writerow(rowout)
                            else:
                                print("---------------------")

print("All Done")
