import qrcode

# Файл атын киргизүү
filename = input("Файл атын киргиз: ")

# Ссылка киргизүү
data = input("Ссылка киргиз: ")

# QR код түзүү
qr = qrcode.make(data)

# PNG болуп сактоо
qr.save(f"{filename}.png")

print("QR код сакталды:", f"{filename}.png")