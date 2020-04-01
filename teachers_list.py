def teachers_list_url():
    
    base_url_teacher = 'https://table.nsu.ru/teacher'
    HOST = 'https://table.nsu.ru'
    
    html = req.get(base_url_teacher)
    
    soup = BeautifulSoup(html.text, 'html.parser')
    teachers = {}
    
    for teacher in soup.find_all('a', class_='tutors_item'):
        teachers[str(teacher.get('title'))] = HOST + teacher.get('href')
    
    return teachers