from apscheduler.schedulers.background import BackgroundScheduler

from weather.views import WeatherViewset



def start():
    print("schedu")
    scheduler = BackgroundScheduler()
    # count+=1
    weather = WeatherViewset()
    # weather.export()
    # weather.forecast()
    # weather.call_schedu()
    # weather.history()
    # scheduler.add_job(weather.call_schedu, trigger="interval", minutes=10)
    # print(count)
    scheduler.start()
#schedule.every().seconds.at(":30").do(weather.call_schedu())


