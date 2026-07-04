# 50 Gbps Fiber Internet NetVBS

Bu proje, bilgisayarında doğrudan çalıştırabileceğin bir yüksek hızlı ağ demo'sudur.

## Çalıştırma

1. Proje klasörüne gidin:

```bash
cd c:\Users\ASUS\NetVBS
```

2. Sunucuyu başlatın:

```bash
python server.py
```

3. Tarayıcıda açın:

```text
http://127.0.0.1:8000/index.html
```

4. Aynı yerel ağdaki diğer cihazlardan erişmek için, sunucunun `README` veya web arayüzünde gösterilen yerel IP adreslerinden birini kullanın:

```text
http://<bilgisayar-ip-adresi>:8000/index.html
```

## Yerel ağda erişim

Eğer bilgisayarınızın IP adresi `192.168.1.25` ise, diğer cihazlardan şu şekilde bağlanabilirsiniz:

```text
http://192.168.1.25:8000/index.html
```

Bu yapı, bilgisayarınızda çalışan gerçek bir yerel hizmettir; ancak yine de gerçek bir internet sağlayıcısı veya modem yerine, yalnızca yerel ağ üzerinden erişilen bir servis olarak çalışır.
