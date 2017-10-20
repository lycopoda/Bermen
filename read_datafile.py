#Reads waarneming.nl/observations.net export files.
#Creates datadict with species name (in floron code),
#date, bermname and Tansley code
import sys

class Import_Data(object):
    def __init__(self):
        self.get_codedict(filename='obsmap_floron_tabel.txt')
        self.import_scale('tansley.txt')
        self._indexlist = [('code',5),
                           ('datum', 9),
                           ('X', 21),
                           ('Y', 22),
                           ('TC', 41)]
    @property
    def indexlist(self):
        return self._indexlist

    def scale(self, symbol):
        return self._scale[symbol]
        
    def import_file(self, filepath):
        filelist = []
        with open(filepath, 'r', encoding='utf-16') as data:
            next(data)
            for line in data:
                info = line.strip().split('\t')
                item = {}
                try:
                    for name, i in self._indexlist:
                        item[name] = info[i]
                    item['code'] = self.get_floron_code(item['code'])
                    filelist.append(item)
                except IndexError:
                    pass
        return filelist 

    def get_floron_code(self, obs_code):
        try:
            return self._codedict[obs_code]
        except KeyError:
            print('{0} niet in obs_floron tabel'.format(obs_code))
            sys.exit(2)
    
    def get_codedict(self, filename):
        self._codedict = {}
        with open(filename, 'r') as table:
            next(table)
            for line in table:
                info = line.strip().split('\t')
                try:
                    self._codedict[info[0]] = info[1]
                except IndexError:
                    print('fout in {0}'.format(filename))
                    sys.exit(2)
        return

    def import_scale(self, filename):
        self._scale={}
        with open(filename, 'r') as cf:
            next(cf)
            for line in cf:
                code, number = line.strip().split('\t')
                self._scale[code] = int(number)
        return
