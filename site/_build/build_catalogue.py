#!/usr/bin/env python3
"""Single source of truth for the ARMINAK CARAVAN catalogue.

Emits:
  site/catalogue.html                  — product grid + spec/RFQ drawer
  site/assets/docs/<slug>.pdf          — branded technical specification sheets
  site/assets/js/i18n-catalogue.js     — Russian strings for the catalogue
"""
import pathlib

ROOT = pathlib.Path("/Users/mohmmadomar/Desktop/ARMINAK CARAVAN /site")
DOCS = ROOT / "assets" / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

ISSUE_DATE_EN = "10 August 2026"
ISSUE_DATE_RU = "10 августа 2026"

# Merchandising: badge ("new" | "best" | None) and collection flags per slug.
BADGES = {
    "milling-wheat-grade-3": "best", "feed-barley-grade-1": "best",
    "flaxseed-food-grade": "new", "crude-sunflower-oil": "best",
    "refined-rapeseed-oil": "new", "skimmed-milk-powder": "best",
    "ice-cream-private-label": "new", "refined-sugar-icumsa-45": "best",
    "tomato-paste-28-30": "new", "chickpeas-kabuli-8mm": "new",
}
PRIVATE_LABEL = {"refined-rapeseed-oil", "uht-milk-3-2", "ice-cream-private-label",
                 "natural-mineral-water", "durum-wheat-pasta"}

HEART = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.3 4.9 13a4.6 4.6 0 0 1 0-6.5'
         ' 4.5 4.5 0 0 1 6.4 0l.7.7.7-.7a4.5 4.5 0 0 1 6.4 0 4.6 4.6 0 0 1 0 6.5Z"/></svg>')

# ---------------------------------------------------------------- data ------
# spec rows: (param_en, value_en, param_ru, value_ru)
# meta rows: same shape.

