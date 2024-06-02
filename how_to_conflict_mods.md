

## Managing Mod Conflicts In Tekken 8 Mod Manager


![conflict](assets\screenshots\conflict\conflicts.gif)


<p>&nbsp;</p>


### Purpose

- To find conflicts between different enabled mods and notify the user.

- It works by matching common strings values that are inputted into the "override parameter text field in the description panel. You can add as many text fields as you want the describe your mod by click on the + button.

- The strings values are not hard coded into the program, so you can type anything. I have put together recommendtion on how I use this but if you decide that the recommendation are not up to your liking then you can go by any format you want. Just make sure that the string values have no spaces.



### Recommended syntax

        header::the-asset-being-replaced

- Any spacing should use -.

- Use in-game names for describing assets




1. header - The area of the game you are replacing.

        - ui
        - sound
        - character-common (e.g for common items between characters)
        - character - character specific (e.g azucena::preset-1)
        - stage
        - avatar
        - others




2. the-asset-being-replaced 

        - preset-name 
        - sound-name
        - character-custom-item-name
        - stage-name





<p>&nbsp;</p>


## Examples


### common items (common item changes)

        character-common::eye-patch




### character (character specific changes)

        zafina::tk8-style-(p1)

        zafina::tk7-style-(p1)

        zafina::astrologer's-earrings
        
        jack8::voice-sfx





### ui (common game ui)

        ui::healthbar

        ui::mainmenu-character



### sound (common game audio)


- Anna Williams (Console ver.) / TEKKEN 3.

        sound::anna-williams-(console-ver.)-/-tekken3




### stage (stage)
        
- Fallen Destiny

        stage::fallen-destiny 




### avatar

- Ski Mask Panda

        avatar::ski-mask-panda


### others
- Remove SSS
  
          others::remove-sss





