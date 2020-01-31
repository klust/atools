#!/usr/bin/env python

from argparse import ArgumentParser
import sys

from vsc.atools.int_ranges import (int_ranges2set, set2int_ranges,
                                   InvalidRangeSpecError)
from vsc.atools.log_parser import LogParser, InvalidLogEntryError
from vsc.atools.work_analysis import (compute_items_todo,
                                      MissingSourceError)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Compute the array ID range')
    arg_parser.add_argument('--data', nargs='*',
                            help='CSV files to use')
    arg_parser.add_argument('-t', help='array ID range to consider')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--redo', action='store_true',
                            help='redo failed items instead of incomplete/missing items')
    arg_parser.add_argument('--completed', action='store_true',
                            help='list completed items in a format suitable for areduce -t')
    arg_parser.add_argument('--summary', action='store_true',
                            help='print a summary of a job that is '
                                 'running or completed')
    arg_parser.add_argument('--list_failed', action='store_true',
                            help='list failed jobs when summarizing')
    arg_parser.add_argument('--list_completed', action='store_true',
                            help='list completed jobs when summarizing')
    arg_parser.add_argument('--list_todo', action='store_true',
                            help='list items to do when summarizing')
    arg_parser.add_argument('--long_summary', action='store_true',
                            help='equivalent to --summary --list_completed '
                                 '--list_failed --list_todo')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    arg_parser.add_argument('--no_sniffer', action='store_true',
                            help='do not use the sniffer for CSV dialect')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    options.list_completed = options.list_completed or options.long_summary
    options.list_failed = options.list_failed or options.long_summary
    options.list_todo = options.list_todo or options.long_summary
    options.summary = options.summary or options.list_completed \
                      or options.list_failed or options.list_todo
    if options.completed and not options.log:
        msg = '### error: --completed requires log files\n'
        sys.stderr.write(msg)
        sys.exit(1)    
    if options.summary and not options.log:
        msg = '### error: summary information (--summary, --long_summary, --list_completed, --list_failed and/or --list_dodo) requires log files\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if options.summary and options.completed:
        msg = '### warning: --completed has no effect when summary information is generated\n'
        sys.stderr.write(msg)
    try:
        todo, completed, failed = compute_items_todo(
            options.data, options.t, options.log, must_redo=options.redo,
            sniff=options.sniff, no_sniffer=options.no_sniffer
        )
        if options.summary:
            print('Summary:')
            print('  items completed: {0:d}'.format(len(completed)))
            print('  items failed: {0:d}'.format(len(failed)))
            print('  items to do: {0:d}'.format(len(todo)))
            if options.list_completed:
                print('completed items list: {0}'.format(set2int_ranges(completed)))
            if options.list_failed:
                print('failed items list: {0}'.format(set2int_ranges(failed)))
            if options.list_todo:
                print('to do items list: {0}'.format(set2int_ranges(todo)))
        elif options.completed:
            print(set2int_ranges(completed))
        else:
            print(set2int_ranges(todo))
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
