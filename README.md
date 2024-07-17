
<div style="text-align: center;">

![banner](assets/branding/banner_bbg.png) 

</div>




<p>&nbsp;</p>



### Index

----
1. [Description](#Description)
2. [Updates](#Latest-Update)
3. [How It Works](#How-It-Works)
4. [Instructions](#Installation)
5. [Know Issues](#Know-Issues)
6. [FAQ](#FAQ)
7. [Credits](#Credits)


<p>&nbsp;</p>


### Description
----
An open sourced mod manager inspired by [CCDTreborn's 8 Mod On / Off Switch (Version 2)](https://tekkenmods.com/mod/3312/tekken-8-mod-on-off-switch-version-2) to enable/disable your mods with a switch.

![screenshot](docs/assets/screenshot.png) 

Source code: [https://github.com/opensource111111/tekken-8-mod-manager](https://github.com/opensource111111/tekken-8-mod-manager)





<p>&nbsp;</p>



### Latest Update

----

2.3.1
#### 17th July 2024
- The program no longer needs to reimport the list of mods into the program when deleting mods.
- Added website links to Tekken mods websites under the "Help" tab at the top of the window. 



2.3
#### 11th July 2024
- Reformed the ini file for mods.
- Reformed the ini file for the program.
- Separated the fonts for the programs text body, title and headers. You can now change the size, font and colour for each.
- The ability to group sub mods under the main mod. For example, [Chun Li Alpha Costume](https://tekkenmods.com/mod/4352/chun-li-s-alpha-costume) and [Vindictus dress](https://tekkenmods.com/mod/4218/vindictus-dress). To use this, open to the details panel of the mod of your choice and click the edit information button. Near the bottom you will see the header called options. Click the + sign which will add a text field and type the absolute folder name of the mod you want to add. The mods you add will now only show under the options header on the mod. To remove the mod just click the - sign in the details panel.

![screenshot](docs/assets/manual/ui/options.png) 


Changelog History: https://github.com/opensource111111/tekken-8-mod-manager/blob/main/changelog.md


<p>&nbsp;</p>


### How It Works

----
[Manual here.](doc/manual.md)

- The program searches for folders/subfolders inside "Steam\steamapps\common\Tekken 8\Polaris\Content\Paks" that have .pak files inside on them and then lists them inside the program to then be able to switch them on/off. 


- The program adds or removes "-x" at the end of each file (.utoc, .ucas, .pak) to enabled/disabled.
	
   - Enabled = Filenames not ending with "-x"
   - Disabled = Filenames ending with "-x"


- Please read the mod creators instruction on how to install there mod. The mod need to have its own separate folder. By doing this you can turn on/off mods separately.

   examples: 

   ![e.g](docs/assets/instructions/recommended.png)



<p>&nbsp;</p>


### Installation

----
   
   #### Option 1: Run from executable. (Windows Only)

   1. Unzip the exe file from the zip file. You will most likely get a virus warning which will then quarantine the file. Any virus warning you may have are false positives. 


   2. Place the executable in "Steam\steamapps\common\Tekken 8" and run.
   
   
   ![folder](docs/assets/instructions/place_inside_tekken8_folder.png)



   Note: The Windows executable was compiled using pyinstaller.
      
        pyinstaller tekken8modmanager.spec



   #### Option 2: Run from script (Windows / Linux)

      
   1. <span style="color:Yellow;"> Windows </span> -  Install Python 3.11.9: https://www.python.org/downloads/release/python-3119/
   2. <span style="color:LightBlue;"> Linux </span> - Open Terminal / Windows - Open Windows command prompt and install required packages using these commands below.

            - pip install pip
            - pip install glfw
            - pip install numpy
            - pip install PyOpenGL PyOpenGL_accelerate
            - pip install imgui
            - pip install pillow

         
   3. Place the "tekken8modmanager.py" script and "assets" folder inside "Steam\steamapps\common\Tekken 8".
     

   ![folder2](docs/assets/instructions/place_script_inside_folder.png)


   
   <span style="color:Yellow;"> Windows </span> - Right click file to open the context menu and open with 
   Python.

   ![folder2](docs/assets/instructions/open_with_python.png)



   <span style="color:LightBlue;"> Linux </span> - Open the python terminal and type "python3". Drag and drop 
   the script onto the terminal and press enter.

      python3 path_to_script



<p>&nbsp;</p>



 ### Known Issues

----

 



<p>&nbsp;</p>



### FAQ

----

- Q = Am i making any videos for the mod manager ?
   - A = Manual here: [Manual here.](docs/manual.md)

- Q = Can you create mod with this program ?
   - A = No



<p>&nbsp;</p>


### Credits:

----

glfw:  https://pypi.org/project/glfw/

numpy: https://github.com/numpy/numpy

PyOpenGL: https://pypi.org/project/PyOpenGL/

imgui: https://pypi.org/project/imgui/

pillow: https://pypi.org/project/pillow/

TARGET FONT BY Iconian Fonts : https://www.fonts4free.net/tarrget-font.html#

