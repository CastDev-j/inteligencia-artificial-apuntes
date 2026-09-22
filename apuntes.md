# Apuntes RISC-V Parte 1

Resumen de "RISC-V Assembly Language Programming Using the ESP32-C3 and QEMU" (Warren Gay).

1. RISC-V es una arquitectura (ISA) libre y de código abierto: cualquier fabricante puede usarla sin licencias caras ni restrictivas.
2. Sus raíces están en los proyectos RISC de Hennessy (Stanford) y Patterson (Berkeley) en los años 80, como alternativa a los CISC.
3. Es una ISA limpia y simple frente a otras (ej. x86), con menos cosas que aprender y provisión para extensiones de fabricante.
4. Se practica en dos plataformas: el microcontrolador ESP32-C3 (RISC-V de 32 bits) y el emulador QEMU (RISC-V de 64 bits corriendo Fedora Linux).
5. Cuidado: el ESP32-C3 usa CPU RISC-V; otros ESP32 (ESP32 original, S2, S3) usan CPU Xtensa y NO son RISC-V.
6. Para el ESP32-C3 se instala el framework ESP-IDF, que compila, flashea y monitorea el dispositivo (`idf.py build`, `idf.py flash`, `idf.py monitor`).
7. QEMU emula RISC-V en 64 bits con `qemu-system-riscv64`; requiere unos 20 GB de disco y descargar una imagen de Fedora/RISC-V.
8. XLEN define el ancho de los registros: 32 bits en el ESP32-C3, 64 bits en QEMU.
9. La memoria RISC-V es little-endian y direccionable por bytes (una palabra de 4 bytes guarda el byte menos significativo primero).
10. El PC (program counter) apunta a la siguiente instrucción; las instrucciones base tienen 32 bits y deben estar alineadas.
11. Hay 32 registros de propósito general x0–x31, con nombres ABI que se usan por convención: ra, sp, gp, tp, t0–t6, s0–s11, a0–a7.
12. x0 (zero) es especial y está cableado a cero: como fuente siempre da 0 y como destino descarta el resultado.
13. RISC-V NO tiene flag bits (Z, C, N...): eso simplifica el hardware y evita estados que salvar/restaurar entre llamadas.
14. Subconjuntos base: RV32I, RV64I, RV128I y RV32E (este último reduce a 16 registros para sistemas embebidos de bajo consumo).
15. Extensiones estándar: M (multiplicación/división), A (atómicas), F/D (punto flotante simple/doble), C (instrucciones comprimidas de 16 bits), V (vector).
16. ESP32-C3 soporta RV32IMC (base 32 bits + multiplicación/división + comprimidas); QEMU soporta rv64imafdcsu (verificable en `/proc/cpuinfo`).
17. Niveles de privilegio: Machine (m), Supervisor (s) y User (u). El ESP32-C3 corre en modo máquina; Fedora/QEMU usa modo usuario.
18. Modelo de memoria: en RV32 (ILP32) int, long y punteros son de 32 bits; en RV64 (LP64) long y punteros son de 64 bits pero int sigue en 32.
19. Formato de ensamblador: `label: opcode operandos # comentario`; pseudo-ops útiles: `.global` (símbolo externo) y `.text` (sección de código).
20. Primer ejemplo: función `add3` en ensamblado llamada desde C; los argumentos llegan en a0–a7, el resultado vuelve en a0 y `ret` regresa usando la dirección guardada en ra (x1).