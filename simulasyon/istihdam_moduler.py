# Varsayımlı MODÜLER senaryo istihdam hesabı — tüm varsayımlar aşağıda (düşük/orta/yüksek)
# Normal (varsayımsız) senaryo: istihdam.py + istihdam_sektorel.py
import pandas as pd, numpy as np, sys
NIOT=sys.argv[1] if len(sys.argv)>1 else 'TUR_NIOT_nov16.xlsx'; SEA=sys.argv[2] if len(sys.argv)>2 else 'Socio_Economic_Accounts.xlsx'
LF=2_224_000; ESN=-0.90                        # TÜİK 2025; Solak&Kabadayı -0,85/-0,95 ortası
S=['dusuk','orta','yuksek']
V={ # varsayım: (düşük, orta, yüksek)  kaynak
 'fiyat_dususu':(0.048,0.148,0.299),          # MODULER_AG.md katman 1–6 kümülatif
 'moduler_pay':(0.10,0.25,0.40),               # platform konutlarında modüler/prefabrik payı; İsveç çok katlı ~%45 (U Toronto 2024)
 'iscilik_tasarruf':(0.10,0.20,0.30),          # modüler birimde toplam işçilik azalması; McKinsey 2019: süre -%20-50, maliyet 0-%20
 'fabrika_payi':(0.60,0.70,0.85),              # modüler birimde işin fabrikaya kayan payı; BoKlok %85 fabrikada
 'toptan_tasfiye':(0.10,0.25,0.50),            # inşaata bağlı toptan ticaret işinin kalkan payı (MODULER_AG bayi katmanı -0,3/-1,4/-4,2%)
 'perakende_tasfiye':(0.0,0.10,0.25),
 'y_yerlilik_artis':(0.0,0.10,0.20),           # Y kalemleri ~%55 -> %55/65/75 (OLCEK_YERLILESTIRME.md)
 'y_girdi_payi':(0.16,0.16,0.16),              # Y kalemlerinin girdi payı (OLCEK_YERLILESTIRME.md)
 'kayitdisi_insaat':(0.25,0.30,0.35),          # inşaata özgü TÜİK oranı yayımlanmıyor; tarım dışı %15,9 alt referans
 'kayit_etkisi':(0.05,0.09,0.13),              # Betcherman, Daysal & Pagés (2010, Labour Econ.) 5084 SGK prim teşviki: kayıtlı istihdam +%5-13
}
df=pd.read_excel(NIOT,'National IO-tables',header=None); codes=df.iloc[0,4:60].tolist()
y=df[df[0]==2014]; dom=y[y[3]=='Domestic'].set_index(1)
Z=dom.loc[codes,list(range(4,60))].astype(float).values
X=y[y[1]=='GO'][list(range(4,60))].astype(float).values.ravel()
A=np.nan_to_num(Z/np.where(X>0,X,np.nan)); L=np.linalg.inv(np.eye(56)-A)
sea=pd.read_excel(SEA,'DATA'); sea=sea[(sea.country=='TUR')&(sea.variable=='EMP')].set_index('code')[2014]
emp=sea.reindex(codes).fillna(0).values*1000; e=np.where(X>0,emp/np.where(X>0,X,1),0)
f=codes.index('F'); imp=y[y[3]=='Imports'][f+4].astype(float).sum(); II=imp+Z[:,f].sum()
oran=(e*L[:,f])/(e[f]*L[f,f])                  # inşaat 1 işine karşı sektör i işi
fab_sek=['C16','C23','C25']; yer_sek=['C22','C27','C28']
cov=1.0                                        # tüm sektör; %10 kapsam = /10
out={}
for k,s in enumerate(S):
  g=lambda n:V[n][k]
  talep=-ESN*g('fiyat_dususu')
  dF=talep*LF*cov                               # talep kaynaklı ek inşaat işi (geleneksel yoğunlukta)
  base=LF*cov*(1+talep)
  mod=base*g('moduler_pay')                      # modüler birimlere düşen iş
  tasarruf=mod*g('iscilik_tasarruf')
  fabrika=(mod-tasarruf)*g('fabrika_payi')
  saha_kayip=tasarruf+fabrika                    # şantiyeden çıkan iş
  sek=dict(zip(codes,(oran*dF)))
  for c in fab_sek: sek[c]+=fabrika/len(fab_sek) # fabrikaya kayan iş
  sek['G46']-=g('toptan_tasfiye')*(sek['G46']+ (122306/2343947)*LF*cov)
  sek['G47']-=g('perakende_tasfiye')*(sek['G47']+(101516/2343947)*LF*cov)
  # yerlileştirme: ikame edilen ithalat = Y payı × yerlilik artışı × ithal ara girdi; iş = e×L
  ik=g('y_girdi_payi')*g('y_yerlilik_artis')*imp*(1+talep)*cov
  yer=0
  for c in yer_sek:
    j=codes.index(c); add=(e*L[:,j]).sum()*ik/len(yer_sek); sek[c]+=add; yer+=add
  insaat_dogrudan=dF-saha_kayip
  kayit=LF*cov*(1-g('kayitdisi_insaat'))*g('kayit_etkisi')
  disi=sum(v for c,v in sek.items() if c!='F')
  out[s]=dict(talep_artis_pct=round(100*talep,1),insaat_saha_net=round(insaat_dogrudan),fabrikaya_kayan=round(fabrika),
    verimlilik_kaybi=round(-tasarruf),aracı_kaybi_G46_G47=round(sek['G46']-oran[codes.index('G46')]*dF+sek['G47']-oran[codes.index('G47')]*dF),
    yerlilestirme_imalat=round(yer),insaat_disi_toplam=round(disi),net_toplam=round(insaat_dogrudan+disi),kayitliya_gecen=round(kayit))
  out[s].update({f'sek_{c}':round(sek[c]) for c in ['C23','C24','C25','C22','C16','C20','C27','C28','B','D35','H49','G46','G47','K64','N']})
r=pd.DataFrame(out); r.to_csv('data/istihdam_moduler.csv'); print(r.to_string())
print('ithal ara girdi payi',round(imp/II,3))
