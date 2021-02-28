from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime as dt
import datetime
import nsepy
from nsetools import Nse
import pandas as pd
import csv
import TechnicalAnalysis.nseUtil as nseUtil
from TechnicalAnalysis.models import StockLastUpdate
import yfinance as yf
import matplotlib.pyplot as plt
import talib as ta
from TechnicalAnalysis.models import StockBasicInfo
# Create your views here.


class StockView(APIView):

    def get(self, request):
        currentDay = dt.now().day
        currentMonth = dt.now().month
        currentYear = dt.now().year
        print(str(currentDay)+str(currentMonth)+str(currentYear))
        nifty100DataFrame = nseUtil.getNSEStocksList()
        print(nifty100DataFrame)
        StockSymbol = ''
        StockName = ''

        for index, row in nifty100DataFrame.iterrows():
            StockSymbol = row['Symbol']
            StockName = row['Stock Name']
            print(StockSymbol)
            StockDataFrame = nsepy.get_history(symbol=StockSymbol, start=datetime.date(
                2020, 2, 2), end=datetime.date(currentYear, currentMonth, currentDay))
            # print(StockDataFrame)
            self.saveStockBasicInfo(StockSymbol, StockName, StockDataFrame)
        return Response(StockDataFrame)

    def saveStockBasicInfo(self, StockSymbol, StockName, StockDataFrame):
        try:
            for date, row in StockDataFrame.iterrows():
                StockBasicInfoModel = StockBasicInfo(Symbol=StockSymbol, Name=StockName, Date=date,
                                                     PrevClose=row['Prev Close'], Open=row['Open'],
                                                     Close=row['Close'], Low=row['Low'], High=row['High'], VWAP=row['VWAP'],
                                                     Volume=row['Volume'], DeliveryPercent=row['%Deliverble']*100)

                StockBasicInfoModel.save()
        except Exception as e:
            print('Error in saving Stock Details for StockName ' +
                  str(StockName)+' for Date ' + str(date)+' ' + str(e))


class Yfinance(APIView):
    def get(self, request):
        nifty100DataFrame = nseUtil.getNSEStocksList()
        # for index, row in nifty100DataFrame.iterrows():
        #     StockSymbol = row['Symbol']
        #     StockName = row['Stock Name']
        #     StockModel = Stock:as(
        #         StockName=StockName, StockSymbol=StockSymbol)
        #     StockModel.save()
        plt.style.use('bmh')
        Abbot = pd.DataFrame(
            list(StockBasicInfo.objects.all().filter(Symbol='ABBOTINDIA').values()))
        print(Abbot['Close'])

        Abbot['Simple MA'] = ta.SMA(Abbot['Close'], 14)
        Abbot['EMA'] = ta.EMA(Abbot['Close'], timeperiod=14)
        # # Plot
        Abbot[['Close', 'Simple MA', 'EMA']].plot(figsize=(15, 15))
        print(Abbot)
        print(plt)
        (plt.show())


def saveStockBasicInfoDB(StockSymbol, StockName, startDate, endDate):
    startDate = datetime.date(2020, 12, 21)
    Flag = True
    # startDate += datetime.timedelta(days=1)
    endDate = datetime.date(2020,  12, 22)
    StockDataFrame = nsepy.get_history(symbol=StockSymbol, start=datetime.date(
        startDate.year, startDate.month, startDate.day), end=datetime.date(endDate.year, endDate.month, endDate.day))
    for date, row in StockDataFrame.iterrows():
        try:
            StockBasicInfoModel = StockBasicInfo(Symbol=StockSymbol, Name=StockName, Date=date,
                                                 PrevClose=row['Prev Close'], Open=row['Open'],
                                                 Close=row['Close'], Low=row['Low'], High=row['High'], VWAP=row['VWAP'],
                                                 Volume=row['Volume'], DeliveryPercent=row['%Deliverble']*100)
            StockBasicInfoModel.save()
            print('Successfully synced DB for stock ' +
                  str(StockName) + ' for date '+str(date))
        except Exception as e:
            Flag = False
            print('Error in saving Stock Details for StockName ' +
                  str(StockName)+' for Date ' + str(date)+' ' + str(e))

    if(Flag):
        StockLastUpdateModel = StockLastUpdate(
            StockName=StockName, StockSymbol=StockSymbol, LastUpdateDate=endDate)
        StockLastUpdateModel.save()


class SyncDB(APIView):
    def get(self, request):
        StockLastUpdateList = StockLastUpdate.objects.all()
        for StockLastUpdateModel in StockLastUpdateList:
            UpdatedDate = StockLastUpdateModel.LastUpdateDate

            if(UpdatedDate != datetime.date.today()):
                print("Updating Stock "+str(StockLastUpdateModel.StockName))
                saveStockBasicInfoDB(StockLastUpdateModel.StockSymbol,
                                     StockLastUpdateModel.StockName, UpdatedDate, datetime.date.today())

class UpdateStock(APIView):
    def get(self, request):
        startDate = datetime.date(2018, 10, 1)
        Flag = True
        # startDate += datetime.timedelta(days=1)
        endDate = datetime.date(2018, 11, 6)
        print('Fetching dataframe')
        StockDataFrame = nsepy.get_history(symbol='TECHM', start=datetime.date(
        startDate.year, startDate.month, startDate.day), end=datetime.date(endDate.year, endDate.month, endDate.day))
        print('Fetched dataframe ')
        StockSymbol = 'ADANITRANS'
        StockName = 'Adani Transmission Ltd.'
        for date, row in StockDataFrame.iterrows():
            try:
                StockBasicInfoModel = StockBasicInfo(Symbol=StockSymbol, Name=StockName, Date=date,
                                                 PrevClose=row['Prev Close'], Open=row['Open'],
                                                 Close=row['Close'], Low=row['Low'], High=row['High'], VWAP=row['VWAP'],
                                                 Volume=row['Volume'], DeliveryPercent=row['%Deliverble']*100)
                StockBasicInfoModel.save()
                print('Successfully synced DB for stock ' +
                str(StockName) + ' for date '+str(date))
            except Exception as e:
                Flag = False
                print('Error in saving Stock Details for StockName ' +
                  str(StockName)+' for Date ' + str(date)+' ' + str(e))
