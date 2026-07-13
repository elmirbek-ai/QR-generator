# QR Generator

Кыргыз тилиндеги жөнөкөй консоль программасы. Киргизилген текстти же шилтемени PNG форматындагы QR кодго айландырат.

## Мүмкүнчүлүктөр

- текст же шилтеме үчүн QR код түзөт;
- файл атын текшерип, папкадан сыртка жазууга жол бербейт;
- бар файлдын үстүнөн жазбайт;
- даяр файлдарды `qr_codes/` папкасына сактайт;
- Windows, macOS жана Linux системаларында иштейт.

## Орнотуу

Python 3.10 же андан кийинки версия керек.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS же Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Иштетүү

```bash
python main.py
```

Программа файлдын атын жана QR кодго киргизиле турган текстти же шилтемени сурайт. `.png` кеңейтүүсүн жазбасаңыз да болот. Мисалы, `менин-кодум` деген ат `qr_codes/менин-кодум.png` болуп сакталат.

Эгер ушундай аталыштагы файл бар болсо, программа аны өзгөртпөй, ката чыгарат.

## Тесттер

```bash
python -m unittest discover -s tests -v
python -m py_compile main.py
```

GitHub Actions бул текшерүүлөрдү Python 3.10, 3.12 жана 3.13 версияларында автоматтык иштетет.
