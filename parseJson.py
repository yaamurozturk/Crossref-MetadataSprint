# Given a list of doi, fetch the json

import json
import os
import csv

if __name__ == '__main__':
    #rootdir = "JsonSet"
    rootdir = "JsonSetOpenCitations"
    #rootdir = "Test"
    first=True
    with open("outputOpenCitations.csv", "w", newline="", encoding="utf-8") as csvfile:
        for subdir, dirs, files in os.walk(rootdir):
             for file in files:
                #print(f" T------------------ {subdir}/{file}")
                if file.endswith(".json"):
                    print(f" ------------------ {subdir}/{file}")
                    path_file = os.path.join(subdir, file)
                    with open(path_file, mode='r', encoding='utf-8') as jsonFile:
                        doi_data = json.load(jsonFile)
                        doi_data = doi_data['message']
                    print(f" Looking at: '{os.path.join(subdir, file)}'")
                    print(f" doi: '{doi_data['DOI']}'")

                    # necessary fields
                    is_referenced_by_count = doi_data.get("is-referenced-by-count", "")
                    created_date_parts = doi_data.get("created", {}).get("date-parts", [[]])[0]
                    publication_date = "-".join(map(str, created_date_parts)) if created_date_parts else ""

                   # links if text is available
                    link_urls = [entry.get("URL") for entry in doi_data.get("link", []) if "URL" in entry]

                    # labels from updates, corrections or retractions
                    updated_by_labels = [
                        entry.get("label") for entry in doi_data.get("updated-by", []) if "label" in entry
                    ]

                    row = {
                        "citing doi": doi_data['DOI'],
                        "is-referenced-by-count": is_referenced_by_count,
                        "publication date": publication_date,
                        "link": json.dumps(link_urls),
                        "updated-by": json.dumps(updated_by_labels) if updated_by_labels else ""
                    }

                    writer = csv.DictWriter(csvfile, fieldnames=row.keys())
                    if first:
                        writer.writeheader()
                        first=False
                    else:
                        writer.writerow(row)
                    print(" ------------------ ")
print("All Done")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
