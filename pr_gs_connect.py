import gspread

import params as prm

gc = gspread.service_account(filename=prm.pr_cred_file)
sh = gc.open_by_key(prm.pr_driving_gs_file_id)
ws = sh.worksheet(prm.pr_driving_gs_sheet_name)
res = ws.get_all_values()
