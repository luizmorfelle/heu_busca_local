import busca_iterada
import primeira_melhora


def main():
    i=0
    for i in range(10):
        primeira_melhora.main()
        busca_iterada.main()


if __name__ == '__main__':
    main()
