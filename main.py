from datetime import datetime 
import json as js
file_name = "Expenses_Track.json"
def save_expense():
    with open(file_name , "w") as file:
        js.dump(expense, file , indent = 4 )

def load_expense():
    try:
        with open(file_name , "r") as file:
            return js.load(file)
    except FileNotFoundError:
        return []
expense = load_expense()

def add_expense():
    while True: 
        try:
            date = input("Enter Date in DD-MM-YYYY format.\n--->").strip().title()
            valid_date = datetime.strptime(date, "%d-%m-%Y")
            if 2000 <= valid_date.year <= 2030:
                break
            else:
                print("please type valid year")
        except ValueError:
            print("Invalid Date! please tyoe the date in this formate (DD-MM-YYYY) (e.g.: 15-08-2026).")

    category = input("Enter The Category of Item.\n--->").strip().title()
    title = input("Enter The Name of the Item (Title).\n--->").strip().title()
    
    
    while True:
        try:
            amount = float(input("Enter Amount Of the Item.\n--->")).strip().title()
            break
        except ValueError:
            print("Invalid Input! Kripya sirf number daalein.")
            
    new_expense = {
        "date" : date,
        "category" : category,
        "title" : title,
        "amount" : amount,
    }
    expense.append(new_expense)
    save_expense()
    print("Expences added successfully")


def view_expense():
    if not expense:
        print("Currently No Data Avilable")
    else:
        for index , requirement in enumerate(expense ,  start = 1):
            print(f"{index}. Date = {requirement['date']} | Category = {requirement['category']} | Name = {requirement['title']} | Amount = {requirement['amount']}")

def filter_expense():
    search_cat = input("Enter The Name of Catergory To Search:\n--->").strip().title()
    found = False
    for search in expense:
        if search['category'].lower() == search_cat.lower():
            print(f"Your Search Result is \nDate = {search['date']} | Category = {search['category']} | Name = {search['title']} | Amount = {search['amount']}")
            found = True
            
   
    if not found:
        print("No expenses found in this category!")

def delete_expense():
    if not expense:
        print("Currently No Data Available to Delete")
        return
    print(f"here is the list of all expenses")
    view_expense()
    choice = int(input("Enter Any number of the expense to delete\n--->")).strip().title()
    if 1 <= choice <= len(expense):
        expense.pop(choice - 1)
        print("Item deleted successfully")
        save_expense()
    else:
        print("Invalid number! Please choose a valid expense number.")
                   
def total_expense():
    total = 0
    for item in expense:
        total += item['amount']
    print(f"Your Total Amount of All Ecpenses : {total}")

def category_summary():
    if not expense:
        print("Currently No Data Available")
        return

    summary = {}
    for item in expense:
        cat = item['category'].lower()
        amt = item['amount']
        
        if cat in summary:
            summary[cat] += amt
        else:
            summary[cat] = amt
            
    print("Category-wise Spending:")
    for cat, total in summary.items():
        print(f"Category = {cat} | Total = {total}")



Done = True
while Done:
    print("-" * 40)
    try:
        permission = int(input("Select Any Number For Perfom Action\nAdd Expence Type 1\nView Expenses Type 2\nTo Search an Item Type 3\nTo See Total Type 4\nTo delete an Item Type 5\nFor summary of expenses Type 6\nTo Exit type 7\n--->"))
    except ValueError:
        print("Please Select any valid number!\n")
        continue

    if permission == 1:
        add_expense()
    elif permission == 2:
        view_expense()
    elif permission == 3:
        filter_expense()
    elif permission == 4:
        total_expense()
    elif permission == 5:
        delete_expense()
    elif permission == 6:
        category_summary()
    elif permission == 7:
        Done = False
        print("Have A Nice Day")
    else:
        print("Galat option! Kripya 1 se 7 ke beech number chunein.")
