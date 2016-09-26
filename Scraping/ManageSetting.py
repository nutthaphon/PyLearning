
from scrapy.settings import Settings


setting1 = Settings()


#print(setting1.set('DOWNLOAD_DELAY', 2))
#print(setting1.set('COOKIES_ENABLED', False))

print(setting1.get('USER_AGENT'))
print(setting1.get('DOWNLOAD_DELAY'))
print(setting1.get('COOKIES_ENABLED'))



