# Changelog

## [1.6.3] - 2026-02-09

### Fixed
- ✅ **Ayarlar Kesin Çözüm** - `TypeError: object.__init__()` hatası giderildi. Farklı Home Assistant sürümleriyle tam uyumluluk sağlandı.

## [1.6.2] - 2026-02-09

### Fixed
- ✅ **Ayarlar AttributeError Düzeltildi** - `property 'config_entry' has no setter` hatası kesin olarak giderildi.

## [1.6.1] - 2026-02-09

### Fixed
- ✅ **Ayarlar 500 Hatası** - Veri tipi uyuşmazlığı nedeniyle oluşan hataya yönelik kesin çözüm uygulandı

## [1.6.0] - 2026-02-09

### Added
- ✨ **Manuel Güncelleme Butonu** - `button.ILCE_IL_guncelle` (Tüm verileri anında günceller)
- ✨ **Bildirim Durumu Sensörü** - `sensor.ILCE_IL_notification_status` (Bildirim ayarının durumunu gösterir: Açık/Kapalı)
- ✨ **24 Saatlik Yağmur Tahmini** - `sensor.ILCE_IL_rain_forecast_24h` (Önümüzdeki 24 saatte yağmur yağıp yağmayacağını gösterir)
- ✨ **24 Saatlik Kar Tahmini** - `sensor.ILCE_IL_snow_forecast_24h` (Önümüzdeki 24 saatte kar yağıp yağmayacağını gösterir)
- ⚙️ **Bildirim Ayarı** - Uyarı bildirimlerini açıp kapatma seçeneği eklendi

### Fixed
- ✅ **Otomatik Güncelleme** - 30 dakikalık güncelleme aralığı artık düzgün çalışıyor
- ✅ **Ayarlar 500 Hatası** - Options flow'daki 500 Internal Server Error düzeltildi
- ✅ **Güncelleme Senkronizasyonu** - Güncelleme yapıldığında tüm sensörler birlikte güncelleniyor

