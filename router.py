import requests, base64, re
from bs4 import BeautifulSoup

class Router:
    def __init__(self, user, password, ip='http://192.168.1.1', login=True):
        self.session = requests.Session()
        self.headers_orig = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'DNT': '1', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
        self.headers = self.headers_orig
        self.auth_token="Authorization=Basic "+base64.b64encode(f'{user}:{password}'.encode('utf-8')).decode()
        self.ip = ip
        if login:
            self.login()

    def login(self):
        r = self.session.get(self.ip,headers={'Cookie': self.auth_token, **self.headers})
        self.headers = {**self.headers, **requests.utils.dict_from_cookiejar(self.session.cookies)}
        r = self.session.get(f'{self.ip}/backupsettings.html', headers={'Referer':self.ip, **self.headers})
        r = self.session.get(f'{self.ip}/resetrouter.html', headers={'Referer':f'{self.ip}/backupsettings.html', **self.headers})

        if r.status_code==200:
            session_id=re.findall('\'(\d\d\d\d\d\d\d\d\d\d)\'', r.text)
            try:
                self.id = session_id[0]
                return session_id[0]
            except:
                return False
        else:
            return False

    def reboot(self):
        r = self.session.get(f'{self.ip}/rebootinfo.cgi?sessionKey={self.id}', headers={'Referer':f'{self.ip}/resetrouter.html', **self.headers})
        if r.status_code==200:
            return True
        else:
            return False

    def users(self):
        r = self.session.get(f'{self.ip}/wlstationlist.cmd', headers={'Referer':f'{self.ip}', **self.headers})
        soup = BeautifulSoup(r.text, 'lxml')
        f = soup.find('table',attrs={'cellspacing':"0", 'cellpadding':"4", 'border':"1"}).text.strip()
        return re.findall('(..:..:..:..:..:..)', f)

    def add_mac_filter(self, mac):
        r = self.session.get(f'{self.ip}/wlmacflt.cmd?action=add&wlFltMacAddr={mac}&wlSyncNvram=1&sessionKey={self.id}', headers={'Referer':f'{self.ip}/wlmacflt.html', **self.headers})
        if r.status_code==200:
            return True
        else:
            return False

    def delete_mac_filter(self, mac):
        r = self.session.get(f'{self.ip}/wlmacflt.cmd?action=remove&rmLst={mac}&sessionKey={self.id}', headers={'Referer':f'{self.ip}/wlmacflt.html', **self.headers})
        if r.status_code==200:
            return True
        else:
            return False

    def set_mac_filter_mode(self, mode):
        r = self.session.get(f'{self.ip}/wlmacflt.cmd?action=save&wlFltMacMode={mode}&sessionKey={self.id}', headers={'Referer':f'{self.ip}/wlmacflt.html', **self.headers})
        if r.status_code==200:
            return True
        else:
            return False

    def get_password(self):
        r = self.session.get(f'{self.ip}/wlsecurity.html', headers={'Referer':f'{self.ip}/wlswitchinterface0.wl', **self.headers})
        if r.status_code==200:
            return re.findall("wpaPskKey ?= ?'?\"?("+ "[^ \'\"]?" * 16 + ")'?\"?;", r.text)[0]
        else:
            return False

    def set_password(self, user, new):
        p = get_password()
        r = self.session.get(f'{self.ip}/password.cgi?inUserName={user}&inPassword={new}&inOrgPassword={p}&sessionKey={self.id}', headers={'Referer':f'{self.ip}/password.html', **self.headers})
        if r.status_code==200:
            return True
        else:
            return False