CATEGORIES = [
{
 "id": "grains", "en": "Agriculture & Grains", "ru": "Сельхозпродукция и зерновые",
 "note_en": "Origination from Black Sea, Turkish and Central Asian producers.",
 "note_ru": "Закупка напрямую у производителей Причерноморья, Турции и Центральной Азии.",
 "items": [
  {"slug": "milling-wheat-grade-3", "art": "wheat",
   "en": "Milling Wheat", "ru": "Пшеница мукомольная",
   "grade_en": "Grade 3 · Milling", "grade_ru": "3 класс · мукомольная",
   "origin_en": "Black Sea · Central Asia", "origin_ru": "Причерноморье · Центральная Азия",
   "metrics_en": ["Protein 12.5% min · Moisture 14% max", "Test weight 770 g/l min", "Bulk / 50 kg bags / big bags"],
   "metrics_ru": ["Протеин 12,5% мин · Влажность 14% макс", "Натура 770 г/л мин", "Навал / мешки 50 кг / биг-бэги"],
   "spec": [
     ("Protein", "12.5% min", "Протеин", "12,5% мин"),
     ("Falling Number", "250 sec min", "Число падения", "250 сек мин"),
     ("Test Weight", "770 g/l min", "Натура", "770 г/л мин"),
     ("Wet Gluten", "23–25%", "Клейковина сырая", "23–25%"),
     ("Moisture", "14% max", "Влажность", "14% макс"),
     ("Foreign Matter", "2% max", "Сорная примесь", "2% макс")],
   "meta": [
     ("Origin", "Russia · Kazakhstan", "Происхождение", "Россия · Казахстан"),
     ("Packing", "Bulk / 50 kg / big bags", "Упаковка", "Навал / 50 кг / биг-бэг"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "3 000 MT", "Минимальная партия", "3 000 тонн")]},

  {"slug": "feed-barley-grade-1", "art": "barley",
   "en": "Feed Barley", "ru": "Ячмень фуражный",
   "grade_en": "Grade 1 · Feed", "grade_ru": "1 класс · фуражный",
   "origin_en": "Black Sea · Turkey", "origin_ru": "Причерноморье · Турция",
   "metrics_en": ["Protein 11% min · Moisture 13.5% max", "Test weight 620 g/l min", "Bulk / 50 kg bags"],
   "metrics_ru": ["Протеин 11% мин · Влажность 13,5% макс", "Натура 620 г/л мин", "Навал / мешки 50 кг"],
   "spec": [
     ("Protein", "11% min", "Протеин", "11% мин"),
     ("Moisture", "13.5% max", "Влажность", "13,5% макс"),
     ("Test Weight", "620 g/l min", "Натура", "620 г/л мин"),
     ("Foreign Matter", "2% max", "Сорная примесь", "2% макс"),
     ("Broken Grains", "5% max", "Битое зерно", "5% макс"),
     ("Damaged Grains", "3% max", "Повреждённое зерно", "3% макс")],
   "meta": [
     ("Origin", "Russia · Ukraine · Kazakhstan", "Происхождение", "Россия · Украина · Казахстан"),
     ("Packing", "Bulk / 50 kg bags", "Упаковка", "Навал / мешки 50 кг"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "3 000 MT", "Минимальная партия", "3 000 тонн")]},

  {"slug": "corn-feed-grade", "art": "corn",
   "en": "Corn (Maize)", "ru": "Кукуруза",
   "grade_en": "Feed Grade", "grade_ru": "Фуражная",
   "origin_en": "Black Sea · East Europe", "origin_ru": "Причерноморье · Восточная Европа",
   "metrics_en": ["Protein 8% min · Moisture 14% max", "Test weight 720 g/l min", "Bulk / 50 kg bags"],
   "metrics_ru": ["Протеин 8% мин · Влажность 14% макс", "Натура 720 г/л мин", "Навал / мешки 50 кг"],
   "spec": [
     ("Protein", "8% min", "Протеин", "8% мин"),
     ("Moisture", "14% max", "Влажность", "14% макс"),
     ("Test Weight", "720 g/l min", "Натура", "720 г/л мин"),
     ("Foreign Matter", "2% max", "Сорная примесь", "2% макс"),
     ("Broken Grains", "5% max", "Битое зерно", "5% макс"),
     ("Aflatoxin", "20 ppb max", "Афлатоксин", "20 ppb макс")],
   "meta": [
     ("Origin", "Ukraine · Russia · Serbia", "Происхождение", "Украина · Россия · Сербия"),
     ("Packing", "Bulk / 50 kg bags", "Упаковка", "Навал / мешки 50 кг"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "3 000 MT", "Минимальная партия", "3 000 тонн")]},

  {"slug": "flaxseed-food-grade", "art": "flaxseed",
   "en": "Flaxseed", "ru": "Семена льна",
   "grade_en": "Brown · Food Grade", "grade_ru": "Коричневый · пищевой",
   "origin_en": "Kazakhstan · Russia", "origin_ru": "Казахстан · Россия",
   "metrics_en": ["Oil content 40% min · Moisture 9% max", "Purity 99% min", "Big bags / 25 kg bags"],
   "metrics_ru": ["Масличность 40% мин · Влажность 9% макс", "Чистота 99% мин", "Биг-бэги / мешки 25 кг"],
   "spec": [
     ("Oil Content", "40% min", "Масличность", "40% мин"),
     ("Moisture", "9% max", "Влажность", "9% макс"),
     ("Purity", "99% min", "Чистота", "99% мин"),
     ("Admixture", "1% max", "Примесь", "1% макс"),
     ("Free Fatty Acids", "2% max", "Кислотное число", "2% макс"),
     ("Damaged Seeds", "2% max", "Повреждённые семена", "2% макс")],
   "meta": [
     ("Origin", "Kazakhstan · Russia", "Происхождение", "Казахстан · Россия"),
     ("Packing", "Big bags / 25 kg bags", "Упаковка", "Биг-бэг / мешки 25 кг"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "500 MT", "Минимальная партия", "500 тонн")]},
 ]},

{
 "id": "oils", "en": "Oils & Grocery", "ru": "Масла и бакалея",
 "note_en": "Crude and refined vegetable oils, milling products and staple grocery.",
 "note_ru": "Сырые и рафинированные растительные масла, продукты помола и базовая бакалея.",
 "items": [
  {"slug": "crude-sunflower-oil", "art": "sunflower-oil",
   "en": "Crude Sunflower Oil", "ru": "Масло подсолнечное сырое",
   "grade_en": "Crude · Degummed", "grade_ru": "Сырое · гидратированное",
   "origin_en": "Black Sea", "origin_ru": "Причерноморье",
   "metrics_en": ["FFA 2% max · Moisture 0.2% max", "Peroxide value 5 meq/kg max", "Flexitank / ISO tank / drums"],
   "metrics_ru": ["Кислотность 2% макс · Влага 0,2% макс", "Перекисное число 5 мэкв/кг макс", "Флекситанк / ISO-танк / бочки"],
   "spec": [
     ("Free Fatty Acids", "2% max", "Кислотное число (олеиновая)", "2% макс"),
     ("Moisture & Volatiles", "0.2% max", "Влага и летучие вещества", "0,2% макс"),
     ("Insoluble Impurities", "0.1% max", "Нерастворимые примеси", "0,1% макс"),
     ("Peroxide Value", "5 meq/kg max", "Перекисное число", "5 мэкв/кг макс"),
     ("Phosphorus", "300 ppm max", "Фосфор", "300 ppm макс"),
     ("Colour (Lovibond)", "30 max", "Цветность (Ловибонд)", "30 макс")],
   "meta": [
     ("Origin", "Russia · Ukraine", "Происхождение", "Россия · Украина"),
     ("Packing", "Flexitank / ISO tank / 200 l drums", "Упаковка", "Флекситанк / ISO-танк / бочки 200 л"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "1 000 MT", "Минимальная партия", "1 000 тонн")]},

  {"slug": "refined-rapeseed-oil", "art": "rapeseed-oil",
   "en": "Refined Rapeseed Oil", "ru": "Масло рапсовое рафинированное",
   "grade_en": "RBD · Winterised", "grade_ru": "Рафинированное · вымороженное",
   "origin_en": "Black Sea · East Europe", "origin_ru": "Причерноморье · Восточная Европа",
   "metrics_en": ["FFA 0.1% max · Moisture 0.1% max", "Peroxide value 2 meq/kg max", "Flexitank / bottled private label"],
   "metrics_ru": ["Кислотность 0,1% макс · Влага 0,1% макс", "Перекисное число 2 мэкв/кг макс", "Флекситанк / бутылка СТМ"],
   "spec": [
     ("Free Fatty Acids", "0.1% max", "Кислотное число (олеиновая)", "0,1% макс"),
     ("Moisture & Volatiles", "0.1% max", "Влага и летучие вещества", "0,1% макс"),
     ("Peroxide Value", "2 meq/kg max", "Перекисное число", "2 мэкв/кг макс"),
     ("Colour (Lovibond)", "2R / 20Y max", "Цветность (Ловибонд)", "2R / 20Y макс"),
     ("Soap Content", "Nil", "Содержание мыла", "Отсутствует"),
     ("Cold Test", "24 h at 0 °C", "Холодный тест", "24 ч при 0 °C")],
   "meta": [
     ("Origin", "Russia · Poland · Ukraine", "Происхождение", "Россия · Польша · Украина"),
     ("Packing", "Flexitank / 1 l · 5 l PET", "Упаковка", "Флекситанк / ПЭТ 1 л · 5 л"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "500 MT", "Минимальная партия", "500 тонн")]},

  {"slug": "wheat-flour-type-550", "art": "flour",
   "en": "Wheat Flour", "ru": "Мука пшеничная",
   "grade_en": "Type 550 · Bakery", "grade_ru": "Тип 550 · хлебопекарная",
   "origin_en": "Turkey · Kazakhstan", "origin_ru": "Турция · Казахстан",
   "metrics_en": ["Protein 10.5% min · Ash 0.55% max", "Wet gluten 26% min", "25 / 50 kg bags"],
   "metrics_ru": ["Протеин 10,5% мин · Зольность 0,55% макс", "Клейковина 26% мин", "Мешки 25 / 50 кг"],
   "spec": [
     ("Protein", "10.5% min", "Протеин", "10,5% мин"),
     ("Ash Content", "0.55% max", "Зольность", "0,55% макс"),
     ("Moisture", "14.5% max", "Влажность", "14,5% макс"),
     ("Wet Gluten", "26% min", "Клейковина сырая", "26% мин"),
     ("Falling Number", "250 sec min", "Число падения", "250 сек мин"),
     ("Granulation", "180 µm", "Гранулометрия", "180 мкм")],
   "meta": [
     ("Origin", "Turkey · Kazakhstan", "Происхождение", "Турция · Казахстан"),
     ("Packing", "25 / 50 kg bags · big bags", "Упаковка", "Мешки 25 / 50 кг · биг-бэг"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "500 MT", "Минимальная партия", "500 тонн")]},

  {"slug": "long-grain-white-rice", "art": "rice",
   "en": "Long Grain White Rice", "ru": "Рис длиннозёрный шлифованный",
   "grade_en": "5% Broken", "grade_ru": "5% дроблёных",
   "origin_en": "India · Pakistan", "origin_ru": "Индия · Пакистан",
   "metrics_en": ["Broken 5% max · Moisture 14% max", "Average length 6.8 mm min", "25 / 50 kg bags"],
   "metrics_ru": ["Дроблёные 5% макс · Влажность 14% макс", "Средняя длина 6,8 мм мин", "Мешки 25 / 50 кг"],
   "spec": [
     ("Broken Grains", "5% max", "Дроблёные зёрна", "5% макс"),
     ("Moisture", "14% max", "Влажность", "14% макс"),
     ("Average Length", "6.8 mm min", "Средняя длина", "6,8 мм мин"),
     ("Chalky Grains", "4% max", "Меловидные зёрна", "4% макс"),
     ("Damaged Grains", "1% max", "Повреждённые зёрна", "1% макс"),
     ("Foreign Matter", "0.1% max", "Сорная примесь", "0,1% макс")],
   "meta": [
     ("Origin", "India · Pakistan · Vietnam", "Происхождение", "Индия · Пакистан · Вьетнам"),
     ("Packing", "25 / 50 kg bags", "Упаковка", "Мешки 25 / 50 кг"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "1 000 MT", "Минимальная партия", "1 000 тонн")]},
 ]},

{
 "id": "dairy", "en": "Dairy & Beverages", "ru": "Молочная продукция и напитки",
 "note_en": "Temperature-controlled and ambient lines, including private label.",
 "note_ru": "Продукция с температурным режимом и длительного хранения, включая СТМ.",
 "items": [
  {"slug": "skimmed-milk-powder", "art": "milk-powder",
   "en": "Skimmed Milk Powder", "ru": "Сухое обезжиренное молоко",
   "grade_en": "Medium Heat · SMP", "grade_ru": "Среднетемпературное · СОМ",
   "origin_en": "EU · Belarus", "origin_ru": "ЕС · Беларусь",
   "metrics_en": ["Protein 34% min · Fat 1.25% max", "Moisture 4% max", "25 kg multi-ply bags"],
   "metrics_ru": ["Белок 34% мин · Жир 1,25% макс", "Влажность 4% макс", "Мешки 25 кг многослойные"],
   "spec": [
     ("Protein (on SNF)", "34% min", "Белок (в СОМО)", "34% мин"),
     ("Milk Fat", "1.25% max", "Молочный жир", "1,25% макс"),
     ("Moisture", "4% max", "Влажность", "4% макс"),
     ("Titratable Acidity", "0.15% max", "Титруемая кислотность", "0,15% макс"),
     ("Scorched Particles", "Disc B", "Пригоревшие частицы", "Диск B"),
     ("Solubility Index", "1.0 ml max", "Индекс растворимости", "1,0 мл макс")],
   "meta": [
     ("Origin", "EU · Belarus", "Происхождение", "ЕС · Беларусь"),
     ("Packing", "25 kg multi-ply bags", "Упаковка", "Мешки 25 кг многослойные"),
     ("Incoterms", "CIF · CFR · DAP", "Условия поставки", "CIF · CFR · DAP"),
     ("Minimum lot", "100 MT", "Минимальная партия", "100 тонн")]},

  {"slug": "uht-milk-3-2", "art": "uht-milk",
   "en": "UHT Milk 3.2%", "ru": "Молоко УВТ 3,2%",
   "grade_en": "Ambient · 9 Months", "grade_ru": "Длительного хранения · 9 месяцев",
   "origin_en": "EU · Turkey", "origin_ru": "ЕС · Турция",
   "metrics_en": ["Fat 3.2% · Protein 3.0% min", "Shelf life 9 months", "1 l Tetra Pak · 12 per case"],
   "metrics_ru": ["Жирность 3,2% · Белок 3,0% мин", "Срок годности 9 месяцев", "Tetra Pak 1 л · 12 шт в коробе"],
   "spec": [
     ("Milk Fat", "3.2%", "Молочный жир", "3,2%"),
     ("Protein", "3.0% min", "Белок", "3,0% мин"),
     ("Solids-Not-Fat", "8.5% min", "СОМО", "8,5% мин"),
     ("Shelf Life", "9 months", "Срок годности", "9 месяцев"),
     ("Packing", "1 l Tetra Pak", "Упаковка", "Tetra Pak 1 л"),
     ("Sterilisation", "UHT 137 °C / 4 sec", "Стерилизация", "УВТ 137 °C / 4 сек")],
   "meta": [
     ("Origin", "EU · Turkey", "Происхождение", "ЕС · Турция"),
     ("Packing", "1 l Tetra Pak · 12 per case", "Упаковка", "Tetra Pak 1 л · 12 шт в коробе"),
     ("Incoterms", "CIF · CFR · DAP", "Условия поставки", "CIF · CFR · DAP"),
     ("Minimum lot", "1 × 40' FCL", "Минимальная партия", "1 × 40-футовый контейнер")]},

  {"slug": "ice-cream-private-label", "art": "ice-cream",
   "en": "Ice Cream", "ru": "Мороженое",
   "grade_en": "Private Label · Frozen", "grade_ru": "СТМ · замороженное",
   "origin_en": "EU · Turkey · UAE", "origin_ru": "ЕС · Турция · ОАЭ",
   "metrics_en": ["Milk fat 8–12% · Overrun 80–100%", "Storage −18 °C", "Cone / stick / 5 l bulk"],
   "metrics_ru": ["Молочный жир 8–12% · Взбитость 80–100%", "Хранение −18 °C", "Рожок / эскимо / 5 л"],
   "spec": [
     ("Milk Fat", "8–12%", "Молочный жир", "8–12%"),
     ("Total Solids", "36% min", "Сухие вещества", "36% мин"),
     ("Overrun", "80–100%", "Взбитость", "80–100%"),
     ("Storage Temperature", "−18 °C", "Температура хранения", "−18 °C"),
     ("Shelf Life", "18 months", "Срок годности", "18 месяцев"),
     ("Format", "Cone / stick / 5 l bulk", "Формат", "Рожок / эскимо / 5 л")],
   "meta": [
     ("Origin", "EU · Turkey · UAE", "Происхождение", "ЕС · Турция · ОАЭ"),
     ("Packing", "Retail multipack / HoReCa bulk", "Упаковка", "Мультипак / HoReCa"),
     ("Incoterms", "CIF · CFR · DAP (reefer)", "Условия поставки", "CIF · CFR · DAP (рефрижератор)"),
     ("Minimum lot", "1 × 40' RF", "Минимальная партия", "1 × 40-футовый рефконтейнер")]},

  {"slug": "natural-mineral-water", "art": "water",
   "en": "Natural Mineral Water", "ru": "Природная минеральная вода",
   "grade_en": "Still · PET", "grade_ru": "Негазированная · ПЭТ",
   "origin_en": "Turkey · Georgia", "origin_ru": "Турция · Грузия",
   "metrics_en": ["TDS 150–500 mg/l · pH 7.0–7.6", "Nitrates 10 mg/l max", "0.5 / 1.5 l PET"],
   "metrics_ru": ["Минерализация 150–500 мг/л · pH 7,0–7,6", "Нитраты 10 мг/л макс", "ПЭТ 0,5 / 1,5 л"],
   "spec": [
     ("Total Dissolved Solids", "150–500 mg/l", "Общая минерализация", "150–500 мг/л"),
     ("pH", "7.0–7.6", "Водородный показатель", "7,0–7,6"),
     ("Nitrates", "10 mg/l max", "Нитраты", "10 мг/л макс"),
     ("Packing", "0.5 / 1.5 l PET", "Упаковка", "ПЭТ 0,5 / 1,5 л"),
     ("Shelf Life", "12 months", "Срок годности", "12 месяцев"),
     ("Certification", "ISO 22000 · HACCP", "Сертификация", "ISO 22000 · HACCP")],
   "meta": [
     ("Origin", "Turkey · Georgia", "Происхождение", "Турция · Грузия"),
     ("Packing", "Shrink 6 / 12 per pack", "Упаковка", "Термоусадка 6 / 12 шт"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "1 × 40' FCL", "Минимальная партия", "1 × 40-футовый контейнер")]},
 ]},

{
 "id": "sugar", "en": "Sugar & Foodstuff", "ru": "Сахар и продукты питания",
 "note_en": "Refined sugar, pulses and processed foodstuff for retail and industry.",
 "note_ru": "Рафинированный сахар, бобовые и переработанная продукция для ритейла и промышленности.",
 "items": [
  {"slug": "refined-sugar-icumsa-45", "art": "sugar",
   "en": "Refined White Sugar", "ru": "Сахар белый рафинированный",
   "grade_en": "ICUMSA 45", "grade_ru": "ИКУМСА 45",
   "origin_en": "Brazil · India", "origin_ru": "Бразилия · Индия",
   "metrics_en": ["Polarisation 99.80% min · ICUMSA 45 max", "Moisture 0.04% max", "50 kg bags / big bags"],
   "metrics_ru": ["Поляризация 99,80% мин · ИКУМСА 45 макс", "Влажность 0,04% макс", "Мешки 50 кг / биг-бэг"],
   "spec": [
     ("Polarisation", "99.80% min", "Поляризация", "99,80% мин"),
     ("ICUMSA", "45 RBU max", "ИКУМСА", "45 RBU макс"),
     ("Moisture", "0.04% max", "Влажность", "0,04% макс"),
     ("Ash Content", "0.04% max", "Зольность", "0,04% макс"),
     ("Sulphur Dioxide", "20 mg/kg max", "Диоксид серы", "20 мг/кг макс"),
     ("Granulation", "0.6–0.8 mm", "Гранулометрия", "0,6–0,8 мм")],
   "meta": [
     ("Origin", "Brazil · India", "Происхождение", "Бразилия · Индия"),
     ("Packing", "50 kg bags / 1 MT big bags", "Упаковка", "Мешки 50 кг / биг-бэг 1 т"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "12 500 MT", "Минимальная партия", "12 500 тонн")]},

  {"slug": "durum-wheat-pasta", "art": "pasta",
   "en": "Durum Wheat Pasta", "ru": "Макаронные изделия из твёрдых сортов",
   "grade_en": "100% Semolina", "grade_ru": "100% семолина",
   "origin_en": "Turkey · Italy", "origin_ru": "Турция · Италия",
   "metrics_en": ["Protein 12% min · Moisture 12.5% max", "Cooking loss 6% max", "400 / 500 g retail · 5 kg catering"],
   "metrics_ru": ["Белок 12% мин · Влажность 12,5% макс", "Потери при варке 6% макс", "400 / 500 г ритейл · 5 кг HoReCa"],
   "spec": [
     ("Raw Material", "100% durum semolina", "Сырьё", "100% семолина твёрдых сортов"),
     ("Protein", "12% min", "Белок", "12% мин"),
     ("Moisture", "12.5% max", "Влажность", "12,5% макс"),
     ("Ash Content", "0.9% max", "Зольность", "0,9% макс"),
     ("Cooking Loss", "6% max", "Потери при варке", "6% макс"),
     ("Shelf Life", "36 months", "Срок годности", "36 месяцев")],
   "meta": [
     ("Origin", "Turkey · Italy", "Происхождение", "Турция · Италия"),
     ("Packing", "400 / 500 g · 5 kg catering", "Упаковка", "400 / 500 г · 5 кг HoReCa"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "1 × 40' FCL", "Минимальная партия", "1 × 40-футовый контейнер")]},

  {"slug": "tomato-paste-28-30", "art": "tomato-paste",
   "en": "Tomato Paste", "ru": "Томатная паста",
   "grade_en": "28/30% · Hot Break", "grade_ru": "28/30% · горячий отжим",
   "origin_en": "Turkey · Iran", "origin_ru": "Турция · Иран",
   "metrics_en": ["Brix 28–30% · pH 4.2–4.4", "Bostwick 4–6 cm / 30 sec", "220 kg aseptic drums"],
   "metrics_ru": ["Брикс 28–30% · pH 4,2–4,4", "Боствик 4–6 см / 30 сек", "Асептические бочки 220 кг"],
   "spec": [
     ("Brix (at 20 °C)", "28–30%", "Брикс (при 20 °C)", "28–30%"),
     ("pH", "4.2–4.4", "Водородный показатель", "4,2–4,4"),
     ("Process", "Hot break", "Способ производства", "Горячий отжим"),
     ("Bostwick", "4–6 cm / 30 sec", "Консистенция по Боствику", "4–6 см / 30 сек"),
     ("Mould (Howard)", "40% max", "Плесень (метод Говарда)", "40% макс"),
     ("Packing", "220 kg aseptic drum", "Упаковка", "Асептическая бочка 220 кг")],
   "meta": [
     ("Origin", "Turkey · Iran", "Происхождение", "Турция · Иран"),
     ("Packing", "220 kg aseptic drum · retail tins", "Упаковка", "Бочка 220 кг · жестебанка"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "1 × 20' FCL", "Минимальная партия", "1 × 20-футовый контейнер")]},

  {"slug": "chickpeas-kabuli-8mm", "art": "chickpeas",
   "en": "Chickpeas", "ru": "Нут",
   "grade_en": "Kabuli · 8 mm", "grade_ru": "Кабули · 8 мм",
   "origin_en": "Turkey · Kazakhstan", "origin_ru": "Турция · Казахстан",
   "metrics_en": ["Calibre 8 mm · Moisture 12% max", "Purity 99% min", "25 / 50 kg bags · big bags"],
   "metrics_ru": ["Калибр 8 мм · Влажность 12% макс", "Чистота 99% мин", "Мешки 25 / 50 кг · биг-бэг"],
   "spec": [
     ("Calibre", "8 mm", "Калибр", "8 мм"),
     ("Moisture", "12% max", "Влажность", "12% макс"),
     ("Purity", "99% min", "Чистота", "99% мин"),
     ("Foreign Matter", "0.5% max", "Сорная примесь", "0,5% макс"),
     ("Damaged Seeds", "2% max", "Повреждённые семена", "2% макс"),
     ("Split Seeds", "1% max", "Колотые семена", "1% макс")],
   "meta": [
     ("Origin", "Turkey · Kazakhstan", "Происхождение", "Турция · Казахстан"),
     ("Packing", "25 / 50 kg bags · big bags", "Упаковка", "Мешки 25 / 50 кг · биг-бэг"),
     ("Incoterms", "FOB · CIF · CFR", "Условия поставки", "FOB · CIF · CFR"),
     ("Minimum lot", "500 MT", "Минимальная партия", "500 тонн")]},
 ]},
]

