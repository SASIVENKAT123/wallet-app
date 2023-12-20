from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate6(ItemTemplate6Template):
  def __init__(self,user = None ,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user= user
  def button_1_click(self, user= None, **event_args):
        # Access the data for the selected user
        selected_user = self.item  # Assuming you have set the 'item' property of the repeating panel to the user row
        
        # Open the admin_view form and pass the user details
        open_form('admin.set_limit', user= self.user, user_data=selected_user)

    # Any code you write here will run before the form opens.
