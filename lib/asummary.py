#!/usr/bin/env python

from argparse import ArgumentParser
import sys

from vsc.atools.int_ranges import (int_ranges2set, set2int_ranges,
                                   InvalidRangeSpecError)
from vsc.atools.log_parser import LogParser, InvalidLogEntryError
from vsc.atools.work_analysis import (compute_items_todo,
                                      MissingSourceError)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Produces summary information from log files')
    arg_parser.add_argument('--data', nargs='*',
                            help='CSV files to use')
    arg_parser.add_argument('-t', help='array ID range to consider')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--long', action='store_true',
                            help='In addition to the summary information, the job items in each category are also listed')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    arg_parser.add_argument('--no_sniffer', action='store_true',
                            help='do not use the sniffer for CSV dialect')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    if not options.log:
        msg = '### error: --log is a mandatory argument\n'
        sys.stderr.write(msg)
        sys.exit(1)
    try:
        todo, completed, failed = compute_items_todo(
            options.data, options.t, options.log, must_redo=False,
            sniff=options.sniff, no_sniffer=options.no_sniffer
        )
        if options.long:
            print('Summary:')
            print('  items completed: {0:d} ({1})'.format(len(completed), set2int_ranges(completed)))
            print('  items failed: {0:d} ({1})'.format(len(failed), set2int_ranges(failed)))
            print('  items to do: {0:d} ({1})'.format(len(todo), set2int_ranges(todo)))
        else:
            print('Summary:')
            print('  items completed: {0:d}'.format(len(completed)))
            print('  items failed: {0:d}'.format(len(failed)))
            print('  items to do: {0:d}'.format(len(todo)))
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidRangeSpecError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except MissingSourceError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidLogEntryError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
