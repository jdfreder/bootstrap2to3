bootstrap2to3
=============

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
