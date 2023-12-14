from ._anvil_designer import serviceTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class service(serviceTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    

  


  

  def link_1_click(self, **event_args):
    open_form('Home')

  def button_2_click(self, **event_args):
    open_form('SIGNUP')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("customer",user=self.user)

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("withdraw",user=self.user)

  def link_9_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("transfer",user=self.user)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    query=self.text_box_1.text
    user_info = app_tables.users.search(username=self.user['username']).get()
    anvil.server.call("add_query",query)
    if user_info:
            # Update the "service" table with the query and user information
            app_tables.service.add_row(
                username=user_info['username'],
                phone=user_info['phone']
            )
            alert("Your query has been submitted and our Technical Executive will get in touch with you")
    else:
      
    

 
