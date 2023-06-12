
import pathlib


import json
from pydantic import BaseModel, error_wrappers


from . import schemas
    

import csv
import os
import chardet
import pathlib
from .models import Data
from .extractors import generate_unique_id,generate_unique_url
# set the directory path for the input and output files

BASE_DIR = pathlib.Path(__file__).resolve().parent
directory = BASE_DIR / "files"
output = BASE_DIR / "output"
print(output)

def valid_schema_data_or_error(raw_data: dict, SchemaModel:BaseModel):
    data = {}
    errors = []
    error_str = None
    try:
        cleaned_data = SchemaModel(**raw_data)
        data = cleaned_data.dict()
    except error_wrappers.ValidationError as e:
        error_str = e.json()
    if error_str is not None:
        try:
            errors = json.loads(error_str)
        except Exception as e:
            errors = [{"loc": "non_field_error", "msg": "Unknown error"}]
    return data, errors

def run_add_data(directory, output, user_id):


    # iterate over each subdirectory and file in the directory tree
    for root, dirs, files in os.walk(directory):
        print(dirs)
        print(root)
        # iterate over each file in the directory
        for filename in files:
            print(filename)

            # check if the file is a text file
            if filename.endswith(".txt"):

                # create the input and output file paths
                input_path = os.path.join(root, filename)
                print(input_path)
                output_filename = "output" + filename[:-4] + ".csv"
                output_path = os.path.join(output, output_filename)

                if os.path.getsize(input_path) == 0:
                    print(f'{filename}is empty , skipping .....')
                    continue

                # open the input and output files
                with open(input_path, "r", encoding="ISO-8859-1") as input_file, open(output_path, "w", newline='') as output_file:

                    # create a CSV writer object
                    csv_writer = csv.writer(
                        output_file, delimiter=',', quoting=csv.QUOTE_ALL, escapechar='\\')

                    # iterate over each line in the input file
                    for line in input_file:

                        # split the line by colon if it exists
                        split_line = line.strip().split(":")
                        if(len(split_line)<2):
                            continue

                        # write the split line to the CSV file as separate columns
                        csv_writer.writerow(split_line)

                        # print the number of elements in the row
                        print(
                            f"Number of elements in {filename}: {len(split_line)}")
                        file_name = filename.strip().split(".")
                        source_name=file_name[0]
                        elem=len(split_line)
                       
                        old_raw_data={
                            "email": 'None',
                            "password": 'None',
                            "firstname": 'None',
                            "lastname": 'None',
                            "address": 'None',
                            "ip": 'None',
                            "hashpassword": 'None',
                            "dateofbirth":'None',
                            "gender":'None',
                            "username":'None',
                            "country":'None',

                        }
                        i=elem
                        # raw_data = { split_line[i]:value for i,value in enumerate(old_raw_data.keys())}
                        # raw_data = {v: k for k, v in raw_data.items()}
                        for i, key in enumerate(old_raw_data.keys()):
                            if i < len(split_line):
                                value = split_line[i]
                                old_raw_data[key] = value 
                        raw_data = old_raw_data


                        raw_data['user_id']=user_id
                        raw_data['source_name']=source_name
                        raw_data['title']=generate_unique_id(split_line[0])
                        raw_data['url']=generate_unique_id(split_line[0])
                        # raw_data['hashpassword']="None"
                        # raw_data['firstname']="None"
                        # raw_data['lastname']="None"
                        # raw_data['address']="None"
                        # raw_data['ip']="None"
                        # raw_data['dateofbirth']="None"
                        # raw_data['gender']="None"
                        # raw_data['username']="None"
                        



                        
                        

                        try:
                            # q = Data.objects.allow_filtering().filter(item_id=item_id)
                            # print(q)
                            # if q.count() != 0:
                            #     continue
                            data, errors = valid_schema_data_or_error(raw_data, schemas.DataCreateSchema)
                            print(data)
                            redirect_path = data.get('path') or "/data/create"
                            print(errors)
                            print(data.get('path'))
                            
                        except:
                            continue
                            return print("error when move data to database")
    return print('Finsh')
                        
                        


    
