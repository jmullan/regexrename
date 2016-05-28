"""Rename things using regexes."""
#
#  Based on a script developed by Robin Barker (Robin.Barker@npl.co.uk),
#  from Larry Wall's original script eg/rename from the perl source.
#
#  This script is free software; you can redistribute it and/or modify it
#  under the same terms as Perl itself.

import os
import os.path
import re
import shutil
import sys
from optparse import OptionParser

__version__ = '0.1'


def main():
    usage = "usage: %prog [options] pattern replacement filenames"

    parser = OptionParser(usage)

    parser.add_option(
        '-v', '--verbose', dest='verbose',
        action='store_true', default=False,
        help='verbose is more verbose')

    parser.add_option(
        '-n', '--no-act', dest='no_act',
        action='store_true', default=False,
        help='No Action: show what files would have been renamed.')

    parser.add_option(
        '-f', '--force', dest='force',
        action='store_true', default=False,
        help='Force: overwrite existing files.')

    parser.add_option(
        '-p', '--parents', dest='parents',
        action='store_true', default=False,
        help='Create missing target parent directories')

    parser.add_option(
        '-c', '--counter', dest='counter',
        action='store_true', default=False,
        help='Add a parentheticized number to resolve conflicts. (1)')

    parser.add_option(
        '--flags', dest='flags', default='',
        help="Python regex flags")

    (options, args) = parser.parse_args()

    verbose = 0
    if options.verbose:
        verbose += 1

    if options.no_act:
        verbose += 1

    if len(args) < 3:
        sys.stderr.write(
            "You must supply a pattern, a replacement"
            " and at least one filename\n")
        exit(1)

    flag_string = options.flags
    flags = []

    flag_mappings = {
        'I': re.I,
        'L': re.L,
        'M': re.M,
        'S': re.S,
        'U': re.U,
        'S': re.X,
    }

    for char in flag_string:
        char = char.upper()
        if char in flag_mappings:
            flags.append(flag_mappings[char])

    pattern = args[0]
    replacement = args[1]

    if verbose:
        sys.stdout.write('%s -> %s\n' % (pattern, replacement))

    filenames = args[2:]

    regex = re.compile(pattern, *flags)

    for from_filename in filenames:

        if not os.path.exists(from_filename):
            sys.stderr.write("%s does not exist\n" % from_filename)

        to_filename = re.sub(regex, replacement, from_filename)
        if from_filename == to_filename:
            if verbose:
                sys.stdout.write('No change for %s\n' % from_filename)
            continue

        if os.path.exists(to_filename) and not options.force:
            if options.counter:
                base_filename, file_extension = os.path.splitext(to_filename)
                matches = re.match(r'(.*)\(([0-9]+)\)\s*$', base_filename)
                counter = 1
                if matches:
                    base_filename = matches.group(1)
                    counter = int(matches.group(2))
                to_filename = '%s (%s)%s' % (
                    base_filename, counter, file_extension)
                while os.path.exists(to_filename):
                    counter += 1
                    to_filename = '%s (%s)' % (base_filename, counter)
            else:
                sys.stderr.write(
                    "%s not renamed: %s already exists\n" % (
                        from_filename, to_filename))
        if options.no_act:
            sys.stdout.write('Dry run: renamed %s to %s\n' % (
                from_filename, to_filename))
        else:
            parent_directory = os.path.dirname(to_filename)
            if parent_directory and not os.path.exists(parent_directory):
                if options.parents:
                    try:
                        os.mkdirs(parent_directory)
                    except os.error as ex:
                        sys.stderr.write('Could not create parent dir %s\n' % (
                            parent_directory))
                        continue
                else:
                    sys.stderr.write(
                        '%s not moved to %s:'
                        ' parent directory %s does not exist (use -p)\n' % (
                            from_filename, to_filename, parent_directory))
                    continue

            if parent_directory and not os.path.isdir(parent_directory):
                sys.stderr.write(
                    '%s not moved to %s:'
                    ' parent directory %s is not a direcotry (use -p)\n' % (
                        from_filename, to_filename, parent_directory))
                continue

            try:
                if verbose:
                    sys.stdout.write('Moving %s to %s\n' % (
                        from_filename, to_filename))
                shutil.move(from_filename, to_filename)
            except Exception as ex:
                sys.stderr.write(
                    "%s not renamed to %s: %s\n" % (
                        from_filename, to_filename, ex))


if __name__ == "__main__":
    main()
