import requests as req
from tkinter import *
import json
import os
import ast
from passlib.hash import pbkdf2_sha256
from datetime import date
class Table:
  def __init__(self,root,rows,columns,lst):
    for i in range(rows):
      for j in range(columns):
        self.e = Label(root, width=20, font=('Arial',16,), text = lst[i][j], borderwidth = 0.5, relief = 'solid', bg = 'white')
        self.e.grid(row=i, column=j)
def main(username):
    root = Tk()
    root.geometry('500x500')
    root.title("Home")
    root.configure(background='white')
    Label(root, text = "Hello! Do you want to go to stocks, forum, profile, chat, or quit?", font = ('arial bold', 14 ), underline = True, background='white').pack()
    Button(root, text = "Stocks", command=lambda :get_stocks(username), background = 'salmon', width = 30, height = 2).pack()
    Button(root, text = "Forum", command=lambda :forum(username), background = 'green', width = 30, height = 2).pack()
    def profile():
      root1 = Tk()
      root1.title(stats['User']+"'s Profile'")
      root1.configure(background = 'white')
      Label(root1, text="Username:"+stats['User'],font=('arial bold', 30), bg = 'white').pack()
      Label(root1, text='Money: $' + str(stats['Money']),font=('arial bold',20), bg = 'white').pack()
      for i in stats:
        if i == 'User' or i == 'Password' or i == 'Money':
          pass
        else:
          this_stock_table = [
            ("Stock Key", i),
            ("Price per share", stats[i]['price']),
            ("Share amount", stats[i]['shares'])
          ]
          profile_frame = Frame(root1)
          profile_frame.pack()
          Table(profile_frame, 3, 2, this_stock_table)
          Label(root1, text = " \n ", bg = 'white').pack()
          # stock_string = str(j['shares']) + ' share(s) of ' + i + ', price $' + str(j['price'])
          # Label(root1, text=stock_string, font=('arial bold', 20)).pack()
    Button(root, text = "My Profile", command=profile, background='aqua', width = 30, height = 2).pack()
    Button(root, text = "Quit", command=quit, background='purple', width = 30, height = 2).pack()
def forum(username):
  fs = open("forum.text", 'r+')
  root3 = Tk()
  root3.title("Forum")
  root3.geometry('500x500')
  root3.configure(background = 'white')
  full_chat = Label(root3, text = fs.read(), font = ('Arial', 8, "bold"), bg = 'white').pack()
  chat_text = Text(root3, height = 2, bg = 'white')
  with open("forum.text", 'r+') as fp:
    line_count = len(fp.readlines())   
  if line_count >= 20 and line_count <= 25:
    fs4 = open("forum.text", 'a')
    fs4.write("\nChat is purging in " + str(26 - line_count))
  elif line_count >= 26:
    fs2 = open("forum.text", 'w')
    fs3 = open("archive.text", 'a')
    fs3.write(fs.read())
    fs2.write('')
  chat_text.pack()
  def post_msg():
    msg = chat_text.get('1.0', 'end-1c')
    fs1 = open("forum.text", 'a')
    fs1.write('\n' + username + ' says: ' + msg)
    fs1.close()
    root3.destroy()
    forum(username)
  Button(root3, text = "Post to Chat", command = post_msg, bg = 'forestgreen').pack()

