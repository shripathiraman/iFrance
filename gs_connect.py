import gspread
import pandas as pd
import paramConfig as prmCon
import appConstants as appCon


def get_data():
    try:
        # blank Dataframe
        final_df = pd.DataFrame()
        # Connect to Google Service Account
        gc = gspread.service_account()
        # open Google Sheet using File name or file ID
        if prmCon.gs_fileID is None:
            wb = gc.open(prmCon.gs_fileName)
        else:
            wb = gc.open_by_key(prmCon.gs_fileID)

        # file the given sheet from the work book
        wks = wb.worksheet(prmCon.al_Sheet_Name)
        if wks is not None:
            # fetch all the data from the given sheet
            data = wks.get_all_values()
            #  get the headers from data and remove it from the data variable
            headers = data.pop(0)
            # define the header for the dataframe
            df = pd.DataFrame(data, columns=headers)
            # Get all the Not Applicable Status
            lst_status_na = appCon.lst_status_na
            # build the query filter to extract the required data
            qry_filter = prmCon.al_status + ' != @lst_status_na & ' + prmCon.al_mail + ' != "" & ' + prmCon.al_pwd + \
                         ' != ""'
            # fetch only the required columns and rows
            final_df = (df.filter(items=[prmCon.al_mail, prmCon.al_pwd, prmCon.al_status])).query(qry_filter)
    finally:
        return final_df
