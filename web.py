from multiprocessing.dummy import Pool
from datetime import datetime
import os
import requests
import win32gui, win32con, ctypes
import dns.resolver

os.system('cls')

hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
ctypes.windll.kernel32.SetConsoleTitleW("Raskovalov")

color = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

class Welcom:
    def __init__(self) -> None:
        pass

    def main(self) -> None:
        print("\n\n\n\n [+] help - просмотр команд\n [+] reference - о программе\n [+] dependencies - зависимости который нужно установить\n")
    
    def help(self) -> None:
        command_dict: dict = {
            'domains' : 'сканирование домена на поддомены и домен верхнего уровня, поддомены и домены верхнеого ур. беруться из файлов(settings\\domains\\domains.txt, settings\\domains\\top_domains.txt), если вам не хватает можите добавить свои', 
            'dns' : 'сканирование на dns и host, показывает ip адреса хостинга и dns сервера на которм находяться хостинги. Сайты беруться из файла(settings\\domains\\good_domains.txt)',
            'reboot' : 'после люых изминений в папке settings необходимо перезагрузиться',
            'clear' : 'очистить окно',
            'exit' : 'выход из программы'
        }
        
        print('\n\n')
        for dic in command_dict:
            print(f' [command] {dic} - {command_dict[dic]}')
        print('\n\n')

    def reference(self) -> None:
        print('\n\n')
        print(' Version 1.1. - Сканирование поддоменов \n\n')
        print(' Автор - Raskovalov')
        print('\n\n')

    def dependencies(self) -> None:
        libs: list = ['requests', 'win32gui', 'win32con', 'ctypes', 'sublist3r']
        print('\n\n')
        for lib in libs:
            print(f' [dependencies] {lib}')
        print(' \n Для установки используйте команду py -m pip install ...')
        print('\n\n')

    def clear(self):
        os.system('cls')
        self.main()

    def reboot(self):
        os.startfile('web_foontic.py')
        exit()

