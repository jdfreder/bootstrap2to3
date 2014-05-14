bootstrap2to3
=============

## About

Script for migrating Bootstrap 2.x code to Bootstrap 3.x

Supports
- html
- js
- less
- py

**Make sure to backup your code before running this script on it!**

This script will automatically search your code and make necessary 
replacements to migrate your codebase to Bootstrap 3.x.  It will create a
`warnings.md` file in the cwd with all of the line numbers that you will need 
to update by hand along with *helpful* warning messages.

## Quickstart

- Configure `config.yml` (or a copy of it) to point to your project(s) directories.  The 
directories defined here get recursively traversed.  *Currently there is no way
to blacklist directories, this only behaves like a whitelist.*  
- Run `python migrate.py config.yml bootstrap2to3.json run` to upgrade the 
directories (optionally replace `config.yml` with the name of your config file).  

### Advanced usage

This tool supports two commands, `run` and `dump`.  `run` executes a migration
file on the contents of a directory.  `dump` creates a template migration file
for a directory.

You can also use this tool as a general python/web refactoring tool.  To export
the list of CSS and LESS variables used by your program, run 
`python migrate.py config.yml output.json dump`.  This will create/overwrite
`output.json` with dictionaries that you can edit by hand.  You can change 
`output.json` to any file name you want.

After editing the outputed file with your refactoring data, you can refactor 
your program by running `python migrate.py config.yml output.json run` 
(you'll need to replace `output.json` with the name of the outputed file).

## Algorithm
This program attempts to make the replacements suggested at http://getbootstrap.com/migration/ .  It also attempts to warn for the removed CSS classes.

### Additionally, the following LESS variables will be handled.  

Change:  
- `@bodyBackground` to `@body-bg`  
- `@textColor` to `@text-color`  
- `@linkColor` to `@link-color`  
- `@linkColorHover` to `@link-hover-color`  
- `@blue` to `@brand-primary`  
- `@green` to `@brand-success`  
- `@red` to `@brand-danger`  
- `@orange` to `@brand-warning`  
- `@gridColumns` to `@grid-columns`  
- `@gridGutterWidth` to `@grid-gutter-width`  
- `@sansFontFamily` to `@font-family-sans-serif `  
- `@serifFontFamily` to `@font-family-serif`  
- `@monoFontFamily` to `@font-family-monospace`  
- `@baseFontSize` to `@font-size-base`  
- `@baseFontFamily` to `@font-family-base `  
- `@baseLineHeight` to `@line-height-base`  
- `@headingsFontFamily` to `@headings-font-family`  
- `@headingsFontWeight` to `@headings-font-weight`  
- `@headingsColor` to `@headings-color`  
- `@fontSizeLarge` to `@font-size-large`  
- `@fontSizeSmall` to `@font-size-small`  
- `@paddingLarge` to `@padding-large-vertical @padding-large-horizontal`  
- `@paddingSmall` to `@padding-small-vertical @padding-small-horizontal`  
- `@paddingMini` to `@padding-xs-vertical @padding-xs-horizontal`  
- `@baseBorderRadius` to `@border-radius-base`  
- `@borderRadiusLarge` to `@border-radius-large`  
- `@borderRadiusSmall` to `@border-radius-small`  
- `@tableBackground` to `@table-bg`  
- `@tableBackgroundAccent` to `@table-bg-accent`  
- `@tableBackgroundHover` to `@table-bg-hover`  
- `@placeholderText` to `@input-color-placeholder`  
- `@inputBackground` to `@input-bg`  
- `@inputBorder` to `@input-border`  
- `@inputBorderRadius` to `@input-border-radius`  
- `@inputDisabledBackground` to `@input-bg-disabled`  
- `@navbarHeight` to `@navbar-height`  
- `@navbarBackground` to `@navbar-default-bg`  
- `@navbarText` to `@navbar-default-color`  
- `@navbarLinkColor` to `@navbar-default-link-color`  
- `@navbarLinkColorHover` to `@navbar-default-link-hover-color`  
- `@navbarLinkColorActive` to `@navbar-default-link-active-color`  
- `@navbarLinkBackgroundHover` to `@navbar-default-link-hover-bg`  
- `@navbarLinkBackgroundActive` to `@navbar-default-link-active-bg`  
- `@dropdownBackground` to `@dropdown-bg`  
- `@dropdownBorder` to `@dropdown-border`  
- `@dropdownLinkColor` to `@dropdown-link-color`  
- `@dropdownLinkColorHover` to `@dropdown-link-hover-color`  
- `@dropdownLinkBackgroundHover` to `@dropdown-link-hover-bg`  

Warn about removal:  
- `@yellow`  
- `@pink`  
- `@purple`  
- `@iconSpritePath`  
- `@iconWhiteSpritePath`  
- `@gridColumnWidth`  
- `@gridColumnWidth1200`  
- `@gridGutterWidth1200`  
- `@gridColumnWidth768`  
- `@gridGutterWidth768`  
- `@altFontFamily`  
- `@fontSizeMini`  
- `@heroUnitBackground`  
- `@heroUnitHeadingColor`  
- `@heroUnitLeadColor`  
- `@tableBorder`  
- `@formActionsBackground`  
- `@btnPrimaryBackground`  
- `@btnPrimaryBackgroundHighlight`  
- `@warningText`  
- `@warningBackground`  
- `@errorText`  
- `@errorBackground`  
- `@successText`  
- `@successBackground`  
- `@infoText`  
- `@infoBackground`  
- `@navbarBackgroundHighlight`  
- `@navbarBrandColor`  
- `@navbarSearchBackground`  
- `@navbarSearchBackgroundFocus`  
- `@navbarSearchBorder`  
- `@navbarSearchPlaceholderColor`  
- `@navbarCollapseWidth`  
- `@navbarCollapseDesktopWidth`  
