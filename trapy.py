#!usr/bin/python
# trapy - v0.1.3
# "The API that wasn't"
# Written by mini-man

from ClientCookie   import urlopen
from ClientForm     import ParseResponse
from BeautifulSoup  import BeautifulSoup
from re             import compile

def info(msg, type=1):
    if type == 1:   # info
        x = "[>]"
    elif type == 2: # error
        x = "[!]"
    print x, msg

def geterr():
    import sys
    return str(sys.exc_info()[:2][1])

class LoginError(Exception):

    def __init__(self, value):
        self.param = value
    
    def __str__(self):
        return 'LoginError: ', str(self.param)

class Connection:
    
    def __init__(self, server, tld, username, password):
        self.server   = server
        self.tld      = tld
        self.username = username
        self.password = password
        self.baseurl  = 'http://s%d.travian.%s/' % (server, tld)
        self.loggedin = self.login()

    def navigate(self, url):
        if type(url) in (str, unicode):
            url = self.baseurl + url
            self.cururl = url
        else:
            self.cururl = url.get_full_url()
        return urlopen(url)
    
    def logout(self):
        if self.loggedin:
            resp = self.navigate('logout.php').read()
            if resp.find('successful') != -1:
                self.loggedin = False
                info('Logout successful. Goodbye!')
            else:
                self.loggedin = True
                info('Error logging out!', 2)
    
    def login(self):
        try:
            info("Logging into s%s.travian.%s as %s..." %
                (self.server, self.tld, self.username))

            soup   = BeautifulSoup(self.navigate(''))
            fields = soup.find('form', {'name':'snd'}).findAll('input')
            fieldu = fields[2]['name']
            fieldp = fields[3]['name']
            
            forms  = ParseResponse(self.navigate(''), backwards_compat=False)
            form   = forms[0]
            form[fieldu] = self.username
            form[fieldp] = self.password
            
            resp   = self.navigate(form.click('s1'))
            
            if resp.read().find("Password forgotten") != -1:
                raise LoginError('Login failed. Username or password incorrect.')
            else:
                info('Login successful.')
                return True
        except:
            info(geterr(), 2)
        return

class World:

    def __init__(self, connection):
        if connection:
            self.conn     = connection
            self.overview = BeautifulSoup(connection.navigate('dorf1.php').read())
            self.villages = []
            self.get_villages()
        else:
            info('Pass me a trapy.Connection object pl0x!', 2)
    
    def get_villages(self):
        if not self.villages:
            self.villages = [
                (a['href'], a.contents[0]) for a in \
                 self.overview.findAll(href=compile('\?newdid=\d+'))
            ]
        return self.villages
    
    def goto_village(self, village):
        if not self.villages: self.get_villages()
        match = None
        if type(village) == int:
            if village > len(self.villages) or village < 0:
                info('Invalid village index!')
            else:
                match = self.villages[village]
        elif type(village) == str:
            for v in self.villages:
                if v[1].lower() == village.lower() or \
                   v[1].lower().startswith(village.lower()):
                    match = v
        if match:
            info('Navigating to village ' + match[1] + '...')
            return self.conn.navigate('dorf2.php' + match[0])
        else:
            info('No village found.', 2)
            return False

    