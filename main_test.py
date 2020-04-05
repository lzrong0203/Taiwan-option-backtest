from back_test import BackTest
import time
import datetime
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import random
import numpy as np
import glob

def read_data():
    """
    Get the option and future data to test
    return: option and future Pandas's dataframe
    """
    # option get
    # opt_file = glob.glob("/home/lzrong/dick1/opt_hist/*.csv") #  path
    opt_file = glob.glob("./opt_hist/*.csv")
    opt_file.sort()
    uns_file = [pd.read_csv(i, na_values="-") for i in opt_file if not "交易日期" in pd.read_csv(i).columns]
    # print(uns_file)
    # df = pd.concat([pd.read_csv(i) for i in opt_file if pd.read_csv(i).columns.contains("交易日期")])
    test_opt = pd.concat(uns_file)
    test_opt = test_opt.sort_values("Unnamed: 0")
    test_opt.rename(columns={"Unnamed: 0": "交易日期"}, inplace=True)
    test_opt["交易日期"] = pd.to_datetime(test_opt["交易日期"])
    test_opt.set_index("交易日期", inplace=True)
    # future get
    f_col = ["index", "Date", "Open^f", "Close^f", "High^f", "Low^f", "Vol^f"]
    f = pd.read_csv("./future.csv", skiprows=1, index_col="index", names=f_col)
    f["Date"] = pd.to_datetime(f["Date"])
    f.set_index("Date", inplace=True)
    return test_opt, f

if __name__ == "__main__":
    test_opt, f = read_data()
    start = "2018-01-02"
    stop_point = 0.5
    back = BackTest(f, test_opt, start, gap=0.03, up_down=1, stop_point=stop_point)
    back.start_run()
    try:
        for i in range(300):
            back.get_the_gap()
#             back.calculate_re_co()
    except IndexError:
        print("END")
