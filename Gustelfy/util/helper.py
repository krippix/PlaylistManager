# external
# python native
import logging
import json
import pathlib
# project

def json_to_dict(file) -> dict:
    '''Returns the given file as dictionary'''
    with open(file) as json_file:
        data = json.load(json_file)
    return data