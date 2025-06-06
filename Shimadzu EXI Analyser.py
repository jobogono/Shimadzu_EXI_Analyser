import os
import pandas as pd
import warnings
import tkinter as tk
from tkinter import filedialog

# open folder and concatenate files
def get_raw_data(path):
    files = os.listdir(path)     
    files_csv = [f for f in files if f[-3:] == 'csv']
    exi_log = pd.DataFrame()
    for f in files_csv:
        data = pd.read_csv(path + '/' + f, encoding_errors='ignore') #some Siemens systems produce an encoding error here so force ignore
        exi_log = pd.concat([exi_log,data])
    return exi_log

# change datatype of numeric columns reported on
def set_dtypes(exi_log):
    exi_log['DAP'] = pd.to_numeric(exi_log['DAP'])
    exi_log['EI'] = pd.to_numeric(exi_log['EI'])
    #exi_log['Collimation 1'] = pd.to_numeric(exi_log['Collimation 1'])
    #exi_log['Collimation 2'] = pd.to_numeric(exi_log['Collimation 2'])
    exi_log['SID'] = pd.to_numeric(exi_log['SID'])
    #exi_log['Dose'] = pd.to_numeric(exi_log['Dose'], errors='coerce') #sets blanks to NaN
        
    return exi_log

	# issue where sometimes DAP == 0. Removes entire row
def remove_zero_dap(exi_log):
    length3 = exi_log.shape[0]
    for column in exi_log:
        exi_log = exi_log[exi_log['DAP'] != 0]
    length4 = exi_log.shape[0]
    print("{} rows removed for zero DAP".format(length3-length4))

    return exi_log

def get_medians(exi_log):
    headers = {
        "Exam":[],
        "n":[],
        "kV":[],
        "mAs":[],
        "mA":[],
        "ms":[],
        "DAP":[],
        "EXI":[],
        "SID":[],
    }
    median_df = pd.DataFrame(headers)
    unique_exams = exi_log['Protocol'].unique()
    
    for exam in unique_exams:
        exam_data = exi_log[exi_log["Protocol"] == exam]
        n = exam_data.shape[0]
        kV = exam_data['kV'].median()
        mAs = exam_data['mAs'].median()
        mA = exam_data['mA'].median()
        time = exam_data['ms'].median()
        DAP = exam_data['DAP'].median()
        EXI  = exam_data['EI'].median()
        SID = exam_data['SID'].median()
        median_df.loc[len(median_df)] = [exam, n, kV, mAs, mA, time, DAP, EXI, SID]

    return median_df

def save_df(df, path):
    df.to_csv(path)

root = tk.Tk()
root.withdraw()
input_dir = tk.filedialog.askdirectory(title="Select input folder")

try:
    exi_log = get_raw_data(input_dir)
except FileNotFoundError:
    print("Files could not be located\n")
        
exi_log = set_dtypes(exi_log)
exi_log = remove_zero_dap(exi_log)
median_df = get_medians(exi_log)

output_dir = tk.filedialog.asksaveasfilename(title="Save As", defaultextension='.csv')
save_df(median_df, output_dir)

print("")

print("Complete")



