import csv
import io
import json
import tempfile
import codecs
from flask import jsonify, make_response

def convert_sup(file): 
    """Converts Wellable SUP-metadata.csv file to .json in specified format."""

    data=[]
    decoded_stream = codecs.iterdecode(file.stream, 'utf-8-sig')
    stream = io.StringIO("".join(decoded_stream), newline=None)
    csv_input = csv.DictReader(stream)
    for d in csv_input:
        for key in d.keys():
            if d[key] == 'null':
                d[key]=None
            # Recode em dash
            if d[key] and '\u2014' in d[key]:
                d[key]=d[key].replace('\u2014','&mdash;')
            # Recode en dash as em dash
            if d[key] and '\u2013' in d[key]:
                d[key]=d[key].replace('\u2013','&mdash;')
            # Trim whitespace around em dash
            if d[key] and '&mdash;' in d[key]:
                d[key]=d[key].replace(' &mdash; ','&mdash;')
                d[key]=d[key].replace('&mdash; ','&mdash;')
                d[key]=d[key].replace(' &mdash;','&mdash;')
            # Recode left and right double-quotes
            if d[key] and '\u201c':
                d[key]=d[key].replace('\u201c','\"')
            if d[key] and '\u201d':
                d[key]=d[key].replace('\u201d','\"')
            # Replace no-break space with regular space
            if d[key] and '\u00a0' in d[key]:
                d[key]=d[key].replace('\u00a0',' ')
        nulls=['user_fields_0','user_fields_1','email_fields_0','email_fields_1']
        for key in nulls:
            if d[key]=="":
                d[key]=None
        data.append(d)
    data = {'include':data} # Comment this out to get rid of the "include" wrapper

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_json_file:
        json.dump(data, tmp_json_file, indent=4)
        tmp_json_file.flush()

    return tmp_json_file.name