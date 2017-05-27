import process_data as pd
from pull_data import main as pull


def process():
    pd.process_adv()
    pd.process_awac()


if __name__ == '__main__':
    pull()
    process()