def get_stocks(username):
  root2 = Tk()
  root2.geometry('500x500')
  root2.title("Stocks")
  root2.configure(background = 'white')

  Label(root2, text = "Enter a stock key.", fg = 'black', bg = 'white').pack()
  inputbox = Text(root2, padx = 40, pady = 30, height = 1)
  inputbox.pack()
  name = ""
  def search_function():
    
    name = inputbox.get("1.0","end-1c")
    layout(name.upper())
  search = Button(root2, text = "Search Info", background = "chocolate", command = search_function, fg = 'white').pack()
  def layout(name):
    root1 = Tk()
    root1.geometry('500x500')
    root1.title(name)
    root1.configure(background = 'white')
    info = req.get('https://finnhub.io/api/v1/stock/candle?symbol=' + name + '&count=5&token=cc36ju2ad3i96jb01qg0&resolution=D&from=' + str(date.today()) + '&to=' + str(date.today()))
    info1 = req.get('https://finnhub.io/api/v1/quote?symbol=' + name + '&token=cc36ju2ad3i96jb01qg0')
    data = info.json()
    data1 = info1.json()
    vol_len = len(data['v'])
    vol = data['v'][vol_len - 1]
    price = data1['c']
    price *= 100
    price = round(price)
    price /= 100
    percent = data1['dp']
    if percent < 0:
        fg = 'red'
    elif percent > 0:
        fg = 'green'
    elif percent == 0:
        fg = 'gray'
    thislist = [
      ("Title", name),
      ("Company Size", vol),
      ("Price per share", '$' + str(price))
    ]
    row_amount = 3
    col_amount = 2
    frame = Frame(root1)
    frame.pack()
    Table(frame, row_amount, col_amount, thislist)
    color = 'red' if percent < 0 else 'green' if percent > 0 else 'gray'
    Label(root1, text = str(percent) + '%', fg = color, bg = 'white').pack()
    try:
      if type(stats[name]) == type({'x':2}):
          sell_shares = Text(root1, height = 5)
          sell_shares.pack()
          stats["Money"] *= 100
          stats["Money"] = round(stats["Money"])
          stats["Money"] /= 100
          def sell():
            share_amount = sell_shares.get('1.0', 'end-1c')
            share_amount = int(share_amount)
            if share_amount > stats[name]['shares']:
              help_me=Tk()
              help_me.geometry('400x400')
              help_me.title('Alert')
              Label(help_me, text='You do not have that many shares',font=('arial bold',12)).pack()
            elif share_amount == stats[name]['shares']:
              stats["Money"] += share_amount * price
              stats["Money"] *= 100
              stats["Money"] = round(stats["Money"])
              stats["Money"] /= 100
              del(stats[name])
            elif share_amount < stats[name]['shares']:
              stats[name]['shares'] -= share_amount
              stats["Money"] += share_amount * price
              stats["Money"] *= 100
              stats["Money"] = round(stats["Money"])
              stats["Money"] /= 100
            root1.destroy()
            f = open(username + '.txt', 'w')
            f.write(str(stats))
            f.close()
            
          Button(root1, text = "Sell shares", command = sell, bg = 'white').pack()
          
      share_amount = Text(root1, height = 5)
      share_amount.pack()
      def buy_shares():
          shares = share_amount.get('1.0', 'end-1c')
          shares = int(shares)
          cost = shares * price
          if cost <= stats["Money"]:
              stats["Money"] -= cost;
              stats["Money"] *= 100
              stats["Money"] = round(stats["Money"])
              stats["Money"] /= 100
              purchase=Tk()
              purchase.geometry('300x300')
              purchase.title('Confirmation')
              Label(purchase,text="You have purchased " + str(shares) + " share(s).", font=('Arial',12)).pack()
              stats[name] = {'shares': shares + stats[name]['shares'], 'price': price}
              root1.destroy()
              f = open(username + '.txt', 'w')
              f.write(str(stats))
              f.close()
          else:
              alert=Tk()
              alert.geometry('200x200')
              alert.title('Alert')
              Label(alert, text = "You can't afford this.", font = ('arial bold', 12 ), underline = True, background='white', fg = 'red').pack()            
      Button(root1, command = buy_shares, text = "Buy shares", bg = 'white').pack()
      if price > 500:
          Label(root1, text = "Definitely consider investing because the earnings you would get is phenomenal!", bg = 'white').pack()
      elif price > 100:
          if percent > 1:
            Label(root1, text = "You may want to consider investing, because the earnings are decent and the stock may go up much more soon.", bg = 'white').pack()
          elif percent < 1:
            Label(root1, text = "Think about how much people would need this product depending on the time, because this stock may fall and cause turmoil in your credit card.", bg = 'white').pack()
      else:
          Label(root1, text = "You may not want to invest in this stock because it stands quite low now, and you may want to invest in it later, if it grows.", bg = 'white').pack()
    except KeyError:
      share_amount = Text(root1, height = 5)
      share_amount.pack()
      def buy_shares():
          shares = share_amount.get('1.0', 'end-1c')
          shares = int(shares)
          cost = shares * price
          if cost <= stats["Money"]:
              Tel
              stats["Money"] -= cost
              stats["Money"] *= 100
              stats["Money"] = round(stats["Money"])
              stats["Money"] /= 100
              stats[name] = {'price': price, 'shares': shares}
              root1.destroy()
              f = open(username + '.txt', 'w')
              f.write(str(stats))
              f.close()
          else:
            alert = Tk()
            x = alert.winfo_screenwidth()/2 - 50
            y = alert.winfo_screenheight()/2 - 50
            alert.geometry('%dx%d+%d+%d' % (100, 100, x, y))
            alert.title("Message")
            alert.configure(background = 'red')
            Label(alert, text = "You don't have enough money to buy this!", bg = 'red').pack()
      Button(root1, command = buy_shares, text = "Buy shares", bg = 'white').pack()
      if price > 500:
          Label(root1, text = "Definitely consider investing because the earnings you would get is phenomenal!", bg = 'white').pack()
      elif price > 100:
          if percent > 1:
            Label(root1, text = "You may want to consider investing, because the earnings are decent and the stock may go up much more soon.", bg = 'white').pack()
          elif percent < 1:
            Label(root1, text = "Think about how much people would need this product depending on the time, because this stock may fall and cause turmoil in your credit card.", bg = 'white').pack()
      else:
          Label(root1, text = "You may not want to invest in this stock because it stands quite low now, and you may want to invest in it later, if it grows.", bg = 'white')

