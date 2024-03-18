import random
import time
import os
import csv
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv
from tweety import Twitter
from tweety.types import User, UserTweets
from seleniumwire.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as Act
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

load_dotenv()


class SiteWalker:
    def __init__(self) -> None:
        self.driver: Chrome = self.get_driver()
        self.wait = WebDriverWait(self.driver, 8)

    def get_driver(self) -> Chrome:
        """Создаём драйвер."""

        service: Service = Service(executable_path=self.find_driver())
        return Chrome(
            service=service,
            options=self.__get_driver_options(),
            seleniumwire_options=self.__get_proxy_options(),
        )

    def __get_driver_options(self):
        """Настрока драйвера."""
        options = ChromeOptions()
        options.add_argument("--disable-proxy-certificate-handler")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.page_load_strategy = "normal"
        return options

    def __get_proxy_options(self) -> dict[str, dict[str, str | bool]] | None:
        """Получаем настройки прокси сервера."""

        login = os.environ.get("proxy_login")
        password = os.environ.get("proxy_password")
        proxy_ip = os.environ.get("proxy_ip")
        if login and password and proxy_ip:
            return {
                "proxy": {
                    "https": f"http://{login}:{password}@{proxy_ip}",
                    "http": f"http://{login}:{password}@{proxy_ip}",
                },
                "ca_cert": "ca.crt",
                "verify_ssl": False,
            }

        else:
            return None

    def find_driver(self, driver: str = "chromedriver.exe") -> Path:
        """Проверяем наличие драйвера и возвращаем путь, или ошибка"""

        file_path: Path = Path("data").resolve().joinpath(driver)
        if os.path.isfile(path=file_path):
            return file_path
        else:
            raise OSError(f"Драйвер {driver} по пути {file_path}, не найден!")

    def wait_click(self, elem: WebElement):
        """Ждем появление элемента и ждём."""

        self.wait.until(lambda d: elem.is_displayed())
        self.action.move_to_element(elem).pause(5).click(elem).perform()

    def find_and_wait(self, by: Literal, option: str) -> WebElement:
        """Ищем элемент и кликаем на него. Действие с задержкой."""

        elem: WebElement = self.delayed_driver.find_element(by, option)
        if not self.wait.until(lambda d: elem.is_displayed()):
            self.driver.refresh()
            self._wait_some
        self.action.scroll_to_element(elem)
        self.action.move_to_element(elem).perform()
        return elem

    @property
    def _wait_some(self):
        """Ждем случайное время."""

        time.sleep(random.randint(6, 8))

    @property
    def __long_wait(self):
        """Ждем 12 секунд."""

        time.sleep(12)

    @property
    def action(self) -> Act:
        """Возвращаем объект действий."""
        return Act(self.driver)

    def put_tr_in_csv(self, tr_data: list[WebElement]):
        """Перебираем список элементов содержащий строки таблицы и пишем в csv файл"""

        data: list[list] = self.get_data_from_tr_list(tr_data)
        with open(f"{str(time.time_ns())}_data.csv", "a", encoding="utf-8") as f:
            wr = csv.writer(f)
            for d in data:
                if len(d) == 0:
                    continue
                wr.writerow([d[1], d[6]])
        return True

    def get_data_from_tr_list(self, tr_data: list[WebElement]) -> list[list]:
        """Приобразуем список элементов строк таблицы(тэг tr) в список списков значений."""

        tr_data.pop(-1)
        data_list: list = []
        for tr in tr_data:
            self.action.scroll_to_element(tr).move_to_element(tr).perform()
            td_data: list[WebElement] = tr.find_elements(By.TAG_NAME, "td")
            data_list.append(self.get_data_from_td_list(td_data))
            self._wait_some
        return data_list

    def get_data_from_td_list(self, td_data: list[WebElement]):
        """
        Приобразуем список из элементов ячеек строки таблицы(тэг td)
        в список из значений ячеек строки таблицы
        """

        data: list = []
        for td in td_data:
            data.append(td.text)
        return data

    @property
    def delayed_driver(self) -> Chrome:
        """Возвращафет драйвер с задержкой"""

        self._wait_some
        return self.driver

    def go_to(self, url: str):
        """Создаем окно и переходим на переданый url и ждем."""

        self.driver.maximize_window()
        self.driver.get(url)
        self._wait_some

    def end(self):
        """Конец работы."""

        self.driver.close()
        self.driver.quit()

    def scroll_some(self):
        """Курутим колесо туда-сюда"""

        y: int = random.randint(2, 10) * 200
        self.action.scroll_by_amount(0, y).perform()
        self._wait_some
        self.action.scroll_by_amount(0, -y).perform()

    def find_and_click(
        self, by: Literal, option: str, elem: WebElement = None
    ) -> WebElement:
        """Ищем элемент и кликаем на него. Действие с задержкой."""

        if not elem:
            elem = self.delayed_driver
        el: WebElement = elem.find_element(by, option)
        self.wait_click(el)
        return el

    def find_scroll_and_click(
        self, by: Literal, option: str, elem: WebElement = None
    ) -> WebElement:
        """Ищем элемент, прокручиваем к нему и кликаем и кликаем на него. Действие с задержкой."""

        if not elem:
            elem = self.delayed_driver
        el: WebElement = elem.find_element(by, option)
        self.action.scroll_to_element(el).perform()
        self._wait_some
        self.wait_click(el)
        return el

    def find_and_scroll(
        self, by: Literal, option: str, elem: WebElement = None
    ) -> WebElement:
        """Ищем элемент, прокручиваем к нему и кликаем и кликаем на него. Действие с задержкой."""

        if not elem:
            elem = self.delayed_driver
        el: WebElement = elem.find_element(by, option)
        self.action.scroll_to_element(el).perform()
        return el

