# Persona 3: Dancing in Moonlight para PC

Port para PC de **Persona 3: Dancing in Moonlight** (PlayStation 4, CUSA12636) para Windows 10/11.

> **No se incluyen archivos del juego.** Necesitas tu propia copia del juego de PS4 como carpeta
> (`eboot.bin`, `sce_module` y `sce_sys`).
> Persona y Persona 3: Dancing in Moonlight son marcas de ATLUS / SEGA. Este proyecto no está
> afiliado a ellas.

## Descargar y jugar

1. Descarga el `.zip` desde la página de
   [Releases](https://github.com/Piscacho/Persona-3-Dancing-in-Moonlight/releases/latest)
   y descomprímelo en una carpeta, por ejemplo `C:\Juegos\Persona 3 Dancing`.
2. Pon la carpeta del juego junto a ella como `juego\CUSA12636` (se detecta sola), o elígela en
   el launcher: **Game → Carpeta del juego**.
3. Abre **`Persona 3 Dancing.exe`** y pulsa **PLAY**. Si Windows muestra "Windows
   protegió tu PC", pulsa **Más información → Ejecutar de todas formas**.

- `Play Persona 3 Dancing.exe` arranca el juego directamente con los ajustes guardados.
- Dentro del juego, **Insert** o **R3 + L2** abre el menú del port.

### Dónde se guarda todo

- Partidas, caché de shaders y registro: carpeta `user\` junto al launcher (consérvala al actualizar).
- Ajustes del juego: `p3d.ini`; ajustes del launcher: `%APPDATA%\p3d-launcher`.
- Registro de la última partida: `user\last_run.log`.

## Requisitos

- Windows 10/11 de 64 bits.
- Tarjeta gráfica con Vulkan 1.3 y controlador actualizado.

## Créditos

- [shadPS4](https://github.com/shadps4-emu/shadPS4): núcleo de video de PS4 a Vulkan.

## Licencia

GNU GPL v2 o posterior ([LICENSE](LICENSE)). Los componentes de terceros mantienen sus propias licencias.
