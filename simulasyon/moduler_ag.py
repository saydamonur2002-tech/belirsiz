"""Moduler uzman firma agi + aracilarin tasfiyesi; katmanli konut birim maliyeti dususu. Kaynakli girdiler ve VARSAYIMlar MODULER_AG.md'de."""
import pandas as pd
GIRDI=0.65  # model: girdi %65 / iscilik %35
S={"dusuk":0,"orta":1,"yuksek":2}
L=[]
def add(ad,v,dayanak): L.append(dict(katman=ad,dusuk=v[0],orta=v[1],yuksek=v[2],dayanak=dayanak))
add("1 Olcek+yerlilestirme+G1 %10 KOBI marji",[-.018,-.071,-.139],"OLCEK_YERLILESTIRME (FAVOK 2025 kaynakli, olcek varsayim)")
# 2 bayi/toptanci marji: girdi payi x bayi uzerinden gecen pay(V) x bayi brut marji(kaynakli bant) x platformun yakaladigi pay(V)
rt=(.6,.75,.9);mg=(.015,.04,.08);cap=(.5,.7,.9)
add("2 Bayi/toptanci marjinin tasfiyesi",[-GIRDI*rt[i]*mg[i]*cap[i] for i in range(3)],"ALTSO brut marj kaba %1-4, ince %2-15; toplu projede %1-2 (Emlakkulisi 2011); kanal payi ve yakalama VARSAYIM")
# 3 taseron zinciri: taseronla yapilan is payi(V) x kaldirilan ara katman kar payi (CSB %25=%10 kar+%15 genel gider; gerceklesen taseron kari %1-10, ITU) - koordinasyon maliyeti(V)
sub=(.4,.6,.8);lay=(.02,.05,.10);coord=(.01,.01,.005)
add("3 Taseron zincirinin kisalmasi (net koordinasyon)",[-(sub[i]*lay[i]-coord[i]) for i in range(3)],"CSB birim fiyat %10 kar+%15 GG; ITU tez taseron gerceklesen kar %1-10; is payi ve koordinasyon VARSAYIM")
# 4 moduler/uzmanlasma verimliligi (yalniz verimlilik; taseron marji 3'te): moduler uygun pay(V) x tasarruf (McKinsey 0-20%, NHBC: uygulayicilarin %44'u tasarruf gordu)
mp=(.3,.4,.5);sv=(0,.05,.10)
add("4 Moduler uzman ag verimliligi",[-mp[i]*sv[i] for i in range(3)],"McKinsey 2019 0-%20; UK MMC kanit karisik (NHBC 2016, NAO); pay VARSAYIM")
add("5 Hedefli GV+damga destegi (platform KOBI)",[-.0283,-.0298,-.0313],"VERGI_SUBVANSIYON (iscilik payi %38-42)")
add("6 Karma oynaklik araclari (alici fiyati)",[-.0018,-.0018,-.0018],"OYNAKLIK_KARMA 18 ay: 1,8086/1,8118")
add("7 6 aylik maliyet bazli guncelleme + %30 tavan",[0,0,0],"Marj/zarar korumasi; birim maliyeti dusurmez")
d=pd.DataFrame(L)
for c in S:
    d[c+"_kumulatif"]=(1+d[c]).cumprod()-1
d.round(4).to_csv("data/moduler_ag_katmanlar.csv",index=False);print(d.round(4).drop(columns="dayanak").to_string())
