import numpy as np
import sys

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

if __name__ == "__main__":
    fileroot = 'data/inputlog/'
    filenames = ['cpuNetVLAD-4-stdout.log','cpuVO-5-stdout.log','dpuNetVLAD-2-stdout.log','dpuVO-3-stdout.log']
    filelines = [0,1,2,2]
    actions = ['cpuNetVLAD','cpuVO','dpuNetVLAD','dpuVO']
    colors = ['"#7b9ce1"','"#bd6d6c"','"#75d874"','"#dc77dc"']
    outputfile = 'data/outputdata/outputlog_test.json'
    main(fileroot,filenames,filelines,actions,colors,outputfile)