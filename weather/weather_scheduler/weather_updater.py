from apscheduler.schedulers.background import BackgroundScheduler

from weather.views import WeatherViewset


def start():
    scheduler = BackgroundScheduler()
    weather = WeatherViewset()
    # weather.save_reportstation()
    scheduler.add_job(weather.save_reportstation, "interval", minutes=15, id="report_001", replace_existing=True)
    # weather.save_weatherdata()
    scheduler.add_job(weather.save_reportstation,"interval",minutes=15,id="weather_data_001",replace_existing=True)
    scheduler.start()
