# Changelog

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
