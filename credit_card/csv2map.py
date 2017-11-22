#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname='/Library/Fonts/meiryo.ttc', size=14)

if len(sys.argv)!=2:
    print("Usage: $ python %s csvFileName" % sys.argv[0])
    quit()

csvfile = sys.argv[1]

# 1月あたり旅行者
tourlist_dic={}
for year in range(2012,2017):
    with open("../tourists_number/FY%d"%year,"r",encoding="utf-8") as f:
        dic = json.load(f)
    for countryData in dic["result"]["changes"]:
        country = countryData["countryName"]
        for i in range(len(countryData["data"])):
            num_qt = countryData["data"][i]
            if num_qt["year"] == year:
                if year == 2012:
                    if num_qt["quarter"] > 2:
                        if num_qt["quarter"] == 3:
                            iteration = 2
                        elif num_qt["quarter"] == 4:
                            iteration = 3
                        num_m = num_qt["value"]/3
                        for i in range(iteration):
                            try:
                                tourlist_dic[country].append(num_m)
                            except:
                                tourlist_dic[country] = [num_m]
                elif year == 2016:
                    if num_qt["quarter"] == 1:
                        num_m = num_qt["value"]/3
                        for i in range(3):
                            try:
                                tourlist_dic[country].append(num_m)
                            except:
                                tourlist_dic[country] = [num_m]
                else:
                    num_m = num_qt["value"]/3
                    for i in range(3):
                        try:
                            tourlist_dic[country].append(num_m)
                        except:
                            tourlist_dic[country] = [num_m]
for k,v in tourlist_dic.items():
    tourlist_dic[k] = np.array(v)

# 1月あたり消費
df = pd.read_csv(csvfile, index_col=0)
df = df.dropna(axis=1)

for country in df:
    if country != "インドネシア":
        # 消費額
        arr = np.array(df[country])
        map_array = np.array([arr[5:17], arr[17:29], arr[29:41]])
        plt.subplot(2, 1, 1)
        plt.pcolor(map_array)
        plt.yticks([0.5,1.5,2.5], ["2013","2014","2015"])
        plt.xticks([0.5+i for i in range(0,12)], range(1,13))
        plt.title(country+"（上:総消費額, 下:一人当たり消費）", fontproperties=fp)

        # 一人当たり
        sr_perone = df[country] / tourlist_dic[country]
        ar_perone = np.array(sr_perone)
        map_array = np.array([ar_perone[5:17], ar_perone[17:29], ar_perone[29:41]])
        plt.subplot(2, 1, 2)
        plt.pcolor(map_array)
        plt.yticks([0.5,1.5,2.5], ["2013","2014","2015"])
        plt.xticks([0.5+i for i in range(0,12)], range(1,13))
        plt.show()
