#!/usr/bin/env python

from argparse import ArgumentParser
import sys

from vsc.atools.int_ranges import (int_ranges2set, set2int_ranges,
                                   InvalidRangeSpecError)
from vsc.atools.log_parser import LogParser, InvalidLogEntryError
from vsc.atools.work_analysis import (compute_items_todo,
                                      MissingSourceError)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Compute the array ID range in a format suitable for the array job '
                                            'submission commands. Combine options at will.')
    arg_parser.add_argument('--data', nargs='*',
                            help='CSV files to use')
    arg_parser.add_argument('-t', help='array ID range to consider')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--completed', action='store_true',
                            help='include completed items')
    arg_parser.add_argument('--failed', action='store_true',
                            help='include completed items')
    arg_parser.add_argument('--todo', action='store_true',
                            help='include missing items')
    arg_parser.add_argument('--redo', action='store_true',
                            help='include failed and missing items, equivalent to --failed --todo')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    arg_parser.add_argument('--no_sniffer', action='store_true',
                            help='do not use the sniffer for CSV dialect')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    if not options.completed and not options.failed and not options.todo and not options.redo:
        options.todo = True
    options.failed = options.failed or options.redo
    options.todo   = options.todo   or options.redo
    if (options.completed or options.failed) and not options.log:
        msg = '### error: --completed and --failed require log files\n'
        sys.stderr.write(msg)
        sys.exit(1)    
    try:
        todo, completed, failed = compute_items_todo(
            options.data, options.t, options.log, must_redo=False,
            sniff=options.sniff, no_sniffer=options.no_sniffer
        )
        elements = set()
        if options.completed:
            elements |= completed
        if options.failed:
            elements |= failed
        if options.todo:
            elements |= todo
        print(set2int_ranges(elements))
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
