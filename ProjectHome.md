# Introduction #
Trapy (Travian + API + Python) is the "Api that wasn't" for the browsergame Travian. It exists because there is no official API, thanks to the fact that the Travian frontend is so horribly implemented and cryptic. It was designed to be fast, minimal, and clean.
# Requirements #
  * [Python 2.5](http://python.org)
  * [BeautifulSoup](http://crummy.com/software/BeautifulSoup)
  * [ClientCookie](http://wwwsearch.sourceforge.net/ClientCookie)
  * [ClientForm](http://wwwsearch.sourceforge.net/ClientForm)
# Roadmap #
  * **1.0 stable**: Complete access to basic Travian functionality - troops, resources, marketplace, upgrades, etc.
  * **1.5**: A fully functional client (HTA or Air) with task queue, with support for attacks, reinforcements, trades, and upgrades/builds.
  * **2.0**: An alliance tool, with (possibly) with bundled server with SMS and email support.
  * **3.0**: Too far out for now ... ;)
# Example #
```
>>> import trapy
>>> con = trapy.Connection(7, 'com', 'username', 'password')
[>] Logging into s7.travian.com as mini-man...
[>] Login successful.
>>> world = trapy.World(con)
>>> world.villages
[(u'?newdid=166948', u'Haddockhurstley'), (u'?newdid=235472', u'Ironhamgrove'),
(u'?newdid=82489', u'Painmouth Abbey'), (u'?newdid=255277', u'Rumingwick Springs
'), (u'?newdid=258519', u'Southlockworthy'), (u'?newdid=230408', u'Wopworthpoint
field')]
>>> world.goto_village(3)
[>] Navigating to village Rumingwick Springs...
<closeable_response at 0x1102648 whose fp = <socket._fileobject object at 0x0107
4C70>>
>>> con.cururl
u'http://s7.travian.com/dorf2.php?newdid=255277'
>>> world.goto_village('pain')
[>] Navigating to village Painmouth Abbey...
<closeable_response at 0x11076c0 whose fp = <socket._fileobject object at 0x0107
4DB0>>
```

# Download #
trapy is under constant development, and would be barely of use to you at the current stage. But you can still grab the latest sourcecode [here](http://code.google.com/p/trapy/source/browse/trunk/trapy.py) to see how things are coming along.