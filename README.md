
![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/icon.png)



# Tekken 8 Mod Manager
A Tekken 8 mod manager to turn on / off mods 

Inspired by CDDTreborn's Tekken 8 Mod On / Off Switch (Version 2) at https://tekkenmods.com/mod/3312/tekken-8-mod-on-off-switch-version-2


Font used in logo
TARRGET FONT : https://www.fonts4free.net/tarrget-font.html#


![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshot.png)



How it works.
- Searches for folder ~mods and logicmods inside the Tekken 8 folder
- Adds or removes "-x" at the end of the files to enabled/disabled.
- Enabled = Filenames not ending with "-x"
- Disabled = Filenames ending with "-x"

   

        Dependence
        - Python: https://www.python.org/
        - glfw: pip install glfw
        - numpy: pip install numpy
        - PyOpenGL : pip install PyOpenGL
        - imgui: pip install imgui
        - pyinstaller(for creating exe)
      

***Instruction***
Create ~mods and logicmods folders and place them in Steam\steamapps\common\Tekken 8\Parlaris\Content\Paks.
Make sure your mods are in seperate folders inside the ~mods or logicmods folders.

Option 1: Script
1. Place this script in <steamapps>\common\Tekken 8.

   Linux - Open terminal and type "python3" or "python". Drag and drop script onto the terminal and press enter.

   Window - Right click file and open with Python

Option 2: EXE
   1. Place the executable in Steam\steamapps\common\Tekken 8 and run.
   

