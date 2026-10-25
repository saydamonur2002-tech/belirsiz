"""Grup bazli karma oynaklik yapisi: sinirli tedarik -> koridor+fon; temel/coklu uretilen -> KOBI tampon stok; geri kalan -> CPWD formulu.
Orta senaryo. Tum paylar/parametreler VARSAYIM (OYNAKLIK_KARMA.md)."""
import os,pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
src=open("girdi_gruplari.py").read().split("rows=[]")[0];ns={};exec(src,ns)
d,GIRDI,LAB,COST,MARJ=ns["d"],ns["GIRDI"],ns["LAB"],ns["COST"],ns["MARJ"]
W1,W2,W3,M2,M3=.70,.10,.20,.60,.50;WY=W2*M2+W3*M3
f=lambda m,s:(1 if m is None else (1-m)/.9)*(1-s)
m1,s1,y,my,sy=.179,.05,.65,.15,.05
DELTA=.10;STOK=.50;R_STOK=.07;STOK_AY=3;CPWD_SABIT=.15   # VARSAYIM (CPWD %15 sabit pay kaynakli: 10CC W=0.85xM)
mz,fx,lc=d.malzeme/d.malzeme.iloc[0],d.usdtry/d.usdtry.iloc[0],d.iscilik/d.iscilik.iloc[0];g3=.5*mz+.5*fx
P={ # parca: (seri, arac)
 "G1 stoklanabilir":(GIRDI*W1*f(m1,s1)*STOK*mz,"stok"),
 "G1 stoklanamayan":(GIRDI*W1*f(m1,s1)*(1-STOK)*mz,"cpwd"),
 "Y yerli kisim":(GIRDI*WY*f(my,sy)*y*mz,"cpwd"),
 "Y ithal bilesen":(GIRDI*WY*f(my,sy)*(1-y)*fx,"fon"),
 "G2 kalan makine":(GIRDI*W2*(1-M2)*fx,"cpwd"),
 "G3 kalan sinirli":(GIRDI*W3*(1-M3)*g3,"fon"),
 "Iscilik":(LAB*lc,"maliyet")}
CI=sum(s for s,_ in P.values())
def trend(ser,t):
    if t<12: return None
    return np.mean([ser.iloc[j]/ser.iloc[j-6]-1 for j in range(max(6,t-24),t+1)])
def corridor(ser,i0,T):
    b=[1.0]
    for k in range(6,T+1,6):
        t=i0+k;g=(ser.iloc[t]/ser.iloc[i0])/b[-1]-1;tr=trend(ser,t-6)
        if tr is not None:g=float(np.clip(g,tr-DELTA,tr+DELTA))
        b.append(b[-1]*(1+g))
    return np.array(b)
def avg3(ser,t): return ser.iloc[max(0,t-2):t+1].mean()
def cohort(i0,T,yapi):
    ks=list(range(0,T+1,6));w={n:s.iloc[i0]/CI.iloc[i0] for n,(s,_) in P.items()}
    mb=np.zeros(len(ks));mc_rev=np.zeros(len(ks));fon=0;stokc=0;Cm=np.zeros(T)
    for n,(s,a) in P.items():
        act=np.array([s.iloc[i0+k]/s.iloc[i0] for k in ks]);mon=np.array([s.iloc[i0+m]/s.iloc[i0] for m in range(T)])
        if yapi=="arac yok": a="maliyet"
        if yapi=="koridor +-10 tum sepet": a="fon"
        if a=="maliyet": b=act;rev=act;cost=mon
        elif a=="cpwd":
            r=np.array([CPWD_SABIT+(1-CPWD_SABIT)*avg3(s,i0+k)/avg3(s,i0) for k in ks]);b=r;rev=r;cost=mon
        elif a=="stok":   # stoktan koridor fiyatiyla tedarik: muteahhit maliyeti = koridor yolu (aylik ara degerleme)
            b=corridor(s,i0,T);rev=b;cost=np.interp(range(T),ks,b)
            stokc+=sum(COST/T*w[n]*mon[m]*STOK_AY*R_STOK/12 for m in range(T))
            stokc+=sum(COST/T*w[n]*(mon[m]-cost[m]) for m in range(T))  # platformun fiyat farki yuku (gercek - koridor)
        elif a=="fon": b=corridor(s,i0,T);rev=act;cost=mon
        mb+=w[n]*b;mc_rev+=w[n]*rev;Cm+=w[n]*cost
    C=sum(COST/T*Cm);P0=(1+MARJ)*COST
    R=min(P0*mc_rev[-1],(1+MARJ)*C)          # %30 tavan tum yapilarda
    k=R/(P0*mc_rev[-1]);Pb=k*P0*mb[-1];fon=R-Pb   # alici: ayni olcek, arac endeksiyle; fark fondan
    return dict(alici=Pb/COST,marj=R/C-1,fon=fon/COST,stok=stokc/COST,upd=list(mb[1:]/mb[:-1]-1),
                fon_payi=sum(w[n] for n,(s,a) in P.items() if a=="fon") if yapi=="karma" else (1 if "koridor" in yapi else 0))
