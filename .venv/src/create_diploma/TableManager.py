import openpyxl # .xlsx,.xlsm,.xltx,.xltm - поддерживаемые форматы
# этот класс должен уметь читать таблицу и создавать новый документ на кадой итерации

class TableManager():

    def __init__(self, user_name, project_name, format='.xlsx') -> None:
        self.user_name = user_name
        self.project_name = project_name
        self.format = format

    def print_excel_rows(self):
        path = f'.venv\\user_folders\\{self.user_name}\\{self.project_name}_table{self.format}'
        
        workbook = openpyxl.load_workbook(filename=path)

        # Получаем активный лист
        sheet = workbook.active
        
        # Проходим по каждой строке в листе
        for row in sheet.iter_rows(values_only=True):
            # Выводим значения каждой ячейки в строке
            print(row)

tableManager = TableManager("ss", "first")
tableManager.print_excel_rows()