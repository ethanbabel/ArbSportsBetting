import schedule
import update_database
import send_email
import traceback2 as traceback
import time

def update_and_send():
    print("Updating All Data ...")
    successful = update_database.update_all()
    if successful:
        print("Database Updated")
        print("Sending Arbitrage Opportunites... ")
        send_email.send_arbs()
        print("Arbitrage Opportunites Sent. ")
    else:
        send_email.send_API_limit_reached()

def keep_alive():
    print("Keeping Alive... ")
    update_database.ping()

# times = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
#         '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
#         '12:00', '13:00', '14:30', '14:00', '15:00', '16:00', '17:00',
#         '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
# for t in times:
#     schedule.every().day.at(t).do(update_and_send)

schedule.every().day.at("00:00").do(update_and_send)
schedule.every(10).minutes.do(keep_alive)

while True:
    try:
        schedule.run_pending()
        print('pending...')
        time.sleep(1)
    except Exception as e:
        traceback.print_exc()
        traceback_info = traceback.format_exc()
        send_email.send_error(traceback_info)
