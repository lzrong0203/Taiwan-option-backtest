# Taiwan option backtest
回測台灣選擇權策略

買進跨式與買進勒式策略回測

## 期貨資料
台指期貨近月

資料來源：台灣期貨交易所

## 選擇權資料
台指選擇權

資料來源：台灣期貨交易所

## 說明

## Prerequisites
numpy pandas

## Installing
```
$ pip install numpy pandas 
or
$ conda install numpy pandas
```

執行方式

```
$ python main_test.py
```
## 策略說明
* 利用台指近月資料找尋日期價平，下單買進跨式或勒式(up_down)
* 開始日期(start)，目前從 201801~202003
* 交易觸發百分比(gap)
* 停損(stop_point)
