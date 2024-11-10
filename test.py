import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from PIL import ImageEnhance

plt.switch_backend('TkAgg')
plt.style.use('fast')

def corazon_3d(x,y,z):
    return (x**2 + (9/4)*(y**2) + z**2 - 1)**3 - (x**2)*(z**3) - (9/80)*(y**2)*(z**3)

fig = plt.figure(figsize=(16, 16))
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('#F5A5C5')
ax.set_facecolor('#F5A5C5')

# Configurar los límites y vista
bbox = (-1.5, 1.5)
xmin, xmax, ymin, ymax, zmin, zmax = bbox*3
ax.set_xlim3d(xmin, xmax)
ax.set_ylim3d(ymin, ymax)
ax.set_zlim3d(zmin, zmax)
ax.set_axis_off()

# Reducir la cantidad de líneas y ajustar su grosor
M = np.linspace(xmin, xmax, 50)  
N = np.linspace(xmin, xmax, 25)  
M1, M2 = np.meshgrid(M, M)

# Dibujar menos contornos con líneas más gruesas
for z in N[::2]:  # Tomar uno de cada dos puntos
    X, Y = M1, M2
    Z = corazon_3d(X, Y, z)
    ax.contour(X, Y, Z+z, [z], zdir='z', colors=('#ff0000'), linewidths=2.5)

for y in N[::2]:
    X, Z = M1, M2
    Y = corazon_3d(X, y, Z)
    ax.contour(X, Y+y, Z, [y], zdir='y', colors=('#ff0000'), linewidths=2.5)

for x in N[::2]:
    Y, Z = M1, M2
    X = corazon_3d(x, Y, Z)
    ax.contour(X+x, Y, Z, [x], zdir='x', colors=('#ff0000'), linewidths=2.5)

# Manejo de la imagen 
img = Image.open("./kiwi.jpg")
img = img.resize((300, 300), Image.Resampling.LANCZOS)  

# Ajsutes de brillo y contraste
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.0) 
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.8)  # Aumentar contraste en 80%

# Ajuste de la saturación
enhancer = ImageEnhance.Color(img)
img = enhancer.enhance(1.0) 

img = np.array(img.convert("RGBA"))

# Ajustar la posición de la imagen inclinándola más hacia arriba
x = np.linspace(-0.75, 0.75, img.shape[1])
y = np.linspace(-1.2, 0.8, img.shape[0])  # Ajustado para inclinar hacia arriba
X1, Y1 = np.meshgrid(x, y)

rgba_norm = img / 255.0
mask = corazon_3d(X1, 0, -Y1) < 0
rgba_norm[~mask] = 0

# Graficar superficie con opacidad total
ax.plot_surface(X1, np.zeros_like(X1), -Y1, 
               facecolors=rgba_norm,
               rstride=1, cstride=1,
               alpha=1.0,
               antialiased=True)

def animate(i):
    ax.view_init(elev=40, azim=i*4)  # Aumentado el ángulo de elevación
    return [ax]


anim = animation.FuncAnimation(fig,
                             animate,
                             frames=180,
                             interval=1,
                             blit=False)

# Guardar con alta calidad
Writer = animation.writers['pillow']
writer = Writer(fps=60, metadata=dict(artist='Melkin'), bitrate=3600)
# Cambiar el color de fondo al guardar
anim.save('corazon_3d.gif', writer=writer, savefig_kwargs={'facecolor': '#F5A5C5'})
plt.close()