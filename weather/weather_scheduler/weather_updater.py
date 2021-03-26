from apscheduler.schedulers.background import BackgroundScheduler

from weather.views import WeatherViewset



def start():
    print("schedu")
    scheduler = BackgroundScheduler()
    # count+=1
    weather = WeatherViewset()


    # weather.save_listname()
    # weather.save_reportstation()
    # weather.save_pm()
    # weather.save_weatherdata()
    # weather.export()
    # weather.add_data_history()

    # weather.add_data_history()
    # weather.test()

    scheduler.add_job(weather.call_schedu, trigger="interval", minutes=15)
    # print(count)
    scheduler.start()
#schedule.every().seconds.at(":30").do(weather.call_schedu())


