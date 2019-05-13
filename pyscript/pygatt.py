import numpy as np
import json 
import sys
import pdb

def get_times(filein, actionname, id, colorname):
    time_stamps = []
    minstart = float("inf")
    with open(filein) as file:
        for line in file.readlines(): 
            line_sp = line.split()
            if len(line_sp) > 10 and "starting" == line_sp[6] and "finishing" == line_sp[9]:
                starttime = float( ''.join(list(filter(lambda ch: ch in '0123456789.', line_sp[8]) ) ) )                 
                endtime =  float( ''.join(list(filter(lambda ch: ch in '0123456789.', line_sp[11]) ) ) )
                assert(starttime < endtime) 
                if (minstart > starttime):
                    minstart = starttime
                stamp = {"action" : actionname , "id": id , "start": starttime, "end": endtime , "duration": (endtime - starttime), "color":colorname }
                time_stamps.append(stamp)
                # tmp = 1
    return time_stamps, minstart

def print_outinfo(outputinfo,minstart=0,file=sys.stdout):
    print('[',file=file)
    length = len(outputinfo)
    for index  in range(length):
        info = outputinfo[index]
        info['start'] -= minstart
        info['end'] -= minstart
        if index < length-1:
            print( '{{ "name" : "{action}", "value" : [{id}, {start}, {end}, {duration} ], "itemStyle":{{"normal": {{"color": {color} }} }}  }}, '.format(**info ), file=file )
        else :
            print( '{{ "name" : "{action}", "value" : [{id}, {start}, {end}, {duration} ], "itemStyle":{{"normal": {{"color": {color} }} }}  }}'.format(**info ), file=file )
    print(']',file=file)


def overlaped(query, match):
    # print(query)
    # print(match)
    if query['start'] < match['start'] and query['end'] > match['start']:
        return True
    if query['start'] >= match['start'] and query['start'] <= match['end']:
        return True
    return False
        

def valid_json(jsonData, line_num = 3, nonoverlap_id=[2]):
    items = json.loads(jsonData)
    # pdb.set_trace()
    time_lines = []
    for index in range(line_num):
        time_lines.append([])
    for item in items:
        item_id = item["value"][0]
        if item_id in nonoverlap_id:
            for time_item in time_lines[item_id]:
                item_query = {'start': item["value"][1], 'end' : item["value"][2] }
                item_match =  {'start': time_item["value"][1],  'end' : time_item["value"][2] }
                try:
                    assert(not overlaped(item_query, item_match) )
                except:
                    print('Error: time_line_overlaped: item_query = {item_query}; item_match= {item_match}'.format(item_query=item_query,item_match=item_match) )
                    exit(0)
        time_lines[item_id].append(item)
        


def main(fileroot,filenames,filelines,actions,colors,outputfile = 'data/outputdata/outputlog_test.json'):
    outputinfo = []
    minstart = float('inf')
    for index in range(len(filenames)):
        filename = filenames[index]
        filein = fileroot + '/' + filename
        tmpout,tmpmin = get_times(filein,actions[index],filelines[index],colors[index])
        outputinfo += tmpout
        if minstart > tmpmin:
            minstart = tmpmin
    tmp = 1
    with open(outputfile,'w') as outfile:
        print_outinfo(outputinfo ,minstart , outfile)
    with open(outputfile,'r') as jsonfile:
        jsonstr = ''
        for line in jsonfile.readlines():
            jsonstr += line.strip()    
        valid_json(jsonstr)

if __name__ == "__main__":
    fileroot = 'data/inputlog/'
    filenames = ['cpuNetVLAD-4-stdout.log','cpuVO-5-stdout.log','dpuNetVLAD-2-stdout.log','dpuVO-3-stdout.log']
    filelines = [0,1,2,2]
    actions = ['cpuNetVLAD','cpuVO','dpuNetVLAD','dpuVO']
    colors = ['"#7b9ce1"','"#bd6d6c"','"#75d874"','"#dc77dc"']
    outputfile = 'data/outputdata/outputlog_test.json'
    main(fileroot,filenames,filelines,actions,colors,outputfile)
