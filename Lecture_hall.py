import requests as req
from bs4 import BeautifulSoup

def lecture_hall(time, day_of_the_week):
    
    base_url_lecture_hall = 'https://table.nsu.ru/room'
    HOST = 'https://table.nsu.ru'
    
    html = req.get(base_url_lecture_hall)    
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('a', class_='tutors_item')
    
    hall = []
    for item in items:
        
        free_room = 0 
        
        url_room_inside = HOST + item.get('href')
        
        html_inside = req.get(url_room_inside)
        soup_inside = BeautifulSoup(html_inside.text, 'html.parser')
                
        td = soup_inside.find_all('tr')[8:-2][time]
        
        if td.find_all('td')[day_of_the_week+1].get_text(strip=True) == '':
            free_room = 1
        else:
            free_room = 0

        hall.append({
            'title':item.get_text(),
            'time':time,
            'free room': free_room
        })

    return hall 

time = 1 # time = {0 - 9:00, 1 - 10:50, 2 - 12:40, 3 - 14:30, 4 - 16:20, 5-18:10, 6-20:00}
day_of_the_week = 1 # day of the week = {0 - понедельник, 1 - вторник, 2 - среда, 3 - четрерг, 4 - пятница, 5 -суббота}

lecture_hall(time, day_of_the_week)