import math

def msf(numero):
    parte_decimal, parte_entera = math.modf(numero)
    decimal = 100*(round(parte_decimal,3))
    frame = (parte_entera*60+decimal)*30
    return frame


def segs(inicio_video, final_video):
    decimal_inicial, entero_inicio = math.modf(inicio_video) 
    decimal_final, entero_final = math.modf(final_video) 
    decimal_inicial =  100*(round(decimal_inicial,3))
    decimal_final =  100*(round(decimal_final,3))

    ef = entero_final
    ei = entero_inicio
    df = decimal_final
    di = decimal_inicial
    
    segs = 60*(ef-ei) + (df-di)
    return int(segs)