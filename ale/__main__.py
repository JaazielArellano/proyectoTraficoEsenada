import sys

from .limpieza import limpiar_archivo


def main() -> None:
    if len(sys.argv) < 3:
        print("uso: python -m cleaner_lib ENTRADA SALIDA [ERRORES]")
        sys.exit(1)
    errores = sys.argv[3] if len(sys.argv) > 3 else None
    resumen = limpiar_archivo(sys.argv[1], sys.argv[2], errores)
    print(f"Leidos: {resumen['leidos']} | Limpios: {resumen['limpios']} | Con error: {resumen['errores']}")


if __name__ == "__main__":
    main()
