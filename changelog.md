
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



   ![](assets\screenshots\description.png)

   - Added a details panel to show details as name, auther etc which can be edited in the program. This will create an mod.ini at the location of the mod. The mod.ini can be created manually also.  

   Example:

         [Mod]
         name= "T8"
         author= "John"
         description= "example"
         url= "www.example.com"
         category= All


   - Thumbnail supported file types: .jpg , .jpeg, .png, .webp

#

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

  

#


#### 3rd May 2024

   - Added the ability to save your viewmode setting. This will create a file called "tekken8modmanager.ini".

#

#### 27th April 2024
   - Fixed aspect ratio on thumbnails when hovering over icon with the mouse curser.

#

#### 17th April 2024

   ![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshots/thumbnailview.png)



   - Cleaned up UI elements
   - Add a hide button for each folder.
   - Can now search for ~mods, logicmods or mods folders in lowercase or uppercase


   ![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshots/thumbnail_structure.png)

   - (Experimental) Added thumbnail support. Only works in List view mode.  Click on the options tab and show thumbnail.  Place a image file  inside the mod folder of your choice and name it "thumbnail"(jpg, png) If no image is found then it will default to using the programs logo as the thumbnail. 
   -Fixed slow loading of thumbnails


#

#### 14th April 2024

   ![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](assets/screenshots/treeview.png)


   - Added a list directory tree view mode. In this mode you can now enable or disable from the top level folder or sub level folder. To switch viewing mode click the View button on the top left corner and select Tree View from the drop menu.


#

#### 11th April 2024
   - Can now search for the folder "mods" inside "Steam\steamapps\common\Tekken 8\Polaris\Content\Paks"

#



#### 10th April 2024
   - Added a button to open mod folders.
   - Changed colour of UI titlebar.
   - Added an indent to the lists of mods under each section.
   - Corrected a issue with paths using the python script under Linux.  

   
#



#### 7th April 2024
   - Added a separator to the UI to show both ~mods and logicmods separately.

   

#
