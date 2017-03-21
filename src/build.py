# -*- coding: ISO-8859-1 -*-

#    This file is part of PyVot
#   
#    Copyright (C) 2001-2006 Thomas Paviot
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from distutils.core import setup
import py2exe
#import glob

from distutils.filelist import findall
##import os

#from py2exe.build_exe import py2exe as BuildExe
#import os,sys

##def TixInfo():
##    import Tkinter
##    import _tkinter
##
##    tk=_tkinter.create()
##
##    tcl_version=_tkinter.TCL_VERSION
##    tk_version=_tkinter.TK_VERSION
##    tix_version=tk.call("package","version","Tix")
##
##    tcl_dir=tk.call("info","library")
##
##    del tk, _tkinter, Tkinter
##
##    return (tcl_version,tk_version,tix_version,tcl_dir)
##
##class myPy2Exe(BuildExe):
##
##    def plat_finalize(self, modules, py_files, extensions, dlls):
##        BuildExe.plat_finalize(self, modules, py_files, extensions, dlls)
##
##        if "Tix" in modules:
##            # Tix adjustments
##            tcl_version,tk_version,tix_version,tcl_dir = TixInfo()
##
##            tixdll="tix%s.dll"% (tix_version.replace(".",""))
##            tcldll="tcl%s.dll"%tcl_version.replace(".","")
##            tkdll="tk%s.dll"%tk_version.replace(".","")
##
##            dlls.add(os.path.join(sys.prefix,"DLLs",tixdll))
##
##            self.dlls_in_exedir.extend( [tcldll,tkdll,tixdll ] )
##
##            tcl_src_dir = os.path.split(tcl_dir)[0]
##            tcl_dst_dir = os.path.join(self.lib_dir, "tcl")
##            self.announce("Copying TIX files from %s..." % tcl_src_dir)
##            self.copy_tree(os.path.join(tcl_src_dir, "tix%s" % tix_version),
##                           os.path.join(tcl_dst_dir, "tix%s" % tix_version))
##
##opts={
##    'py2exe':{
##        'bundle_files':1
##    }
##}

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="*"
    name="PyVot"
    type="win32"
/>
<description>PyVot</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="*"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

def files(folder):
    for path in glob.glob(folder+'/*'):
        if os.path.isfile(path):
            yield path

data_files=[]
##            ('.',)# glob.glob(sys.prefix+'/DLLs/tix84*.dll')),
####            ('tcl/tix8.4', files(sys.prefix+'/tcl/tix8.4')),
####            ('tcl/tix8.4/bitmaps', files(sys.prefix+'/tcl/tix8.4/bitmaps')),
####            ('tcl/tix8.4/pref', files(sys.prefix+'/tcl/tix8.4/pref')),
##           ]

setup(
    script_args=['py2exe'],
##    cmdclass={'py2exe':myPy2Exe},
    windows=[{
        "script":"PyVot.py",
        "icon_resources":[(1,"D:\\Documents\\Developpement\\PyVot 0.6\\Images\\logo32b.ico")],
        "other_resources": [(24,1,manifest)]
    }],
    data_files=data_files,
    options={
             'py2exe':{
#                       'bundle_files':1,
                       "dll_excludes":["gdiplus.dll"]#, "MSVCP71.dll"]
             }
             }
)

