#!usr/bin/python
# trapy - v0.1.12
# "The API that wasn't"
# Written by mini-man

from ClientCookie   import urlopen
from ClientForm     import ParseResponse
from BeautifulSoup  import BeautifulSoup
from re             import compile, sub

SILENT = 0

def info(msg, type=1):
    if not SILENT:
        if type == 1:   # info
            x = "[>]"
        elif type == 2: # error
            x = "[!]"
        print x, msg

def geterr():
    import sys
    return str(sys.exc_info()[:2][1])

def stripent(string):
    return sub('&.*?;', '', string)

class LoginError(Exception):

    def __init__(self, value):
        self.param = value
    
    def __str__(self):
        return 'LoginError: ', str(self.param)

class Connection:
    
    def __init__(self, server, tld, username, password, silent=0):
        if silent:
            global SILENT
            SILENT    = 1
        self.server   = server
        self.tld      = tld
        self.username = username
        self.password = password
        self.baseurl  = 'http://%s.travian.%s/' % (server, tld)
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
            info("Logging into %s.travian.%s as %s..." %
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
            info('Grabbing village data...')
            self.conn     = connection
            self.navigate = connection.navigate
            
            self.overview = BeautifulSoup(self.navigate('dorf1.php').read())
            self.village  = BeautifulSoup(self.navigate('dorf2.php').read())
            self.stats    = BeautifulSoup(self.navigate('statistiken.php').read())
            self.profurl  = self.stats.find('a', text=self.conn.username).parent['href']
            self.profile  = BeautifulSoup(self.navigate(self.profurl))
            self.villages = []
            
            self.get_villages()
            info('Done. %d villages found.' % len(self.villages))
        else:
            info('Pass me a trapy.Connection object pl0x!', 2)
    
    def get_villages(self):
        if not self.villages:
            villages = self.profile.findAll(href=compile('\?newdid=\d+'))
            
            for a in villages:
                v = [a['href'], a.contents[0]]
                if a.has_key('class'):
                    v.append('Capital')
                self.villages.append(v)
        
        info('Your villages: ')
        for v in self.villages:
            print '--->', v[1], 
            if len(v) == 3:
                print '(Capital)',
            print
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
            self.overview = BeautifulSoup(self.navigate('dorf1.php' + match[0]))
            self.village = BeautifulSoup(self.navigate('dorf2.php' + match[0]))
            return self.village
        else:
            info('No village found.', 2)
            return False
            
    def get_resources(self, village):
        if self.goto_village(village):
            res = self.village.findAll(text=compile('\d+/\d+'))[:-1]
            return [[int(x) for x in r.split('/')] for r in res]
        else:
            return False
    
    def get_production(self, village):
        if self.goto_village(village):
            pro = self.overview.findAll('b', text=compile('\d+&nbsp;'))
            return [int(p[:-6]) for p in pro]
        else:
            return False

    def get_population(self, village='all'):
        if village.lower() == 'all':
            pop = int(self.profile.find(text='Population:').findNext('td').contents[0])
        else:
            if self.goto_village(village):
                name = self.village.find('a', 'active_vl').contents[0]
                pop  = int(self.profile.find(text=name).findNext('td').contents[0])
            else:
                pop  = False
        return pop
            
    def get_troops(self, village):
        if self.goto_village(village):
            trtable = self.overview.find(text=compile('Troops:$')).findNext('table')
            troops  = [
                (t, t.findNext('td').contents[0]) for t in trtable.findAll(text=compile('\d+'))
            ]
            return troops
        else:
            return False
