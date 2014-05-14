#!/usr/bin/python
# Copyrighted, see License.txt for more information.
from __future__ import print_function
import yaml
import re
import os
import sys
import json

config_filename = sys.argv[1]
migration_filename = sys.argv[2]
command = sys.argv[3].lower()
if command not in ['dump', 'run']:
    print('The third argument is the `Command` and must be "dump" or "run".')
print('Loading config from {0} and using {1} as migration instructions.'.format(config_filename, migration_filename))


#-------------------------------------------------------------------------------
# Load configuration
#-------------------------------------------------------------------------------
with open(config_filename, 'r') as f:
    config = yaml.load(f.read())

# What should be processed for replacements?
process_css = config.get('process css', True)
process_js = config.get('process js', True)
process_html = config.get('process html', True)
process_py = config.get('process py', True)
process_less_css = config.get('process less css', True)
process_less_variables = config.get('process less variables', True)

# Everything but the static/componets directory should be listed.  Algorithm is
# recursive, no need to list sub directories if search is meant to be all 
# inclusive.
app_dirs = config.get('directories', [])


#-------------------------------------------------------------------------------
# Run
#-------------------------------------------------------------------------------
re_html = re.compile('.*\\.html$|.*\\.htm$')
re_js = re.compile('.*\\.js$')
re_less = re.compile('.*\\.less$')
re_css = re.compile('.*\\.css$')
re_py = re.compile('.*\\.py$')

app_dirs = [os.path.expanduser(p) for p in app_dirs]
get_files = lambda regex: [os.path.join(dirpath, f)
    for app_dir in app_dirs
    for dirpath, dirnames, files in os.walk(app_dir)
    for f in files if regex.match(f)]
htmlfiles = get_files(re_html)
cssfiles = get_files(re_css)
jsfiles = get_files(re_js)
lessfiles = get_files(re_less)
pyfiles = get_files(re_py)

css_less_var_name = r'[a-zA-Z][a-zA-Z0-9\_\-]*?'
css_class = [r"([\.@])({0})([\s{{\(\.#:])"]
less_class = ['(@)({0})([:;\\)\\s,])']
html_class = [
    "(\".*? )({0})( .*?\")", 
    "(\".*? )({0})(\")", 
    "(\")({0})( .*?\")", 
    "(\")({0})(\")", 
    "('.*? )({0})(')", 
    "(')({0})( .*?')", 
    "(')({0})(')", 
    "('.*? )({0})( .*?')", 
]
selector_class = ["([\"].*?\\.)({0})([ \\.#:\"])", "('.*?\\.)({0})([ \\.#:'])"]

if os.path.isfile(migration_filename):
    with open(migration_filename, 'r') as f:
        migration = json.load(f)
else:
    migration = {}
replace_css = migration.get('replace_css', {})
replace_css_split_class = migration.get('replace_css_split_class', {})
warn_abouts = migration.get('warn_abouts', {})
replace_less = migration.get('replace_less', {})
removed_less = migration.get('removed_less', [])

def progress(percent):
    print('\r[' + ('#' * int(percent * 50)) + (' ' * int((1-percent) * 50)) + ']', end='')
    sys.stdout.flush()
def regex_sub_file(filename, regex, repl):
    with open(filename, 'r') as f:
        contents = f.read()
    (contents, count) = regex.subn(repl, contents)
    with open(filename, 'w') as f:
        f.write(contents)
    return count
def regex_warn_file(filename, regex, warn):
    with open(filename, 'r') as f:
        contents = f.read()
    warnings = []
    for index, line in enumerate(contents.split('\n')):
        results = regex.findall(line)
        if results and len(results) > 0:
            warnings.append(' - [ ] %s line %d: %s' % (filename, (index + 1), warn.replace('*', '\\*')))
    return warnings
def regex_find_file(filename, regex):
    with open(filename, 'r') as f:
        contents = f.read()
    result_list = []
    for index, line in enumerate(contents.split('\n')):
        results = regex.findall(line)
        if results and len(results) > 0:
            for result in results:
                result_list.append(result[1])
    return result_list

