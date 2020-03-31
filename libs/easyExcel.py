from win32com.client import Dispatch
import win32com.client


class winExcel:
    def __init__(self, filepath):
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        try:
            self.Excel = self.xlApp.Workbooks.Open(filepath)
        except:
            raise Exception("文件打开失败")

    def save(self):
        self.Excel.Save()

    def close(self):
        self.Excel.Close(SaveChanges=0)
        self.xlApp.Quit()

    def getSheet(self, sheet):
        return self.Excel.Worksheets(sheet)

    def getCell(self, sheet, row, col):  # 获取单元格的数据
        "Get value of one cell"
        return self.getSheet(sheet).Cells(row, col)

    def getRow(self, sheet, row):
        return self.getSheet(sheet).Rows(row)

    def getCol(self, sheet, col):
        return self.getSheet(sheet).Columns(col)

    def getRange(self, sheet, row1, col1, row2, col2):
        '''get the range object'''
        sht = self.getSheet(sheet)
        return sht.Range(self.getCell(sheet, row1, col1), self.getCell(sheet, row2, col2))

    def getCellValue(self, sheet, row, col):
        assert row > 0 and col > 0
        return self.getCell(sheet, row, col).Value

    def getRowValue(self, sheet, row):
        '''get the row values'''
        return self.getRow(sheet, row).Value

    def getColValue(self, sheet, col):
        '''get the row values'''
        return self.getCol(sheet, col).Value

    def getRangeValue(self, sheet, row1, col1, row2, col2):
        '''return a tuples of tuple)'''
        return self.getRange(sheet, row1, col1, row2, col2).Value

    def getMaxRow(self, sheet):
        '''get the max row number, not the count of used row number'''
        return self.getSheet(sheet).Rows.Count

    def getMaxCol(self, sheet):
        '''get the max col number, not the count of used col number'''
        return self.getSheet(sheet).Columns.Count

    def getUsedRow(self, sheet):
        return self.getSheet(sheet).UsedRange.Rows.Count

    def getUsedCol(self, sheet):
        return self.getSheet(sheet).UsedRange.Columns.Count

    def setCellValue(self, sheet, row, col, value):  # 设置单元格的数据
        "set value of one cell"
        self.getCell(sheet, row, col).Value = value

    def setRowValue(self, sheet, row, values):
        '''set the row values'''
        self.getRow(sheet, row).Value = values

    def setColValue(self, sheet, col, values):
        '''set the row values'''
        self.getCol(sheet, col).Value = values

    def setRangeValue(self, sheet, row1, col1, data):
        '''set the range values'''
        row2 = row1 + len(data) - 1
        col2 = col1 + len(data[0]) - 1
        range = self.getRange(sheet, row1, col1, row2, col2)
        range.Clear()
        range.Value = data

    def clearCell(self, sheet, row, col):
        '''clear the content of the cell'''
        self.getCell(sheet, row, col).Clear()

    def deleteCell(self, sheet, row, col):
        '''delete the cell'''
        self.getCell(sheet, row, col).Delete()

    def clearRow(self, sheet, row):
        '''clear the content of the row'''
        self.getRow(sheet, row).Clear()

    def deleteRow(self, sheet, row):
        '''delete the row'''
        self.getRow(sheet, row).Delete()

    def clearCol(self, sheet, col):
        '''clear the col'''
        self.getCol(sheet, col).Clear()

    def deleteCol(self, sheet, col):
        '''delete the col'''
        self.getCol(sheet, col).Delete()

    def clearSheet(self, sheet):
        '''clear the hole sheet'''
        self.getSheet(sheet).Clear()

    def deleteSheet(self, sheet):
        '''delete the hole sheet'''
        self.getSheet(sheet).Delete()

    def deleteRows(self, sheet, fromRow, count=1):
        '''delete count rows of the sheet'''
        maxRow = self.getMaxRow(sheet)
        maxCol = self.getMaxCol(sheet)
        endRow = fromRow + count - 1
        if fromRow > maxRow or endRow < 1:
            return
        self.getRange(sheet, fromRow, 1, endRow, maxCol).Delete()

    def deleteCols(self, sheet, fromCol, count=1):
        '''delete count cols of the sheet'''
        maxRow = self.getMaxRow(sheet)
        maxCol = self.getMaxCol(sheet)
        endCol = fromCol + count - 1
        if fromCol > maxCol or endCol < 1:
            return
        self.getRange(sheet, 1, fromCol, maxRow, endCol).Delete()


if __name__ == '__main__':
    from libs.caluTimer import caluCodeTime

    timecount = caluCodeTime()
    path = r'D:\software\common\WPS Office\11.3.0.8632\office6\mui\default\resource\xlsx\Kingsoft_Et_Area.xlsx'
    sheet = 'Sheet1'
    excel = winExcel(path)
    a = excel.getColValue(sheet, 2)
    print(excel.getUsedCol(sheet))
    print(excel.getUsedRow(sheet))

    list1 = []
    # for value in a:
    #     if value[0] != None:
    #         list1.append(value[0])
    for Row in range(1, excel.getUsedRow(sheet)):
        list1.append(excel.getCellValue(sheet, Row, 2))
    # print(excel.getCellValue(sheet, 1, 2))
    excel.close()
    timecount.end()
    print(list1)
