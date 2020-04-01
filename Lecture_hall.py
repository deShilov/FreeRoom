import requests as req
from bs4 import BeautifulSoup
import pickle

def lecture_hall(time, day_of_the_week, corp):
    """
    lecture_hall(time, day_of_the_week, corp)
    
        time = {0 - 9:00, 1 - 10:50, 2 - 12:40, 3 - 14:30, 4 - 16:20, 5-18:10, 6-20:00}
        day_of_the_week = {0 - понедельник, 1 - вторник, 2 - среда, 3 - четрерг, 4 - пятница, 5 - суббота}
        corp = {0 - новый корпус, 1 - старый корпус}
    """
    
    pickle_in = open('new_corp.pickle', 'rb')
    new_corp = pickle.load(pickle_in)

    pickle_in = open('old_corp.pickle', 'rb')
    old_corp = pickle.load(pickle_in)

    corps = [new_corp, old_corp]

    base_url_lecture_hall = 'https://table.nsu.ru/room'
    HOST = 'https://table.nsu.ru'
    
    html = req.get(base_url_lecture_hall)    
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('a', class_='tutors_item')
    
    week = soup.find_all('div', class_='parity')[0].get_text(strip=True).replace('неделя','')
    
    hall = []
    for item in items:
        
        if str(item.get_text()) not in corps[corp]:
            continue
        
#         if str(item.get_text()) != '5211':
#             continue
        
        free_room = 0  # {0 - занята, 1 - свободна}
        
        url_room_inside = HOST + item.get('href')
        
        html_inside = req.get(url_room_inside)
        soup_inside = BeautifulSoup(html_inside.text, 'html.parser')
                
        td   = soup_inside.find_all('tr')[8:-2][time]
        td_1 = td.find_all('td')[day_of_the_week+1]        
        week_tag = td_1.find('div', class_='week')
        
        if week_tag:
            if td_1.get_text(strip=True) == '' or td_1.find('div', class_='week').get_text(strip=True) != week.replace(' ', ''):
                free_room = 1
        else:
            if td_1.get_text(strip=True) == '':
                free_room = 1
        
        hall.append({
            'title':            item.get_text(),
            'day of the week':  day_of_the_week,
            'time':             time,
            'free room':        free_room
        })
#         break
    return hall