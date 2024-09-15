import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestRun:
    def __init__(self, website: str, driver):
        self.website = website
        self.driver = driver
        self.wait_download = 5
        self.wait_show = 1.5
        self.error_on = False
        self.driver.get(website)

    def wait_load(self, teg_id: str):
        """
        Ожидание прогрузки страницы до появления элемента с id=teg_id
        """
        if not self.error_on:
            try:
                myElem = WebDriverWait(self.driver, self.wait_download).until(
                    EC.presence_of_element_located((By.ID, teg_id)))
                print(f'Успешно на странице найден тег с id: "{teg_id}"')
            except TimeoutException:
                print(f'ОШИБКА: Загрузка заняла слишком много времени, искомый id: "{teg_id}"')
                self.error_on = True
            # Ожидание для отображения
            self.wait_01()

    def wait_01(self):
        """
        Ожидание при отображении теста
        """
        if not self.error_on:
            time.sleep(self.wait_show)

    def set_input_text(self, teg_id, new_text: str):
        """
        Задание текста элемента с id=teg_id
        """
        if not self.error_on:
            try:
                self.driver.find_element(By.ID, teg_id).send_keys(new_text)
                print(f'Успешно задан текст "{new_text}" для элемента с id "{teg_id}"')
            except:
                print(f'ОШИБКА: Не задан текст "{new_text}" для элемента с id: "{teg_id}"')
                self.error_on = True

    def run_click(self, teg_id):
        """
        Нажатие на кнопку с id=teg_id
        """
        if not self.error_on:
            try:
                self.driver.find_element(By.ID, teg_id).click()
                print(f'Успешно выполнен клик по элементу с id "{teg_id}"')
            except:
                print(f'ОШИБКА: Не выполнен клик по элементу с id: "{teg_id}"')
                self.error_on = True

    def check_text(self, text):
        """
        Проверка наличия текста на странице
        """
        if not self.error_on:
            rez = text in self.driver.page_source
            if rez:
                print(f'Успешно найден текст "{text}"')
            else:
                print(f'ОШИБКА: Не найден текст "{text}"')
                self.error_on = True
            return rez

    def close_driver(self):
        """
        Закрытие окна браузера
        """
        if not self.error_on:
            self.driver.close()


if __name__ == "__main__":
    # Создание объекта выполняющего тестирование
    test = TestRun("https://www.saucedemo.com/", webdriver.Firefox())
    # test = TestRun("https://www.saucedemo.com/", webdriver.Chrome())

    # Проведение теста

    # Ожидание кнопки авторизации
    test.wait_load('login-button')

    # Ввод логина и пароля
    test.set_input_text('user-name', 'standard_user')
    test.set_input_text('password', 'secret_sauce')
    test.wait_01()

    # Нажатие на кнопку отправки логина и пароля
    test.run_click('login-button')

    # Ожидание списка товаров
    test.wait_load('add-to-cart-sauce-labs-backpack')

    # Добавление в корзину товар
    test.run_click('add-to-cart-sauce-labs-backpack')

    # Ожидание для отображения
    test.wait_01()

    # Активация корзины
    test.run_click('shopping_cart_container')

    # Проверка наличия товара в корзине
    test.wait_load('item_4_title_link')

    # Оформление покупки
    test.run_click('checkout')

    # Ожидание прогрузки страницы ввода информации о пользователе
    test.wait_load('continue')

    # Ввод данных пользователя
    test.set_input_text('first-name', 'Alex')
    test.set_input_text('last-name', 'Petrov')
    test.set_input_text('postal-code', '1234')
    test.wait_01()

    # Нажатие кнопки подтверждения ввода
    test.run_click('continue')

    # Ожидание сообщения о завершении покупки
    test.wait_load('finish')

    # Нажатие кнопки завершения покупки
    test.run_click('finish')

    # Ожидание последнего сообщения
    test.wait_load('back-to-products')

    # Проверка успешности покупки - наличие текста "Checkout: Complete!"
    if test.check_text("Checkout: Complete!"):
        print('Успешное завершение покупки!')

    # Нажатие кнопки возврата к списку товаров
    test.run_click('back-to-products')
    test.wait_01()

    # Закрытие окна браузера
    test.close_driver()

    if not test.error_on:
        print('Тест выполнен без ошибок !!!')
