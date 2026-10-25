# İnşaatta Ücret Farkları ve İşçilik Maliyeti Oynaklığı (kısa not)

**Kısa cevap:**
- **Meslekler arası fark yüksek.** İnşaatta yönetici ile nitelik gerektirmeyen işçinin net ücreti arasında yaklaşık **3,5 kat** fark var (2020, TÜİK Hanehalkı İşgücü Anketi mikro verisi; akademik çalışma).
- **Sektör içindeki dağılım ise dar.** Ücretlilerin **%71,4'ü asgari ücret civarında veya altında** çalışıyor (TCMB, 2021). Yani ücretler tabanda yığılmış, üstte ince bir yönetici/mühendis kesimi var.
- **Sektör ortalaması düşük:** inşaat, en düşük ortalama kazançlı üç sektörden biri (TÜİK 2022: 104.768 TL; tüm sektörler 144.390 TL, yani ortalamanın %73'ü).

## 1. Kaynaklı veriler

| Gösterge | Değer | Dönem | Kaynak |
|---|---|---|---|
| İnşaat yıllık ort. brüt kazanç | 104.768 TL | 2022 | TÜİK Kazanç Yapısı İst. 2022 ([Sözcü](https://www.sozcu.com.tr/turkiye-de-en-yuksek-kazanc-getiren-sektor-ve-meslekler-aciklandi-p10800)) |
| Tüm sektörler ort. (erkek / kadın) | 144.390 TL (147.446 / 138.366) | 2022 | aynı |
| En yüksek sektör (finans) / en düşük (konaklama) | 293.511 / 99.290 TL | 2022 | aynı |
| Tüm ekonomide yönetici / nitelikli tarım çalışanı | 276.507 / 94.849 TL (2,9 kat) | 2022 | aynı |
| İnşaatta net ücret, meslek: yönetici / usta (craft) / nitelik gerektirmeyen | 4.346 / 1.614 / 1.249 TL → yönetici/nitelik gerektirmeyen ≈ **3,5 kat** | 2020 | [ELRR, Cambridge](https://www.cambridge.org/core/journals/the-economic-and-labour-relations-review/article/multiple-faces-of-labour-market-segmentation-within-the-turkish-construction-industry/3815FFDBE9A28CF58EA84128C9A4927F) (TÜİK HİA mikro verisi) |
| İnşaatta net ücret, eğitim: diplomasız / yükseköğretim | 1.272 / 3.697 TL → **2,9 kat** | 2020 | aynı |
| İnşaatta net ücret, işyeri büyüklüğü: 10'dan az çalışan / 50+ | 1.345 / 3.103 TL → **2,3 kat** | 2020 | aynı |
| İnşaatta net ücret, göçmen / Türkiye doğumlu | 1.373 / 1.885 TL | 2020 | aynı |
| Asgari ücret (net, karşılaştırma için) | 2.324 TL | 2020 | aynı |
| **İnşaatta asgari ücret ve altı ücretli payı** | **%71,4** (tarım dışı %43,1; sanayi %50,4; hizmet %37,9) | 2021 | [TCMB Enflasyon Raporu 2023-III Kutu 2.6](https://www.tcmb.gov.tr/wps/wcm/connect/6adfc471-cb81-4414-b8e7-d06db05ec176/Box_2.6_2023_iii_.pdf?CACHEID=ROOTWORKSPACE-6adfc471-cb81-4414-b8e7-d06db05ec176-oGIinsn&MOD=AJPERES) |
| Personel gideri / üretim değeri, inşaat | %9,0 | 2021 | aynı |
| SGK 4/a, asgari ücret ve altı (tüm sektörler) | %40,5; ort. kazanç asgari ücretin 2,06 katı | 2025 sonu | SGK İstatistik Yıllığı ([derleme](https://asgariucret.co/asgari-ucretle-calisan-orani)) |
| Kayıt dışı istihdam (toplam / tarım dışı) | %26,9 / %16,9 | 2025 Ç3 | TÜİK HİA ([BMD özeti](https://www.bmd.com.tr/application/files/9617/7002/5925/Issizlik_ve_Istihdam_Verileri_-_Aralik_2025.pdf)) |
| Kayıt dışı istihdam (toplam) | %24,6 | 2025 Ç4 | TÜİK HİA ([TEPAV](https://tepav.org.tr/tr/haberler/s/11182)) |
| İnşaat Maliyet Endeksi, işçilik | Aylık **+%23,58** (Ocak 2025); yıllık +%34,37; malzeme aylık +%1,96 | Ocak 2025 | TÜİK İME ([AA](https://www.aa.com.tr/tr/ekonomi/insaat-maliyetlerindeki-artis-49-ayin-en-dusugunde/3507078)) |

**Bulunamayanlar:**
- İnşaat sektöründe meslek, cinsiyet ve eğitim kırılımlı TÜİK KYA tabloları ve P90/P10 oranı: TÜİK veri portalı otomatik erişime kapalı.
- İnşaata özel kayıt dışılık oranı: yalnız "tarımdan sonra en yaygın" ifadesi var (BMD).
- SGK'nın inşaata özel kazanç dağılımı.
- Eurostat SES 2022'de inşaat (NACE F) ve Türkiye satırı: API'den alınamadı. AB içinde ülke bazında tüm ekonomi D9/D1 oranı 2,2 (İsveç) ile 4,5 (Bulgaristan) arasında ([Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Earnings_statistics)). Türkiye inşaat için doğrudan karşılaştırılabilir bir oran yok.

## 2. Modele çıkarımlar
1. **İşçilik oynaklığının ana kaynağı asgari ücret artışları.** İşçilerin %71'i asgari ücret civarında olduğu için zam doğrudan işçilik endeksine geçiyor: Ocak 2025'te bir ayda +%23,6. Malzeme aynı ay +%2,0.
2. **Model açığı:** simülasyondaki aylık işçilik serisi yumuşatılmış (her ay eşit artış), Ocak/Temmuz sıçramalarını göstermiyor. 6 aylık güncelleme Ocak ve Temmuz'a hizalanırsa sıçrama tek adımda fiyata geçer. Bu, OYNAKLIK_KARMA.md'deki işçilik kaynaklı oynaklığın gerçekte **daha yüksek** olabileceği anlamına gelir.
3. **Standart işçilik ücret skalası (öneri, VARSAYIM):**
   - Asgari ücreti taban alan kademeli bir skala; örnek katlar: nitelik gerektirmeyen 1,0; usta 1,3–1,6; operatör/teknisyen 1,6–2,0; mühendis 2,5+ (katlar varsayım; kalibrasyon için KYA meslek verisi gerekli).
   - Skala, asgari ücret takvimine (Ocak/Temmuz) bağlı ve önceden ilan edilir. Böylece işçilik artışı öngörülebilir olur ve CPWD formülündeki "L" (işçilik) bileşenine doğrudan girer. CPWD 10CC de işçilik endeksi olarak asgari ücreti kullanır.
   - Skala, sigortalı çalıştırmayı KOBİ teşvikinin şartı yaparak kayıt dışılığı da azaltır.
   - Skalanın etkisi seviyededir. Oynaklığı azaltmaz; yalnız öngörülebilir kılar.
