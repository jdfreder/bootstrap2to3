# Copyrighted, see License.txt for more information.
#-------------------------------------------------------------------------------
# Coonfiguration
#-------------------------------------------------------------------------------

# Everything but the static/componets directory should be listed.  Algorithm is
# recursive, no need to list sub directories if search is meant to be all 
# inclusive.
app_dirs = [
    '~/ipython/IPython/html/auth',
    '~/ipython/IPython/html/base',
    '~/ipython/IPython/html/nbconvert',
    '~/ipython/IPython/html/notebook',
    '~/ipython/IPython/html/services',
    '~/ipython/IPython/html/templates',
    '~/ipython/IPython/html/tests',
    '~/ipython/IPython/html/tree',
    '~/ipython/IPython/html/widgets',
    '~/ipython/IPython/html/static/auth',
    '~/ipython/IPython/html/static/base',
    '~/ipython/IPython/html/static/custom',
    '~/ipython/IPython/html/static/dateformat',
    '~/ipython/IPython/html/static/notebook',
    '~/ipython/IPython/html/static/services',
    '~/ipython/IPython/html/static/style',
    '~/ipython/IPython/html/static/tree',
    '~/ipython/IPython/html/static/widgets',
]

#-------------------------------------------------------------------------------
# Do not edit below this line
#-------------------------------------------------------------------------------

import re
import os
import sys

re_html = re.compile('.*\\.html$|.*\\.htm$')
re_js = re.compile('.*\\.js$')
re_less = re.compile('.*\\.less$')
re_py = re.compile('.*\\.py$')

app_dirs = [os.path.expanduser(p) for p in app_dirs]
get_files = lambda regex: [os.path.join(dirpath, f)
    for app_dir in app_dirs
    for dirpath, dirnames, files in os.walk(app_dir)
    for f in files if regex.match(f)]
htmlfiles = get_files(re_html)
jsfiles = get_files(re_js)
lessfiles = get_files(re_less)
pyfiles = get_files(re_py)

css_class = [r"([\.@])({0})([ {{\(\.#:])"]
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

quick_replacements = {
    "row-fluid": "row",
    "brand": "navbar-brand",
    "nav-collapse": "navbar-collapse",
    "nav-toggle": "navbar-toggle",
    "btn-navbar": "navbar-btn",
    "hero-unit": "jumbotron",
    "btn-mini": "btn-xs",
    "btn-small": "btn-sm",
    "btn-large": "btn-lg",
    "alert-error": "alert-danger",
    "visible-phone": "visible-xs",
    "visible-tablet": "visible-sm",
    "hidden-phone": "hidden-xs",
    "hidden-tablet": "hidden-sm",
    "input-block-level": "form-control",
    "control-group": "form-group",
    "input-prepend": "input-group",
    "input-append": "input-group",
    "add-on": "input-group-addon",
    "img-polaroid": "img-thumbnail",
    "unstyled": "list-unstyled",
    "inline": "list-inline",
    "muted": "text-muted",
    "label-important": "label-danger",
    "text-error": "text-danger",
    "bar": "progress-bar",
    "accordion": "panel-group",
    "accordion-heading": "panel-heading",
    "accordion-body": "panel-collapse",
    "accordion-inner": "panel-body",
    "checkbox.inline": "checkbox-inline",
    "radio.inline": "radio-inline",
}
warn_abouts = {
    'inline': 'If this is a radio or checkbox, replace ".inline" with ".checkbox-inline" or ".radio-inline".',
    'accordion-group': '".accordion-group" should be replace with ".panel.panel-default".',
    'error': 'If this is a ".table.error", replace it with ".table.danger".\n\t".control-group.*" should be replaced with ".form-group.has-*".',
    'label': '".label" should be replace with ".label.label-default".',
    'btn': '".btn" should be replace with ".btn.btn-default".',
    'bar-.*?': '"bar-*" should be replaced with ".progress-bar-*".',
    'icon-.*?': '"icon-*" should be replaced with ".glyphicon .glyphicon-*".',
    'span.*?': '"span.*" should be replaced with ".col-md-*".',
    'offset.*?': '"offset.*" should be replaced with ".col-md-offset-*".',
    'success': '".control-group.*" should be replaced with ".form-group.has-*".',
    'warning': '".control-group.*" should be replaced with ".form-group.has-*".',
    '.hidden-desktop': 'Split into .hidden-md .hidden-lg',
    '.visible-desktop': 'Split into .visible-md .visible-lg',
}

def progress(percent):
    print '\r[' + ('#' * int(percent * 50)) + (' ' * int((1-percent) * 50)) + ']',
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
            warnings.append('%s line #%d: %s' % (filename, (index + 1), warn))
    return warnings

replacements = 0
warnings = []
file_types = [
    ('less', [css_class]),
    ('js', [html_class, selector_class]),
    ('html', [html_class]),
    ('py', [html_class, selector_class]),
]
print 'Processing...'
for type_index, (type_name, regex_groups) in enumerate(file_types):
    files = eval('%sfiles' % type_name)
    for index, file_name in enumerate(files):

        # Perform quick replacements.
        for find, replace in quick_replacements.items():
            for regex in [re.compile(r.format(find)) for rs in regex_groups for r in rs]:
                replacements += regex_sub_file(file_name, regex, r'\1' + replace + r'\3')

        # Check for lines that we can't automatically upgrade and warn about them.
        for find, warn in warn_abouts.items():
            for regex in [re.compile(r.format(find)) for rs in regex_groups for r in rs]:
                warnings +=  regex_warn_file(file_name, regex, warn)

        # Update progress bar with our current progress.
        progress((float(index) / float(len(files))) * 0.33 + 0.33 * type_index)
print '\n    %d replacements made.' % replacements
print ''

with open('warnings.txt', 'w') as f:
    f.write('\n'.join(warnings))
print '%d warnings saved to "warnings.txt".' % len(warnings)