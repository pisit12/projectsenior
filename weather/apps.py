from django.apps import AppConfig



class WeatherConfig(AppConfig):
    name = 'weather'

    def ready(self):
        # print("start scheduler")
        from weather.weather_scheduler import weather_updater
        weather_updater.start()