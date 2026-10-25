# İnşaat Dışı Girdi Sektörlerine İstihdam Etkisi — Varsayımsız

Bu dosya [ISTIHDAM.md](ISTIHDAM.md)'nin devamıdır. Script: `istihdam_sektorel.py`, tam tablo: `data/istihdam_sektorel.csv` (55 sektör).

## Veri ve yöntem
- **G-Ç tablosu:** TÜİK'in en güncel simetrik G-Ç tablosu 2012 yılına ait (A64). TÜİK veri portalında doğrudan indirilebilir dosyası bulunamadı. OECD 2025 IOT/ICIO dosyaları Cloudflare engeline takıldı. Bu yüzden **WIOD 2016 sürümündeki Türkiye ulusal G-Ç tablosu (2014, yurtiçi akışlar, 56 sektör)** kullanıldı. Bu tablo TÜİK arz-kullanım tablolarından türetilmiştir. Kaynak: Timmer vd. (2015), [doi:10.34894/PJ2M1C](https://doi.org/10.34894/PJ2M1C), `TUR_NIOT_nov16.xlsx`.
- **Sektörel istihdam:** WIOD Sosyo-Ekonomik Hesaplar, EMP 2014. Aynı veri setinden alındı ve TÜİK HİA'ya dayanıyor.
- **Hesap:** İstihdam katsayısı e = EMP / üretim (kişi / milyon USD). Leontief tersi yurtiçi tablodan hesaplandı (Tip I), yani ithal girdi sızıntısı zaten dışarıda bırakıldı. Bir sektörün ek işi şöyle bulunur: inşaattaki ek doğrudan iş × (e_i·L_iF)/(e_F·L_FF).
- **Talep:** ISTIHDAM.md ile aynı. Alt sınır %0, üst sınır %4,2–8,5. İnşaat bazı TÜİK 2025'teki 2.224.000 kişi.
- **Sonuç:** İnşaatta her 100 ek işe karşılık inşaat dışındaki sektörlerde **34,4 ek iş** çıkar (Tip I çarpanı 1,344). Uyarılmış tüketim etkisi dahil değildir. Tip II çarpanı 1,678 (bkz. ISTIHDAM.md).

## Tablo (2014 yapısı, 2025 inşaat bazı; alt sınır her satırda 0)
| Sektör | İstihdam (2014) | Çıktının inşaata satılan payı | İnşaata bağlı istihdam (2014) | Ek iş / %10 kapsam | Ek iş / tüm sektör |
|---|---|---|---|---|---|
| C23 Metalik olmayan mineral (çimento, seramik, cam) | 368.331 | %27,1 | 108.410 | 0 – 455–920 | 0 – 4.547–9.202 |
| C24 Ana metal (çelik, alüminyum) | 425.063 | %3,4 | 16.973 | 0 – 71–144 | 0 – 712–1.441 |
| C25 Fabrikasyon metal | 253.488 | %11,6 | 29.578 | 0 – 124–251 | 0 – 1.240–2.511 |
| C22 Kauçuk-plastik (PVC) | 296.418 | %3,4 | 12.252 | 0 – 51–104 | 0 – 514–1.040 |
| C16 Ağaç ürünleri | 144.973 | %18,5 | 29.432 | 0 – 123–250 | 0 – 1.234–2.498 |
| C20 Kimya (boya vb.) | 169.271 | %1,3 | 3.963 | 0 – 17–34 | 0 – 166–336 |
| C27 Elektrikli teçhizat | 148.634 | %3,8 | 6.056 | 0 – 25–51 | 0 – 254–514 |
| C28 Makine | 472.128 | %1,2 | 6.218 | 0 – 26–53 | 0 – 261–528 |
| B Madencilik / taş ocakçılığı | 167.842 | %3,2 | 13.664 | 0 – 57–116 | 0 – 573–1.160 |
| D35 Elektrik-gaz | 207.116 | %0,7 | 8.522 | 0 – 36–72 | 0 – 357–723 |
| H49 Kara taşımacılığı | 1.088.577 | %2,7 | 46.771 | 0 – 196–397 | 0 – 1.962–3.970 |
| G46 Toptan ticaret | 1.930.361 | %4,7 | 122.306 | 0 – 513–1.038 | 0 – 5.129–10.381 |
| G47 Perakende | 2.069.329 | %3,9 | 101.516 | 0 – 426–862 | 0 – 4.258–8.617 |
| K64 Finans | 339.653 | %3,6 | 20.239 | 0 – 85–172 | 0 – 849–1.718 |
| N İdari destek (kiralama, işgücü) | 265.627 | %5,2 | 21.645 | 0 – 91–184 | 0 – 908–1.837 |
| **Toplam inşaat dışı (55 sektör)** | — | — | **767.079** | **0 – 3.217–6.511** | **0 – 32.171–65.108** |

Not: Fabrikasyon metalin bağlı istihdamı nihai talepten hesaplanır; doğrudan satış payı ise ara girdi akışından. Alüminyum WIOD'da C24 içinde yer alır, ayrıca ayrıştırılamıyor. M71 (mimarlık-mühendislik) Türkiye SEA'da ayrı verilmemiş, M69-M75 içinde kalıyor.

## Hesaplanamayanlar
- **Güncel sektörel istihdam:** Tablo 2014 yapısını kullanıyor. TÜİK'in 2025 NACE-2 haneli istihdamı ve SGK sektörel sigortalı serisi bu çalışmada çekilmedi. Verimlilik 2014'ten bu yana arttıysa (kişi / üretim düştüyse) rakamlar olduğundan yüksek çıkar.
- **Yerlileştirmenin ithalat sızıntısını değiştirmesi:** 2014'te inşaatın ara girdilerinin %28,5'i ithaldi. Yerlileştirme bu payı düşürürse yurtiçi iş artar. Ancak ne kadar artacağı, yeni tesislerin işgücü yoğunluğuna bağlı ve bu veri yok.
- **Ticaret satırları (G46/G47):** Aracı tasfiyesi bu sektörlerde iş **azaltır**. Tablodaki artış, aracıların yerinde kaldığı yapıya göre hesaplandı. Tasfiyenin net etkisi pilot verisi gerektirir.
- **Modüler ağ:** Prefabrikasyon işi inşaattan C23 ve C25'e kaydırabilir. Toplam iş sayısı değişmeden dağılım değişebilir.
- **Kapsam:** Platformun pazar payı bilinmiyor. Rakamlar her %10 kapsam başına verildi.
