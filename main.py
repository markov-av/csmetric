import sys
import argparse
from pprint import pprint


from demo_loader import Demo
from executor import MetricExecutor


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-m-list', nargs='+', default=[], help='list of metrics')
    parser.add_argument('-d', help='path to dem file')
    args = parser.parse_args()

    if not args.d:
        print('Demo file was not specified')
        sys.exit()

    data = Demo(path=args.d)
    executor = MetricExecutor(args.m_list, data=data)
    executor.execute()
    pprint(executor.result)