process_less = process_less_css or process_less_variables
replacements = 0
warnings = []
file_types = []
if process_css: file_types.append(('css', [(css_class, '.')]))
if process_less: file_types.append(('less', [(css_class, '.')]))

# JS, HTML, and Py are only supported for the 'run' command.
if command == 'run':
    if process_js: file_types.append(('js', [(html_class, ' '), (selector_class, '.')]))
    if process_html: file_types.append(('html', [(html_class, ' ')]))
    if process_py: file_types.append(('py', [(html_class, ' '), (selector_class, '.')]))

if command == 'dump':
    if os.path.isfile(migration_filename):
        if raw_input('Are you sure you want to replace the existing "%s"? (y/[n])').lower() != 'y':
            exit()

print('Processing...')
dumped_css = []
dumped_less = []
for type_index, (type_name, regex_groups) in enumerate(file_types):
    files = eval('%sfiles' % type_name)
    for index, file_name in enumerate(files):
        # If this is not less or it is less that should be processed, process it here.
        if type_name != 'less' or process_less_css:
            if command == 'run':
                # Perform quick replacements.
                for find, replace in replace_css.items():
                    for regex, class_sep in [(re.compile(r.format(find)), rs[1]) for rs in regex_groups for r in rs[0]]:
                        replacements += regex_sub_file(file_name, regex, r'\1' + replace + r'\3')

                # Perform split replacements.
                for find, replace in replace_css_split_class.items():
                    for regex, class_sep in [(re.compile(r.format(find)), rs[1]) for rs in regex_groups for r in rs[0]]:
                        replacements += regex_sub_file(file_name, regex, r'\1' + class_sep.join(replace) + r'\3')

                # Check for lines that we can't automatically upgrade and warn about them.
                for find, warn in warn_abouts.items():
                    for regex, class_sep in [(re.compile(r.format(find)), rs[1]) for rs in regex_groups for r in rs[0]]:
                        warnings += regex_warn_file(file_name, regex, warn)
            elif command == 'dump':
                for regex, class_sep in [(re.compile(r.format(css_less_var_name)), rs[1]) for rs in regex_groups for r in rs[0]]:
                    dumped_css += regex_find_file(file_name, regex)

        # If this is LESS, perform LESS specific replacements.
        if type_name == 'less' and process_less_variables:
            if command == 'run':
                for find, replace in replace_less.items():
                    for regex in [re.compile(r.format(find)) for r in less_class]:
                        if isinstance(replace, (tuple, list)):
                            warnings += regex_warn_file(file_name, regex, '"@%s" should be replaced by ["@%s"]' % (find, '", "@'.join(replace)))
                        else:
                            replacements += regex_sub_file(file_name, regex, r'\1' + replace + r'\3')
                for find in removed_less:
                    for regex in [re.compile(r.format(find)) for r in less_class]:
                        warnings += regex_warn_file(file_name, regex, '"@%s" was removed from Bootstrap3.' % find)
            elif command == 'dump':
                for regex in [re.compile(r.format(css_less_var_name)) for r in less_class]:
                    dumped_less += regex_find_file(file_name, regex)

        # Update progress bar with our current progress.
        fraction = 1./float(len(file_types))
        progress((float(index) / float(len(files))) * fraction + fraction * type_index)

if command == 'run':
    print('\n    %d replacements made.' % replacements)
    print('')

    with open('warnings.md', 'w') as f:
        f.write('\n'.join(warnings))
    print('%d warnings saved to "warnings.md".' % len(warnings))
elif command == 'dump':
    migration = {
        'replace_css': {match:match for match in sorted(set(dumped_css))}, 
        'replace_less': {match:match for match in sorted(set(dumped_less))}, 
    }
    with open(migration_filename, 'w') as f:
        json.dump(migration, f, indent=4)
    print('\n\nContents exported to "%s"' % migration_filename)
