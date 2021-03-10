from apscheduler.schedulers.background import BackgroundScheduler

from weather.views import WeatherViewset




def start():
    scheduler = BackgroundScheduler()
    weather = WeatherViewset()
    # weather.save_reportstation()
    # weather.call_schedu()
    scheduler.add_job(weather.call_schedu, "interval", minutes=15, id="report_001", replace_existing=True)
    # weather.save_weatherdata()
    # scheduler.add_job(weather.save_reportstation,"interval",minutes=15,id="weather_data_001",replace_existing=True)
    # scheduler.add_job(weather.export() ,"interval" , minutes=15 ,id="history_data_001" , replace_existing=True)
    scheduler.start()
