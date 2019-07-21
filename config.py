import os
import configparser
SETTINGS_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.ini')

class Settings:
    def __init__(self):
        self.settings = self.populate_settings()

    class SectionNames:
        Database = 'database'
        AppSettings='app_settings'
        Cookie = 'cookie'

    class SettingNames:
        DbHost = 'db_host'
        DbPort = 'db_port'
        DbName = 'db_name'
        AutoReload = 'auto_reload'
        CookieSecret= 'cookie_secret'

    @property
    def CookieSecret(self):
        return self.get_setting(self.SectionNames.AppSettings, self.SettingNames.CookieSecret)

    @property
    def DbHost(self):
        return self.get_setting(self.SectionNames.Database, self.SettingNames.DbHost)

    @property
    def DbPort(self):
        return self.get_setting(self.SectionNames.Database, self.SettingNames.DbPort)

    @property
    def DbName(self):
        return self.get_setting(self.SectionNames.Database, self.SettingNames.DbName)

    @property
    def AutoReload(self):
        return self.get_setting(self.SectionNames.AppSettings, self.SettingNames.AutoReload)




    def populate_settings(self):
        config = configparser.ConfigParser()
        config.read(SETTINGS_PATH)
        return config

    def get_setting(self, section_name, option_name):
        if not section_name and not option_name:
            raise ValueError
        return self.settings.get(section_name, option_name)
