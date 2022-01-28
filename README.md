## _SHELL_

- Universidad Catolica "Nuestra Señora de la Asunción"

- Enero 2022

## Manual de Instalacion
### Paso 1
Para este paso, es necesario contar con git. Desde ubuntu, clonar el repositorio https://github.com/amparooliver/SO1.git en directorio a eleccion.
### Paso 2
Aun desde ubuntu y root, mover shell.py y logger.py a $LFS/usr/local/bin y darle permisos de ejecucion.
```sh
mv /path/to/shell.py $LFS/usr/local/bin
mv /path/to/logger.py $LFS/usr/local/bin
chmod 755  $LFS/usr/local/bin/shell.py
chmod 755  $LFS/usr/local/bin/logger.py
``` 
### Paso 3
Crear el directorio para el logger
```sh
mkdir -v $LFS/var/log/shell
```
### Paso 4
Crear los archivos necesarios para los logger y darle permisos.
```sh
touch $LFS/var/log/shell/sistema_error.log
touch $LFS/var/log/shell/usuario_horarios_log.log
touch $LFS/var/log/shell/Shell_transferencias.log
touch $LFS/var/log/shell/Shell_registro.log
chmod 777 $LFS/var/log/shell/sistema_error.log
chmod 777 $LFS/var/log/shell/usuario_horarios_log.log
chmod 777 $LFS/var/log/shell/Shell_transferencias.log
chmod 777 $LFS/var/log/shell/Shell_registro.log
```
### Paso 5
Entrar al ambiente de LFS (siguiendo los pasos del libro de LFS), modificar el archivo /etc/shells y agregar el path del shell.py 
```sh
/usr/local/bin/shell.py
```
### Paso 6
Modificar el archivo /etc/passwd y asignarle al usuario root la shell. En este caso:
```sh
root: ...........:/usr/local/bin/shell.py
```
### Paso 7
Reiniciar el sistema e ingresar a el usuario root. 

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
Se utiliza para cambiar la contraseña de un usuario.
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
### doFTP
Se utiliza para tranferir archivos desde una network remota.
>Sintaxis: doFtp domain

```sh
ftp domain.com
```
### Demonio
Se utiliza para levantar/apagar demonios.
>Sintaxis: demonio levantar/apagar pid

```sh
demonio apagar 708
```
### doShell
Se utiliza para poder ejecutar cualquier comando del sistema.
>Sintaxis: doShell unixCommand

```sh
doShell ls -l
```


