import requests as req
from bs4 import BeautifulSoup
import pickle

def teachers_list_url():
    
    base_url_teacher = 'https://table.nsu.ru/teacher'
    HOST = 'https://table.nsu.ru'
    
    html = req.get(base_url_teacher)
    
    soup = BeautifulSoup(html.text, 'html.parser')
    teachers = {}
    
    for teacher in soup.find_all('a', class_='tutors_item'):
        teachers[str(teacher.get('title'))] = HOST + teacher.get('href')
    
    return teachers

def teacher_timetable(full_name_teacher):
    
    pickle_in = open('teachers_list.pickle', 'rb')
    teachers_list = pickle.load(pickle_in)
    
    HOST = 'https://table.nsu.ru'
    url_teacher = teachers_list[full_name_teacher]
    
    html_teacher = req.get(url_teacher)
    soup = BeautifulSoup(html_teacher.text, 'html.parser')
    tr = soup.find_all('tr')[8:-2]
    
    type_par = soup.find_all('span')[3:-1]
        
    days = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    
    pari = []
    
    type_par_index = 0
    
    for cells in tr:
        
        day_of_the_week = 0    
    
        time = cells.find_all('td')[0]
        
        for cell in cells.find_all('td')[1:]:
            
            if cell.get_text(strip=True) == '':
                pari.append({
                    'day': days[day_of_the_week],
                    'time': time.get_text(strip=True),
                    'week': '',
                    'type': '',
                    'subject': '',
                    'cab': '',
                    'group': '',    
                })
                day_of_the_week += 1
                continue
            
            if len(cell.find_all('div', class_='groups')) == 2:
                subject = cell.find_all('div')[1::5]   
                             
                for k in range(2):
                    
                    list_group = []             
                    for groups in cell.find_all('div', class_='groups')[k].find_all('a', class_="group"):
                        list_group.append(groups.get_text(strip=True))
    
                    pari.append({
                        'day': days[day_of_the_week],
                        'time': time.get_text(),
                        'week': cell.find_all('div', class_='week')[k].get_text(strip=True),
                        'type': type_par[type_par_index].get_text(),
                        'subject': subject[k].get_text(strip=True),
                        'cab': cell.find_all('div', class_='room')[k].get_text(strip=True),
                        'group': list_group, 
                    })
        
                    type_par_index += 1   
                    
                day_of_the_week += 1
            
            else:
                
                week = ''
                
                list_groups = []  # {}
                for groups in cell.find_all('a', class_="group"):
                    list_groups.append(groups.get_text(strip=True))
                    
                if cell.find('div', class_='week'):
                    week = cell.find('div', class_='week').get_text(strip=True)
                    
                pari.append({
                    'day': days[day_of_the_week],
                    'time': time.get_text(),
                    'week': week,
                    'type': type_par[type_par_index].get_text(),
                    'subject': cell.find_all('div')[1].get_text(strip=True),
                    'cab': cell.find('div', class_='room').get_text(strip=True),
                    'group': list_groups,
                })
                
                type_par_index += 1
                day_of_the_week += 1
                
    return pari

# 
for i in teacher_timetable('Грешнов Александр Валерьевич'):
    print(i)