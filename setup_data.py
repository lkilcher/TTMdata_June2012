import process_data as proc
from main import pull, FILEINFO


if __name__ == '__main__':
    pull()
    proc.process_adv()
    proc.process_awac()
