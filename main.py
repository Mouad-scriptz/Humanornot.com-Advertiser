import tls_client, tls_client.exceptions, uuid, os, threading, itertools, json, time
from colorama import init, Fore

init(True,True)
print_lock = threading.Lock()
reset = Fore.RESET
lblue = Fore.LIGHTBLUE_EX; cyan = Fore.CYAN
green = Fore.GREEN; lgreen = Fore.LIGHTGREEN_EX
yellow = Fore.YELLOW; lyellow = Fore.LIGHTYELLOW_EX

def tprint(text):
    print_lock.acquire()
    print(text)
    print_lock.release()    


def advertise(text, proxies):
    while True:
        proxy = next(proxies)
        try:
            session = tls_client.Session("chrome_114")
            session.headers = {
                'authority': 'api.humanornot.ai',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json',
                'hon-client-version': '1.0.11',
                'origin': 'https://app.humanornot.ai',
                'referer': 'https://app.humanornot.ai/',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }
            session.proxies = {
                'http': "http://"+proxy,
                'https': "http://"+proxy
            }

            # Starting a chat
            user_id = str(uuid.uuid4())
            r = session.post('https://api.humanornot.ai/human-or-not/chat/',json={'user_id':user_id,'origin':'honLandPage'})
            data = r.json()
            tprint(f"({lyellow}~{reset}) Started chat: {yellow}{data['chat_id']}")
            if data['is_my_turn'] == False:
                r = session.put(f'https://api.humanornot.ai/human-or-not/chat/{data["chat_id"]}/wait-message',json={'user_id':user_id})

            # Sending message
            r = session.put(f'https://api.humanornot.ai/human-or-not/chat/{data["chat_id"]}/send-message',json={'user_id':user_id,'text':text})
            tprint(f'({lgreen}+{reset}) Sent message: {green}{data["chat_id"]}')
        except tls_client.exceptions.TLSClientExeption:
            pass
        except json.decoder.JSONDecodeError:
            pass

banner = '''   _____                             _   __                
  / ___/__  ______  ___  _____      / | / /___ _   ______ _
  \__ \/ / / / __ \/ _ \/ ___/_____/  |/ / __ \ | / / __ `/
 ___/ / /_/ / /_/ /  __/ /  /_____/ /|  / /_/ / |/ / /_/ / 
/____/\__,_/ .___/\___/_/        /_/ |_/\____/|___/\__,_/  
          /_/                                              '''
for line in banner.splitlines():
    print(cyan+line.center(os.get_terminal_size().columns))
print(f"{lblue}[Humanornot.ai Advertiser. By Mouad#1111]".center(os.get_terminal_size().columns))
text = input(f"({cyan}>{reset}) Message {lblue}>>{reset} ")
print(reset,end="\r")
threads_num = int(input(f"({cyan}>{reset}) Threads {lblue}>>{reset} "))
proxies = itertools.cycle(open("proxies.txt").read().splitlines())
for _ in range(threads_num):
    threading.Thread(target=advertise,args=(text,proxies)).start()
