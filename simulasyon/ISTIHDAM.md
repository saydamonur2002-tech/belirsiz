# İstihdam Etkisi — Varsayımsız

Yalnızca yayımlanmış verilerle hesaplanabilenler ile hesaplanamayanları ayırır. Script: `istihdam.py`, çıktı: `data/istihdam_sonuc.csv`.

## 1. Kullanılan gerçek veriler
| Veri | Değer | Kaynak |
|---|---|---|
| İnşaat istihdamı (NACE F), 2025 | 2.224.000 kişi (toplamın %6,8'i) | TÜİK İşgücü İstatistikleri, TBMM soru önergesinde aktarılan ([pdf](https://cdn.tbmm.gov.tr/KKBSPublicFile/D28/Y4/T7/WebOnergeMetni/0b87f84e-a035-4ef8-a786-38be85aad887.pdf)) |
| İnşaat istihdamı yıllık değişim, 2025 Ç4 | +86 bin (%4,0) | TÜİK, [BMD özet](https://www.bmd.com.tr/application/files/4917/7262/1554/Issizlik_ve_Istihdam_Verileri_-_Ocak_2026.pdf) |
| Kayıt dışı oran, toplam / tarım dışı, 2025 Ç4 | %24,6 / %15,9 | TÜİK; **inşaata özgü oran TÜİK bültenlerinde yayımlanmıyor** |
| Bina inşaatı SGK sigortalı artışı, Aralık 2025 (yıllık) | +146.745 | SGK, [TEPAV](https://tepav.org.tr/tr/haberler/s/11182) |
| Konut talebi fiyat esnekliği | −0,85 / −0,95 (il paneli 2004–2011) | Solak & Kabadayı (2016), [Adv. Mgmt & Appl. Econ.](http://www.scienpress.com/download.asp?ID=1784) |
| Konut talebi fiyat esnekliği | −0,29 / −0,35, **istatistiksel olarak anlamsız** | Ceritoğlu (2017), [TCMB WP 17/14](https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Publications/Research/Working+Paperss/2017/17-14) |
| İnşaat Tip II istihdam çarpanı, 2014 | 1,678 (2000–2014 aralığı 1,61–2,07) | Gül & Çakaloğlu, WIOD G-Ç ([doi](https://doi.org/10.25294/auiibfd.357622)) |

## 2. Hesaplanabilen (a)
Fiyat düşüşü (VARSAYIMSIZ.md): alıcı USD bazında %5–9 az öder.

| Senaryo | Talep artışı | Doğrudan iş (tüm sektör üst sınırı) | Doğrudan+dolaylı+uyarılmış (×1,678) |
|---|---|---|---|
| Esneklik anlamsız (TCMB) | %0 | 0 | 0 |
| %5 düşüş, −0,85 | %4,2 | ~94.500 | ~158.600 |
| %9 düşüş, −0,95 | %8,5 | ~190.200 | ~319.100 |

**Bu rakamlar üst sınırdır, tahmin değildir:**
- Fiyat düşüşü yalnız platformdaki KOBİ konutlarına uygulanır. Platformun pazar payı bilinmiyor. Etki kabaca kapsamla orantılıdır: **her %10 kapsam başına doğrudan 0 – ~19 bin iş**.
- 2,224 milyonun tamamı konut değildir (altyapı ve ticari yapılar dahil). Konut payı ayrıştırılmadı.
- İşgücü yoğunluğunun (iş/m²) sabit kaldığı kabul ediliyor. Modüler üretim bunu düşürebilir (bkz. b).
- Yerinden etme yok sayıldı (platform dışı müteahhitlerden talep kayması). Kayma tamsa net etki sıfıra yaklaşır.
- Esneklik literatürü çelişiyor. Ceritoğlu sıfırdan ayırt edilemiyor; daha uzun dönemli toplu çalışmalar (örn. 1964–2014 sınır testi) pozitif ilişki bile buluyor (yatırım malı etkisi). **Dolayısıyla kanıtla savunulabilir aralık 0'dan başlar.**

## 3. Hesaplanamayan, pilot veri gerekir (b)
| Kanal | Yön | Neden hesaplanamıyor |
|---|---|---|
| KOBİ sigorta dışı işçilik desteğinin kayıt altına alma etkisi | + (kayıtlı) | İnşaata özgü kayıt dışı oran yayımlanmıyor; Türkiye'de bu desteğe ait bir esneklik tahmini bulunamadı |
| Aracıların tasfiyesi | − | Aracı/taşeron istihdamı ayrı ölçülmüyor |
| Modüler/uzmanlaşmış ağ | ± (şantiye işi azalır, fabrika işi artar) | Türkiye verisi yok |
| Yerlileştirme/G1 orta ölçekli üretim (çimento vb.) | + (imalat) | Kapasite ve yatırım verisi pilot gerektirir |
| Zarar eden kohortların 87→15 / 103→15 düşmesi | + (iflas kaynaklı iş kaybı azalır) | Kohort başına istihdam verisi yok |

## 4. Sonuç
Veriyle kanıtlanabilen net istihdam etkisi **0 ile pozitif bir üst sınır arasındadır**. Üst sınır her %10 platform kapsamı başına doğrudan ~19 bin, zincirle birlikte ~32 bin iştir. Sıfırın altında olduğunu gösteren bir veri yok. Sıfırın üstünde olduğunu kanıtlayan, anlamlı ve güncel bir esneklik de yok. Kayıt dışılık, aracılar ve modüler ağ etkilerinin işareti bile pilot olmadan belirlenemez.

**Pilotta ölçülmesi gerekenler:** iş/m², SGK kayıtlı çalışan/şantiye, aracı sayısı, platform ve kontrol grubu satış hacmi (fark-farklar yöntemi).
