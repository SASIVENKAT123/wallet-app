from ._anvil_designer import set_limitTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class set_limit(set_limitTemplate):
  def __init__(self, user= None, user_data=None, **properties):
        # Initialize the base class
        self.init_components(**properties)
        self.user= user
        # Access the user_data passed from the calling form
        self.user_data = user_data
        if self.user is not None:
            print("DEBUG: Before accessing 'email'")
            self.name = self.user['email']
            print(name)
            print("DEBUG: After accessing 'email'")
        
        # Now you can access the username or any other user data
            
  def outlined_button_1_click(self, **event_args):
    username = self.user_data['username']
    new_limit = self.text_box_1.text
        
    # Call the server function and update the user's limit
    setter = anvil.server.call('user_detail', username, new_limit)
        
    # Log changes to 'actions' table
    changes_made = [f"Limit updated to {new_limit} by admin"]
    if self.user is not None:
            self.log_action(username, changes_made, self.name)
    else:
      print("it's none - not logging action")
    

  def log_action(self, username, changes,email):
        # Retrieve last_login from the 'users' table
        user = app_tables.users.get(username=username)
        last_login = None
        
        if user and user['last_login']:
            last_login = user['last_login']
        # Log actions to 'actions' table if changes were made
        if changes:
            print("reached changes")
            current_datetime = datetime.now()
            app_tables.actions.add_row(
                username=username,
                last_login=last_login,
                changes=", ".join(changes),
                date=current_datetime,
                admin_email= email
            )
    
