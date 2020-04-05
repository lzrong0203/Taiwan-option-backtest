import pandas as pd
import numpy as np


class BackTest:

    def __init__(self, f, opt, start, gap=0.01, up_down=1, stop_point=0.5):
        self.cost = 0
        self.revenue = 0
        self.f = f
        self.opt = opt
        self.start = start
        self.shift_days = 1
        self.gap_num = up_down
        self.contract_num = 0
        self.no_count = 0
        #         self.gg = 0
        self.shift_days_list = []
        self.date = []
        self.gap = gap
        self.call_price = ""
        self.put_price = ""
        self.stop_point = stop_point
        self.ohlc = 0
        self.opt_point = np.array(['開盤價', '最高價', '最低價', '收盤價'])

    def start_run(self):
        print("=============================")
        start = self.start
        #         if start > pd.date_range("2020-01-01", periods=1):
        #             raise EOFError
        self.date.append(self.start)
        print(start)
        self.value = self.f.loc[start]["Open^f"]
        day_opt = self.opt.loc[start][~self.opt.loc[start]["到期月份(週別)"].apply(str.strip).str.contains("W")]
        #         print(day_opt)
        self.contract = day_opt["到期月份(週別)"].apply(str.strip).unique().min()  #
        print("台指價格", self.value)
        print("CONTRACT", self.contract)
        day_match = day_opt[day_opt["到期月份(週別)"].apply(str.strip) == self.contract]
        self.call_price = day_match[(day_match["履約價"] == round(self.value / 100) * 100 + self.gap_num * 100) &
                                    (day_match["買賣權"] == "買權")]["開盤價"]
        self.call_price.name = round(self.value / 100) * 100 + 100

        self.put_price = day_match[(day_match["履約價"] == round(self.value / 100) * 100 - self.gap_num * 100) &
                                   (day_match["買賣權"] == "賣權")]["開盤價"]
        self.put_price.name = round(self.value / 100) * 100 - 100
        print(self.call_price, self.put_price)
        self.cost = self.call_price * 50 + self.put_price * 50 + 60 + 0.001 * (
                    self.call_price * 50 + self.put_price * 50)

    #         print(day_match[day_match["履約價"] == call_price.name])
    #         print(day_match[day_match["履約價"] == put_price.name])
    #         self.revenue -= self.cost.values[0]
    #         print(self.revenue)

    def get_the_gap(self, shift_days=1):
        f = self.f
        start = self.start
        test_opt = self.opt
        loc = f.index.get_loc(start)
        open_com = abs((f.loc[start:]["Open^f"] - f.loc[start:].shift(-shift_days)["Open^f"]) / f.loc[start]["Open^f"])
        close_com = abs(
            (f.loc[start:]["Open^f"] - f.loc[start:].shift(-shift_days)["Close^f"]) / f.loc[start]["Open^f"])
        high_com = abs((f.loc[start:]["Open^f"] - f.loc[start:].shift(-shift_days)["High^f"]) / f.loc[start]["Open^f"])
        low_com = abs((f.loc[start:]["Open^f"] - f.loc[start:].shift(-shift_days)["Low^f"]) / f.loc[start]["Open^f"])

        four_gap = np.array((open_com.iloc[0], close_com.iloc[0], high_com.iloc[0], low_com.iloc[0]))
        #         four_ture = np.array((open_com, close_com, high_com, low_com)) # > self.gap
        #         opt_name = np.array(['開盤價', '最高價', '最低價', '收盤價'])
        #         trigger = opt_name[four_ture]
        #         print(four_ture)

        if not True in (four_gap > self.gap):
            #             print("Gap not get", shift_days)
            #             print(four_gap)
            if not self.contract in test_opt.loc[f.iloc[loc + shift_days:].index[0]]["到期月份(週別)"].apply(
                    str.strip).unique():
                #                 print("@@", test_opt.loc[f.iloc[loc+shift_days:].index[0]]["到期月份(週別)"].apply(str.strip).unique())
                print("Contract end", )
                self.shift_days = shift_days
                #                 print(self.shift_days)
                self.shift_days_list.append(shift_days)
                self.ohlc = 3
                self.calculate_re_co()
                return shift_days
            else:
                day_opt = test_opt.loc[f.iloc[loc + shift_days:].index[0]]
                day_match = day_opt[day_opt["到期月份(週別)"].apply(str.strip) == self.contract]
                day_call = day_match[(day_match["履約價"] == self.call_price.name) & (day_match["買賣權"] == "買權")]["收盤價"]
                day_put = day_match[(day_match["履約價"] == self.put_price.name) & (day_match["買賣權"] == "賣權")]["收盤價"]
                if (day_call + day_put).values[0] <= self.stop_point * (self.call_price + self.put_price).values[0]:
                    print("停損", end="")
                    self.shift_days = shift_days
                    self.shift_days_list.append(shift_days)
                    self.ohlc = 3
                    self.calculate_re_co()
                    return shift_days
            shift_days += 1
            self.shift_days_list.append(shift_days)
            return self.get_the_gap(shift_days)
        #         else if:

        else:
            print("Gap get", shift_days)
            #             print(four_gap)
            self.ohlc = list(four_gap > self.gap).index(True)
            print("價位", self.ohlc)
            self.shift_days = shift_days
            self.shift_days_list.append(shift_days)
            self.calculate_re_co()
            return shift_days

    def calculate_re_co(self):
        self.contract_num += 1
        shift_days = self.shift_days
        #         f = self.f
        loc = self.f.index.get_loc(self.start)
        #         test_opt = self.opt
        #         contract = self.contract
        #         open_com = abs((f.iloc[loc]["Open^f"] - f.iloc[loc+shift_days]["Open^f"]) / f.loc[start]["Open^f"])
        #         close_com = abs((f.iloc[loc]["Open^f"] - f.iloc[loc+shift_days]["Close^f"]) / f.loc[start]["Open^f"])
        #         high_com = abs((f.iloc[loc]["Open^f"] - f.iloc[loc+shift_days]["High^f"]) / f.loc[start]["Open^f"])
        #         low_com = abs((f.iloc[loc]["Open^f"] - f.iloc[loc+shift_days]["Low^f"]) / f.loc[start]["Open^f"])
        #         four_ture = np.array((open_com, high_com, low_com, close_com)) > self.gap
        #         opt_name = np.array(['開盤價', '最高價', '最低價', '收盤價'])
        #         trigger = opt_name[four_ture]

        if self.contract in self.opt.loc[self.f.iloc[loc + shift_days:].index[0]]["到期月份(週別)"].apply(str.strip).unique():
            print("平倉")
            self.cal_revenue(self.shift_days)
        #             self.new_contract(loc)

        else:
            self.no_count += 1
            print("履約")
            self.cal_revenue(shift_days - 1)

    #             self.shift_days += 1
    #             self.new_contract(loc)

    def new_contract(self, loc):
        new_day = self.f.iloc[loc + self.shift_days].name
        self.start = new_day
        self.start_run()

    def cal_revenue(self, shift_days):
        loc = self.f.index.get_loc(self.start)
        print(self.opt.loc[self.f.iloc[loc + shift_days:].index[0]]["到期月份(週別)"].apply(str.strip).unique())
        print(self.contract)
        if self.ohlc == 0:
            point = [0, 0]
        elif self.ohlc == 1:
            point = [1, 2]
        elif self.ohlc == 2:
            point = [2, 1]
        else:
            point = [3, 3]

        opt1 = self.opt.loc[self.f.iloc[loc + shift_days:].index[0]]
        opt1_match = opt1[opt1["到期月份(週別)"].apply(str.strip) == self.contract]
        new_call_price = opt1_match[(opt1_match["履約價"] == round(self.value / 100) * 100 + self.gap_num * 100) &
                                    (opt1_match["買賣權"] == "買權")][self.opt_point[point[0]]]
        new_call_price.name = round(self.value / 100) * 100 + self.gap_num * 100
        new_put_price = opt1_match[(opt1_match["履約價"] == round(self.value / 100) * 100 - self.gap_num * 100) &
                                   (opt1_match["買賣權"] == "賣權")][self.opt_point[point[1]]]
        new_put_price.name = round(self.value / 100) * 100 - self.gap_num * 100
        print()
        print(new_call_price, self.opt_point[point[0]], new_put_price, self.opt_point[point[1]])
        income = new_call_price * 50 + new_put_price * 50 - 60 - 0.001 * (new_call_price * 50 + new_put_price * 50)
        print("***INCOME***", income.values[0], "***Cost***", self.cost.values[0])
        self.revenue += (income.values[0] - self.cost.values[0])
        print("***Balance***", self.revenue)
        self.new_contract(loc)

