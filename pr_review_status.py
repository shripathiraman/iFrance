from __future__ import print_function

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import constants as cst
import params as prm
import pr_gs_connect as gsc


def f_pr_login(strusr, strpwd) -> str:

    browser.get("https://www.maprimerenov.gouv.fr/")

    if strusr.strip() != "" and strpwd.strip() != "":
        login_status = "LOGIN_INIT"
        btn_connect_stat = ""

        try:
            browser.implicitly_wait(10)
            btn_cookies = browser.find_element_by_id("cookieChoiceAccept")
            if btn_cookies.is_displayed():
                btn_cookies.click()
        except NoSuchElementException:
            pass

        finally:
            try:
                btn_connect = browser.find_element_by_name("AnonymusPortalHeader_pyPortalHarness_8")
                if btn_connect.is_displayed():
                    btn_connect.click()
                    btn_connect_stat = "LOGIN_READY_YES"
            except NoSuchElementException:
                btn_connect_stat = "LOGIN_READY_NO"
            finally:
                pass

            if btn_connect_stat == "LOGIN_READY_YES":
                try:
                    login_status = "LOGIN_OK"
                    username = browser.find_element_by_id("txtUserID")
                    password = browser.find_element_by_id("txtPassword")
                    submit = browser.find_element_by_id("submit_row")
                    username.clear()
                    password.clear()
                    username.send_keys(strusr)
                    password.send_keys(strpwd)
                    submit.click()
                    browser.implicitly_wait(10)
                    login_error = browser.find_element_by_id('errorDiv')
                    if login_error.is_displayed():
                        login_status = "Id. invalides"
                except NoSuchElementException:
                    pass
                finally:
                    return login_status
    else:
        login_status = "MDP_VIDE"
        return login_status


def f_pr_data():
    mpr_stat = ""
    try:
        mesdossiers = browser.find_element_by_xpath("//button[contains(text(),'Mes dossiers')]")
        mesdossiers.click()
        browser.implicitly_wait(10)
    except NoSuchElementException:
        pass
    finally:
        pass

    # Statut MPR
    try:
        ele_stat_encours = browser.find_element_by_xpath(
            "//div[@id='CT' and contains(@show_when, 'En cours de montage')]")
        ele_stat_acceptee = browser.find_element_by_xpath("//div[@id='CT' and contains(@show_when, 'Acceptée')]")

        if ele_stat_encours.is_displayed():
            mpr_stat = "En cours de montage"
        if ele_stat_acceptee.is_displayed():
            mpr_stat = "Acceptée"
    except NoSuchElementException:
        mpr_stat = "Inconnu"

    try:
        # Montant prime
        lst_mpr = browser.find_elements_by_xpath(
            "(//div[@class='flex  content  false layout-content-default content-default flex-grow-1 right-aligned'])[1]/div")

        details_prime = ''.join(lst_mpr)
        '''
        
        
        for x in lst_mpr:
            print("details prime 1 : " + x.text)
            details_prime = details_prime + " " + x.text
            print("details prime 2 : " + details_prime)
          '''



        details_prime = details_prime.replace("Montant estimé de la subvention ", "").lstrip()
        print("details prime 3 : " + details_prime)

    except NoSuchElementException:
        details_prime = "Inconnu"
    finally:
        pass

    try:
        btn_voirmondossier = browser.find_element_by_xpath("//button[contains(text(),'Voir mon dossier')]")
        btn_voirmondossier.click()

        browser.implicitly_wait(10)

        lst_mandataire = browser.find_elements_by_xpath(
            "(//div[contains(text(),'Informations mandataire')]/following::div)[1]/div/div")
        details_mandat = ""
        for x in lst_mandataire:
            details_mandat = details_mandat + " " + x.text
            details_mandat = details_mandat.lstrip()

        if details_mandat.startswith("Izol France mandataire administratif et financier"):
            details_mandat = "MANDAT_OK"
        else:
            details_mandat = "MANDAT_KO"

    except NoSuchElementException:
        details_mandat = "MANDAT_KO"

    finally:
        pass
    try:
        lbl_dossier = browser.find_element_by_xpath(
            "//div[@class='content-item content-label item-2 remove-bottom-spacing remove-right-spacing flex flex-row standard_bold_dataLabelRead dataLabelRead heading_6_dataLabelRead']")
        ref_dossier = lbl_dossier.text
    except NoSuchElementException:
        ref_dossier = ""
    finally:
        pass
    pr_data = [mpr_stat, details_prime, details_mandat, ref_dossier]
    browser.quit()
    return pr_data


try:
    res = gsc.res
    ws = gsc.ws
    idx = 0
    if not res:
        print('No data found.')
    else:
        for row in res:
            s_pr_data = []
            idx = idx + 1
            s_user = row[prm.pr_col_mail]
            s_pr_pwd = row[prm.pr_col_pwd]
            s_pr_old_status = row[prm.pr_col_old_status].upper()
            s_client = row[prm.pr_col_client].lstrip().upper()

            if s_client.upper() not in cst.pr_list_clients_to_ignore:
                if s_pr_old_status.upper() not in cst.lst_status_na and s_pr_old_status.upper() not in cst.pr_valid_status:
                    if s_pr_pwd.strip() == "":
                        s_pr_log_status = "MDP vide"
                    else:
                        browser = webdriver.Chrome()
                        try:
                            s_pr_log_status = f_pr_login(s_user, s_pr_pwd)
                            if s_pr_log_status == cst.pr_login_ok:
                                s_pr_data = f_pr_data()
                                ws.update_cell(idx, prm.pr_col_mpr_stat, s_pr_data[0])
                                ws.update_cell(idx, prm.pr_col_mpr_Amt, s_pr_data[1])
                                ws.update_cell(idx, prm.pr_col_mpr_mandat, s_pr_data[2])
                                ws.update_cell(idx, prm.pr_col_mpr_dossier, s_pr_data[3])
                            else:
                                ws.update_cell(idx, prm.pr_col_mpr_stat, s_pr_log_status)
                        finally:
                            browser.quit()

finally:
    print("fin")
