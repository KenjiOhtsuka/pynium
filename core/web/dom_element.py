from datetime import date
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.by import By

class DomElement():
    def __init__(self, web_element):
        """

        :param web_element: webelement
        :return:
        """
        self.web_element = web_element

    def has_element(self, css_selector) -> str:
        """

        :param css_selector:
        :return:
        """
        if 0 < len(self.web_element.find_elements_by_css_selector(css_selector)):
            return True
        return False

    def find_element(self, css_selector):
        return self.web_element.find_element_by_css_selector(css_selector)

    def find_elements(self, css_selector) -> list:
        elements = self.web_element.find_elements_by_css_selector(css_selector)
        return DomElementFactory.create_dom_element_list(elements)

    def click(self):
        """
        click the element
        :return:
        """
        self.web_element.click()
        return self

    def double_click(self):
        """
        double click the element
        :return:
        """
        driver = self.web_element.parent
        driver.double_click(self)
        return self

    def get_classes(self) -> list:
        """
        get classes of element and return sorted list
        :return: list
        """
        class_attribute = self.get_attribute('class')
        if class_attribute == None:
            return []
        classes = list(set(class_attribute.split()))
        classes.sort()
        return classes

    def get_attribute(self, attribute_name) -> str:
        return self.web_element.get_attribute(attribute_name)

    def has_attribute(self, attribute_name) -> bool:
        if self.web_element.get_attribute(attribute_name) == None:
            return False
        return True

    def get_tag_name(self) -> str:
        return self.web_element.tag_name

    def get_parent(self):
        return self.web_element.find_element(By.xpath('..'))

    def get_style(self, property_name):
        return self.web_element.value_of_css_property(property_name)

    def get_text(self) -> str:
        return self.web_element.text

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

class Input(DomElement):
    def get_value(self) -> str:
        return self.get_attribute('value')

class TextInput(Input):
    def set_input_text(self, value):
        self.web_element.clear()
        self.web_element.sendKeys(value)
        return self

class NumberInput(Input):
    def set_input_text(self, value):
        self.web_element.clear()
        self.web_element.sendKeys(value)
        return self

class CheckBox(Input):
    def is_checked(self) -> bool:
        return self.web_element.is_selected()

    def check(self):
        if not self.is_checked():
            self.web_element.click()
        return self

class RadioButton(Input):
    def is_selected(self):
        return self.web_element.is_selected()

    def select(self):
        if not self.is_selected():
            self.web_element.click()
        return self

class Button(DomElement):
    def get_type(self):
        if 'button' == self.get_attribute('type'):
            return 'button'
        else:
            return 'submit'

class TextArea(DomElement):
    def get_rows(self) -> int:
        """
        get rows value as int
        :return:
        """
        rows = self.get_attribute('rows')
        if (None == rows or 0 == len(rows)):
            return None
        return int(rows)

    def get_cols(self) -> int:
        """
        get cols value as int
        :return:
        """
        cols = self.get_attribute('cols')
        if (None == cols or 0 == len(cols)):
            return None
        return int(cols)

class Anchor(DomElement):
    def get_link_url(self) -> str:
        return self.get_attribute('href')

    def get_title(self) -> str:
        return self.get_attribute('title')

    def get_target(self) -> str:
        return self.get_attribute('target')

class Img(DomElement):
    def get_img_src(self) -> str:
        return self.get_attribute('src')

    def get_alt(self) -> str:
        return self.get_attribute('alt')

class Ul(DomElement):
    def get_items(self) -> list:
        li_list = self.web_element.find_elements(By.xpath('/li'))
        return DomElementFactory.create_dom_element_list(li_list)

class Ol(DomElement):
    def get_items(self) -> list:
        li_list = self.web_element.find_elements(By.xpath('/li'))
        return DomElementFactory.create_dom_element_list(li_list)

class DomElementFactory():
    @staticmethod
    def create_dom_element(ingredient) -> DomElement:
        """

        :param ingredient: webelement
        :return:
        """
        tag_name = ingredient.tag_name
        if 'input' == tag_name:
            type = ingredient.get_attribute('type')
            if 'text' == type:
                return TextInput(ingredient)
            elif 'number' == type:
                return NumberInput(ingredient)
            elif 'radio' == type:
                return RadioButton(ingredient)
            elif 'checkbox' == type:
                return CheckBox(ingredient)
            return Input(ingredient)
        elif 'textarea' == tag_name:
            return TextArea(ingredient)
        elif 'a' == tag_name:
            return Anchor(ingredient)
        elif 'img' == tag_name:
            return Img(ingredient)
        elif 'ul' == tag_name:
            return Ul(ingredient)
        elif 'ol' == tag_name:
            return Ol(ingredient)
        return DomElement(ingredient)

    @staticmethod
    def create_dom_element_list(ingredient_list) -> DomElement:
        """

        :param ingredient_list: list
        :return:
        """
        return map(
            lambda i: DomElementFactory.create_dom_element(i),
            ingredient_list)

class Cookie():
    def __init__(self, name):
        self.set_name(name)
        self.set_value('')
        self.set_path(None)
        self.set_domain(None)
        self.set_secure(None)
        self.set_expiry(None)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_value(self, value):
        self.__value = value
        return self

    def get_value(self):
        return self.__value

    def set_secure(self, value):
        """

        :param value: bool
        :return:
        """
        self.__secure = value
        return self

    def get_secure(self) -> bool:
        return self.__secure

    def set_path(self, value):
        """

        :param value: str
        :return:
        """
        self.__path = value
        return self

    def get_path(self) -> str:
        return self.__path

    def set_domain(self, value):
        self.__domain = value
        return self

    def get_domain(self):
        return self.__domain

    def set_expiry(self, value):
        self.__expiry = value
        return self

    def get_expiry(self):
        return date.fromtimestamp(self.__expiry)

    def get_expiry_int(self):
        return self.__expiry

    def to_dict(self):
        cookie_dict = {
            'name': self.get_name(),
            'value': self.get_value()}
        if None != self.get_path():
            cookie_dict['path'] = self.get_path()
        if None != self.get_domain():
            cookie_dict['domain'] = self.get_domain()
        if None != self.get_secure():
            cookie_dict['secure'] = self.get_secure()
        if None != self.get_expiry():
            cookie_dict['expiry'] = self.get_expiry_int()
        return cookie_dict

class CookieFactory():
    @staticmethod
    def create_cookie(cookie_dict):
        return Cookie(cookie_dict['name']).\
            set_domain(cookie_dict['domain']).\
            set_value(cookie_dict['value']).\
            set_secure(cookie_dict['secure']).\
            set_value(cookie_dict['value']).\
            set_expiry(cookie_dict['expiry'])

    @staticmethod
    def create_cookie_list(cookie_dict_list):
        return map(
            lambda c: CookieFactory.create_cookie(c),
            cookie_dict_list)