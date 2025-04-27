import tkinter as tk
import random


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

CANVAS_WIDTH = CANVAS_HEIGHT = WINDOW_HEIGHT

RADIO_CIRCULO = CANVAS_WIDTH // 2

window = tk.Tk()
#window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2}+{window.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2}')
window.geometry(f'+{window.winfo_screenwidth() // 2 - WINDOW_WIDTH // 2}+{window.winfo_screenheight() // 2 - WINDOW_HEIGHT // 2}')
window.title('Simulador de pi')

window_frame = tk.Frame(window)

canvas = tk.Canvas(window_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')

canvas.grid(column=0, row=0, rowspan=20)
puntos_var = tk.IntVar(window_frame, value=5000)
puntos_frame = tk.LabelFrame(window_frame, text='Cantidad de puntos')
puntos_entry = tk.Entry(puntos_frame, textvariable=puntos_var)
puntos_entry.pack(padx=5, pady=5)
puntos_frame.grid(column=1, row=0, columnspan=2)
#simular_btn = tk.Button(window_frame, text='Simular', command=lambda: dibujar_puntos(canvas, generar_puntos(puntos_var.get())))
#simular_btn = tk.Button(window_frame, text='Simular', command=lambda: dibujar_puntos_2(canvas, generar_puntos(puntos_var.get())))
simular_btn = tk.Button(window_frame, text='Simular c/anim', command=lambda: dibujar_wrapper(canvas, generar_puntos(puntos_var.get())))
simular_btn.grid(column=1, row=1, padx=5)
finalizar_btn = tk.Button(window_frame, text='Simular s/anim', command=lambda: dibujar_puntos(canvas, generar_puntos(puntos_var.get())))
finalizar_btn.grid(column=2, row=1, padx=5)

resultado_label = tk.Label(window_frame)
resultado_label.grid(column=1, row=2, columnspan=2)

window_frame.pack()

canvas.create_rectangle(2, 2, CANVAS_WIDTH + 1, CANVAS_HEIGHT + 1)
canvas.create_oval(3, 3, CANVAS_WIDTH, CANVAS_HEIGHT)

def generar_puntos(cant_puntos):
    return [(random.randint(3, CANVAS_HEIGHT), random.randint(3, CANVAS_HEIGHT)) for _ in range(cant_puntos)]

def punto_esta_adentro(punto):
    #print((punto[0] - RADIO_CIRCULO) * (punto[0] - RADIO_CIRCULO) + (punto[1] - RADIO_CIRCULO) * (punto[1] - RADIO_CIRCULO) <= RADIO_CIRCULO*RADIO_CIRCULO)
    return (punto[0] - RADIO_CIRCULO) * (punto[0] - RADIO_CIRCULO) + (punto[1] - RADIO_CIRCULO) * (punto[1] - RADIO_CIRCULO) <= RADIO_CIRCULO * RADIO_CIRCULO

def dibujar_puntos(canvas:tk.Canvas, puntos):
    puntos_entry['state'] = 'disabled'
    simular_btn['state'] = 'disabled'
    canvas.delete('all')
    canvas.create_rectangle(2, 2, CANVAS_WIDTH + 1, CANVAS_HEIGHT + 1)
    canvas.create_oval(3, 3, CANVAS_WIDTH, CANVAS_HEIGHT)
    cant_adentro = 0
    for punto in puntos:
        color = 'blue'
        if punto_esta_adentro(punto):
            color = 'red'
            cant_adentro += 1
        canvas.create_oval(punto[0]-1, punto[1]-1, punto[0]+1, punto[1]+1, outline=color, fill=color)
    resultado_label.config(text=f'4 * {cant_adentro} / {puntos_var.get()} = {4 * cant_adentro / puntos_var.get()}')
    puntos_entry['state'] = 'normal'
    simular_btn['state'] = 'active'


def dibujar_wrapper(canvas, puntos):
    def dibujar_puntos_inner(canvas:tk.Canvas, puntos):
        nonlocal index
        nonlocal cant_adentro
        i = 0
        #print(index)
        while i < 5 * len(puntos) / 100  and index < len(puntos):
            punto = puntos[index]
            color = 'blue'
            if punto_esta_adentro(punto):
                color = 'red'
                cant_adentro += 1
            canvas.create_oval(punto[0]-1, punto[1]-1, punto[0]+1, punto[1]+1, outline=color, fill=color)
            i += 1
            index += 1
        #resultado_label.config(text=f'4 * {cant_adentro} / {puntos_var.get()} = {4 * cant_adentro / puntos_var.get():.4f}')
        resultado_label.config(text=f'4 * {cant_adentro} / {index} = {4 * cant_adentro / index:.4f}')
        if index < len(puntos):
            canvas.after(10, dibujar_puntos_inner, canvas, puntos)
        else:
            #print('TERMINADO')
            puntos_entry['state'] = 'normal'
            simular_btn['state'] = 'normal'
            finalizar_btn['state'] = 'normal'
    puntos_entry['state'] = 'disabled'
    simular_btn['state'] = 'disabled'
    finalizar_btn['state'] = 'disabled'
    index = 0
    cant_adentro = 0
    canvas.delete('all')
    canvas.create_rectangle(2, 2, CANVAS_WIDTH + 1, CANVAS_HEIGHT + 1)
    canvas.create_oval(3, 3, CANVAS_WIDTH, CANVAS_HEIGHT)
    dibujar_puntos_inner(canvas, puntos)


window.mainloop()
