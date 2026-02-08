# GitHub Kurulum Kılavuzu

## ✅ Hazırlık Tamamlandı

Git repository oluşturuldu ve tüm dosyalar commit edildi:
- ✅ 22 dosya initial commit'te
- ✅ Logolar kullanıcı tasarımıyla güncellendi
- ✅ Main branch hazır

## 📋 Sonraki Adımlar

### 1. GitHub'da Repository Oluşturun

1. [GitHub](https://github.com) → **New Repository**
2. Repository adı: `hava-durumu`
3. **Public** seçin (HACS için gerekli)
4. **README, .gitignore, LICENSE eklemeyin** (zaten var)
5. **Create repository**

### 2. Remote Ekleyin ve Push Yapın

GitHub'da repository oluşturduktan sonra, size verilen komutları kullanın:

```bash
cd "/Users/hamitdurmus/Hava Durumu"

git remote add origin https://github.com/ahamitd/hava-durumu.git

# Push yapın
git push -u origin main
```

### 3. Release Oluşturun (HACS için gerekli)

1. GitHub repository → **Releases** → **Create a new release**
2. **Tag**: `v1.0.0`
3. **Release title**: `v1.0.0 - Initial Release`
4. **Description**:
```markdown
## 🎉 İlk Sürüm

MGM (Meteoroloji Genel Müdürlüğü) API'sini kullanan Home Assistant entegrasyonu.

### Özellikler
- ✅ Anlık hava durumu
- ✅ 5 günlük tahmin
- ✅ Saatlik tahmin
- ✅ 10 sensör
- ✅ Uyarı sistemi
- ✅ Türkçe/İngilizce dil desteği

### Kurulum
HACS → Entegrasyonlar → Özel Depolar → Bu repository'yi ekleyin
```
5. **Publish release**

### 4. HACS ile Test Edin

1. Home Assistant → HACS → Entegrasyonlar
2. Sağ üst menü (⋮) → **Özel depolar**
3. Repository: `https://github.com/KULLANICI_ADI/hava-durumu`
4. Kategori: **Integration**
5. **Ekle**
6. "Hava Durumu" arayın ve yükleyin

## 🔐 SSH Kullanmak İsterseniz

```bash
git remote set-url origin git@github.com:KULLANICI_ADI/hava-durumu.git
git push -u origin main
```

## 📝 Notlar

- Repository **public** olmalı (HACS gereksinimi)
- En az bir **release** olmalı (HACS gereksinimi)
- `hacs.json` dosyası mevcut ✅
- Logo dosyaları mevcut ✅
