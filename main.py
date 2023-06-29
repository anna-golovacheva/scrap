from utils import parse, save_data_to_file


def main():
    result = parse()
    save_data_to_file(result)


if __name__ == '__main__':
    main()