class Web:
    def __init__(self, welcom: object) -> None:
        self.subdomains: list = open('settings\\domains\\subdomains.txt', 'r', encoding='utf-8').read().split('\n')
        self.domains: list = open('settings\\domains\\domains.txt', 'r', encoding='utf-8').read().split('\n')
        self.top_domains: list = open('settings\\domains\\top_domains.txt', 'r', encoding='utf-8').read().split('\n')
        self.good_domains: list = open('settings\\domains\\good_domains.txt', 'r', encoding='utf-8').read().split('\n')
        self.welcom: object = welcom

    def serch_dns(self, dir: str):
        print(f' [{dir}] Начинаю сканирование')
        my_resolver = dns.resolver.Resolver()
        my_resolver.nameservers = ['8.8.8.8']
        
        f = open('settings\\dns\\good_dns.txt', 'w', encoding='utf-8')
        for i in range(len(self.good_domains) - 1):
            datenow: str = str(datetime.now())[:-7]
            try:
                for u in str(my_resolver.resolve(self.good_domains[i].split('//')[1], 'A').rrset).split('\n'):
                    f.write(f'{i} |  HOST | {u}\n')
                    print(f' [{dir}] ' + color[1] + f'{i} | {datenow} | INFO |  HOST | {u}' + '\033[0m') # Возвращяет IP сервера хостинга
            except:
                print(f' [{dir}] ' + color[0] + f'{i} | {datenow} | INFO |  HOST | ERROR - {self.good_domains[i]}' + '\033[0m')
                
            try:
                for u in str(my_resolver.resolve(self.good_domains[i].split('//')[1], 'NS').rrset).split('\n'):
                    f.write(f'{i} |  DNS  | {u}\n')
                    print(f' [{dir}] ' + color[1] + f'{i} | {datenow} | INFO |  DNS  | {u}' + '\033[0m') # Сервер на котором нахходиться домен, т. е. ДНС сервера домена 
            except:
                print(f' [{dir}] ' + color[0] + f'{i} | {datenow} | INFO |  DNS  | ERROR - {self.good_domains[i]}' + '\033[0m')



    def _top_domains(self, dir: str) -> list:
        if len(self.domains[0]) == 0:
            print(f' [domains] ERROR - у вас нет целей, добавти их в файл settings\\domains\\domains.txt и перезагрузитесь(приложение)')
            return 
        
        print(f' [{dir}] Обрабатываю домены второго ур')
        
        top_domains_good: list = list()
        top_domains_good_return: list = list()

        def wrapper(top_domains: list):
            for domein in self.domains:
                datenow: str = str(datetime.now())[:-7]
                url: str = f'https://{domein.split(".")[0]}{top_domains}'
                try:
                    respons = requests.get(url).status_code
                    sign: str = color[1] + '[+'
                    status: str = 'Обнаружен домен вверхнего уровня'
                    top_domains_good_return.append(f'{url}')
                except:
                    respons: str = '400'
                    sign: str = color[0] + '[-'
                    status: str = 'Не существует'

                top_domains_good.append(f' [{dir}] {sign}] {datenow} | INFO | {url} | {status} | {respons}' + '\033[0m')
        
        p = Pool(len(self.top_domains))
        p.map(wrapper, self.top_domains)

        for i in top_domains_good:
            print(i)

        return top_domains_good_return

    def _subdomains(self, dir: str) -> list:
        if len(self.domains[0]) == 0:
            print(f' [domains] ERROR - у вас нет целей, добавти их в файл settings\\domains\\domains.txt и перезагрузитесь(приложение)')
            return 
        
        print(f' [{dir}] Обрабатываею поддомены')

        subdomains_good: list = list()
        subdomains_return: list = list()

        def wrapper(subdomains: list):
            for domein in self.domains:
                datenow: str = str(datetime.now())[:-7]
                url: str = f'https://{subdomains}.{domein}'
                try:
                    respons = requests.get(url).status_code
                    sign: str = color[1] + '[+'
                    status: str = 'Обнаружен поддомен'
                    subdomains_return.append(f'{url}')
                except:
                    respons: str = '400'
                    sign: str = color[0] + '[-'
                    status: str = 'Не существует'

                subdomains_good.append(f' [{dir}] {sign}] {datenow} | INFO | {url} | {status} | {respons}' + '\033[0m')
        
        p = Pool(len(self.subdomains))
        p.map(wrapper, self.subdomains)

        for i in subdomains_good:
            print(i)

        return subdomains_return
        
welcom: object = Welcom()
web: object = Web(welcom)

dir: str = 'home'

welcom.main()
while True:
    event: str = input(f' [{dir}] ').split(' ')[0]

    #Начальные комманды
    if event == 'help':
        welcom.help()
    elif event == 'reference':
        welcom.reference()
    elif event == 'dependencies':
        welcom.dependencies()
    elif event == 'exit':
        exit()
    elif event == 'clear':
        welcom.clear()
    elif event == 'reboot':
        welcom.reboot()
    
    #Проверка на комманды второго эшилона
    if event == 'domains':
        datestart: object = datetime.now()
        dir:str = 'domains'
   
        subdomains_good: list = web._subdomains(dir=event)        
        top_domains_good: list = web._top_domains(dir=event)

        if subdomains_good != None and top_domains_good != None:
            with open('settings\\domains\\good_domains.txt', 'w', encoding='utf-8') as f:
                for i in subdomains_good: f.write(i + '\n')
                for i in top_domains_good: f.write(i + '\n')

            dateend: object = datetime.now()
            print(f' [{dir}] Успешные запросы сохронил в файл settings\\domains\\good_domains.txt')
            print(f' [{dir}] Успещных запросов {len(top_domains_good) + len(subdomains_good)}')
            print(f' [{dir}] Затраченное время {str(dateend - datestart)[:-7]}\n')

        dir: str = 'home'
    elif event == 'dns':
        datestart: object = datetime.now()
        dir:str = 'dns'

        web.serch_dns(dir=dir)

        dateend: object = datetime.now()
        print(f' [{dir}] Успешные запросы сохронил в файл settings\\dns\\good_dns.txt')
        print(f' [{dir}] Затраченное время {str(dateend - datestart)[:-7]}\n')

        dir: str = 'home'

