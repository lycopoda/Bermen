from xlrd import open_workbook
import sys, os
import numpy as np
import matplotlib.pyplot as plt

def tansley(table='tansley.csv'):
    tansley_dict = {}
    with open(table,'r') as spreadsheet:
        for line in spreadsheet:
            code, score = line.strip().split(';')
            tansley_dict[code] = score
    return tansley_dict

class Ellenberg(object):
    def __init__(self, table='ellenbergtabel.csv'):
        self.gettable(table)

    def gettable(self, table):
        self._ellenberg_dict = {}
        with open(table, 'r') as spreadsheet:
            header = spreadsheet.readline().strip().split(',')
            self._itemlist = header[1:]
            for line in spreadsheet:
                info = line.strip().split(',')
                name = info[0].lower()
                self._ellenberg_dict[name] = {}
                for i in range(1,len(header)):
                    try:
                        score = float(info[i])
                    except:
                        score = None
                    if score:
                        self._ellenberg_dict[name][header[i]] = score
        return 

    @property
    def itemlist(self):
        return self._itemlist

    def values(self, name):
        if name in self._ellenberg_dict:
            return self._ellenberg_dict[name]
        else:
            return None

class Survey(object):
    def __init__(self, file_name, tansley_dict):
        self._file = file_name
        self._tansley = tansley_dict
        self._species_dict = {}
        self.extract_data()
        return

    def extract_data(self):
        survey = open_workbook(self._file).sheet_by_index(0)
        col_tot = 6
        row_tot = survey.nrows
        for n in range(3,row_tot):
            name = survey.cell(n,0).value
            code  =  survey.cell(n,5).value
            self.add_data(name, code)

    def add_data(self, name, code):
        try:
            name = name.lower()
        except:
            return
        if name == 42:
            return
        try:
            score = self._tansley[code]
        except KeyError:
            return
        if name in self._species_dict:
            if score > self._species_dict[name]:
                self._species_dict[name] = score
        else:
            self._species_dict[name] = score
        return

    @property
    def survey_dict(self):
        return self._species_dict

def calc_eb(eb, score_dict):
#calc relative, abs ellenbergscores and histograms
    eb_abs = {}
    eb_rel = {}
    hist_abs = {}
    hist_rel = {}
    for item in eb.itemlist:
        eb_abs[item] = 0.
        eb_rel[item] = [0.,0.] 
        hist_abs[item] = np.zeros(9)
        hist_rel[item] = np.zeros(9)
    score_count = 0
    for name in score_dict:
        score = int(score_dict[name])
        eb_dict = eb.values(name)
        if eb_dict:
            for item in eb.itemlist:
                eb_abs[item] = []
                value = eb_dict[item]
                idx = int(value)
                if idx>8:
                    idx = 8
                if idx < 0:
                    idx = 0
                hist_abs[item][idx] += 1
                hist_rel[item][idx] += score
                if item in eb_dict:
                    eb_abs[item].append(value)
                    eb_rel[item][0] += value*score
                    eb_rel[item][1] += score
    eb_score = {}
    for item in eb.itemlist:
        eb_score[item] = (sum(eb_abs[item]) / len(eb_abs[item]),
                          eb_rel[item][0] / eb_rel[item][1])
    return eb_score, hist_abs, hist_rel


def histogram(data_dict, filename, score='rel'):
    name = os.path.basename(filename).split('.')[:-1]
    for item in data_dict:
        plot_name = os.path.join('histograms','{0}_{1}_{2}.png'.format(\
                             item, score, name))
        index = np.arange(9)
        plt.bar(index, data_dict[item])
        plt.title(name)
        plt.xlabel('Ellenberg score')
        plt.ylabel('{0}. score {1}'.format(score, item))
        plt.savefig(plot_name)
        plt.close()

def analyse(file_list):
    eb = Ellenberg()
    tansley_dict = tansley()
    survey_dict = {}
    for file_name in file_list:
        survey = Survey(file_name, tansley_dict)
        survey_dict[file_name] = survey.survey_dict
    for site in survey_dict:
        print(os.path.basename(site))
        el_score, hist_abs, hist_rel = calc_eb(eb, survey_dict[site])
        for item in el_score:
            absolute, weighed = el_score[item]
            print('{0}: , abs: {1}, gewogen; {2}'.format(item, absolute,
            weighed))
            histogram(hist_abs, site, score='abs')
            histogram(hist_rel, site, score='rel')
    return

def main(project='surveys'):
    file_list = []
    for file_name in os.listdir(project):
        if file_name.endswith('.xls'):
            file_list.append(os.path.join(project,file_name))
    analyse(file_list)
    return

if __name__=='__main__':
    status = main()
    sys.exit(status)
