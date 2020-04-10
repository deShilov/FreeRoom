import requests as req
from bs4 import BeautifulSoup

def YouTubeTime(url_playlist):
    
    HOST = 'https://www.youtube.com/'
    
    if url_playlist[:13] != 'playlist?list':
        print('Sorry, this is not a playlist.')
        return ''
    
    try:
        html = req.get(HOST+url_playlist)
        
    except:
        print('Connection error')
        return ''

    html_time = BeautifulSoup(html.text, 'html.parser')
    
    j=[]
    for i in html_time.find_all('span')[170:-30]:
        if i.get_text().replace(' ', '').replace('\n', '') != '':
            if i.get_text().replace(' ', '').replace('\n', '').find('.') != -1:
                break
            j.append(i.get_text().replace(' ', '').replace('\n', ''))
    
    sec = 0
    minuts = 0
    hours = 0
    for i in j:
        sec += int(i[-2:])
        minuts += int(i[-5:-3])
        if len(i) >= 7:
            hours_vid = ''
            for simbol in i:
                if simbol != ':':
                    hours_vid += simbol
                else:
                    break
            hours += int(hours_vid)
    
    sec_in_min = sec//60
    sec -= (sec//60)*60
    minuts += sec_in_min
    minuts_in_hour = minuts//60
    minuts -= (minuts//60)*60
    hours += minuts_in_hour

    if hours == 0 and minuts == 0 and sec == 0:
        print('\nInvalid playlist address or no video in playlist')
        return ''
    else:
        print('\n(Only the first 100 videos can be counted)')
        print('first', len(j), 'videos counted')
        
    return (str(hours) +':'+ str(minuts)+':' + str(sec))

while True:
    print('Please enter a playlist address (example: playlist?list=PLwHnNqZbC7qaw62maoBsxuMFES9QnVqtb):')
    base_url_playlist = str(input()).replace(' ', '')

    if base_url_playlist == '':
        print('Empty line!')
    
    else:
        time = YouTubeTime(base_url_playlist)
        if time == '':
            print('Error!')
        else:
            print('Total time -', time, '(h:m:s)')
    
    print("\nWrite \"u\" to exit or something different if you want to repeat:")
    exit = str(input())
    if exit == "u":
        break