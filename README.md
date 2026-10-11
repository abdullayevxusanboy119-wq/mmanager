# Mmanager

Mobil telefon do'koni uchun boshqaruv tizimi.

## Imkoniyatlar
- Mahsulotlar va ombor (IMEI bo'yicha hisob)
- Savdo va POS (kassa)
- Muddatli to'lov (kredit) nazorati
- Ta'mirlash buyurtmalari (qabul qilindi → ta'mirlanmoqda → tayyor)
- Trade-in kalkulyatori
- Mijozlar va ta'minotchilar
- Dashboard (kunlik foyda, qarzdorlik, kam qolgan mahsulotlar)
- Rollar: admin va sotuvchi

## Texnologiyalar
Django, Django REST Framework, JWT (SimpleJWT), PostgreSQL, HTML/CSS/JavaScript

## O'rnatish
```
pip install -r requirements.txt
```
`.env.example` faylidan `.env` yarating va qiymatlarini to'ldiring, so'ng:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Brauzerda `http://127.0.0.1:8000/` oching.
