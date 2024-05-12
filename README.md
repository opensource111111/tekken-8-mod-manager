
![banner](assets/branding/banner_bbg.png)


## Description
A Tekken 8 mod manager to turn on / off your mods.

Source code can be found here: [https://github.com/opensource111111/tekken-8-mod-manager](https://github.com/opensource111111/tekken-8-mod-manager)

Inspired by CDDTreborn's Tekken 8 Mod On / Off Switch (Version 2) at https://tekkenmods.com/mod/3312/tekken-8-mod-on-off-switch-version-2


![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshots/screenshot.png)




## Updates

Any feedback, bugs or issues, please post in the comment section. Thank you.



####  12th May 2024

   - Removed the ~mods,mods,logicmods folder requirement. It will now search for any folder/subfolder inside the Pak folder.

   - Added a category filter box at the top of the window to help organize your mod collection. 
         
         Available categories:
         - All
         - Character Customization
         - Stage
         - Sound
         - UI/HUD
         - Movesets/Animations
         - Miscellaneous


   - Added a details box/panel to show details of the mods such as name, auther etc which can be edited in the program. This will create an mod.ini at the location of the mod. The mod.ini can be created manually also.

   Example:

         [Mod]
         name= "T8"
         author= "John"
         description= "example"
         url= "www.example.com"
         category= "All"


   - Thumbnail supported file types: .jpg , .jpeg, .png, .webp, .bmp
 

Changelog History: https://github.com/opensource111111/tekken-8-mod-manager/blob/main/changelog.md





## How it works.

Searches for the folders ~mods, mods and logicmods inside "Steam\steamapps\common\Tekken 8\Polaris\Content\Paks" and lists every mod inside theses folders. 

The program adds or removes "-x" at the end of each file (.utoc, .ucas, .pak) to enabled/disabled.
	
   - Enabled = Filenames not ending with "-x"
   - Disabled = Filenames ending with "-x"



 <span style="color:orange;"> 
 
 ## Please make sure that each mod has it own separate folder or you will get an error.

example: 

![e.g](assets/screenshots/s.png)

 </span>




## Install Instruction
   
   ### Option 1: Run from executable. (Windows Only)

   1. Unzip the exe file from the zip file. You will most likely get a virus warning which will then quarantine the file. Any virus warning you may have are false positives. 




   2. Place the executable in "Steam\steamapps\common\Tekken 8" and run.
   
   
   ![folder](assets/screenshots/place_inside_tekken8_folder.png)


   The Windows excutable was compiled using pyinstaller.

      pyinstaller tekken8modmanager.spec


#

  ### Option 2: Run from script (Windows / Linux)

      
   1. <span style="color:Yellow;"> Windows </span> -  Install Python 3.11.9: https://www.python.org/downloads/release/python-3119/
   2. <span style="color:Yellow;"> Windows </span> - Microsoft C++ Build Tools:  https://visualstudio.microsoft.com/visual-cpp-build-tools/
   2. <span style="color:LightBlue;"> Linux </span> - Open Terminal / Windows - Open Windows command prompt
      
      Install required pacakges using these commands:

            - pip install pip
            - pip install glfw
            - pip install numpy
            - pip install PyOpenGL PyOpenGL_accelerate
            - pip install imgui[full]
            - pip install pillow
         

   3. Place the "tekken8modmanager.py" script and "assets" folder inside "Steam\steamapps\common\Tekken 8".
     

   ![folder2](assets/screenshots/place_script_inside_folder.png)


   
   <span style="color:Yellow;"> Windows </span> - Right click file to open the context menu and open with 
   Python.

   ![folder2](assets/screenshots/open_with_python.png)



   <span style="color:LightBlue;"> Linux </span> - Open the python terminal and type "python3". Drag and drop 
   the script onto the terminal and press enter.

      python3 path_to_script





## Credits

TARGET FONT BY Iconian Fonts : https://www.fonts4free.net/tarrget-font.html#

