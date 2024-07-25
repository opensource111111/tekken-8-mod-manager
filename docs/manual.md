


<div style="text-align: center;">

![banner_bbg.png](assets/banner_bbg.png)

</div>




### Table Of Content

1. [How It Works](#How-It-Works)
1. [Files and Folders](#Files-and-Folders)
2. [UI Overview](#UI-Overview)
   - [How To Add A Sub Mod](#How-To-Add-A-Sub-Mod)
4. [Managing Mod Conflicts In Tekken 8 Mod Manager](#Managing-Mod-Conflicts-In-Tekken-8_Mod-Manager)


<p>&nbsp;</p>
<p>&nbsp;</p>




### How It Works

----

- The program searches for folders/subfolders inside "Steam\steamapps\common\Tekken 8\Polaris\Content\Paks" that have .pak files inside on them and then lists them inside the program to then be able to switch them on/off. 


- The program adds or removes "-x" at the end of each file (.utoc, .ucas, .pak) to enabled/disabled.
	
   - Enabled = Filenames not ending with "-x"
   - Disabled = Filenames ending with "-x"


- Please read the mod creators instruction on install there mod. The mod need to have its own separate folder. By doing this you can enable/disable mods indefinitely.


<p>&nbsp;</p>




### Files and Folders

    
- Recommended starting folders to create are ~mods, mods and logicmods. To keep things organized, I recommend to have a separate folders for each mod. By doing this you can turn on/off mods separately.

   examples: 

  ![e.g](assets/instructions/recommended.png)


   - 1.1 - Inside a mod folder. The profile folder is created at startup or by pressing the refresh button on the main menu bar.
      ![e.g](assets/manual/file_folders/mod.png)


   - 1.2 - Inside a profile folder located inside each mod folder. Add your image files inside here. The file type(.png, .jpg/jpeg, .bmp, .webp). The image file can be named want ever you want.

   ![e.g](assets/manual/file_folders/profile.png)
   

   You add as many images as you want. In the detail panel hover over the image and use the scroll wheel to scroll through the images.
   
   ![e.g](assets/manual/ui/thumbnail.gif)


   <p>&nbsp;</p>




### UI Overview

   - 1.1. Window Configuration Menu.
   ![e.g](assets/manual/ui/config.gif)

     
   <p>&nbsp;</p>


   - 1.2. View modes.

      ![e.g](assets/manual/ui/viewmodes.png)

      - List - Enable/disable individual mods. Adds a search bar.
      
         ![e.g](assets/manual/ui/viewmodes/list_view.png)

      - Tree: Enable/disable Individual mods including sub folders.
         ![e.g](assets/manual/ui/viewmodes/tree_view.png)

      
      

   <p>&nbsp;</p>



   - 1.3. Help
      - 1.3.1. Mod Links

         ![e.g](assets/manual/ui/mod_links.png)

      - 1.3.2. About

         ![e.g](assets/manual/ui/about.png)


   <p>&nbsp;</p>



   - 1.4. Tool Bar
      
      ![e.g](assets/manual/ui/bar.png)

     - 1.4.1 - Filter
     ![e.g](assets/manual/ui/filter.gif)
        
        How to add mod to category.
     - In the details panel, click on edit information and in the category section pick from the drop-down the category and click the save button.
 


- 1.4.2 - Presets
     ![e.g](assets/manual/ui/presets.gif)

       - Rename Preset
       ![e.g](assets/manual/ui/rename.gif)
    
       - Add Preset
       ![e.g](assets/manual/ui/addtopresets.gif)


         
   <p>&nbsp;</p>
 
   

   - 1.5.  Details Panel
   
      ![e.g](assets/manual/ui/detailspanel.png)

      How to access this.
      ![e.g](assets/manual/ui/detailspanel.gif)
      You can edit the information by clicking on the edit information button.

     
   ##### How To Add A Sub Mod

  - You can group sub mods under the main mod. For example, [Chun Li Alpha Costume](https://tekkenmods.com/mod/4352/chun-li-s-alpha-costume) and [Vindictus dress](https://tekkenmods.com/mod/4218/vindictus-dress). 
![screenshot](assets/manual/ui/options.png) 

     - To use this, open to the details panel of the mod of your choice and click the edit information button. Near the bottom you will see the header called "Options". Click the + sign which will add a text field and type the absolute folder name, or copy and paste the folder name from your file explorer of the mod you want to be a submod. If you want to add more then one then clicking the + button again create additional text boxes. One per text box.
     
     - The mods you flag ad sub mods will now only show under the options header in the details panel of the mod you decided add the sub mods to.
     - To remove a sub mod, open the details panel of mod with the submods and click the edit information button. By each text box under the options header will have a "-" sign. Click it to remove and click the save button. This will remove the sub mod flag for that mod and put it back to be shown in the mod list on the left.
    

<p>&nbsp;</p>



### Managing Mod Conflicts

   
   #### How it works

   - It works by matching common strings values that are inputted into the "override parameter" text field in the description panel. You can add as many text fields as you want the describe your mod by click on the + button.

   - The strings values are not hard coded into the program, so you can type anything. I have put together recommendation on how I use this but if you decide that the recommendation are not up to your liking then you can go by any format you want. Just make sure that the string values have no spaces.

   ### How to enable this feature ?
   - To enable this open the window configuration menu and click on the Mod Conflict Notification box.

   ![conflict](assets/manual/conflict/conflicts.gif)


   <p>&nbsp;</p>


   #### Recommended Setup

         header::asset

   - Any spacing should use - .

   - Use in-game names for describing assets



    
   1. header - The area of the game you are replacing.

         - ui
         - sound
         - character-common (e.g for common items between characters)
         - character - character specific (e.g azucena::preset-1)
         - stage
         - avatar
         - others

   2. asset - The game asset being replaced. 

      - preset-name 
      - sound-name
      - character-custom-item-name
      - stage-name

   
   <p>&nbsp;</p>



   #### Examples

    # to do - Add pictures of items and areas of the game for examples.
   - common items (common item changes)

         character-common::eye-patch




   - character (character specific changes)

         zafina::tk8-style-(p1)

         zafina::tk7-style-(p1)

         zafina::astrologer's-earrings
         
         jack8::voice-sfx





   - ui (common game ui)

         ui::healthbar

         ui::mainmenu-character



   - sound (common game audio)


      - Anna Williams (Console ver.) / TEKKEN 3.

            sound::anna-williams-(console-ver.)-/-tekken3




   - stage (stage)
            
      - Fallen Destiny

            stage::fallen-destiny 




   - avatar

      - Ski Mask Panda

            avatar::ski-mask-panda


   - others
      - Remove SSS
      
               others::remove-sss







