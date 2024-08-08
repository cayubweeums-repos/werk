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

# Init DB if not already initialized
init_data={
    'username': admin_name,
    'password': general.get_hashed_pass(admin_pass),
    'authenticated_sessions': []
}
db_helpers.insert_db('werk', 'users', init_data, log)


"""
#----------------------------------
"""

async def main(page: Page):
    page.title = "W.I.P. werk"
    page.theme_mode = 'dark'
    page.theme = theme.Theme(color_scheme_seed='blue')
    
    def user_disconnect():
        log.warn(f'Disconnect detected, running cleanup on session {page.session_id}')
        
        user_row = db_helpers.get_row_db('users', 'authenticated_sessions', page.session_id)
        
        log.warn(f"Attempting to remove session {page.session_id} from the user {user_row['username']}")
        
        try:
            user_row.update_one(
                {"_id": user_row["_id"]},  # Find the user by _id
                {"$pull": {"authenticated_sessions": page.session_id}}  # Remove the session_id from the list
            )
            
            log.info(f"Successfully removed session {page.session_id} from the user {user_row['username']}")

        except:
            log.error(f"FAILED to remove session {page.session_id} from the user {user_row['username']}")
    
    page.on_disconnect = user_disconnect
    
    log.error(f"current session {page.session_id}")
    
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
    
    log.error(f"Admin name is: {admin_name}\nAdmin pass is: {admin_pass}")
    log.error(f"Running the hash again = {general.get_hashed_pass(admin_pass)}")

ft.app(target=main, view=ft.WEB_BROWSER, port=5554)