def i_am_a_simple_dude(walker: SiteWalker):
    """Имитируем действия."""

    walker.find_and_click(By.ID, "link_0")
    walker.find_scroll_and_click(By.ID, "tab1_container")
    walker.find_scroll_and_click(By.ID, "NIFTY BANK")
    elem: WebElement = walker.driver.find_element(
        By.CSS_SELECTOR, "div.link-wrap"
    ).find_element(By.LINK_TEXT, "View All")
    walker.action.scroll_to_element(elem).scroll_by_amount(0, 200).perform()
    walker.driver.get(
        "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY BANK"
    )
    walker._wait_some
    elem: WebElement = walker.find_and_click(By.ID, "equitieStockSelect")
    select = Select(elem)
    select.select_by_value("NIFTY ALPHA 50")
    walker.find_and_scroll(By.CLASS_NAME, "note_container")


def go_to_nseindia():
    """действия на https://www.nseindia.com"""
    walker = SiteWalker()
    try:
        walker.go_to("https://www.nseindia.com")
        walker.scroll_some()
        walker.find_and_click(By.ID, "link_2")
        walker.find_and_click(By.PARTIAL_LINK_TEXT, "Pre-Open Market")
        walker.find_and_wait(By.ID, "livePreTable")
        data: list[WebElement] = walker.delayed_driver.find_elements(By.TAG_NAME, "tr")
        walker.put_tr_in_csv(data)
        i_am_a_simple_dude(walker=walker)
    except Exception as e:
        print(e)
    finally:
        walker.end()


def get_hi5_elon():
    """Действия на twitter, получаем 10 последних твитов Маска"""

    login = os.environ.get("proxy_login")
    password = os.environ.get("proxy_password")
    proxy_ip = os.environ.get("proxy_ip")
    proxy = {
        "https://": f"http://{login}:{password}@{proxy_ip}",
        "http://": f"http://{login}:{password}@{proxy_ip}",
    }
    max_results = 10
    app = Twitter("session", proxy=proxy)
    user: User = app.get_user_info("elonmusk")
    all_tweets: UserTweets = app.get_tweets(user)
    tweets_list = sorted(all_tweets.tweets, key=lambda x: x.created_on, reverse=True)
    for i, tweet in enumerate(tweets_list):
        if i >= max_results:
            break
        print(tweet.text)


def main():
    go_to_nseindia()
    get_hi5_elon()


if __name__ == "__main__":
    main()