# =================================================================== PDF =====
# Minimal PDF writer — base-14 fonts, no external dependencies.

SAND = (0.969, 0.953, 0.925)
SAND2 = (0.922, 0.890, 0.843)
NAVY = (0.106, 0.165, 0.255)
BRASS = (0.690, 0.553, 0.341)
GREY = (0.361, 0.392, 0.439)


# Characters outside cp1252 that appear in the trade data.
_FOLD = {0x2212: "-", 0x2011: "-", 0x00A0: " ", 0x2009: " "}


def esc(s):
    out = s.translate(_FOLD).encode("cp1252", "replace").decode("cp1252")
    return out.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


class Page:
    def __init__(self):
        self.ops = []

    def rect(self, x, y, w, h, color):
        r, g, b = color
        self.ops.append(f"{r:.3f} {g:.3f} {b:.3f} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f")

    def line(self, x1, y1, x2, y2, color, width=0.6):
        r, g, b = color
        self.ops.append(
            f"{r:.3f} {g:.3f} {b:.3f} RG {width} w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S"
        )

    def text(self, x, y, s, font="F1", size=10, color=NAVY, spacing=0.0):
        r, g, b = color
        self.ops.append(
            f"BT {r:.3f} {g:.3f} {b:.3f} rg /{font} {size} Tf {spacing} Tc "
            f"{x:.1f} {y:.1f} Td ({esc(s)}) Tj ET"
        )

    def watermark(self, s, x, y, size=48):
        r, g, b = BRASS
        self.ops.append(
            f"q /GS1 gs 0.866 0.5 -0.5 0.866 {x:.1f} {y:.1f} cm "
            f"BT {r:.3f} {g:.3f} {b:.3f} rg /F3 {size} Tf 6 Tc 0 0 Td ({esc(s)}) Tj ET Q"
        )

    def stream(self):
        return "\n".join(self.ops)


