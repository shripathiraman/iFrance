from __future__ import print_function

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def f_open_browser():
    browser.get("https://piv.actionlogement.fr/login")


def f_al_login(strusr, strpwd) -> str:
    login_status = "LOGIN_KO"
    try:
        browser.get("https://piv.actionlogement.fr/login")
        username = browser.find_element_by_id("usrEmail")
        password = browser.find_element_by_id("usrPassword")
        submit = browser.find_element_by_id("connection")
        username.clear()
        password.clear()
        if strusr.strip() != "" and strpwd.strip() != "":
            username.send_keys(strusr)
            password.send_keys(strpwd)
            submit.click()
            browser.implicitly_wait(10)
            login_error = browser.find_element_by_class_name('error')
            if login_error.is_displayed():
                login_status = "Id. invalides"
            else:
                login_status = "LOGIN_OK"
        else:
            login_status = "Mot de passe vide"
    except NoSuchElementException:
        login_status = "LOGIN_OK"
    finally:
        return login_status

def f_al_read_status() -> str:
    al_stat = "OK"
    try:
        WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.XPATH, "//div[@class='subvention-card__inner']"))
        )
        fstatus = browser.find_element_by_xpath(
            "//div[@class='subvention-card__inner']//following::span[@class='subvention-card__info "
            "sub-status']//span[1]")

        al_stat = fstatus.text

    except NoSuchElementException:
        al_stat = "Erreur Affichage Statut"
    finally:
        return al_stat


def f_al_logout() -> str:
    user_logout_stat = "LOGOUT_OK"
    try:
        toggleuser = browser.find_element_by_id("dropdown-right__BV_toggle_")
        toggleuser.click()
        bdisconnect = browser.find_element_by_id("disconnection")
        bdisconnect.click()
    except NoSuchElementException:
        user_logout_stat = "Erreur Affichage"
    finally:
        return user_logout_stat

browser = webdriver.Chrome()
