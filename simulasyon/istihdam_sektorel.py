# Sektörel (inşaat dışı girdi sektörleri) istihdam etkisi — varsayımsız, Tip I (yurtiçi Leontief)
# Veri: WIOD 2016 release, Türkiye NIOT 2014 (yurtiçi akışlar, mn USD) + Socio-Economic Accounts (EMP, bin kişi)
# https://doi.org/10.34894/PJ2M1C  (dosyalar: NIOTS.zip/TUR_NIOT_nov16.xlsx, Socio_Economic_Accounts.xlsx)
import pandas as pd, numpy as np, sys
NIOT = sys.argv[1] if len(sys.argv)>1 else 'TUR_NIOT_nov16.xlsx'
SEA  = sys.argv[2] if len(sys.argv)>2 else 'Socio_Economic_Accounts.xlsx'
YIL=2014; L_INSAAT_2025=2_224_000           # TÜİK 2025 inşaat istihdamı
TALEP=(0.042,0.085)                           # ISTIHDAM.md: %0 / %4,2–8,5 talep artışı
df=pd.read_excel(NIOT,'National IO-tables',header=None)
codes=df.iloc[0,4:60].tolist()
y=df[df[0]==YIL]
dom=y[y[3]=='Domestic'].set_index(1)
Z=dom.iloc[:,4-0:60-0].astype(float).values if False else dom.loc[codes, list(range(4,60))].astype(float).values
fd=dom.loc[codes, list(range(60,66))].astype(float).sum(axis=1).values
X=y[y[1]=='GO'][list(range(4,60))].astype(float).values.ravel()
A=Z/np.where(X>0,X,np.nan); A=np.nan_to_num(A)
L=np.linalg.inv(np.eye(56)-A)
sea=pd.read_excel(SEA,'DATA'); sea=sea[(sea.country=='TUR')&(sea.variable=='EMP')].set_index('code')[YIL]
emp=sea.reindex(codes).fillna(0).values*1000
e=np.where(X>0,emp/X,0)                       # kişi / mn USD
f=codes.index('F')
yF=np.zeros(56); yF[f]=fd[f]
bagli=e*(L@yF)                                # inşaat nihai talebine bağlı istihdam (2014)
pay=Z[:,f]/np.where(X>0,X,np.nan)             # çıktının inşaata satılan payı (doğrudan)
oran=(e*L[:,f])/(e[f]*L[f,f])                 # inşaatta 1 ek işe karşılık i sektöründe ek iş
grup={'B':'Madencilik/taş ocakçılığı','C16':'Ağaç ürünleri','C20':'Kimya (boya vb.)','C22':'Kauçuk-plastik (PVC dahil)',
 'C23':'Metalik olmayan mineral (çimento, seramik, cam)','C24':'Ana metal (çelik, alüminyum)','C25':'Fabrikasyon metal',
 'C27':'Elektrikli teçhizat','C28':'Makine','C19':'Kok/rafine petrol','D35':'Elektrik-gaz','G46':'Toptan ticaret','G47':'Perakende',
 'G45':'Motorlu taşıt ticareti','H49':'Kara taşımacılığı','H52':'Depolama','K64':'Finans','L68':'Gayrimenkul','M69_M70':'Hukuk/muhasebe/yönetim',
 'M71':'Mimarlık-mühendislik','N':'İdari destek (kiralama, işgücü)','A01':'Tarım','C31_C32':'Mobilya','C33':'Makine kurulum/onarım','I':'Konaklama-yiyecek'}
rows=[]
for i,c in enumerate(codes):
  if c=='F': continue
  dE=[d*L_INSAAT_2025*oran[i] for d in TALEP]
  rows.append(dict(kod=c,sektor=grup.get(c,df.iloc[1,4+i]),istihdam_2014=round(emp[i]),insaata_satis_payi_pct=round(100*pay[i],1),
    insaata_bagli_istihdam_2014=round(bagli[i]),kisi_per_mnUSD=round(e[i],1),is_per_100_insaat_isi=round(100*oran[i],2),
    ek_is_kapsam10_alt=0,ek_is_kapsam10_ust_dusuk=round(dE[0]*0.1),ek_is_kapsam10_ust_yuksek=round(dE[1]*0.1),
    ek_is_tum_dusuk=round(dE[0]),ek_is_tum_yuksek=round(dE[1])))
r=pd.DataFrame(rows).sort_values('ek_is_tum_yuksek',ascending=False)
r.to_csv('data/istihdam_sektorel.csv',index=False)
top=r.head(15).copy()
print(top[['kod','sektor','istihdam_2014','insaata_satis_payi_pct','insaata_bagli_istihdam_2014','is_per_100_insaat_isi','ek_is_kapsam10_ust_dusuk','ek_is_kapsam10_ust_yuksek','ek_is_tum_dusuk','ek_is_tum_yuksek']].to_string(index=False))
print('TOPLAM insaat disi: per100=',round(100*(oran.sum()-1),1),' kapsam10=',round(0.1*TALEP[0]*L_INSAAT_2025*(oran.sum()-1)),'-',round(0.1*TALEP[1]*L_INSAAT_2025*(oran.sum()-1)),
 ' tum=',round(TALEP[0]*L_INSAAT_2025*(oran.sum()-1)),'-',round(TALEP[1]*L_INSAAT_2025*(oran.sum()-1)))
print('insaat emp2014',emp[f],'bagli toplam disi',round(bagli.sum()-bagli[f]),'Tip I istihdam carpani',round(oran.sum(),3))
print('ithalat sizinti: insaat ara girdi ithal payi',round(y[(y[3]=='Imports')][f+4].astype(float).sum()/ (y[(y[3]=='Imports')][f+4].astype(float).sum()+Z[:,f].sum())*100,1),'%')
