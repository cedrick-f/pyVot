#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys, os
import globdef

## Remove the build folder, a bit slower but ensures that build contains the latest
import shutil
shutil.rmtree("build", ignore_errors=True)

#if 'bdist_msi' in sys.argv:
#    sys.argv += ['--install-script', 'install.py']


# Inculsion des fichiers de données
#################################################################################################
includefiles = []
includefiles.extend([#('Microsoft.VC90.CRT', "Microsoft.VC90.CRT"),
                     ('Images', "Images"),
                     'LICENSE.txt',
                     ('../Aide', "../Aide"),
                     ('../Donnees', "../Donnees"),
                     ('../Exemples', "../Exemples"),
                     ])

if sys.platform == "win32":
    includefiles.extend([('C:\Users\Cedrick\Documents\Developp\Microsoft.VC90.CRT', "Microsoft.VC90.CRT"),])


# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'build_exe': 'build/bin',
                     "packages": ["os"], 
                     "excludes": ["tkinter",
                                  '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
                                  'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                                  'Tkconstants', 'pydoc', 'doctest', 'test', 'sqlite3',
                                  "PyQt4", "PyQt4.QtGui","PyQt4._qt",
                                  "matplotlib", "numpy", "scipy"
                                  ],
                     "include_files": includefiles,
                     "bin_path_includes": binpathincludes,
                     'bin_excludes' : ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl85.dll',
                                              'tk85.dll', "UxTheme.dll", "mswsock.dll", "POWRPROF.dll",
                                              "QtCore4.dll", "QtGui4.dll" ]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"



name = u"pyVot"
version = globdef.VERSION
author = u"Cédrick FAURY"
author_email = "cedrick.faury@ac-clermont.fr"
description = u"pyVot"
url = "https://github.com/cedrick-f/pyVot"
long_description = u"Construction et Analyse de liaisons Pivot avec roulements"
license = "GPL"

if sys.platform == "win32":
    from cx_Freeze import setup, Executable
    cible = Executable( script = "pyvot.py",
                        targetName="pyVot.exe",
                        base = base,
                        compress = True,
                        icon = os.path.join("", 'logo32b.ico'),
                        initScript = None,
                        copyDependentFiles = True,
                        appendScriptToExe = False,
                        appendScriptToLibrary = False
                        )


    setup(  name = name,
            version = version,
            author = author,
            author_email = author_email,
            url = url,
            description = description,
            long_description = long_description,
            license = license,
            options = {"build_exe": build_exe_options},
    #        include-msvcr = True,
            executables = [cible])

else:
    from setuptools import setup, find_packages
    print "PACKAGES", find_packages()
    setup(  name = name,
            version = version,
            author = author,
            author_email = author_email,
            url = url,
            description = description,
            long_description = long_description,
            license = license,
            scripts=["pyvot.py"],
            package_dir = {'':''},
            packages = find_packages(),
            install_requires=['python-wxgtk3.0',
                              'python-reportlab']
            )
    



# 
#     
# cible = Executable(
#     script = "PyVot.py",
#     base = base,
#     compress = True,
#     icon = 'logo32b.ico',
#     initScript = None,
#     copyDependentFiles = True,
#     appendScriptToExe = False,
#     appendScriptToLibrary = False
#     )
# 
# 
# setup(  name = "PyVot",
#         version = "6.1",
#         author = "Cedrick FAURY",
#         description = "Construction et Analyse de liaisons Pivot avec roulements",
#         options = {"build_exe": build_exe_options},
# #        include-msvcr = True,
#         executables = [cible])
# 
# 


