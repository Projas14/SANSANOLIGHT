**[PROYECTO RAMO UNIVERSIDAD]**

SANSANOLIGHT / PROYECTO INTRODUCCIÓN A LA INGENIERA INFORMÁTICA / 2015-2
========================================

ACERCA DEL PROYECTO
------------------
- Sistema de retroiluminación para LCDs y Monitores que estén conectados a un pc
- Su objetivo es mejorar la experiencia visual y los parámetros de la imagen mediante el contraste, brillo, viveza de colores, etc.
- Lo logra mediante tecnología capaz de producir luz ambiental adecuada para el contenido que se está visualizando en pantalla.

COMPONENTES
------------------
- **Luces LED RGB:** Estas tiras de luces LEDs cuentan con la ventaja de poder tomar el color de toda la gama RGB. Las hay de dos tipos: análogas (Toda la tira toma un solo color simultáneamente) y digitales (Permiten el control individual de los leds)
- **Socket:** Concepto abstracto, que se puede definir como el mecanismo que permite la conexión entre distintos procesos, habitualmente se utilizan para establecer comunicaciones entre distintas máquinas que estén conectadas a través de la red; en nuestro caso el PC y la RPi. Cuando utilizamos Sockets para comunicar procesos nos basamos en la arquitectura cliente y servidor.

CÓDIGO
------------------

**SANSANOLIGHT-CLIENTE**

Programa con una simple interfaz gráfica en donde el usuario puede:
- Iniciar/Detener el programa
- Seleccionar la cantidad de luces a utilizar
- Seleccionar la Tira Led RGB a utilizar (análoga o digital)

Este programa obtiene los datos de la pantalla:
- Tira Análoga: Obtiene el color mas predominante de la pantalla
- Tira Digital: Obtiene los colores laterales y superiores asociados a cada luz

Funciones:
- `capturar_pantalla()`: Captura la pantalla y analiza según la opción elegida por el usuario (Modo análogo, modo digital)
- `ordenar_archivo()`: Se ordena el archivo creado en la función capturar_pantalla() para el modo digital de tal forma que se tengan los leds en orden.
- `Iniciar_programa()`: inicia programa
- `detener_programa()`: detiene programa

**ENVO DE DATOS**

Conexión vía socket, usando la red Wifi disponible. La raspberry actúa como servidor y el PC como el cliente. Al iniciar el programa se establece una conexión y cada vez que se obtienen los datos de la pantalla estos son enviados como string a la Raspberry Pi.

**SANSANOLIGHT-SERVIDOR**

Programa sin interfaz que recibe los datos del cliente e inicia el control de leds.

Funciones:
- `control_leds()`: función q recibe como parámetro el color de los leds y los enciende de acuerdo a la información
- `setLigths()`: ajusta el brillo de acuerdo al color que se debe obtener.
