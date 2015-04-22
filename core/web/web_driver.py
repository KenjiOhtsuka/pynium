from enum import IntEnum
from datetime import date
from selenium import webdriver
from .dom_element import DomElement

class BrowserType(IntEnum):
    Firefox = 0
    Chrome = 1

class WebDriver():
    def __init__(self, browser_type):
        if (browser_type == BrowserType.Chrome):
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()

    def get(self, path):
        self.driver.get(path)

    def has_element(self, css_selector):
        """
        check element existence
        :param css_selector: str
        :return:
        """
        if len(self.driver.find_elements_by_css_selector(css_selector)) > 0:
            return True
        return False

    def find_element(self, css_selector):
        """
        find element by css selector
        :param css_selector: str
        :return:
        """
        return DomElement(self.driver.find_element_by_css_selector(css_selector))

    def find_elements(self, css_selector):
        """

        :param css_selector: str
        :return:
        """
        elements = self.driver.find_elements_by_css_selector(css_selector)
        return map(lambda e: DomElement(e), elements)

    def exec_javascript(self, script):
        """
        execute javascript
        :param script:
        :return:
        """
        self.driver.execute_script(script)
        return self

    def set_cookie(self, cookie_dict):
        """

        :param cookie_dict:
        :return:
        """
        if 'name' in cookie_dict and 'value' in cookie_dict:
            self.driver.add_cookie(cookie_dict)
            return self
        raise Exception('parameter should contain "name" and "value" entry.')

    def delete_cookie(self, cookie_name):
        """
        delete cookie
        exception doesn't occur when you delete non-existing cookie
        :param cookie_name:
        :return:
        """
        self.driver.delete_cookie(cookie_name)
        return self

    def delete_all_cookies(self):
        """
        delete all cookies
        :return:
        """
        self.driver.delete_all_cookies()
        return self

    def get_cookie(self, cookie_name):
        """
        get cookie value
        :param cookie_name:
        :return:
        """
        return self.driver.get_cookie(cookie_name)

    def get_whole_cookie(self) -> dict:
        """
        get whole cookie
        :return:
        """
        return self.driver.get_cookies()

    def quit(self):
        """
        close browser
        :return:
        """
        self.driver.quit()
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

class LogLevel(IntEnum):
    Off = 0
    Severe = 1
    Warning = 2
    Info = 3
    Debug = 4
    All = 5

class LogType(IntEnum):
    pass

class Log():
    def __init__(self, log_dict):
        self.__message = log_dict['message']
        if 'SEVERE' == log_dict['level']:
            self.__level = LogLevel.Severe
        elif 'WARNING' == log_dict['level']:
            self.__level = LogLevel.Warning
        elif 'INFO' == log_dict['level']:
            self.__level = LogLevel.Info
        elif 'DEBUG' == log_dict['level']:
            self.__level = LogLevel.Debug
        else:
            self.__level = None
        self.__type = log_dict['type']
        self.__timestamp = log_dict['timestamp']

    def get_message(self):
        return self.__message

    def get_type(self):
        return self.__type

    def get_level(self):
        return self.__level

    def get_timestamp(self):
        return date.fromtimestamp(self.__timestamp / 1000)

    def get_timestamp_int(self):
        return self.__timestamp

class LogFactory():
    @staticmethod
    def create_log(log_dict):
        return Log(log_dict)

    @staticmethod
    def create_log_list(log_dict_list):
        return map(
            lambda l: LogFactory.create_log(l),
            log_dict_list
        )