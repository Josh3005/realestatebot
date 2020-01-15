import requests
from requests import get
from bs4 import BeautifulSoup
import pandas
import itertools
import streamlit as st

def net_operating(rent, tax_rate, price):
    
    #Takes input as monthly mortgage amount and monthly rental amount
    #Uses managment expense, amount for repairs, vacancy ratio
    #Example input: net_operating(1000,1,400,200)
    #879.33
    #1000 - 16.67 (tax) - 100 (managment) - 4 (repairs)
    
    mortgage_amt = mortgage_monthly(price,20,3)
    prop_managment = rent * 0.10
    prop_tax = (price * (tax_rate/100)/12)
    prop_repairs = (price * 0.02)/12
    vacancy = (rent*0.02)
    #These sections are a list of all the expenses used and formulas for each
    
    net_income = rent - prop_managment - prop_tax - prop_repairs - vacancy - mortgage_amt
    #Summing up expenses
    output = [prop_managment, prop_tax, prop_repairs, vacancy, net_income]
  
    
    return output

def down_payment(price,percent):
    #This function takes the price and the downpayment rate and returns the downpayment amount 
    #Ie down_payment(100,20) returns 20
    amt_down = price*(percent/100)
    return(amt_down)

def mortgage_monthly(price,years,percent):
    
    
    #This implements an approach to finding a monthly mortgage amount from the purchase price,
    #years and percent. 
    #Sample input: (300000,20,4) = 2422
    #
    
    
    percent = percent /100
    down = down_payment(price,20)
    loan = price - down
    months = years*12
    interest_monthly = percent/12
    interest_plus = interest_monthly + 1
    exponent = (interest_plus)**(-1*months)
    subtract = 1 - exponent
    division = interest_monthly / subtract
    payment = division * loan
    
    
    return(payment)


def price_mine(url):
    #Currently this function takes an input of a URL and returns the listing prices 
    #The site it mines is remax
    #The input must be a string input, we can reformat the input to force this to work
    #Next we use regex to remove space and commas and dollar signs 
    headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    response = get(url)
    response_text = response.text
    html_soup = BeautifulSoup(response_text, 'html.parser')
    prices = html_soup.find('h2',{'class': 'price'}).text
    prices = prices.replace(",", "")
    prices = prices.replace("$", "")
    prices = prices.replace(" ", "")
    prices = float(prices)
  
    return prices
    
    
def cap_rate(monthly_income, price):
    #This function takes net income, and price and calculates the cap rate
    #
    cap_rate = ((monthly_income*12) / price)*100
    
    return cap_rate


def cash_on_cash(monthly_income, down_payment):
    cash_return = ((monthly_income*12)/down_payment)*100
    return cash_return

st.write("""# Python Real Estate Investment Analysis Bot""")
st.write("""Any real estate listing can be automatically analyzed""") 

# trial = input("Enter a URL to a Remax listing:   ")
# rent_amt = input("Enter the monthly rent price:  ")
# property_tax = input("Enter the tax rate:  ")
#We have to change these generic inputs to streamlit inputs

trial = st.sidebar.text_input("Enter the listing URL:   ")
rent_amt = st.sidebar.text_input("Enter the monthly rent price:   ")
property_tax = st.sidebar.text_input("Enter the tax rate:   ")

trial = str(trial)
rent_amt = float(rent_amt)
property_tax = float(property_tax)


listing_notice = price_mine(trial)
mortgage = mortgage_monthly(listing_notice, 20, 3)

cash = down_payment(listing_notice, 20)
net_income = net_operating(rent_amt, property_tax , listing_notice)
monthly_cash = net_income[4]
cap_return = cap_rate(monthly_cash,listing_notice)
cash_percent = cash_on_cash(monthly_cash,cash)
# net_operating(rent, tax_rate, mortgage_amt, price):

# print("INPUT: ")
# print("The price of: ", listing_notice) 
# print("The monthly rent of : ", rent_amt)
# print("The tax rate of : ", property_tax)
# print("OUTPUTS: ")
# print("Monthly mortgage of  :  ",mortgage)
# print("Net operating income:  ", net_income)
# print("Cap rate of:  ", cap_return," % ")
# print("Cash return rate of:  ", cash_percent, " % ")

#We have to convert the above outputs to streamlit outputs 

st.write("The monthly cashflow is: ")
st.write(monthly_cash)
st.write("The cap rate is: ")
st.write(cap_return)
st.write("The cash on cash return rate is: ")
st.write(cash_percent)