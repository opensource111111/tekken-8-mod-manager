<div style="text-align: center;">


![banner](assets/branding/banner_bbg.png) 


![screenshot](docs/assets/screenshot1.png)


</div>




<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>



# Index
1. [Description](#Description)
2. [Updates](#Latest_Update)
3. [How It Works](#How_It_Works)
4. [Instructions](#Installation)
5. [KnowIssues](#Know_Issues)
6. [FAQ](#FAQ)
7. [Credits](#Credits)





<p>&nbsp;</p>






## Description
An open sourced mod manager inspired by [CCDTreborn's 8 Mod On / Off Switch (Version 2)](https://tekkenmods.com/mod/3312/tekken-8-mod-on-off-switch-version-2)
to enable/disable your mods with a switch.

Source code: [https://github.com/opensource111111/tekken-8-mod-manager](https://github.com/opensource111111/tekken-8-mod-manager)

Program Manual:  [Manual here.](docs/manual.md)


Any feedback, bugs or issues, please post in the comment section. Thank you. :)



<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>




## Latest_Update



### 19th June 2024
- Added a delete mod button in the details panel.
- When opening the mod manager, new mods that are installed will be disabled.


### 9th June 2024
- Adjusted the offset values on UI elements when changing the application scale value in the window configuration menu. The application scale goes from 1 - 3 in the menu.


### 2nd June 2024
1. Added a manual including gifs. [Manual](docs/manual.md)




Changelog History: https://github.com/opensource111111/tekken-8-mod-manager/blob/main/changelog.md




<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>




## How_It_Works

- Searches for folders/subfolders inside "Steam\steamapps\common\Tekken 8\Polaris\Content\Paks" that have .pak files inside and then lists them inside the program to then be able to switch them on/off. 


- The program adds or removes "-x" at the end of each file (.utoc, .ucas, .pak) to enabled/disabled.
	
   - Enabled = Filenames not ending with "-x"
   - Disabled = Filenames ending with "-x"


- Recommended folders to create are ~mods, mods and logicmods. To keep things organized, I recommend to have a separate folders for each mod. By doing this you can turn on/off mods separately but that's up to you.

   examples: 

   ![e.g](docs/assets/instructions/recommended.png)




<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>



## Installation
   
   ### Option 1: Run from executable. (Windows Only)

   1. Unzip the exe file from the zip file. You will most likely get a virus warning which will then quarantine the file. Any virus warning you may have are false positives. 


   2. Place the executable in "Steam\steamapps\common\Tekken 8" and run.
   
   
   ![folder](docs/assets/instructions/place_inside_tekken8_folder.png)



   Note: The Windows executable was compiled using pyinstaller.
      
        pyinstaller tekken8modmanager.spec



<p>&nbsp;</p>


  ### Option 2: Run from script (Windows / Linux)

      
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
<p>&nbsp;</p>
<p>&nbsp;</p>




 ## Known_Issues

 - 


<p>&nbsp;</p>


 ## FAQ

 - 

<p>&nbsp;</p>




## Credits:


glfw:  https://pypi.org/project/glfw/

numpy: https://github.com/numpy/numpy

PyOpenGL: https://pypi.org/project/PyOpenGL/

imgui: https://pypi.org/project/imgui/

pillow: https://pypi.org/project/pillow/

TARGET FONT BY Iconian Fonts : https://www.fonts4free.net/tarrget-font.html#

