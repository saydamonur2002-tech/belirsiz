# Varsayımsız değerlendirme (pt20u)

**Kısa cevap:** Varsayımlar çıkarıldığında kanıtlanabilen maliyet düşüşünün **alt sınırı %0, üst sınırı yaklaşık %6**. Orta senaryodaki %14,8 kaynakla desteklenmiyor.
- **Fiyat kuralının bulgusu sağlam:** Kural, sabit fiyata göre müteahhidi açıkça koruyor ve alıcı çoğu kohortta piyasanın altında kalıyor.
- **Düşen iddia:** "Zarar eden kohort yok, marj %30" iddiası resmî endeksle tutmuyor.

Kod: `varsayimsiz.py`. Çıktılar:
- `data/varsayimsiz_backtest.csv`
- `data/varsayimsiz_marj10.csv`
- `data/varsayimsiz_ozet.csv`
- `data/varsayimsiz_siniflandirma.csv`

## 1. Kaynaklı ağırlıklar
- **TÜİK bina inşaatı maliyet endeksi (2005=100) ağırlıkları:** işçilik %30,9; genel inşaat malzemesi %52,3; tesisat malzemesi %15,6; makine %1,2. Kaynak: Yeni Asya (12.06.2006), TÜİK dağılımı aktarılıyor. Güncel İME 2015=100 ağırlıkları yayımlanmıyor; 77 projeden ~2.300 ürünle belirlendiği biliniyor (Eurostat metaverisi).
- **Zımni güncel malzeme payı:** TÜİK'in Aralık ayı yıllık değişimlerinden Laspeyres özdeşliğiyle türetildi, tüm inşaat için. Önceki Aralık itibarıyla: 2020'de 0,680; 2021'de 0,708; 2022'de 0,785; 2023'te 0,773; 2024'te 0,713; 2025'te 0,671. Buna göre işçilik payı %22–33 arasında oynuyor.
- **Çimentonun konut maliyetindeki payı:** %3–5, ortalama %3,5 (ODTÜ çalışması, TÜRKÇİMENTO aktarımıyla). TOKİ tünel kalıpta %6,5 (2006).

## 2. Sınıflandırma
| Mekanizma / sonuç | Sınıf | Hangi varsayıma bağlı |
|---|---|---|
| 6 aylık maliyet bazlı güncelleme + %30 tavan (TÜİK İME toplam, resmî ağırlıklı) | **Tamamen kaynaklı** | — |
| Grup bazlı endeks (G1/G2/G3, Y) | Kısmen | Girdi %65 / işçilik %35 ve G1/G2/G3 = %70/10/20 ağırlıkları |
| Karma oynaklık (koridor + fon, tampon stok, CPWD) | Kısmen | Grup ağırlıkları, ±10 puanlık koridor, stok maliyeti |
| Ölçek + yerlileştirme + %10 KOBİ marjı (−%1,8 / −7,1 / −13,9) | Kısmen | Ölçek kazancı, G1 payı, yerlilik hedefleri |
| %10 marj, yalnız çimento | **Kaynaklı (sınır)** | FAVÖK net marj değil, bu yüzden sonuç üst sınır |
| Y kalemlerinin yerlileştirilmesi | Tamamen varsayım | Yerlilik hedefleri ve ölçek |
| Gelir vergisi istisnası A1/A2 (statik kayıp ~485 mrd / ~1,24 trilyon TL) | Kısmen | Bant orta noktaları, 2025 dağılımının 2026'ya taşınması |
| A1/A2 geri dönüşleri (KDV/ÖTV, kayıtlılık) | Tamamen varsayım | Tüketim eğilimi, efektif vergi oranı, esneklik |
| Hedefli GV + damga desteği, birim maliyet etkisi | Kısmen, sınır verilebilir | Net ücret sözleşmesi; inşaatta asgari ücret üstü dağılım |
| Hedefli destek mali maliyeti (12–24 mrd TL) | Tamamen varsayım | Platform payı %10–20 |
| Bayi marjının tasfiyesi | **Kaynaklı (sınır)** | Tüm alımın bayiden geçtiği ve marjın tamamının yakalandığı üst sınır |
| Taşeron zincirinin kısalması | **Hesaplanamaz** | Taşeronla yapılan iş payı için kaynak yok |
| Koordinasyon maliyeti | Tamamen varsayım | — |

## 3. Varsayımsız fiyat kuralı backtest'i (2015–2026, aylık kohortlar)
- **Veri:** maliyet olarak TÜİK İME toplam endeksi (resmî ağırlıklı); kur için ECB (USD/TRY); piyasa karşılaştırması için BIS Türkiye konut endeksi.
- **Kural:** fiyat 6 ayda bir maliyetin 1,30 katına güncelleniyor. Teslim anında ek güncelleme yapılmıyor (önceki modelde vardı).

| Teslim | Kohort | Sabit fiyat: ortalama marj / en düşük / zarar eden | Kural: ortalama marj / en düşük / zarar eden | Alıcı fiyat çarpanı (TL) | BIS konut çarpanı | Alıcı çarpanı (USD) |
|---|---|---|---|---|---|---|
| 18 ay | 122 | −%13,9 / −%53,7 / 87 | **%12,4 / −%26,5 / 15** | 1,37 | 1,76 | 0,91 |
| 24 ay | 116 | −%25,4 / −%64,8 / 103 | **%11,7 / −%26,5 / 15** | 1,63 | 2,21 | 0,95 |

