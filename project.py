import os
import json


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path='C:\SWSetup\PythonProjectForUniversity\Analizator\price_catalog'):
        # Сканируем папку по указанному адресу
        dirs = os.scandir(file_path)
        data_price = []
        # Найденные файлы сортируем по имени и собираем в список файлов
        for dir in dirs:
            if dir.name[:5] == 'price':
                data_price.append(dir)
        data1 = []
        # открываем файлы и данные из них переписываем в один общий список
        for i in data_price:
            with open(i, 'r') as file:
                data1.append(file.readlines())

        def data_open(data):
            # вспомогательный метод.
            # для каждого файла определяем номера столбцов из которых данные нужны для дальнейшей работы
            data_pr = []
            a, b, c = 0, 0, 0
            for i in data:
                d = i[0].split(',')
                for j in d:
                    if j.lower() == 'название' or j.lower() == 'продукт' or j.lower() == 'наименование' or j.lower() == 'товар':
                        a = d.index(j)
                    elif j.lower() == 'цена' or j.lower() == 'розница':
                        b = d.index(j)
                    elif j.lower() == 'вес' or j.lower() == 'масса' or j.lower() == 'фасовка':
                        c = d.index(j)
                    elif j.lower() == 'вес\n' or j.lower() == 'масса\n' or j.lower() == 'фасовка\n':
                        c = d.index(j)
                data_pr.append([a, b, c])
                # получили список списков номеров нужных столбцов в каждом файле
            return data_pr

        def data_prom(data):
            data_itog = []
            # применим вспомогательный метод: k - список списков с номерами столбцов
            k = data_open(data)
            for i in data:   # каждый файл-price рассмотрим отдельно
                t = i[1:]
                s = data.index(i)
                for j in t:
                    p = j.split(',')    # уберем лишние символы из строки в прайсе
                    b = (float(p[k[s][1]]) / float(p[k[s][2]]))   #  цена за килограмм
                    # формируем строку единого прайса
                    data_itog.append([p[k[s][0]], p[k[s][1]], p[k[s][2]].rstrip('\n'), f'price {s}', f'{b:.2f}'])
            return data_itog

        self.data = data_prom(data1)
        print(self.data)
        # возвращаем единый прайс
        return self.data


        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

    def _search_product_price_weight(self, data1):
        data_pr = []
        a, b, c = 0, 0, 0
        for i in data1:
            d = i[0].split(',')
            for j in d:
                if j.lower() == 'название' or j.lower() == 'продукт' or j.lower() == 'наименование' or j.lower() == 'товар':
                    a = d.index(j)
                elif j.lower() == 'цена' or j.lower() == 'розница':
                    b = d.index(j)
                elif j.lower() == 'вес' or j.lower() == 'масса' or j.lower() == 'фасовка':
                    c = d.index(j)
                elif j.lower() == 'вес\n' or j.lower() == 'масса\n' or j.lower() == 'фасовка\n':
                    c = d.index(j)
            data_pr.append([a, b, c])
        return data_pr
        '''
            Возвращает номера столбцов
        '''

    def export_to_html(self, fname='GrossPrice'):        # получаем единый прайс и записываем его в файл HTML
        data_exp = self.data
        html_prom = open('GrossPrice.html', 'w')
        result = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Позиции продуктов</title>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>Номер</th>
                            <th>Название</th>
                            <th>Цена</th>
                            <th>Фасовка</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>

                '''
        for number, item in enumerate(data_exp, start=1):
            product_name, price, weight, file_name, value = item
            result += '<tr>'
            result += f'<td>{number}</td>'
            result += f'<td>{product_name}</td>'
            result += f'<td>{price}</td>'
            result += f'<td>{weight}</td>'
            result += f'<td>{file_name}</td>'
            result += f'<td>{value}</td>'
            result += '</tr>'
        html_prom.write(result)
        #print(result)
        html_prom.close()

    def find_text(self, text):
        # для работы в программе организуем бесконечный цикл
        while True:
            data_prom = []
            if text == 'exit':      # выход только так
                print(f'Программа закончила работу')
                break
            d = len(text)
            for i in self.data:     # проверяем совпадение введенного текста с имеющимся в прайсе
                if i[0][0:d] == text:
                    data_prom.append(i)
            if len(data_prom) == 0:   # если ничего не найдено, то предлагаем написать другой текст или закончить
                print(f'Ничего не найдено')
                text = input('Введите наименование для поиска (или выход: "exit"): ')
            else:
                data_prom.sort(key=lambda x: float(x[4]), reverse=False)  # Сортируем найденное по убыванию цены за кг
                for m in data_prom:
                    print(*m, sep=', ')     # вывод на печать в консоль
                text = input('Введите наименование для поиска (или выход: "exit"): ')  # продолжаем работу



pm = PriceMachine()
pm.load_prices('C:\SWSetup\PythonProjectForUniversity\Analizator\price_catalog')  # вывод в консоль единого прайса
pm.export_to_html('GrossPrice.html') # запись единого прайса в файл HTML
text = input('Введите наименование для поиска: ')  # начало работы с поиском по прайсу
pm.find_text(text)
print('the end')
