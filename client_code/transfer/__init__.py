from ._anvil_designer import transferTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


class transfer(transferTemplate):
    def __init__(self, user=None, **properties):
        self.user = user
        self.init_components(**properties)
        self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"
        user_account_numbers = anvil.server.call('get_user_account_numbers', self.user['username'])
        self.dropdown_account_numbers.items = user_account_numbers
        self.display()
        
        
    def link_1_click(self, **event_args):
      open_form('customer', user= self.user)


    def button_1_click(self, **event_args):
      current_datetime = datetime.now()
      acc = self.dropdown_account_numbers.selected_value
      print(acc)
      user_currency = anvil.server.call('get_currency_data', acc)
      fore_money = anvil.server.call('get_accounts_emoney', acc)
    
      if self.user is not None:
        wallet3 = anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
        
        if wallet3 is None:
            self.label_2.text = "Error: Wallet is empty"
            return
    
      selected_symbol = self.drop_down_1.selected_value
      money_value = float(self.text_box_4.text)
    # Add your conversion rates here
      conversion_rate_usd_to_inr = 80.0
      conversion_rate_swis_to_inr = 95.0
      conversion_rate_euro_to_inr = 90.0
      user_for_emoney = self.user['username']
      e_wallet_for_emoney = wallet3
    
      if (money_value < 5) or (money_value > 50000):
        self.label_4.text = "Money value should be between 5 and 50000 for a transfer Funds."
      else:
        if selected_symbol == 'Є':  
            if float(user_currency['money_euro']) > money_value:
                user_currency['money_euro'] = str(float(user_currency['money_euro']) - money_value)
                fore_money['e_money'] = str(float(fore_money['e_money'] or 0) + (money_value * conversion_rate_euro_to_inr))
                
                # Update the 'e_money' value in the accounts table
                account_row = app_tables.accounts.get(casa=int(acc))
                account_row['e_money'] = fore_money['e_money']
                account_row.save()
            else:
                self.label_4.text = "Insufficient funds"
        elif selected_symbol == '$':
            if float(user_currency['money_usd']) > money_value:
              user_currency['money_usd'] = str(float(user_currency['money_usd']) - money_value)
              money_inr_equivalent_string = str(money_value * conversion_rate_usd_to_inr + float(fore_money['e_money'] or 0))
              #anvil.server.call('update_all_rows', user_for_emoney, money_inr_equivalent_string)
            else:
              self.label_4.text = "Insufficient funds"
        elif selected_symbol == '₣':
            if float(user_currency['money_swis']) > money_value:
              user_currency['money_swis'] = str(float(user_currency['money_swis']) - money_value)
              money_inr_equivalent_string = str(money_value * conversion_rate_swis_to_inr + float(fore_money['e_money'] or 0))
              #anvil.server.call('update_all_rows', user_for_emoney, money_inr_equivalent_string)
            else:
              self.label_4.text = "Insufficient funds"
        elif selected_symbol == '₹':
            if float(user_currency['money_inr']) > money_value:
              user_currency['money_inr'] = str(float(user_currency['money_inr']) - money_value)
              money_inr_equivalent_string = str(money_value * 1 + float(fore_money['e_money'] or 0))
              #anvil.server.call('update_all_rows', user_for_emoney, money_inr_equivalent_string)
            else:
              self.label_4.text = "Insufficient funds"
        else:
          self.label_4.text = "Error: Invalid currency symbol selected."
        
      new_transaction = app_tables.transactions.add_row(
                user=self.user['username'],
                casa=int(acc),
                e_wallet=wallet3,
                money=f"{selected_symbol}-{money_value}",
                date=current_datetime,
                transaction_type="Money transferred"
            )
      open_form('transfer',user=self.user)
      

    def display(self, **event_args):
        acc=self.dropdown_account_numbers.selected_value
        user_for_emoney = self.user['username']
        print(acc)
        fore_money = anvil.server.call('get_accounts_emoney',acc)
        acc_validate = anvil.server.call('validate_acc_no_to_display_in_transfer',acc)
        self.label_6.text = "$" + str(acc_validate['money_usd'])
        self.label_10.text = "₹ " + str(acc_validate['money_inr'])
        self.label_11.text = "€ " + str(acc_validate['money_euro'])
        self.label_12.text = "₣ " + str(acc_validate['money_swis'])
        e_money_value = str(fore_money['e_money'])
        eb= self.drop_down_2.selected_value
        if e_money_value and e_money_value != 'None' and e_money_value.replace('.', '', 1).isdigit() and eb == '$':
           try:
             e_money_value = float(e_money_value)
             dollar_to_rupee = e_money_value / 80.0  # Set a default value, adjust as needed
             self.label_14.text = str(dollar_to_rupee)
           except ValueError:
              # Handle the case where e_money_value cannot be converted to a float
             # Provide a default value or display an error message
             pass  # You might add specific handling or error message here
           else:
              # Handle the case where e_money_value is None or eb is not '$'
             # For example, provide a default value or display an error message
             pass  # You might add specific handling or error message here
        if eb == 'Є':
          euro_to_rupee = (e_money_value)/90.0
          self.label_14.text = euro_to_rupee
          # anvil.server.call('update_all_rows', user_for_emoney, money_inr_equivalent_string)
        if eb == '₣':
          swis_to_rupee = (e_money_value)/95
          self.label_14.text = swis_to_rupee

        if eb == '₹':
          self.label_14.text = (e_money_value)

    def drop_down_2_change(self, **event_args):
      acc=self.dropdown_account_numbers.selected_value
      fore_money = anvil.server.call('get_accounts_emoney',acc)
      e_money_value = float(fore_money['e_money'])
      eb= self.drop_down_2.selected_value
      if eb == '$':
          dollar_to_rupee = (e_money_value)/80.0
          self.label_14.text = dollar_to_rupee
      if eb == 'Є':
          euro_to_rupee = (e_money_value)/90.0
          self.label_14.text = euro_to_rupee
      if eb == '₣':
          swis_to_rupee = (e_money_value)/95.0
          self.label_14.text = swis_to_rupee
      if eb == '₹':
          self.label_14.text = (e_money_value)

    def dropdown_account_numbers_change(self, **event_args):
      self.display()

    def link_8_click(self, **event_args):
      open_form('deposit',user= self.user)

    def link_10_click(self, **event_args):
      open_form('withdraw',user= self.user)
