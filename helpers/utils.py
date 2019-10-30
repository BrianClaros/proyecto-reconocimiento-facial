from PIL import Image

def obtenerPorcentajeDeDiferencia(frameAnterior, frameActual): 
    imagen1 = Image.fromarray(frameAnterior)
    imagen2 = Image.fromarray(frameActual)

    pairs = zip(imagen1.getdata(), imagen2.getdata())
    if len(imagen1.getbands()) == 1:
        dif = sum(abs(p1-p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = imagen1.size[0] * imagen1.size[1] * 3

    percentaje = ((dif / 255.0 * 100) / ncomponents) * 100
    return percentaje