### Removed
- 🗑️ **Uyarı Sayısı Sensörü** - Gereksiz `sensor.ILCE_IL_alert_count` sensörü kaldırıldı (Bilgi zaten binary_sensor'de mevcut)

### Changed
- 🔧 Config flow güncelleme aralığı integer olarak saklanıyor (string yerine)
- 📊 Button platform eklendi (PLATFORMS listesine)

## [1.5.1] - 2026-02-08

### Fixed
- ✅ **Basınç Sensörü** - Artık -9999 hPa gibi geçersiz değerler gösterilmiyor
- ✅ **Nem Sensörü** - Geçersiz değerler filtreleniyor
- ✅ **Rüzgar Hızı** - Geçersiz değerler filtreleniyor
- ✅ **Hissedilen Sıcaklık** - Geçersiz değerler filtreleniyor
- 🔧 Tüm sayısal sensörlere -9999 değer kontrolü eklendi

## [1.5.0] - 2026-02-08

### Added
- ✨ **Bugün Hava Tahmini Sensörü** - `sensor.ILCE_IL_forecast_today` (Bugünün hava durumu tahmini)
- ✨ **Yarın Hava Tahmini Sensörü** - `sensor.ILCE_IL_forecast_tomorrow` (Yarının hava durumu tahmini)
- 📊 Tahmin sensörlerinde min/max sıcaklık ve tarih bilgisi attribute'larda
- 💧 **Anlık Yağış Sensörü** - `sensor.ILCE_IL_precipitation_current` (MGM uygulamasındaki ana yağış değeri)

### Changed
- 🧭 **Rüzgar Yönü** - Artık derece yerine Türkçe yön kısaltmaları gösteriyor (K, KB, D, GD, G, GB, B, KB)
- 📊 Rüzgar yönü sensörü attribute'larına tam derece değeri ve uzun yön adı eklendi

### Fixed
- ✅ Görüş mesafesi ve bulutluluk sensörlerinin bazı konumlarda "bilinmeyen" görünme sorunu düzeltildi
- ✅ Binary sensor f-string syntax hatası düzeltildi
- ✅ MGM uygulamasıyla yağış değeri tutarsızlığı düzeltildi

## [1.4.1] - 2026-02-08

### Fixed
- ✅ Görüş mesafesi ve bulutluluk sensörlerinin bazı konumlarda "bilinmeyen" görünme sorunu düzeltildi

## [1.4.0] - 2026-02-08

### Added
- ✨ **Bugün Hava Tahmini Sensörü** - `sensor.ILCE_IL_forecast_today` (Bugünün hava durumu tahmini: Güneşli, Yağmurlu, Karlı vb.)
- ✨ **Yarın Hava Tahmini Sensörü** - `sensor.ILCE_IL_forecast_tomorrow` (Yarının hava durumu tahmini)
- 📊 Tahmin sensörlerinde min/max sıcaklık ve tarih bilgisi attribute'larda

## [1.3.1] - 2026-02-08

### Added
- ✨ **Anlık Yağış Sensörü** - `sensor.ILCE_IL_precipitation_current` (MGM uygulamasındaki ana yağış değeri)

### Changed
- 🧭 **Rüzgar Yönü** - Artık derece yerine Türkçe yön kısaltmaları gösteriyor (K, KB, D, GD, G, GB, B, KB)
- 📊 Rüzgar yönü sensörü attribute'larına tam derece değeri ve uzun yön adı eklendi

### Fixed
- ✅ MGM uygulamasıyla yağış değeri tutarsızlığı düzeltildi

## [1.3.0] - 2026-02-08

### Added
- ✨ **Sıcaklık Sensörü** - `sensor.ILCE_IL_sicaklik` (anlık sıcaklık °C)
- 🎨 **HACS İkonu** - Entegrasyon için özel ikon eklendi

### Fixed
- ✅ **MeteoAlarm Bildirimleri** - Boş MeteoAlarm girişleri artık gösterilmiyor
- ✅ **İlçe Listesi** - Tüm ilçeler gösteriliyor (limit 15'ten 100'e çıkarıldı)

### Changed
- 📊 Toplam sensör sayısı 13'e çıktı

## [1.2.0] - 2026-02-08

### Added
- ✨ **Uyarı Sayısı Sensörü** - `sensor.ILCE_IL_uyari_sayisi` (aktif uyarı sayısını gösterir)
- ✨ **Uyarı Detayları Sensörü** - `sensor.ILCE_IL_uyari_detaylari` (uyarı başlığını ve detaylarını gösterir)
- 📊 Uyarı sensörlerinde tüm uyarıların listesi attributes'da

## [1.1.2] - 2026-02-08

### Fixed
- ✅ Ayarlar menüsü 500 hatası düzeltildi
- ✅ JSON yapısı düzeltildi (strings.json, tr.json)

## [1.1.1] - 2026-02-08

### Fixed
- ✅ Bulutluluk, Görüş Mesafesi ve Yağış sensörleri artık doğru değerleri gösteriyor
- ✅ Sensor alan adları düzeltildi (gorus, yagis, kapalilik)

## [1.1.0] - 2026-02-08

### Added
- ✨ **Ayarlar menüsü** - Güncelleme sıklığını ayarlardan değiştirebilme (5, 10, 15, 30, 60 dakika)
- ✨ **Min/Max sıcaklık** - Weather kartında bugünün min/max sıcaklıkları gösteriliyor
- ✨ **Yağış bilgisi** - Saatlik yağış miktarı eklendi

### Changed
- Güncelleme sıklığı artık yapılandırılabilir

## [1.0.4] - 2026-02-08

### Changed
- Güncelleme sıklığı 10 dakikadan 30 dakikaya çıkarıldı

## [1.0.3] - 2026-02-08

### Fixed
- ✅ 5 günlük hava durumu tahmini artık gösteriliyor
- ✅ Min/Max sıcaklık değerleri eklendi
- ✅ Bulutluluk ve görüş mesafesi sensörleri düzeltildi
- ✅ Hava durumu uyarısı "Güvensiz" hatası giderildi
- ✅ API alan adları düzeltildi (gorus, kapalilik, yagis)

## [1.0.2] - 2026-02-08

### Fixed
- Tüm ilçeler artık gösteriliyor (önceden sadece il merkezleri geliyordu)
- Config flow arama endpoint'ini kullanacak şekilde güncellendi

## [1.0.1] - 2026-02-08

### Fixed
- İlçe seçimi sorunu düzeltildi
- Config flow API yapısına uygun hale getirildi

## [1.0.0] - 2026-02-08

### Added
- Initial release
- MGM API integration for Turkish weather data
- Weather entity with current conditions
- 5-day and hourly forecasts
- 10 sensor entities (humidity, wind, pressure, precipitation, etc.)
- Binary sensor for weather alerts
- Automatic persistent notifications for alerts
- Turkish and English translations
- Province and district selection in config flow
- HACS compatibility
