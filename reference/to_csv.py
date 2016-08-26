import xlrd
import csv


def Excel2CSV(ExcelFile='SicCodesAllLevels.xls',
              SheetName='SIC4', CSVFile='ref_list.csv'):
    workbook = xlrd.open_workbook(ExcelFile)
    worksheet = workbook.sheet_by_name(SheetName)
    csvfile = open(CSVFile, 'wb')
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

    for rownum in xrange(worksheet.nrows):
        wr.writerow(
            list(x.encode('utf-8')
                 for x in worksheet.row_values(rownum)))

    csvfile.close()

Excel2CSV()
