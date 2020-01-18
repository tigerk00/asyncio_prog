#Паралельный запуск сопрограмм и использование библиотеки для асинхронного программирования asyncio
#Код не несет никакой практической пользы , он был написан для того , чтобы понять насколько быстрее асинхронный  код выполняется в сравнении с обычным  методом кода.


### Обычный  код (время выполнения , в начальном виде) - 9 сек
### Асинхронный код (время выполнения) - 4.5 сек
### Асинхронный код , с использованием паралельного запуска сопрограмм (время выполнения) - 1.5 сек



from time import time
import asyncio

async def get_pages(site_name):  
    await asyncio.sleep(0.5)
    print("Открытие страницы: {}".format(site_name))  # симуляция открытия страницы
    return range(1 , 4)

async def get_page_data(site_name , page):
    await asyncio.sleep(1)
    return "Информация со страницы {} ({})".format(page  , site_name)  #симуляция парсинга страницы 

async def tiger(site_name):
    pages = await get_pages(site_name)
    co_pages = list()   # Присваиваем пустой список
    
    for page in pages:
        co_pages.append(get_page_data(site_name , page)) #создаём обьект корутин и добавляем его методом .append в список co_pages
    
    for co_page in asyncio.as_completed(co_pages):       # as_completed возвращает итератор из переданых в него сопрограм
        data = await co_page                             # as_completed ожидает завершение сопрограммы
        print(data)                                      # как только сопрограмма закончится , мы получим данные , выведим их на екран и цикл уйдёт  на вторую итерацию.
        
start = time()

tigers = [
    asyncio.ensure_future(tiger("Main_File")),
    asyncio.ensure_future(tiger("Second_File")),
    asyncio.ensure_future(tiger("Third_File")),
    asyncio.ensure_future(tiger("Last_File")),
]

# event_loop - ядро любого asyncio приложения , он запускает асинхронные задачи и обратные вызовы, выполняет операции сетевого ввода-вывода и запускает подпроцессы.
event_loop = asyncio.get_event_loop()
now = event_loop.time()
event_loop.run_until_complete(asyncio.gather(*tigers)) # run_until_complete - нужен для того , чтобы программа исполнялась до того момента , пока экземпляр Future не закончится.
event_loop.close()  # .close  - тут всё понятно , закрытие цикла событий.

print ( "Время выполнения задачи: " + " {:.2f}".format(time() - start))  