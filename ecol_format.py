import openpyxl, sys, os

class Excel(object):
    def __init__(self, berm, year):
        self._xls = openpyxl.load_workbook("moederbestand.xlsx")
        dd = 'data_ecologica'
        filename = '{0}_{1}.xlsx'.format(berm, year)
        self._path = os.path.join(dd,filename)
        self.create_rowlist()

    def create_rowlist(self):
        self._codedict = {}
        self._sheet = self._xls.get_sheet_by_name("Plantenstreeplijst")
        for i in range(7,1101):
            code = int(self._sheet["C"+str(i)].value)
            self._codedict[code] = i
        return

    def export_berm(self, bermlist):
        for i in bermlist:
            code = int(i['code'])
            self._sheet['B{0}'.format(self._codedict[code])] = i['TC'].strip('"')
        self._xls.save(self._path)
        return



