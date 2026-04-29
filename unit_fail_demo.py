precipitation_mm = 12.0
precipitation_m = precipitation_mm / 1000
precipitation_mm_back = precipitation_m * 1000

assert abs(precipitation_mm_back - precipitation_mm) < 1e-9, "Ошибка"
print("Конвертация прошла успешно, точность сохранена.")