def build_pdf(page, title):
    content = page.stream().encode("cp1252", "replace")

    objs = []
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objs.append(
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources "
        b"<< /Font << /F1 5 0 R /F2 6 0 R /F3 7 0 R >> /ExtGState << /GS1 8 0 R >> >> "
        b"/Contents 4 0 R >>"
    )
    objs.append(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
    objs.append(b"<< /Type /ExtGState /ca 0.07 >>")
    objs.append(
        b"<< /Title (" + esc(title).encode("cp1252", "replace") +
        b") /Author (ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD) "
        b"/Creator (ARMINAK CARAVAN) >>"
    )

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_at = len(out)
    n = len(objs) + 1
    out += f"xref\n0 {n}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {n} /Root 1 0 R /Info {len(objs)} 0 R >>\n"
        f"startxref\n{xref_at}\n%%EOF\n"
    ).encode()
    return bytes(out)


def spec_sheet(item, lang="en"):
    L = lang == "ru"
    p = Page()

    p.rect(0, 0, 595, 842, SAND)

    # Letterhead
    p.rect(0, 742, 595, 100, NAVY)
    p.text(48, 796, "ARMINAK CARAVAN", font="F3", size=21, color=SAND, spacing=1.6)
    p.text(48, 774, "FOODSTUFF AND BEVERAGES TRADING LTD", font="F1", size=6.5,
           color=(0.65, 0.68, 0.72), spacing=1.5)
    p.text(48, 758, "KEZAD FREE ZONE  ·  ABU DHABI  ·  UNITED ARAB EMIRATES", font="F1",
           size=6.5, color=(0.55, 0.58, 0.63), spacing=1.2)
    p.text(400, 796, "ТЕХНИЧЕСКАЯ СПЕЦИФИКАЦИЯ" if L else "TECHNICAL SPECIFICATION",
           font="F2", size=7.5, color=BRASS, spacing=1.4)
    p.text(400, 778, (f"Выпущено {ISSUE_DATE_RU}" if L else f"Issued {ISSUE_DATE_EN}"),
           font="F1", size=7, color=(0.55, 0.58, 0.63), spacing=0.6)

    p.watermark("ARMINAK CARAVAN", 96, 250, 46)
    p.watermark("ARMINAK CARAVAN", 176, 430, 46)

    # Title block
    p.text(48, 700, (item["grade_ru"] if L else item["grade_en"]).upper(),
           font="F2", size=7.5, color=BRASS, spacing=1.6)
    p.text(48, 664, item["ru"] if L else item["en"], font="F3", size=26, color=NAVY, spacing=0.4)
    p.line(48, 640, 547, 640, BRASS, 0.7)

    # Laboratory specification
    p.text(48, 614, "ЛАБОРАТОРНАЯ СПЕЦИФИКАЦИЯ" if L else "LABORATORY SPECIFICATION",
           font="F2", size=7.5, color=BRASS, spacing=1.6)

    y = 586
    p.text(48, y, "ПАРАМЕТР" if L else "PARAMETER", font="F2", size=7, color=NAVY, spacing=1.2)
    p.text(330, y, "ЗНАЧЕНИЕ" if L else "VALUE", font="F2", size=7, color=NAVY, spacing=1.2)
    y -= 10
    p.line(48, y, 547, y, SAND2, 0.8)

    for (pe, ve, pr, vr) in item["spec"]:
        y -= 26
        p.text(48, y, pr if L else pe, font="F1", size=9.5, color=GREY)
        p.text(330, y, vr if L else ve, font="F2", size=9.5, color=NAVY)
        p.line(48, y - 9, 547, y - 9, SAND2, 0.8)

    # Commercial terms
    y -= 52
    p.text(48, y, "КОММЕРЧЕСКИЕ УСЛОВИЯ" if L else "COMMERCIAL TERMS",
           font="F2", size=7.5, color=BRASS, spacing=1.6)
    y -= 12
    p.line(48, y, 547, y, SAND2, 0.8)

    for (pe, ve, pr, vr) in item["meta"]:
        y -= 26
        p.text(48, y, pr if L else pe, font="F1", size=9.5, color=GREY)
        p.text(330, y, vr if L else ve, font="F2", size=9.5, color=NAVY)
        p.line(48, y - 9, 547, y - 9, SAND2, 0.8)

    # Inspection note
    y -= 46
    p.text(48, y, "КОНТРОЛЬ КАЧЕСТВА" if L else "QUALITY CONTROL",
           font="F2", size=7.5, color=BRASS, spacing=1.6)
    y -= 20
    note = ([
        "Качество и количество каждой партии подтверждаются независимой",
        "инспекцией SGS / Intertek / Bureau Veritas в порту погрузки.",
        "Сертификаты выпускаются на согласованные сторонами параметры.",
    ] if L else [
        "Quality and quantity of every consignment are certified by independent",
        "inspection — SGS / Intertek / Bureau Veritas — at the load port.",
        "Certificates are issued against the parameters agreed by both parties.",
    ])
    for ln in note:
        p.text(48, y, ln, font="F1", size=9, color=GREY)
        y -= 15

    # Footer
    p.line(48, 96, 547, 96, BRASS, 0.7)
    p.text(48, 78, "ARMINAK CARAVAN FOODSTUFF AND BEVERAGES TRADING LTD", font="F2",
           size=7.5, color=NAVY, spacing=0.8)
    p.text(48, 64, "KEZAD Free Zone, Abu Dhabi, United Arab Emirates  ·  Free Zone Licence #5820194",
           font="F1", size=7.5, color=GREY)
    p.text(48, 50, ("Документ носит справочный характер. Цены и ставки фрахта предоставляются по официальному запросу."
                    if L else
                    "Indicative document. Prices and freight rates are released against a formal written request only."),
           font="F1", size=7.5, color=GREY)

    return build_pdf(p, (item["ru"] if L else item["en"]) + " — Technical Specification")


