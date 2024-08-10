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


from utils import db_helpers, general
from objects.user import User

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
logging.basicConfig(filename='/data/logs/{}.log'.format(_time), format=FORMAT, level=logging.DEBUG, datefmt="[%X]")
log = logging.getLogger("rich")
log.addHandler(RichHandler())

# Get values set in compose file
admin_name = os.getenv('ADMIN_NAME')
admin_pass = os.getenv('ADMIN_PASS')

# Init DB if it does not already exist
admin_user = User(admin_name, admin_pass, [], {}, {})
db_helpers.insert_db('werk', 'users', admin_user.to_dict(), log)


def user_disconnect(e):
    log.warning(f'Disconnect detected, running cleanup on session {e.page.session_id}')
    
    user_row = db_helpers.get_row_db('users', 'authenticated_session', e.page.session_id)
    
    log.warning(f"Attempting to remove session {e.page.session_id} from the user {user_row['username']}")
    
    try:
        db_helpers.update_user_field_db(user_row['username'], 'authenticated_session', '', log)
        
        log.debug(f"Successfully removed session {e.page.session_id} from the user {user_row['username']}")
    except:
        log.error(f"FAILED to remove session {e.page.session_id} from the user {user_row['username']}")

"""
#----------------------------------
"""

async def main(page: Page):
    page.title = "W.I.P. werk"
    page.theme_mode = 'dark'
    page.theme = theme.Theme(color_scheme_seed='blue')
    
    page.on_disconnect = user_disconnect
    
    log.debug(f"current session {page.session_id}")
    
    console.print(logo)

    def route_change(e):
        if db_helpers.check_if_authenticated_session(page.session_id, log):
            log.debug(f"Route change: {e.route}")
            page.views.clear()
            page.views.append(
                views_handler(page, log)[e.route]
            )
            page.update()
        else:
            page.route = "/"
            log.warning(f"Not authenticated route change request to route: {e.route} - Rerouting to login page")
            page.views.clear()
            page.views.append(
                views_handler(page, log)[page.route]
            )
            page.update()
            

    page.on_route_change = route_change
    page.go(page.route)
    

ft.app(target=main, view=ft.WEB_BROWSER, port=5554)