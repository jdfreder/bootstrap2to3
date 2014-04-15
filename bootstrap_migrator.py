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
re_less = re.compile('.*\\.less$|.*\\.css$')
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
    "container-fluid": "container",
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
replace_split_class = {
    'btn': ['btn', 'btn-default'],
    'label': ['label', 'label-default'],
    'accordion-group': ['panel', 'panel-default'],
}
warn_abouts = {
    'inline': 'If this is a radio or checkbox, replace ".inline" with ".checkbox-inline" or ".radio-inline".',
    'error': 'If this is a ".table.error", replace it with ".table.danger".\n\t".control-group.*" should be replaced with ".form-group.has-*".',
    'bar-.*?': '"bar-*" should be replaced with ".progress-bar-*".',
    'icon-.*?': '"icon-*" should be replaced with ".glyphicon .glyphicon-*".',
    'span.*?': '"span.*" should be replaced with ".col-md-*".',
    'offset.*?': '"offset.*" should be replaced with ".col-md-offset-*".',
    'success': '".control-group.*" should be replaced with ".form-group.has-*".',
    'warning': '".control-group.*" should be replaced with ".form-group.has-*".',
    '.hidden-desktop': 'Split into .hidden-md .hidden-lg',
    '.visible-desktop': 'Split into .visible-md .visible-lg',
    'form-actions': '"Form actions" removed; replaced by "N/A".',
    'form-search': '"Search form" removed; replaced by "N/A".',
    'control-group.info': '"Form group with info" removed; replaced by "N/A".',
    'input-mini': '"Fixed-width input sizes" removed; replaced by "Use .form-control and the grid systeminstead.".',
    'input-small': '"Fixed-width input sizes" removed; replaced by "Use .form-control and the grid systeminstead.".',
    'input-medium': '"Fixed-width input sizes" removed; replaced by "Use .form-control and the grid systeminstead.".',
    'input-large': '"Fixed-width input sizes" removed; replaced by "Use .form-control and the grid systeminstead.".',
    'input-xlarge': '"Fixed-width input sizes" removed; replaced by "Use .form-control and the grid systeminstead.".',
    'input-xxlarge': '"Fixed-width input sizes" removed; replaced by "Use .form-control and the grid systeminstead.".',
    'input-block-level': '"Block level form input" removed; replaced by "No direct equivalent, but forms controlsare similar.".',
    'btn-inverse': '"Inverse buttons" removed; replaced by "N/A".',
    'row-fluid': '"Fluid row" removed; replaced by ".row (no more fixed grid)".',
    'controls': '"Controls wrapper" removed; replaced by "N/A".',
    'controls-row': '"Controls row" removed; replaced by ".row or .form-group".',
    'navbar-inner': '"Navbar inner" removed; replaced by "N/A".',
    'divider-vertical': '"Navbar vertical dividers" removed; replaced by "N/A".',
    'dropdown-submenu': '"Dropdown submenu" removed; replaced by "N/A".',
    'tabs-left': '"Tab alignments" removed; replaced by "N/A".',
    'tabs-right': '"Tab alignments" removed; replaced by "N/A".',
    'tabs-below': '"Tab alignments" removed; replaced by "N/A".',
    'pill-content': '"Pill-based tabbable area" removed; replaced by ".tab-content".',
    'pill-pane': '"Pill-based tabbable area pane" removed; replaced by ".tab-pane".',
    'nav-header': '"Nav lists" removed; replaced by "No direct equivalent, but list groups and.panel-groups are similar.".',
    'help-inline': '"Inline help for form controls" removed; replaced by "No exact equivalent, but .help-block is similar.".',
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
    ('less', [(css_class, '.')]),
    ('js', [(html_class, ' '), (selector_class, '.')]),
    ('html', [(html_class, ' ')]),
    ('py', [(html_class, ' '), (selector_class, '.')]),
]
print 'Processing...'
for type_index, (type_name, regex_groups) in enumerate(file_types):
    files = eval('%sfiles' % type_name)
    for index, file_name in enumerate(files):

        # Perform quick replacements.
        for find, replace in quick_replacements.items():
            for regex, class_sep in [(re.compile(r.format(find)), rs[1]) for rs in regex_groups for r in rs[0]]:
                replacements += regex_sub_file(file_name, regex, r'\1' + replace + r'\3')

        # Perform split replacements.
        for find, replace in replace_split_class.items():
            for regex, class_sep in [(re.compile(r.format(find)), rs[1]) for rs in regex_groups for r in rs[0]]:
                replacements += regex_sub_file(file_name, regex, r'\1' + class_sep.join(replace) + r'\3')

        # Check for lines that we can't automatically upgrade and warn about them.
        for find, warn in warn_abouts.items():
            for regex, class_sep in [(re.compile(r.format(find)), rs[1]) for rs in regex_groups for r in rs[0]]:
                warnings +=  regex_warn_file(file_name, regex, warn)

        # Update progress bar with our current progress.
        fraction = 1./float(len(file_types))
        progress((float(index) / float(len(files))) * fraction + fraction * type_index)
print '\n    %d replacements made.' % replacements
print ''

with open('warnings.txt', 'w') as f:
    f.write('\n'.join(warnings))
print '%d warnings saved to "warnings.txt".' % len(warnings)