Y=["arac yok","koridor +-10 tum sepet","karma"];rows=[];upd=[]
for T in (18,24):
  for yp in Y:
    for i0 in range(len(d)-T):
        r=cohort(i0,T,yp);rows.append(dict(yapi=yp,teslim_ay=T,baslangic=d.index[i0].date(),**{k:v for k,v in r.items() if k!="upd"}))
        upd+= [dict(yapi=yp,teslim_ay=T,degisim=g) for g in r["upd"]]
bt=pd.DataFrame(rows);u=pd.DataFrame(upd)
o=bt.groupby(["teslim_ay","yapi"]).agg(alici=("alici","mean"),alici_std=("alici","std"),marj_ort=("marj","mean"),marj_min=("marj","min"),
   zarar=("marj",lambda x:int((x<0).sum())),fon_ort=("fon","mean"),fon_max=("fon","max"),stok_ort=("stok","mean"),stok_max=("stok","max"))
o["kohort_CV"]=o.alici_std/o.alici
o=o.join(u.groupby(["teslim_ay","yapi"]).degisim.agg(upd_ort="mean",upd_std="std"))
o=o.reindex([(T,yp) for T in (18,24) for yp in Y])
o.round(4).to_csv("data/oynaklik_karma_ozet.csv");bt.to_csv("data/oynaklik_karma_backtest.csv",index=False)
w0={n:s.iloc[-1]/CI.iloc[-1] for n,(s,_) in P.items()}
pd.DataFrame([dict(parca=n,arac=a,pay_Ara2019=round(s.iloc[0]/CI.iloc[0],4),pay_Ara2025=round(s.iloc[-1]/CI.iloc[-1],4)) for n,(s,a) in P.items()]).to_csv("data/oynaklik_karma_paylar.csv",index=False)
print(o.round(4).to_string());print(pd.read_csv("data/oynaklik_karma_paylar.csv"))
fig,ax=plt.subplots(1,2,figsize=(13,5));x=np.arange(3)
for j,T in enumerate((18,24)):
    v=[o.loc[(T,yp),"upd_std"]*100 for yp in Y];ax[0].bar(x+j*.38,v,.38,label=f"{T} ay")
    for xi,vi in zip(x+j*.38,v): ax[0].text(xi,vi+.1,f"{vi:.1f}",ha="center",fontsize=8)
ax[0].set_xticks(x+.19,Y,fontsize=8);ax[0].set_title("6 aylik alici fiyat guncellemesi std (puan)");ax[0].legend()
ax[1].boxplot([u[(u.yapi==yp)&(u.teslim_ay==24)].degisim*100 for yp in Y],tick_labels=Y);ax[1].set_title("6 aylik guncelleme % dagilimi (24 ay)");ax[1].tick_params(labelsize=8)
fig.tight_layout();fig.savefig("grafik_oynaklik_karma.png",dpi=120);fig.savefig("grafik_oynaklik_karma.svg")