loginAttempts=5
openacc=input("Welcome to Capita Gain! This project was made by Anakin Dasgupta and Rian Chadha.\nDo you have an account? (Y or N) ")
if openacc.lower()=='y':
  login=input("What is your username? \n>")
  if os.path.isfile(login + '.txt'):
    askPassword = input('What is your password?  \n>')
    
    with open(login + '.txt', 'r') as f:
        data = f.read()
        stats = ast.literal_eval(data)
    while not pbkdf2_sha256.verify(askPassword, stats['Password']) and loginAttempts > 0:
        print('Wrong password')
        loginAttempts -= 1
        askPassword = input('What is your password?  \n>')
    else:
        if loginAttempts <= 0:
            print('Too many failed tries. Please reload')
            exit()
        else:
          print('Logged in!')
          print("Fullscreen is recommended.")
          main(login)
  else:
    print("We couldn't find your account. Please try again. ")
    exit()
elif openacc.lower()=='n':
    print('Welcome!')
    stats = {'Money':1000}

    newuser = input('What would you like your user name to be?\n>')
    while True:
        if newuser == 'no':
            print('Sorry, this name cannot be used.')
            newuser = input('What would you like your user name to be?  \n>')
        elif os.path.isfile(newuser + '.txt'):
            a = input(
                'This name is in use. Do you have an account? (Yes or no) \n>')
            if a.lower() == 'yes':
                print('Please reload.')
                exit()
            elif a.lower() == 'no':
                newuser = input(
                    'What would you like your user name to be?  \n>')
        else:
            break

    name = open(str(newuser) + '.txt', 'w')
    stats.__setitem__('User', (newuser))
    pwd = input('What would you like your password to be? \n>')
    pwd= pbkdf2_sha256.hash(pwd)
    stats.__setitem__('Password', pwd)
    name.write(str(stats))
    print('Adding...\n')
    name.close()
    print(
        'Thank you for creating an account! Please reload, then try to log in.'
    )
    exit()

else:
    print(
        'There was an error logging in. Please reload, or your information will not be saved.'
    )
    exit() 
