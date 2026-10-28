from datetime import date , time , datetime 


today=date.today()
print("todays date is ", today)
now = datetime.now()
print("\ncurrent date and time is ", now)

print("\ndate components: ", today.day, today.month, today.year)