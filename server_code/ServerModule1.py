import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from datetime import datetime, timedelta
import anvil.server
from anvil import tables, app
import time
import random
import uuid
# server_module.py

# Function to validate login credentials
@anvil.server.callable
def validate_login(username, password):
    # Query the 'users' table
    user = tables.app_tables.users.get(username=username, password=password)

    if user:
        return user['usertype']
    else:
        return None



@anvil.server.callable
def add_info(email, username, password, pan, address, phone, aadhar):
    user_row = app_tables.users.add_row(
        email=email,
        username=username,
        password=password,
        pan=pan,
        address=address,
        phone=phone,
        aadhar=aadhar,
        usertype='customer',
        confirmed=True,
        limit=100000
    )
    return user_row

@anvil.server.callable
def generate_unique_id(username, phone):
    unique_id = f"{username}-{phone}"

    return unique_id
  

def convert_to_inr(amount, currency):
    conversion_rates = {
        'usd': 75.0,   # Replace with actual rates
        'euro': 85.0,  # Replace with actual rates
        'inr': 1.0,    # 1:1 conversion for INR
        'swiss': 80.0  # Replace with actual rates
        # Add more currencies as needed
    }

    return amount * conversion_rates[currency.lower()]

# Define a function to transfer money to e_wallet
@anvil.server.callable
def transfer_money(username, amount, selected_currency):
    # Get the current user's data from the accounts table
    account_row = app_tables.accounts.get(user=username)

    # Convert the entered amount to INR
    amount_inr = convert_to_inr(float(amount), selected_currency)

    # Update the e_wallet column with the transferred amount
    account_row['e_wallet'] += amount_inr

    # Update the specific currency column with the transferred amount
    currency_column = f'money_{selected_currency.lower()}'
    account_row[currency_column] -= float(amount)

    # Save the changes to the accounts table
    account_row.save()

    # Return a success message or any relevant information
    return f"Transferred {amount} {selected_currency} to e_wallet for {user_id}"


# for deposit
@anvil.server.callable
def get_currency_data(acc):
    currency_table = app_tables.currencies.get(casa= int(acc))
    return currency_table

# fot populating the dropdown section
@anvil.server.callable
def get_user_account_numbers(username):
    # Fetch all matching rows for the specified user
    user_currencies = app_tables.currencies.search(user=username)
    # Extract 'casa' values from all matching rows
    return [str(currency['casa']) for currency in user_currencies]
  
#for the transfer form
@anvil.server.callable
def validate_acc_no_to_display_in_transfer(acc):
  user_validate= app_tables.currencies.get(casa=int(acc))
  return user_validate

#for getting the e_money in accounts
@anvil.server.callable
def get_accounts_emoney(acc):
  user_emoney= app_tables.accounts.get(casa=int(acc))
  return user_emoney

# for keeping the e_wallet same throughout
@anvil.server.callable
def update_all_rows(user,e_money_value):
    # Print statements with proper formatting
    print("hi this is server code")
    print(f"E-money: {e_money_value}")
    matching_rows = app_tables.accounts.search(user=user)
    
    for row in matching_rows:
        row['e_money'] =e_money_value
        row.update()

@anvil.server.callable
def update_rows_emoney_trasaction(wallet, e_money_value):
  matching_rows = app_tables.accounts.search(e_wallet=wallet)
  print("hi we will start deducting")
  for row in matching_rows:
    row['e_money'] = e_money_value
    row.update()

#for getting the e_money in accounts using wallet id
@anvil.server.callable
def get_accounts_emoney_using_wallet_id(wallet):
    print(f"Received wallet ID: {wallet}")

    user_emoney = app_tables.accounts.search(e_wallet=wallet)

    if len(user_emoney) == 1:
        # If only one row is found, return it
        result = user_emoney[0]
        print(f"Found user emoney: {result}")
        return result
    elif len(user_emoney) > 1:
        # If multiple rows are found, handle the first one
        print("Multiple rows found. Handling only the first one.")
        result = user_emoney[0]
        return result
    else:
        # If no rows are found, return None
        print("No matching row found.")
        return None


@anvil.server.background_task
def refresh_transaction_limit():
    # Set the transaction limit to 100,000 every 24 hours
    while True:
        # Wait for 24 hours
        anvil.server.wait(24 * 60 * 60)  # 24 hours in seconds

        # Update the transaction limit to 100,000 for every user
        with anvil.server.transaction():
            users_table = app_tables.users
            all_users = users_table.search()  # Get all users in the table
            
            for user_record in all_users:
                user_record['limit'] = 100000
                users_table.update(user_record)

# Start the background task
refresh_transaction_limit()
@anvil.server.callable
def add_query(query):
  row=app_tables.sevices.add_row(Query=query)



    
    
        
