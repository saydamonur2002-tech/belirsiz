# Dijital tahsilat ve hakediş sistemi (tahsilatın düzenli ödenmesi)

Amaç: Hakedişin alıcıdan müteahhide, müteahhitten taşeron ve tedarikçiye zamanında ve eksiksiz akması. Hesap: [tahsilat_sistemi.py](tahsilat_sistemi.py) → [data/tahsilat_sistemi.csv](data/tahsilat_sistemi.csv).

## 1. Tasarım
| Bileşen | İşleyiş | Emsal / mevcut altyapı |
|---|---|---|
| **Proje emanet hesabı** (her platform projesine bir hesap) | Alıcı ödemeleri ve banka kredisi bu hesaba girer. Para müteahhidin genel hesabına geçmez; ona ve alt yüklenicilere ayrı ayrı (halka çitli) dağıtılır. Müteahhit iflas etse de taşeron payı korunur. | UK Project Bank Accounts (Highways England, Scottish SPPN 10/2016, Crossrail); Avustralya NSW/QLD Project Trust Accounts; Hindistan RERA: tahsilatın %70'i proje hesabında, yalnız o projeye harcanır |
| **Dijital hakediş (kilometre taşı)** | Hakediş, platform kataloğundaki iş kalemleri ve yapı denetim onayıyla e-imzalı olarak düzenlenir. Onaylanan tutar emanetten otomatik serbest bırakılır. | EKAP e-hakediş (kamu yapım işleri); e-imza/KEP |
| **Faturalama ve kayıt** | Her hakediş e-fatura/e-arşiv ile eşleşir. Ödenmeyen e-fatura gecikmeye düşer. | GİB e-fatura/e-arşiv |
| **Ödeme kanalı** | Serbest bırakılan tutar anlık transferle gönderilir. | TCMB FAST |
| **Süre kuralı** | Azami 60 gün; sözleşmede süre yoksa 30 gün. | TTK m.1530 |
| **Gecikme faizi** | Vade geçince ticari temerrüt faizi ve gecikme tazminatı sistemde otomatik hesaplanıp borçlunun bir sonraki hakedişinden kesilir. | TTK m.1530 |
| **Hızlı uyuşmazlık çözümü** | İtiraz edilen hakediş, platform uzlaştırma merkezinde 28 günde bağlayıcı geçici kararla çözülür; yargı yolu açık kalır. | UK Construction Act 1996 adjudication; Avustralya Security of Payment Acts |
| **Tedarikçi finansmanı** | Onaylı hakediş, bankada DBS/tedarikçi finansmanında teminat olarak kullanılabilir. | DBS (Doğrudan Borçlandırma Sistemi) |
| **Bildirim** | Uyarı, ihtar ve gecikme bildirimleri KEP ile gider. | KEP |
| **Yaptırım zinciri** | Platform uyarı ve bildirimde bulunur, Bakanlık yaptırım uygular (bkz. README §8). Tekrarlayan gecikmede onay/teşvik askıya alınır. | Model §8 (asil–vekil) |

## 2. Türkiye'de tahsilat sorunu (kaynaklı)
| Veri | Değer | Kaynak |
|---|---|---|
| Karşılıksız çek, Ocak–Kasım 2025 | 272 bin adet, 225 mrd TL | TBMM soru önergesi (TBB/TCMB verisi) |
| Karşılıksız çek, Ocak–Eylül 2025 | 219 bin adet, 175 mrd TL; Eylül'de tutarın %2,8'i | TBB (TBMM kanun teklifi 2/3400) |
| Vadesi geçmiş B2B fatura payı, 2025 | %61; batık alacak ~%11 | Atradius Payment Practices Barometer Türkiye 2025 |
| Yurtiçi ortalama ödeme gecikmesi | 41 gün (2019) | Coface Turkey Payment Survey 2019 |
| İflasların tahsil edilemeyen alacak kaynaklı payı | ~%25 (tüm sektörler) | Hazine ve Maliye Bakanı açıklaması, AA 2018 |
| Konkordato firmalarında ticari borç/varlık | %36 (diğerlerinde %11) | TCMB blog, 2024 |
| Avrupa'da geç ödenen ciro | %11 | Intrum EPR 2025 (Türkiye'ye özgü rakam bulunamadı) |

İnşaat sektörüne özgü karşılıksız çek veya protestolu senet kırılımı bulunamadı. TCMB/TBB veriyi sektörel olarak yayımlamıyor.

## 3. Yurtdışı etki kanıtı
- **UK PBA:** Highways England'da alt kademeye ödeme döngüsü ortalama 19 gün; PBA olmadan bu süre 100 güne kadar çıkıyor. Yükleniciler PBA'nın iflasları azaltacağına inanıyor, ancak bu bir algı anketi; iflas azalmasını ölçen nedensel çalışma yok (J. Financial Management of Property and Construction, 2017).
- **Avustralya:** Murray Review (2017): inşaat, GSYH'nin %8–10'u iken iflasların %20–25'ini oluşturuyor; ana neden kötü ödeme pratikleri. Security of Payment yasaları 1999'dan beri yürürlükte, ama inşaat 2023–24'te kurumsal iflasların hâlâ %26,4'ü (Hazine yanıtı 2025). Yani yasalar iflası ölçülebilir biçimde düşürmedi.
- **Sonuç:** Ödeme süresinin kısaldığı kanıtlı. İflasın azaldığı kanıtlı değil.

## 4. Korunan iş (IFLAS_ISTIHDAM ile birleşik)
Kurgu: Kapanışların %25'i tahsilat kaynaklı (kaynaklı pay), %75'i diğer nedenlerden. Maliyet açığı kuralı bu %75'e backtest azalmasıyla (%83–85) uygulanıyor; tahsilat sistemi %25'i tamamen önlüyor (üst sınır).

| Taban | Risk altındaki iş | Yalnız maliyet kuralı | Yalnız tahsilat | **Birleşik üst sınır** | %10 kapsam | Alt sınır |
|---|---|---|---|---|---|---|
| TOBB kapanış | 28.700 | 23.700–24.500 | 7.200 | **25.000–25.500** (%1,12–1,15) | ~2.500 | 0 |
| Konkordato | 4.400 | 3.700–3.800 | 1.100 | **3.900–4.000** | ~390 | 0 |

**Alt sınır 0**, çünkü tahsilat sistemlerinin iflası azalttığına dair nedensel kanıt yok (Avustralya bunun tersine işaret ediyor) ve maliyet zararı ile iflas arasındaki bağ da kanıtlanmadı. %25 tüm sektörler için verilmiş bir pay; inşaata özgü değer yok.