# ================================================================== HTML =====

def spec_template(item, indent="        "):
    slug = item["slug"]
    spec_rows = "\n".join(
        f'{indent}    <tr><th scope="row" data-i18n="p.{slug}.sp{i}">{pe}</th>'
        f'<td data-i18n="p.{slug}.sv{i}">{ve}</td></tr>'
        for i, (pe, ve, _, _) in enumerate(item["spec"])
    )
    meta_rows = "\n".join(
        f'{indent}    <div><dt data-i18n="p.{slug}.mp{i}">{pe}</dt>'
        f'<dd data-i18n="p.{slug}.mv{i}">{ve}</dd></div>'
        for i, (pe, ve, _, _) in enumerate(item["meta"])
    )
    return f'''{indent}<template class="card__spec">
{indent}  <table class="spec">
{indent}    <thead>
{indent}    <tr>
{indent}      <th scope="col" data-i18n="cat.param">Parameter</th>
{indent}      <th scope="col" data-i18n="cat.value">Value</th>
{indent}    </tr>
{indent}    </thead>
{indent}    <tbody>
{spec_rows}
{indent}    </tbody>
{indent}  </table>
{indent}  <dl class="drawer__meta">
{meta_rows}
{indent}  </dl>
{indent}</template>'''


def card_html(item, cat_id, cat_en):
    slug = item["slug"]
    badge = BADGES.get(slug)
    badge_html = ""
    if badge == "new":
        badge_html = '\n          <span class="card__badge" data-i18n="shop.badgeNew">New</span>'
    elif badge == "best":
        badge_html = '\n          <span class="card__badge" data-i18n="shop.badgeBest">Bestseller</span>'

    collections = []
    if badge == "new":
        collections.append("new")
    if badge == "best":
        collections.append("bestsellers")
    if slug in PRIVATE_LABEL:
        collections.append("private-label")

    return f'''      <a class="card fade-up" href="product.html?p={slug}"
         data-product="{item["en"]}" data-grade="{item["grade_en"]}"
         data-product-key="p.{slug}.name" data-grade-key="p.{slug}.grade"
         data-cat="{cat_id}" data-name="{item["en"]}" data-collections="{' '.join(collections)}">
        <div class="card__figure">{badge_html}
          <button type="button" class="card__fav" aria-label="Save to favourites">{HEART}</button>
          <img class="card__art" src="assets/img/products/{item["art"]}.svg" alt="" loading="lazy" width="400" height="500">
          <button type="button" class="card__quick" data-drawer-trigger data-i18n="shop.quickRfq">Quick RFQ</button>
        </div>

        <div class="card__row">
          <h3 class="card__title" data-i18n="p.{slug}.name">{item["en"]}</h3>
          <span class="card__price" data-i18n="shop.onRequest">On request</span>
        </div>
        <span class="card__cat" data-i18n="cat.c.{cat_id}">{cat_en}</span>

{spec_template(item)}
      </a>'''


