# Importar librerías necesarias
import matplotlib.pyplot as plt          # Para crear gráficos
import numpy as np                       # Para cálculos numéricos
from PIL import Image                    # Para procesar imágenes
from mpl_toolkits.mplot3d import Axes3D  # Para gráficos 3D
from matplotlib import animation         # Para crear animaciones
from PIL import ImageEnhance            # Para ajustar brillo/contraste

# Configurar matplotlib
plt.switch_backend('TkAgg')  # Usar TkAgg como backend para mejor rendimiento
plt.style.use('fast')        # Usar estilo rápido para mejor rendimiento

# Función que define la forma matemática del corazón 3D
def corazon_3d(x,y,z):
    # Ecuación paramétrica del corazón
    return (x**2 + (9/4)*(y**2) + z**2 - 1)**3 - (x**2)*(z**3) - (9/80)*(y**2)*(z**3)

# Crear figura y configurar espacio 3D
fig = plt.figure(figsize=(16, 16))                    # Tamaño de la figura
ax = fig.add_subplot(111, projection='3d')            # Agregar subplot 3D
fig.patch.set_facecolor('#F5A5C5')                   # Color de fondo rosa
ax.set_facecolor('#F5A5C5')                          # Color de fondo del eje

# Configurar los límites del espacio 3D
bbox = (-1.5, 1.5)                                    # Límites base
xmin, xmax, ymin, ymax, zmin, zmax = bbox*3          # Expandir límites
ax.set_xlim3d(xmin, xmax)                            # Establecer límites X
ax.set_ylim3d(ymin, ymax)                            # Establecer límites Y
ax.set_zlim3d(zmin, zmax)                            # Establecer límites Z
ax.set_axis_off()                                    # Ocultar ejes

# Crear puntos para dibujar el corazón
M = np.linspace(xmin, xmax, 50)                      # 50 puntos en cada dirección
N = np.linspace(xmin, xmax, 25)                      # 25 puntos para contornos
M1, M2 = np.meshgrid(M, M)                          # Crear malla 2D

# Dibujar contornos del corazón en el plano Z
for z in N[::2]:                                     # Usar uno de cada dos puntos
    X, Y = M1, M2
    Z = corazon_3d(X, Y, z)
    ax.contour(X, Y, Z+z, [z], zdir='z', colors=('#ff0000'), linewidths=2.5)

# Dibujar contornos del corazón en el plano Y
for y in N[::2]:
    X, Z = M1, M2
    Y = corazon_3d(X, y, Z)
    ax.contour(X, Y+y, Z, [y], zdir='y', colors=('#ff0000'), linewidths=2.5)

# Dibujar contornos del corazón en el plano X
for x in N[::2]:
    Y, Z = M1, M2
    X = corazon_3d(x, Y, Z)
    ax.contour(X+x, Y, Z, [x], zdir='x', colors=('#ff0000'), linewidths=2.5)

# Procesar la imagen
img = Image.open("./kiwi.jpg")                       # Abrir imagen
img = img.resize((300, 300), Image.Resampling.LANCZOS)  # Redimensionar

# Ajustar brillo y contraste de la imagen
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.0)                          # Brillo normal
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.8)                          # Aumentar contraste 80%

# Ajustar saturación de la imagen
enhancer = ImageEnhance.Color(img)
img = enhancer.enhance(1.0)                          # Saturación normal

# Convertir imagen a array numpy con transparencia
img = np.array(img.convert("RGBA"))

# Posicionar la imagen en el espacio 3D
x = np.linspace(-0.75, 0.75, img.shape[1])
y = np.linspace(-1.2, 0.8, img.shape[0])            # Inclinar hacia arriba
X1, Y1 = np.meshgrid(x, y)

# Normalizar colores y aplicar máscara de corazón
rgba_norm = img / 255.0                              # Normalizar valores de color
mask = corazon_3d(X1, 0, -Y1) < 0                   # Crear máscara con forma de corazón
rgba_norm[~mask] = 0                                 # Aplicar máscara

# Dibujar la imagen en la superficie del corazón
ax.plot_surface(X1, np.zeros_like(X1), -Y1, 
               facecolors=rgba_norm,
               rstride=1, cstride=1,                 # Calidad de renderizado
               alpha=1.0,                            # Opacidad total
               antialiased=True)                     # Suavizar bordes

# Función para animar la rotación
def animate(i):
    ax.view_init(elev=40, azim=i*4)                 # Rotar vista (40° elevación)
    return [ax]

# Crear la animación
anim = animation.FuncAnimation(fig,
                             animate,
                             frames=180,             # Número de frames
                             interval=1,             # Intervalo entre frames (ms)
                             blit=False)             # No usar blitting

# Configurar y guardar la animación
Writer = animation.writers['pillow']                 # Usar pillow como escritor
writer = Writer(fps=60,                             # 60 frames por segundo
               metadata=dict(artist='Melkin'),       # Metadata
               bitrate=3600)                         # Calidad del video
# Guardar como GIF
anim.save('corazon_3d.gif',                         # Nombre del archivo
         writer=writer,                             # Configuración del escritor
         savefig_kwargs={'facecolor': '#F5A5C5'})   # Color de fondo
plt.close()                                         # Cerrar la figura 