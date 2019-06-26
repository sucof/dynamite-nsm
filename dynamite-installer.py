import sys
import argparse
import traceback

from installer import elasticsearch
from installer import utilities


def _parse_cmdline():
    parser = argparse.ArgumentParser(
        description='Install/Configure the Dynamite Analysis Framework.'
    )
    parser.add_argument('mode', metavar='mode', type=str, help='The install/configure mode. [install-elasticsearch]')
    return parser.parse_args()


def install_elasticsearch():
    if not utilities.is_root():
        sys.stderr.write('[-] This script must be run as root.\n')
        sys.exit(1)

    if utilities.get_memory_available_bytes() < 6 * (1000 ** 3):
        sys.stderr.write('[-] Dynamite ElasticSearch requires at-least 6GB to run currently available [{} GB]\n'.format(
            utilities.get_memory_available_bytes()/(1024 ** 3)
        ))
        sys.exit(1)
    try:
        es_installer = elasticsearch.ElasticInstaller()
        es_installer.download_java(stdout=True)
        es_installer.extract_java(stdout=True)
        es_installer.setup_java()
        utilities.create_dynamite_user('password')
        es_installer.download_elasticsearch(stdout=True)
        es_installer.extract_elasticsearch(stdout=True)
        es_installer.setup_elasticsearch(stdout=True)
    except Exception:
        sys.stderr.write('[-] A fatal error occurred while attempting to install ElasticSearch: ')
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    sys.stdout.write('[+] *** ElasticSearch installed successfully. ***\n')
    sys.exit(0)


if __name__ == '__main__':
    args = _parse_cmdline()
    if args.mode == 'install-elasticsearch':
        install_elasticsearch()