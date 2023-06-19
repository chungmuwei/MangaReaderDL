import argparse

def get_args():
    '''
    Parse the argument using argparse library and return the corresponding Namespace object
    '''
 
    parser = argparse.ArgumentParser(description='Download the manga on mangareader.to')
    parser.add_argument('url', type=str, nargs="?",  default=None, help='the url of the manga on mangareader.to')
    parser.add_argument('-d', '--dir', type=str, default=".", help='the path to save the downloaded manga')

    return parser.parse_args()