def build_cards():
    """One flat list of cards for the filterable shop grid."""
    cards = []
    for c in CATEGORIES:
        for item in c["items"]:
            cards.append(card_html(item, c["id"], c["en"]))
    return cards


def build_filters():
    cats = "\n".join(
        f'''          <label class="check">
            <input type="checkbox" data-filter-cat="{c["id"]}">
            <span data-i18n="cat.c.{c["id"]}">{c["en"]}</span>
            <span class="check__n tabular">{len(c["items"])}</span>
          </label>'''
        for c in CATEGORIES
    )
    return cats


def build_products_js():
    """Client-side catalogue: PDP renderer + home rails read this."""
    order = []
    data = {}
    for c in CATEGORIES:
        for item in c["items"]:
            s = item["slug"]
            order.append(s)
            data[s] = {
                "cat": c["id"],
                "art": item["art"],
                "badge": BADGES.get(s),
                "collections": (["new"] if BADGES.get(s) == "new" else [])
                             + (["bestsellers"] if BADGES.get(s) == "best" else [])
                             + (["private-label"] if s in PRIVATE_LABEL else []),
                "en": {
                    "name": item["en"], "grade": item["grade_en"],
                    "origin": item["origin_en"], "catName": c["en"],
                    "metrics": item["metrics_en"],
                    "spec": [[pe, ve] for (pe, ve, _, _) in item["spec"]],
                    "meta": [[pe, ve] for (pe, ve, _, _) in item["meta"]],
                },
                "ru": {
                    "name": item["ru"], "grade": item["grade_ru"],
                    "origin": item["origin_ru"], "catName": c["ru"],
                    "metrics": item["metrics_ru"],
                    "spec": [[pr, vr] for (_, _, pr, vr) in item["spec"]],
                    "meta": [[pr, vr] for (_, _, pr, vr) in item["meta"]],
                },
            }
    return order, data


