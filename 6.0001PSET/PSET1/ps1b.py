# Problem Set 1B
# Name: Elahe Ahmadi
# Time Spent: Dont know 2 or 3h maybe  
# Declaring variables of the problem


# Declaring variables of the problem
annual_salary = float(input('What is your starting salary: '))
portion_saved = float(input('What is the portion of the salary you want to save: '))
total_cost = float(input('What is the total cost of your dream home: '))
semi_annual_raise = float(input('Insert your semi annual raise: '))
portion_down_payment = 0.18
current_savings = 0
r = 0.03
months = 0 
saved = 0
# Calculating the cost of down payment we need
down_payment_cost = round(total_cost * portion_down_payment,2) 

while saved <= down_payment_cost: 
    
    saved = (saved)* (1 + r/12)+ (annual_salary * portion_saved)/12 
    saved = round(saved, 2)
    print('amount saved = %f after %d of months' %(saved, months))
    months += 1
    if months%6==0:
        annual_salary = annual_salary * (1+ semi_annual_raise)
        print('Raise happened in this month %d and the new salary is %f'%
              (months, annual_salary))
        
    
    
    
print(months)



