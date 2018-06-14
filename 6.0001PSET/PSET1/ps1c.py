# Problem Set 1C
# Name: Elahe Ahmadi
# Time Spent: Dont know 2 or 3h maybe  
# Declaring variables of the problem

initial_deposit = int(input('What is your initial deposit: '))
total_cost = 800000
portion_down_payment = 0.30
months = 48
least_difference = 100 
upper_r = 10000
lower_r = 0
current_savings = 0
steps = 0
# Calculating the cost of down payment we need
down_payment_cost = total_cost * portion_down_payment

while True:
    steps += 1
    r = (upper_r + lower_r)/2
    current_savings = initial_deposit*((1+r/(12*10000))**months)
    print ('step = %d, current saving = %f, and down payment is = %f, r = %d' 
           %(steps, current_savings, down_payment_cost, r))
    if current_savings - down_payment_cost > least_difference:
        upper_r = r
    elif current_savings - down_payment_cost < 0: 
        lower_r = r
    elif current_savings - down_payment_cost < 0 and r >= 9999:   
        r = 'no r possible' 
    else:
        break
if r == 'no r possible':
    print('it is not possible to save for he down payment in 4 years')
print('The r = ',round(r/10000,4))
print('The steps= ', steps)



