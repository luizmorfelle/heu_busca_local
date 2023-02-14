import busca_iterada
import primeira_melhora


def main():
    for i in range(10):
        primeira_melhora.main(i)
        busca_iterada.main(i)


if __name__ == '__main__':
    main()
