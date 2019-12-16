import os
import configparser
SETTINGS_PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.ini')

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
        AppName = 'app_name'
        Debug = 'debug'
        Version = 'version'
        KeyVersion = 'key_version'
        JwtAlgorithm = 'jwt_algorithm'

    @property
    def Version(self):
        version = self.get_setting(self.SectionNames.AppSettings, self.SettingNames.Version)
        return version

    @property
    def KeyVersion(self):
        key_version =  self.get_setting(self.SectionNames.AppSettings, self.SettingNames.KeyVersion)
        return int(key_version)

    @property
    def Debug(self):
        deb = self.get_setting(self.SectionNames.AppSettings, self.SettingNames.Debug)
        return bool(deb)

    @property
    def AppName(self):
        return self.get_setting(self.SectionNames.AppSettings, self.SettingNames.AppName)

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

    @property
    def JwtAlgorithm(self):
        return self.get_setting(self.SectionNames.AppSettings, self.SettingNames.JwtAlgorithm)

    def populate_settings(self):
        config = configparser.ConfigParser()
        config.read(SETTINGS_PATH)
        return config

    def get_setting(self, section_name, option_name):
        if not section_name and not option_name:
            raise ValueError
        return self.settings.get(section_name, option_name)