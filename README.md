# GUI-BoundingBoxes

Interfaz para la validacion de las anotocianes sobre imagenes en el dataset.
Los valores 0 en faces del xml es error de deteccion y el valor -1 indica imagen inapropiada.

## Instrucciones

### Hot Keys

#### Ventana principal

|    Tecla     |          Accion          |
| :----------: | :----------------------: |
|      A       |     Anterior imagen      |
|      D       |     Siguiente imagen     |
|      L       |    Error de deteccion    |
|      J       |    Imagen inapropiada    |
| Boton arriba | Seleccionar bounding box |
| Boton abajo  | Seleccionar bounding box |
|    Intro     |    Abrir bounding box    |

#### Ventana de imagen cortada

|   Tecla   |          Accion           |
| :-------: | :-----------------------: |
| Boton izq |      Siguiente clase      |
| Boton der |      Anterior clase       |
|    Esc    |    Para cerrar ventana    |
| Backspace | Eliminar box seleccionada |

### Paso 1

El primer boton habilitado te dejara seleccionar una imagen debes seleccionar solo una y esta debe estar en la carpeta con esta estructura

- annotations(Esta carpeta puede ser Annotations o annotation)
- imagenes
  - imagen1.jpg
  - imagen2.jpg
  - ..
  - ...

### Paso 2

Al seleccionar la imagen se habilitaran los controles para ir iterando por cada una.
Para cambiar el tipo de cubreboca se debe dar doble click en la list view de la izquierda

### Paso 3

Al tener esa vista ahora podras modificar el tipo de cubreboca que hay y se actualizara en la imagen.

Nota: Esta ventana se cierra al apretar en el de cerrar no al quitar el foco sobre ella
