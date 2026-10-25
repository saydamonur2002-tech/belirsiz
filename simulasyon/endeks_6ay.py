"""6 aylik fiyat guncelleme: (A) maliyet bazli, (B) kur bazli; %30 tavan korunur. Agirliklar VARSAYIM (GIRDI_GRUPLARI.md)."""
import pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
src=open("girdi_gruplari.py").read().split("rows=[]")[0];ns={};exec(src,ns)
d,W,GIRDI,LAB,COST,MARJ=ns["d"],ns["W"],ns["GIRDI"],ns["LAB"],ns["COST"],ns["MARJ"]
b=pd.read_csv("data/QTRN628BIS.csv",parse_dates=["observation_date"]).set_index("observation_date").QTRN628BIS
b=np.exp(np.log(b).resample("MS").interpolate());d=d.join(b.rename("bis")).dropna()
G1KOBI=(1-.179)/.9*(1-.05)  # Cimsa FAVOK %17,9 + %5 olcek (varsayim)
def run(i0,T,rule,f=1.0):
    fx=d.usdtry/d.usdtry.iloc[i0];mz=d.malzeme/d.malzeme.iloc[i0];lc=d.iscilik/d.iscilik.iloc[i0]
    ci=GIRDI*(W["G1_olcekli"]*f*mz+W["G2_ithal_makine"]*fx+W["G3_sinirli_yerli"]*(.5*mz+.5*fx))+LAB*lc
    ci0=ci.iloc[i0]
    C=sum(COST/T*ci.iloc[i0+k] for k in range(T))/ci0*f**0  # TL/fx0 birimi
    C=sum(COST/T*ci.iloc[i0+k] for k in range(T))
    P0=(1+MARJ)*COST*ci0
    r=(T//6)*6
    if rule=="eski_6ay_kur_sonra_sabit": P=P0*fx.iloc[i0+min(T,6)]/ci0*ci0
    elif rule=="A_maliyet_bazli_6ay": P=P0*ci.iloc[i0+r]/ci0
    else: P=P0*fx.iloc[i0+r]
    raw=P/C-1;cap=raw>MARJ+1e-9;P=min(P,(1+MARJ)*C)
    pr=(P/P0)/(d.bis.iloc[i0+T]/d.bis.iloc[i0])
    return dict(ham_marj=raw,alici_fiyat_baslangic_maliyet_kati=P/(COST*1.0),marj=P/C-1,tavan_asim=cap,alici_fiyat_piyasa_orani=pr)
rows=[]
for sc,f in [("temel",1.0),("G1_KOBI_orta",G1KOBI)]:
 for rule in ["eski_6ay_kur_sonra_sabit","A_maliyet_bazli_6ay","B_kur_bazli_6ay"]:
  for T in [6,12,18,24,30]:
   for i0 in range(len(d)-T):
    x=run(i0,T,rule,f);rows.append(dict(senaryo=sc,kural=rule,teslim_ay=T,baslangic=d.index[i0].date(),**x))
bt=pd.DataFrame(rows);bt.to_csv("data/backtest_endeks_6ay.csv",index=False)
o=bt.groupby(["senaryo","kural","teslim_ay"]).agg(kohort=("marj","size"),ort_marj=("marj","mean"),min_marj=("marj","min"),
  zarar=("marj",lambda x:int((x<0).sum())),ham_marj_ort=("ham_marj","mean"),alici_fiyat_x=("alici_fiyat_baslangic_maliyet_kati","mean"),tavan_asim=("tavan_asim","sum"),alici_fiyat_piyasa_ort=("alici_fiyat_piyasa_orani","mean")).round(3)
o.to_csv("data/ozet_endeks_6ay.csv");print(o.to_string())
fig,ax=plt.subplots(1,2,figsize=(12,4.8))
for rule,c in [("eski_6ay_kur_sonra_sabit","r"),("A_maliyet_bazli_6ay","g"),("B_kur_bazli_6ay","b")]:
  for sc,ls in [("temel","-"),("G1_KOBI_orta","--")]:
    s=o.loc[(sc,rule)];ax[0].plot(s.index,s.ort_marj*100,ls,c=c,marker="o",label=f"{rule} / {sc}")
    ax[1].plot(s.index,s.alici_fiyat_piyasa_ort,ls,c=c,marker="o")
ax[0].axhline(30,c="gray",ls=":");ax[0].axhline(0,c="k",lw=.6);ax[0].set_title("Ort. muteahhit marji % (tavan %30)");ax[0].set_xlabel("teslim ay");ax[0].legend(fontsize=6)
ax[1].axhline(1,c="k",lw=.6);ax[1].set_title("Alici fiyat artisi / BIS konut endeksi artisi (<1 = piyasadan ucuz)");ax[1].set_xlabel("teslim ay")
fig.tight_layout();fig.savefig("grafik_endeks_6ay.png",dpi=120);fig.savefig("grafik_endeks_6ay.svg")
