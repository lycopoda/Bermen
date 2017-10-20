import os, sys
import read_datafile as rd

def import_coordinates():
    bermdict = {}
    with open('2017.txt', 'r') as coord:
        next(coord)
        for line in coord:
            berm, x, y = line.strip().split('\t')[:3]
            bermdict[berm] = (float(x)/1000.,float(y)/1000.)
    return bermdict

def check_berm(X,Y,gpsdict):
    for berm in gpsdict:
        if abs(X-gpsdict[berm][0])<0.1:
            return berm
    return 'buiten range'


def savedata(bermdict, indexlist):
    header = ''
    directory = 'data_berm'
    for i in indexlist:
        header += '{0}\t'.format(i[0])
    header += '\n'
    for berm in bermdict:
        filename = os.path.join(directory,'{0}.txt'.format(berm))
        with open(filename, 'w') as f:
            f.write(header)
            for i in bermdict[berm]:
                f.write(bermline(i, indexlist))
    return

def bermline(obs,indexlist):
    line = ''
    for item in indexlist:
        try:
            value = obs[item[0]]
        except KeyError:
            value = ''
        line +='{0}\t'.format(value)
    line += '\n'
    return line

def gettopscores(bermdict, obs):
    topscoredict = {}
    for berm, bl in bermdict.items():
        topscoredict[berm] = {}
        for i in bl:
            if i['code'] not in topscoredict[berm] or \
                    obs.scale(topscoredict[berm][i['code']]) < \
                    obs.scale(i['TC']):
                topscoredict[i['code']] = i
    return bermdict
			    
def save_ecol(bermdict):
    #create Excel object
    #for each berm, save data
    import ecol_format
    for berm in bermdict:
        xls = ecol_format.Excel(berm, 2017)
        xls.export_berm(bermdict[berm])
    return

def import_data(obs):
    obs_list = []
    dd = 'data_obs'
    for datafile in [os.path.join(dd, f) for f in os.listdir(dd) if \
            os.path.isfile(os.path.join(dd, f))]:
        print('read {0}'.format(datafile))
        obs_list.extend(obs.import_file(datafile))
    return obs_list


def main():
    obs = rd.Import_Data()
    obs_list = import_data(obs)
    gpsdict = import_coordinates()
    bermdict = {}
    for berm in gpsdict:
        bermdict[berm]=[]
    for item in obs_list:
        x,y = [float(item[key].strip('"').replace(',','.')) \
                for key in ['X','Y']]
        berm=check_berm(x,y,gpsdict)
        bermdict[berm].append(item)
    savedata(bermdict, obs.indexlist)
    save_ecol(gettopscores(bermdict, obs))
 #   export_to_ecologica(topscoredict)
    #order data and save data
    #select highest scores and save data
    #Calculate Ellenberg scores
    return 0

if __name__=='__main__':
    status = main()
    sys.exit(status)
