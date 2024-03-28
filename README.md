# tekken-8-mod-manager
A Tekken 8 mod manager to turn on / off mods 


Inspired by CDDTreborn's Tekken 8 Mod On / Off Switch (Version 2) at https://tekkenmods.com/mod/3312/tekken-8-mod-on-off-switch-version-2


How it works.
- Searches for folder ~mods and logicmods inside the Tekken 8 folder
- Adds or removes "-x" at the end of the files to enabled/disabled a mod.
- Enabled = Filenames not ending with "-x"
- Disabled = Filenames ending with "-x"

   

        Dependence
        - Python: https://www.python.org/
        - glfw: pip install glfw
        - numpy: pip install numpy
        - PyOpenGL : pip install PyOpenGL
        - imgui: pip install imgui

***Instruction***
Create ~mods and logicmods folders and place them in "Tekken 8/Parlaris/Content/Paks".
Make sure your mods are in seperate folders inside the ~mods or logicmods folders.
   
1. Place script inside the Tekken 8 game folder.

   Linux - Open terminal and type "python3" or "python". Drag and drop script onto the terminal and press enter.

   Window - Right click file and Open with Python



