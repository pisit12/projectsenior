from apscheduler.schedulers.background import BackgroundScheduler

from weather.views import WeatherViewset




def start():
    scheduler = BackgroundScheduler()
    weather = WeatherViewset()
    # weather.call_schedu()
    scheduler.add_job(weather.call_schedu, "interval", minutes=15, id="report_001", replace_existing=True)
    scheduler.start()