- **Müteahhit:** Kural, sabit fiyatta zarar eden kohort sayısını 87'den 15'e indiriyor. Ama marj %30'da kalmıyor; ortalama %12 civarına iniyor. Zararlar 2021–2023 maliyet şoklarında yoğunlaşıyor.
- **Alıcı:** Kohortların %73'ünde fiyat artışı BIS konut endeksinin artışından düşük. USD cinsinden alıcı fiyatı ortalama %5–9 geriliyor.

## 4. Varsayımsız birim maliyet etkisi (konut)
| Kalem | Varsayımsız sonuç | Dayanak |
|---|---|---|
| %10 marj, çimento | Hazır beton 0; Akçansa −%0,12…−0,20; Çimsa −%0,26…−0,44; Oyak çimento −%0,93…−1,55 | FAVÖK 2025 × çimento payı %3–5, ölçek = 0 |
| %10 marj, diğer G1 kalemleri | **Hesaplanamaz** | Kalem payları ve marjları için kaynak yok |
| Hedefli GV + damga desteği | **0 ile −%2,66 arası** | 2026 tarifesi ve asgari ücret, işçilik %30,9. Alt sınır: asgari ücret üstü dağılım bilinmiyor (inşaatın %71,4'ü asgari ücrette, vergi 0). Üst sınır: SGK ekonomi geneli dağılımı ve net ücret sözleşmesi |
| Bayi marjı | **−%0,5 ile −%2,1 arası (üst sınır)** | Genel malzeme %52,3 × kaba malzeme bayi marjı %1–4 (ALTSO) |
| Taşeron zinciri | Hesaplanamaz | — |
| Karma oynaklık araçları | Hesaplanamaz (grup ağırlıkları varsayım) | — |
| 6 aylık güncelleme + %30 tavan | 0 | Birim maliyeti düşürmez, marjı korur |
| **Toplam** | **Kanıtlanabilen alt sınır %0; üst sınır ≈ −%6,2** (1,55 + 2,66 + 2,09) | — |

## 5. Düşen iddialar
1. **"Orta senaryoda −%14,8 (yüksekte −%29,9)":** Kaynakla desteklenmiyor. Kaynaklı üst sınır ≈ %6.
2. **"Zarar eden kohort yok, marj %30":** Resmî endeksle, teslim anında güncelleme yapılmadığında 116–122 kohorttan 15'i zararda; ortalama marj ~%12.
3. **"Ölçek + yerlileştirme −%7,1":** Ölçek ve G1 payı varsayım. Kaynaklı tek kalem olan çimentoda etki ≤ %1,6.
4. **"Taşeron −%2":** Hesaplanamaz.
5. **"Karma araçlar −%0,2" ve fon/stok yükü rakamları:** Grup ağırlıkları varsayım olduğu için hesaplanamaz.
6. **Hedefli destek için "%2,8–3,1" ve "12–24 mrd TL":** Birim maliyet etkisi yalnızca üst sınır olarak (≤ %2,66) kalıyor. Mali maliyet varsayıma bağlı.
7. **A1/A2 net etkileri (geri dönüşler):** Varsayım. Sağlam kalan, statik kaybın büyüklük sırası (yüz milyarlarca TL) ve "devlet daha az toplar" sonucu.

## 6. Eksik veri
- TÜİK İME 2015=100 madde ve grup ağırlıkları yayımlanmıyor. Kullanılan 2005 ağırlığı 20 yıllık ve basın aktarımı.
- Malzeme ve işçilik alt endekslerinin aylık seviyeleri elimde yok; yalnız toplam endeks ve Aralık yıllık değişimleri var.
- İnşaatın 2026 ücret dağılımı yok.
- Taşeronla yapılan iş payı yok.
- Diğer G1 kalemlerinin konut maliyetindeki payı ve net marjları yok.
- BIS konut serisi 2024 sonrasında kesiliyor (son kohort 2024-07).

## 7. Kaynaklar
- https://www.hakedis.org/endeksler/insaat-maliyet-endeksi-ve-degisim-orani (TÜİK İME yansısı)
- https://ec.europa.eu/eurostat/cache/metadata/EN/sts_cons_pri_esms_tr.htm
- https://www.yeniasya.com.tr/2006/06/12/ekonomi/h5.htm
- https://imarpanosu.com/cimentocular-savunmada-muteahhitin-1-milyona-sattigi-evin-cimento-masrafi-7-bin-tl/
- https://www.milliyet.com.tr/ekonomi/daireler-ucuzlasin-cimento-bedava-6599007
- https://www.altso.org.tr/bilgi-hizmetleri/sektorlere-gore-karlilik-oranlari/
- https://fred.stlouisfed.org/series/QTRN628BIS (BIS)
- https://frankfurter.app (ECB referans kurları)
- https://cdn.gib.gov.tr/api/gibportal-file/file/getFileResources?objectKey=arsiv%2Fyardim-kaynaklar%2Fyararli-bilgiler%2Fgelir-vergisi-tarifeleri%2Fgelir-vergisi-tarifesi-2026.pdf
- https://asgariucret.co/asgari-ucretle-calisan-orani (SGK yıllığı)
- https://www.mckinsey.com/capabilities/operations/our-insights/modular-construction-from-projects-to-products
- https://www.nao.org.uk/reports/using-modern-methods-of-construction-to-build-homes-more-quickly-and-efficiently/
