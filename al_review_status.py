from __future__ import print_function

import al_gs_connect as gsc
import al_utils as alu
import constants as cst
import params as prm

try:
    s_al_new_status = ""
    alu.f_open_browser()
    browser = alu.browser
    res = gsc.res
    ws = gsc.ws
    idx = 0
    if not res:
        print('No data found.')
    else:
        for row in res:
            s_al_new_status = ""
            idx = idx + 1
            s_user = row[prm.al_col_mail]
            s_al_pwd = row[prm.al_col_pwd]
            s_al_old_status = row[prm.al_col_old_status]
            s_client = row[prm.al_col_client].lstrip().upper()
            if s_client.upper() not in cst.al_list_clients_to_ignore:
                if s_al_old_status.upper() not in cst.lst_status_na and s_al_old_status.upper() not in cst.al_valid_status:
                    if s_al_pwd.strip() == "":
                        s_al_log_status = "MDP vide"
                    else:
                        try:
                            s_al_log_status = alu.f_al_login(s_user, s_al_pwd)
                            if s_al_log_status == cst.al_login_ok:
                                s_al_new_status = alu.f_al_read_status()
                                alu.f_al_logout()
                            else:
                                s_al_log_status = "Problème Identifiants"
                        finally:
                            s_al_new_status = cst.al_status_dict.get(s_al_new_status, s_al_new_status)
                            ws.update_cell(idx, prm.al_col_tgt_status, s_al_new_status)
finally:
    print("fin")
    alu.browser.quit()
