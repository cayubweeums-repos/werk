"""
# Init Imports --------------------------------------------
"""
import os
import subprocess
import datetime
import logging
import flet as ft
from flet import theme, Page
from rich.logging import RichHandler
from rich.traceback import install
from rich import pretty
from rich.console import Console

from pages.landing import Landing_Page
from pages.views_handler import views_handler


"""
# -------------------------------------------------------
"""

logo='''
WWWWWWWW                           WWWWWWWW                                   kkkkkkkk           
W::::::W                           W::::::W                                   k::::::k           
W::::::W                           W::::::W                                   k::::::k           
W::::::W                           W::::::W                                   k::::::k           
 W:::::W           WWWWW           W:::::W eeeeeeeeeeee    rrrrr   rrrrrrrrr   k:::::k    kkkkkkk
  W:::::W         W:::::W         W:::::Wee::::::::::::ee  r::::rrr:::::::::r  k:::::k   k:::::k 
   W:::::W       W:::::::W       W:::::We::::::eeeee:::::eer:::::::::::::::::r k:::::k  k:::::k  
    W:::::W     W:::::::::W     W:::::We::::::e     e:::::err::::::rrrrr::::::rk:::::k k:::::k   
     W:::::W   W:::::W:::::W   W:::::W e:::::::eeeee::::::e r:::::r     r:::::rk::::::k:::::k    
      W:::::W W:::::W W:::::W W:::::W  e:::::::::::::::::e  r:::::r     rrrrrrrk:::::::::::k     
       W:::::W:::::W   W:::::W:::::W   e::::::eeeeeeeeeee   r:::::r            k:::::::::::k     
        W:::::::::W     W:::::::::W    e:::::::e            r:::::r            k::::::k:::::k    
         W:::::::W       W:::::::W     e::::::::e           r:::::r           k::::::k k:::::k   
          W:::::W         W:::::W       e::::::::eeeeeeee   r:::::r           k::::::k  k:::::k  
           W:::W           W:::W         ee:::::::::::::e   r:::::r           k::::::k   k:::::k 
            WWW             WWW            eeeeeeeeeeeeee   rrrrrrr           kkkkkkkk    kkkkkkk
'''

install()
pretty.install()
console = Console()

_time = datetime.date.today()
if not os.path.exists('/data'):
    os.makedirs('/data')
    os.makedirs('/data/logs')
    os.makedirs('/data/db')
elif not os.path.exists('/data/logs'):
    os.makedirs('/data/logs')
elif not os.path.exists('/data/db'):
    os.makedirs('/data/db')
FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(filename='./data/logs/{}.log'.format(_time), format=FORMAT, level=logging.DEBUG, datefmt="[%X]")
log = logging.getLogger("rich")
log.addHandler(RichHandler())
"""
#----------------------------------
"""

async def main(page: Page):
    
    page.title = "W.I.P. werk"
    page.theme_mode = 'dark'
    page.theme = theme.Theme(color_scheme_seed='blue')
    
    console.print(logo)

    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()
        page.views.append(
            views_handler(page, log)[e.route]
        )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER, port=5554)