
![banner](assets/branding/banner_bbg.png)


## Description
A Tekken 8 mod manager to turn on / off your mods.

Source code can be found here: [https://github.com/opensource111111/tekken-8-mod-manager](https://github.com/opensource111111/tekken-8-mod-manager)

Inspired by CDDTreborn's Tekken 8 Mod On / Off Switch (Version 2) at https://tekkenmods.com/mod/3312/tekken-8-mod-on-off-switch-version-2


![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshots/screenshot.png)




## Updates


#### 6th May 2024

   ![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshots/window_setting.png)
   
   - Added a windows configuration menu. Will add onto this at a later date. Option > Windows Configuration:

      - Global Scale (Disabled for now)
      - Font Size
      - Font Style
      - Thumbnail Scale
      - Show Thumbnail
      - Start Maximised Window
      - Button Colour
      - Background Colour

   All setting will be saved in the "tekken8modmanager.ini". The file will be created in the same location as the program.



    ![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshots/custom_fonts.png)


   Custom Fonts
   - You can add your own fonts by creating the folders "assets/fonts" in the same location as the program. Paste your font files in the folder "fonts". The font format have to be .ttf or .otf. 


 

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

      
   1. <span style="color:Yellow;"> Windows </span> -  Install Python: https://www.python.org/

   2. <span style="color:LightBlue;"> Linux </span> - Open Terminal / Windows - Open Windows command prompt
      
      Install required pacakges using these commands:

            - pip install pip
            - pip install glfw
            - pip install numpy
            - pip install PyOpenGL PyOpenGL_accelerate
            - pip install imgui
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

