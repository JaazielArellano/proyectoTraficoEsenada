import extractorx
import extractorx_tcapi


def main():
    print("Ejecutando extractorx...")
    extractorx.main()
    print("extractorx terminado.\n")

    print("Ejecutando extractorx_tcapi...")
    extractorx_tcapi.main()
    print("extractorx_tcapi terminado.\n")

    print("Todo terminado.")


if __name__ == "__main__":
    main()