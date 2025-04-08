# Given a list of doi, fetch the json

import json
import requests
import os
import sys
import re

if __name__ == '__main__':
    #rootdir = "JsonSet"
    rootdir = "Test"
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            print(os.path.join(subdir, file))

print("All Done")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
