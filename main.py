import smtplib
my_email = Your email
my_pass = Your password
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import requests
firstname = input("Enter your first name")
lastname = input("Enter your last name")
email =input("Enter your email")

body ={
    "user":{
        "firstname": firstname,
        "lastname": lastname,
        "email":email
    }
}

SHEETY = user endpoint
response = requests.post(url=SHEETY,json=body)
print(response.text)
get_email = requests.get(url=SHEETY)
getemails =get_email.json()["users"]
users = len(getemails)
users_emails = [i["email"] for i in getemails]
print(users_emails)

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = Your origin city

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    try:
        if flight.price < destination["lowestPrice"]:
            message = f"Low price alert! Only {flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
            notification_manager.send_sms(
                message=message
            )
            for user in users_emails:
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()
                    connection.login(user=my_email, password=my_pass)
                    connection.sendmail(from_addr=my_email, to_addrs=email,
                                        msg=message)
                print("Your email has been succesfully sent")

    except AttributeError:
        None
