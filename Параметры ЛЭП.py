from math import log10, sin, pi

# Для расщепления 330-500 кВ на 2 или на 3 провода: а = 400 мм
# Для расщепления 750 кВ на 4 провода: а = 600 мм
# Для расщепления 750 кВ на 5 проводов: а = 300 мм

print ("")

wires = {"1": ("АС-500/64", 0.058, 30.6, 1),
         "2": ("АС-500/26", 0.058, 30.1, 1), 
         "3": ("АС-400/51", 0.073, 27.5, 1), 
         "4": ("АС-300/39", 0.096, 24, 1), 
         "5": ("АС-240/32", 0.118, 21.6, 1),
         "6": ("АС-185/29", 0.159, 18.8, 1),
         "7": ("АС-150/24", 0.204, 17.1, 1),
         "8": ("АС-120/19", 0.244, 15.2, 1),
         "9": ("АС-95/16", 0.301, 13.5, 1),
         "10": ("АС-70/16", 0.422, 11.4, 1),
         "11": ("ACCR 470-T16 Hawk", 0.1153, 21.6, 1),
         "12": ("ACCR 656-T16 Grosbeak", 0.0828, 25.5, 1),
         "13": ("2×АС-300/39, a = 400 мм", 0.096, 24, 2, 400),
         "14": ("3×АС-300/39, a = 400 мм", 0.096, 24, 3, 400),
         "15": ("3×АС-400/51, a = 400 мм", 0.073, 27.5, 3, 400),
         "16": ("3×АС-330/43, a = 400 мм", 0.087, 25.2, 3, 400),
         "17": ("АС-AERO-z AAcsr Z 647 a3F", 0.0771, 31, 1),
         "18": ("3×АС-500/64, a = 400 мм", 0.058, 30.6, 3, 400)}

standart_d_sg = {"35": 3.5, "110": 5, "150": 6.5, "220": 8, "330": 11, "500": 14, "750": 22.7}

def calc_r0(r_pr, n = 1):
  return r_pr / n

def calc_x0(r_ekv, d_sg, n = 1):
  return 0.1445 * log10(d_sg*10**3 / r_ekv) + (0.0157 / n)

def calc_b0(r_ekv, d_sg):
  return 7.58 / log10(d_sg*10**3 / r_ekv)


for key, value in wires.items():
  print("{k}: {w}".format(k=key, w=value[0]))

print ("")
n_uchastkov = input("Введите количество участков ЛЭП: ")
if n_uchastkov == "":
  n_uchastkov = 1
else:
  n_uchastkov = int(n_uchastkov)
u_nom = input("Введите Uном: ")
d_sg = standart_d_sg.get(u_nom)
r_sum = 0
x_sum = 0
b_sum = 0
for i in range(n_uchastkov):
  print ("")
  wire = input("Выберите провод № {} (1-18): ".format(i+1))
  l = float(input("Введите длину участка, км: "))
  n = wires[wire][3]
  r0 = calc_r0(wires[wire][1], n)
  rad_pr = wires[wire][2] / 2
  if n > 1:
    a = wires[wire][4]
    R_r = a/(2*sin(pi/n))
    r_eq = R_r * (n * rad_pr / R_r)**(1/n)
    rad_pr = r_eq
  x0 = calc_x0(rad_pr, d_sg, n)
  b0 = calc_b0(rad_pr, d_sg)
  r_sum += r0 * l
  x_sum += x0 * l
  b_sum += b0 * l

print ("")
print("Параметры ЛЭП:")
print("R = {0:.5f} Ом\nX = {1:.5f} Ом\nB = -{2:.5f} мкСм".format(r_sum, x_sum, b_sum))
