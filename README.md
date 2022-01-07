# Manual de Uso

## _SHELL_

- Universidad Catolica "Nuestra Señora de la Asunción"

- Enero 2022

## Manual de Uso
## Comandos

### Copiar
Se utiliza para copiar el contenido del archivo de origen al archivo o directorio de destino. 
>Sintaxis: copiar archivo destino

```sh
copiar /path/to/File /path/to/Destination
```

### Mover
Se utiliza para mover un archivo o directorio (origen) a otro directorio (destino). 
>Sintaxis: mover origen destino

```sh
mover /path/to/Origin /path/to/Destination
```

### Renombrar
Se utiliza para renombrar un archivo o directorio (origen) a otro directorio (destino). 
>Sintaxis: renombrar origen destino

```sh
renombrar /path/to/Original /path/to/Renamed
```

### Listar
Se utiliza para listar todas las entradas dentro de un directorio (path). Se puede listar el directorio actual ejecutando el comando sin ningún argumento.
>Sintaxis: listar destino

```sh
listar
listar Folder
```

### Creardir
Se utiliza para crear un directorio. 
>Sintaxis: creardir destino

```sh
creardir /path/to/Directory
```

### Ir
Se utiliza para cambiar del directorio actual (origen) a otro (destino). Se puede ejecutar el comando ir sin argumento para cambiar del directorio actual a HOME. 
>Sintaxis: ir destino

```sh
ir
ir /path/to/Directory
```

### Permisos
Se utiliza para cambiar los permisos de un archivo o directorio. 
>Sintaxis: permisos modo path

```sh
permisos 777 Example.txt
```
![alt text](https://preview.redd.it/vkxuqbatopk21.png?auto=webp&s=81f97dac1e1ceb5054ee43cbe96ec6fa55215695)

### Propietario
Se utiliza para cambiar el propietario de un archivo o directorio. 
>Sintaxis: propietario usuario destino

```sh
propietario thisUser Example.txt
```
### Contraseña
Se utiliza para enlazar una contraseña a un usuario o cambiar la contraseña.
>Sintaxis: contrasenha usuario

```sh
contrasenha thisUser
```
### Usuario
Se utiliza para crear un nuevo usuario. 
>Sintaxis: usuario username

```sh
usuario thisUser
```
### Groups
Se utiliza para imprimir los ID de los grupos de determinado usuario.
>Sintaxis: grupos username

```sh
grupos thisUser
```
### Diff
Se utiliza para comparar dos archivos linea por linea.
>Sintaxis: difer file1 file2

```sh
difer file1 /path/to/file2
```