def build_i18n():
    d = {}
    for c in CATEGORIES:
        d[f"cat.c.{c['id']}"] = c["ru"]
        d[f"cat.n.{c['id']}"] = c["note_ru"]
        for item in c["items"]:
            s = item["slug"]
            d[f"p.{s}.name"] = item["ru"]
            d[f"p.{s}.grade"] = item["grade_ru"]
            d[f"p.{s}.origin"] = item["origin_ru"]
            for i, m in enumerate(item["metrics_ru"]):
                d[f"p.{s}.m{i}"] = m
            for i, (_, _, pr, vr) in enumerate(item["spec"]):
                d[f"p.{s}.sp{i}"] = pr
                d[f"p.{s}.sv{i}"] = vr
            for i, (_, _, pr, vr) in enumerate(item["meta"]):
                d[f"p.{s}.mp{i}"] = pr
                d[f"p.{s}.mv{i}"] = vr
    return d


if __name__ == "__main__":
    # English only: PDF base-14 fonts carry no Cyrillic, and technical
    # specification sheets in international trade are issued in English.
    count = 0
    for old in DOCS.glob("*.ru.pdf"):
        old.unlink()
    for c in CATEGORIES:
        for item in c["items"]:
            (DOCS / f"{item['slug']}.pdf").write_bytes(spec_sheet(item, "en"))
            count += 1

    import json

    cards = build_cards()
    here = pathlib.Path(__file__).parent
    (here / "_cards.html").write_text("\n".join(cards), encoding="utf-8")
    (here / "_filters.html").write_text(build_filters(), encoding="utf-8")

    order, data = build_products_js()
    (ROOT / "assets" / "js" / "products.js").write_text(
        "/* Generated by build_catalogue.py — full catalogue data (EN + RU). */\n"
        "window.PRODUCT_ORDER = " + json.dumps(order) + ";\n"
        "window.PRODUCTS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")

    ru = build_i18n()
    (ROOT / "assets" / "js" / "i18n-catalogue.js").write_text(
        "/* Generated by build_catalogue.py — Russian strings for the catalogue. */\n"
        "window.__RU_CATALOGUE = " + json.dumps(ru, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8")

    print(f"pdfs: {count}  ·  cards: {len(cards)}  ·  products.js: {len(order)}  ·  ru keys: {len(ru)}")
