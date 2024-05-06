import os
import sys
import subprocess
import configparser


import glfw

import imgui
from imgui.integrations.glfw import GlfwRenderer

from OpenGL.GL import *
import OpenGL.GL as gl

from PIL import Image, ImageOps



class description_format:
    name : str = ""
    aurther : str = ""
    url : str = ""
    description : str = ""
    _type : str = ""




class mod_list_format:
        name : str = ""
        location : str = ""
        _type : str = ""
        active : bool = True
        icon  =  None
        description : description_format  = None
        

   

    
def name_sort(mod_list):
    return mod_list.name.title()
   




class mod_manager:
    


    def __init__(self):

        # system path
        self.path : str = ""
        self.pure_dir : str = ""
        self.window_icon  = None
        self.banner = None



        #mod data
        self._mod_list : mod_list_format = []
        self.mod_list : mod_list_format = []
        self.logicmods_list : mod_list_format = []

        
        #folders
        self._mods_folder : str = "~mods"
        self.mods_folder : str = "mods"
        self.logicmods_folder :str = "logicmods"


        self.ui = None


   

       
        

    class configs:

        def __init__(self,owner):
            self.window = None
            self.owner = owner


            #fonts
            self.selected_font = None
            self.selected = 4
            self.selected_size = 9
            self.fonts = []
            self.scale = 1
            self.font_colour = 1,1,1,1


            #ui
            self.button_colour = 0,0.290,0.783,1
            self.bg_colour = 0,0,0,1

            #ui
            self.thumbnail_size = 50

            #window
            self.maximised = False
            

            self.config = configparser.ConfigParser()
       


        def window_check(self):
            
            #Preset Setting - Read from imgui.ini
            filecheck = self.config.read('tekken8modmanager.ini')
            if filecheck:
    
                for i in self.config.sections():
                    if i =="Preset":
                        self.maximised= self.config.getboolean('Preset', 'maximised',fallback=False)
                        


        def ui_check(self):
            
            #Preset Setting - Read from imgui.ini
            filecheck = self.config.read('tekken8modmanager.ini')
            if filecheck:
    
                for i in self.config.sections():
                    if i =="Preset":
                        self.owner.ui.config_viewmode= self.config.get('Preset', 'viewmode',fallback=False)
                        self.owner.ui.toggle_viewmode = self.config.getboolean('Preset', 'viewmode',fallback=False)
                        self.owner.ui.config_thumbnail = self.config.get('Preset', 'thumbnail', fallback=False)
                        self.owner.ui.show_thumbnail = self.config.getboolean('Preset', 'thumbnail', fallback=False)
                        self.owner.ui.toggle_hide_mods = self.config.getboolean('Preset', 'hide_mods', fallback=False)
                        self.owner.ui.toggle_hide__mods = self.config.getboolean('Preset', 'hide__mods', fallback=False)
                        self.owner.ui.toggle_hide_logicmods = self.config.getboolean('Preset', 'hide_logicmods', fallback=False)
                        

                        
                        self.owner.thumbnail_size =  self.config.getint('Preset', 'thumbnail_size', fallback=50)
                        


                        #colours
                        temp = self.config.get('Preset', 'font_colour', fallback= (1,1,1,1))
                        if temp != (1,1,1,1):
                            temp2 = temp.replace("(","").replace(")","").replace("[","").replace("]","").replace(",","").split()
                            self.font_colour = list(map(float,temp2))
                        
                        
                        temp = self.config.get('Preset', 'button_colour', fallback=(0,0.290,0.783,1))
                        if temp != (0,0.290,0.783,1):
                            temp2 = temp.replace("(","").replace(")","").replace("[","").replace("]","").replace(",","").split()
                            self.button_colour = list(map(float, temp2))


                        temp = self.config.get('Preset', 'bg_colour', fallback=(0,0,0,1))
                        if temp != (0,0,0,1):
                            temp2 = temp.replace("(","").replace(")","").replace("[","").replace("]","").replace(",","").split()
                            self.bg_colour = list(map(float, temp2))




                        #font
                        self.selected =self.config.getint('Preset', 'font',fallback=4)
                        self.selected_size =self.config.getint('Preset', 'font_size',fallback=9)
                        self.config_font_type(self.fonts[self.selected][1][self.selected_size][1])
                        


            
        def config_setting(self,header = "Preset"):
            
            with open('tekken8modmanager.ini', 'w') as configfile:
                self.config['Preset'] = {'viewmode': str( self.owner.ui.toggle_viewmode),'Thumbnail': str( self.owner.ui.show_thumbnail),'hide_mods': str(self.owner.ui.toggle_hide_mods),'hide__mods': str( self.owner.ui.toggle_hide__mods),'hide_logicmods': str( self.owner.ui.toggle_hide_logicmods),'maximised' : str(self.maximised), "font" : str(self.selected),"font_size" : str(self.selected_size),"thumbnail_size" : str(self.thumbnail_size), "font_colour" : str(self.font_colour),"button_colour" : str(self.button_colour), "bg_colour" : str(self.bg_colour)}
                self.config.write(configfile)
            


        def get_font_collection(self):
                
             
                
                imgui.get_font_size()
                io = imgui.get_io()
                
                win_w, win_h = glfw.get_window_size(self.window)
                fb_w, fb_h = glfw.get_framebuffer_size(self.window)
                font_scaling_factor = max(float(fb_w) / win_w, float(fb_h) / win_h)
                font_size_in_pixels = 2
                io.font_global_scale /= font_scaling_factor



                for i in os.listdir(os.path.dirname(os.path.abspath(__file__)) +"/assets/fonts"):
                    font = []
                    
                    for jj in range(13):
                        font.append((i + " " + str(font_size_in_pixels) + "px",io.fonts.add_font_from_file_ttf(os.path.dirname(os.path.abspath(__file__)) +"/assets/fonts/" + i , font_size_in_pixels * font_scaling_factor)))
                        font_size_in_pixels +=2
                    font_size_in_pixels = 2
                    self.fonts.append([i,font])


                #hack for user custom fonts
                if os.path.isdir(self.owner.pure_dir +"/assets/fonts"):
                    for i in os.listdir(self.owner.pure_dir +"/assets/fonts"):
                        font = []
                        
                        for jj in range(13):
                            font.append((i + " " + str(font_size_in_pixels) + "px",io.fonts.add_font_from_file_ttf(self.owner.pure_dir +"/assets/fonts/" + i , font_size_in_pixels * font_scaling_factor)))
                            font_size_in_pixels +=2
                        font_size_in_pixels = 2
                        self.fonts.append([i,font])


                
               
                self.selected_font = (self.fonts[4][1][9][1])
                
            



        def config_font_type(self,name):
            for i in self.fonts[self.selected][1][self.selected_size]:
                
                self.selected_font = i
               



        def config_window_scale(self):
             
            win_w, win_h = glfw.get_window_size(self.window)
            fb_w, fb_h = glfw.get_framebuffer_size(self.window)
            font_scaling_factor = max(float(fb_w) / win_w, float(fb_h) / win_h)
                
            io = imgui.get_io()
            io.font_global_scale = self.scale            
            io.font_global_scale /= font_scaling_factor




        def config_default(self):
        

            
            self.selected = 4
            self.selected_size = 9
            self.selected_font = (self.fonts[4][1][9][1])
            self.scale = 1
            self.font_colour = 1,1,1,1
            self.button_colour = 0,0.290,0.783,1
            self.bg_colour = 0,0,0,1
            self.thumbnail_size = 50
            self.maximised = False



            self.config_setting()

        



    class windows_ui:
        
        def __init__(self, owner, window,impl,config):
            self.owner = owner
            self.window = window
            self.impl = impl
            self.config = config


                

            #ui toggles
            self.toggle_about : bool = False
            self.toggle_viewmode : bool = False
            self.toggle_hide_mods : bool = False
            self.toggle_hide__mods : bool = False
            self.toggle_hide_logicmods : bool = False
            self.show_thumbnail : bool = False
            self.toggle_mods : bool = True
            self.toggle__mods : bool = True
            self.toggle_logicmods : bool = True
            self.show_window_setting : bool = False
        


            #ui messages
            self.about_logo = self.owner.ui_images(self.owner.banner)
            self.about_message : str = "Created by Beanman"
            self.no_mod_message : str = "No mods were found inside the {0} folder"
            self.tip_message : str = "Tip: Please make sure that each mod has its own separate folder."
            self.path_error_message : str = "This program was not placed inside {0}.".format("Steam\steamapps\common\Tekken 8")


         
            
            self.filterbar : str = "Filter"
            
            self.highlight : mod_list_format = None
            
        


        

        def main_filter_bar(self):
            
            
            win_w, win_h = glfw.get_window_size(self.window)
            fb_w, fb_h = glfw.get_framebuffer_size(self.window)
            scaling = max(float(fb_w) / win_w, float(fb_h) / win_h)


            #Filter Bar

            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,0,0,0)
            imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE,0.0)
            imgui.set_next_window_size( scaling * 1000, scaling *  60)
            imgui.set_next_window_position(0,38)
            
            imgui.begin("##filter", False, imgui.WINDOW_NO_TITLE_BAR  | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)
            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND,1,1,1,0.04)
            changed,self.filterbar = imgui.input_text("Filter",self.filterbar)
            imgui.pop_style_color()

                                    
            imgui.end()
                                
            imgui.pop_style_color()
            imgui.pop_style_var()
            
            pass



        


        def main_window_bar(self):

            #https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html#imgui.core.listbox_header
    
            with imgui.begin_main_menu_bar():
                #imgui.set_window_font_scale(4)
                
            

             
                #Options 
                if imgui.begin_menu("Options"):
    

                
                    if imgui.button("Window Configuration"):
                    
                        imgui.open_popup("Window Configuration")
                        
                    
                    imgui.set_next_window_size_constraints((600,400), (600, 400))
                    with imgui.begin_popup_modal("Window Configuration",imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_DECORATION) as select_popup:
                        if select_popup.opened:
                            
                            #Window
                            imgui.separator()
                            imgui.text("Window & UI Settings")
                            imgui.separator()
                            imgui.text("Start Maximised:")
                            imgui.same_line()
                            changed,self.config.maximised = imgui.checkbox("##m",self.config.maximised)
                            self.config.config_setting()


                            imgui.text("Show Thumbnails") 
                            imgui.same_line()
                            _, self.show_thumbnail = imgui.checkbox("##Show Thumbnails",self.show_thumbnail)
                            if imgui.is_item_edited():
                                self.generate_modlist()
                                self.config.config_setting("Preset")
                            
                            
                            imgui.text("Thumbnails Scale") 
                            imgui.same_line()
                           
                            self.config.thumbnail_size = imgui.slider_int("##Thumbnail_scale",self.config.thumbnail_size,50,100)[1]
                            
                            #if changed:
                               
                                #print(self.config.thumbnail_size)
                                #self.config.config_setting("Preset")
                            
                            
                            
                            imgui.text("Button Colour:")
                            imgui.same_line()
                            _, self.config.button_colour = imgui.color_edit4("##button_colour",*self.config.button_colour,imgui.COLOR_EDIT_NO_ALPHA)
                            self.config.config_setting()


                            imgui.text("Background Colour:")
                            imgui.same_line()
                            _, self.config.bg_colour = imgui.color_edit4("##backgound_colour",*self.config.bg_colour,imgui.COLOR_EDIT_NO_ALPHA)
                            self.config.config_setting()


                            
                            """
                            #scale
                            imgui.text("globle scale:")
                            imgui.same_line()
                            changed, self.config.scale = imgui.slider_int("##scale", self.config.scale,1,50)
                            self.config.config_window_scale()
                            """

                            imgui.text("")
                            imgui.separator()

                            #change font
                            imgui.text("Font Setting")
                            imgui.separator()
                            imgui.text("Font Style:")
                            imgui.same_line()
                            
                            items = []
                            for i in self.config.fonts:
                        
                                items.append(i[0])
                                   
                        
                      

                          
                            with imgui.begin_combo("##dfff",items[self.config.selected]) as combo:
                                if combo.opened:
                                    for i, item in enumerate(items):
                                        is_selected = (i == self.config.selected)
                                        if imgui.selectable(item, is_selected)[0]:
                                            self.config.selected = i
                                            self.config.config_font_type(items[i])
                                            self.config.config_setting()
                                                    


                                        # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)
                                        if is_selected:
                                            imgui.set_item_default_focus()
                            items.clear()

                            imgui.text("Font Size:")
                            imgui.same_line()


                            
                            
                            items = []
                            for i in self.config.fonts[self.config.selected][1]:
                                items.append(i[0])
                                
                                
                            
                            
                            with imgui.begin_combo("##dffeef",items[self.config.selected_size]) as combos:
                                if combos.opened:
                                    for i, item in enumerate(items):
                                        is_selected = (i == self.config.selected_size)
                                        if imgui.selectable(item, is_selected)[0]:
                                            self.config.selected_size = i
                                            self.config.config_font_type(items[i])
                                            self.config.config_setting()
                                                    


                                        # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)
                                        if is_selected:
                                            imgui.set_item_default_focus()




                            imgui.text("Font Colour:")
                            imgui.same_line()
                            _, self.config.font_colour = imgui.color_edit4("##font_colour",*self.config.font_colour,imgui.COLOR_EDIT_NO_ALPHA)
                          
                            self.config.config_setting()




                            imgui.separator()
                            if imgui.button("Reset to Default"):
                                self.config.config_default()
                            
                                


                            
                            
                             


                    
                    
                    imgui.end_menu()
                    
                


                
                #view modes
                if imgui.begin_menu("View"):
                    
                    _, list_view = imgui.menu_item("List View")
                    _, tree_view = imgui.menu_item("Tree View")
                    
                    if list_view:
                        self.toggle_viewmode = False
                        self.generate_modlist()
                        
                        self.config.config_setting("Preset")
                    

                    if tree_view:
                        self.toggle_viewmode  = True
                        self.generate_modlist()

                        self.config.config_setting("Preset")
                        


                    
        
                    imgui.end_menu()




                
                #view modes
                if imgui.begin_menu("Help"):

                    _,about = imgui.menu_item("About")

                    if about:
                        if self.toggle_about  == True:
                            self.toggle_about = False
                        elif self.toggle_about  == False:
                            self.toggle_about  = True
            
                    
                    imgui.end_menu()





                #about box
                if self.toggle_about:
                    imgui.set_next_window_size_constraints((270,200), (270, 200))
                    imgui.begin("About",False,imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
                
                    
                    imgui.indent(10)
                    imgui.image(self.about_logo[0],self.about_logo[1]*0.5,self.about_logo[2]*0.5)
                    imgui.text_wrapped(self.about_message)
                    imgui.indent(-10)
                    imgui.same_line()
                    
                    if imgui.button("Close"):
                        self.toggle_about = False
                    imgui.end()
                



                #Refresh Button
        
                imgui.set_window_position(20,0)
                
                if imgui.button("Refresh List"):
                    self.generate_modlist()
                
                





        def get_decription(self,location):
            
            description = configparser.ConfigParser()
            description_info = description_format()
    
            
            if bool(description.read(location)) == True:
                description_info.name = description.get("Mod","name", fallback="none")
                #print(decription_info.name)
                description_info.aurther = description.get("Mod","aurther", fallback="none")
                #print(decription_info.Aurther)
                description_info.decription = description.get("Mod","decription", fallback= "none")
                #print(decription_info.decription)
                description_info.url = description.get("Mod","url", fallback="none")
                #print(decription_info.url)
            

            return description_info
                    
            
        
          

        def generate_modlist(self):
            
            self.owner.clear_images()

            self.owner._mod_list.clear()
            self.owner.mod_list.clear()
            self.owner.logicmods_list.clear()   
            

            
            if self.show_thumbnail == True: 

                default_icon = self.owner.ui_images() 
            else: 
                default_icon = None
        


            if os.path.isdir(self.owner.path):
                

                for folder in os.listdir(self.owner.path):
                    
                    #checking for root mod folders.
                    if os.path.isdir(self.owner.path + "/" + folder):

                        if folder.lower() == self.owner._mods_folder.lower() or folder.lower() == self.owner.mods_folder.lower() or folder.lower() == self.owner.logicmods_folder.lower():
                            

                            # look through the root mod folders.
                            for root, dirnames, filenames  in os.walk(self.owner.path +"/" + folder):

                                    for mod_folder in dirnames:

                                        if os.path.isdir(root + "/" + mod_folder):
                                    
                                            if os.listdir(root  + "/" + mod_folder) != []:
                                                
                                                if self.toggle_viewmode == False:
                                                    for i in os.listdir(root  + "/" + mod_folder):
                                                        if i.endswith("pak") | i.endswith("pak-x") | i.endswith("ucas") | i.endswith("ucas-x") | i.endswith("utoc") | i.endswith("utoc-x"):
                                                            

                                                            new = mod_list_format()
                                                            new._type = folder
                                                            new.name = mod_folder
                                                            new.location = root  + "/" + mod_folder
                                                            new.icon = default_icon
                                                            new.description = self.get_decription( root  + "/" + mod_folder + "/mod.ini")
                                                        
                                                            for filecheck in os.listdir(root  + "/" + mod_folder):
                                                                if filecheck.startswith("thumbnail") and self.show_thumbnail == True:
                                                                    new.icon = self.owner.ui_images(root  + "/" + mod_folder + "/" + filecheck)
                                                                
                                                                if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                                        
                                                                    if filecheck.endswith("-x"):
                                                                            new.active = False
                                                                            
                                                                    else:
                                                                            new.active = True
                                                                    
                                                                
                                                            if folder.lower() == self.owner._mods_folder.lower():        
                                                                self.owner._mod_list.append(new)
                                                            
                                                            if folder.lower() == self.owner.mods_folder.lower():        
                                                                self.owner.mod_list.append(new)
                                                                
                                                            if folder.lower() == self.owner.logicmods_folder.lower():
                                                                self.owner.logicmods_list.append(new)
                                                                
                                                            
                                                            

                                                            break
                                                
                                                else:
                                                    
                                                            new = mod_list_format()
                                                            new._type = folder
                                                            new.name = mod_folder
                                                            new.location = root  + "/" + mod_folder
                                                            new.icon = default_icon
                                                            new.description = self.get_decription( root  + "/" + mod_folder + "/mod.ini")
                                                        
                                                            for filecheck in os.listdir(root  + "/" + mod_folder):
                                                                """
                                                                if filecheck.startswith("thumbnail") and self.show_thumbnail == True:
                                                                    new.icon = self.ui_images(root  + "/" + mod_folder + "/" + filecheck)
                                                                """
                                                                if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                                        
                                                                    if filecheck.endswith("-x"):
                                                                            new.active = False
                                                                            
                                                                    else:
                                                                            new.active = True
                                                                    
                                                                
                                                            if folder.lower() == self.owner._mods_folder.lower():        
                                                                self.owner._mod_list.append(new)
                                                            
                                                            if folder.lower() == self.owner.mods_folder.lower():        
                                                                self.owner.mod_list.append(new)
                                                                
                                                
                                                            if folder.lower() == self.owner.logicmods_folder.lower():
                                                                self.owner.logicmods_list.append(new)




            
                self.owner._mod_list.sort(reverse=False,key=name_sort)
                self.owner.mod_list.sort(reverse=False,key=name_sort)
                self.owner.logicmods_list.sort(reverse=False,key=name_sort)
            
        




        def ui_listview(self):
                
        
            
            
         
          
                        
                
                    
                #~mods ui list
                if os.path.isdir(self.owner.path + "/" + self.owner._mods_folder) == True:
                    
                    imgui.separator()
                    imgui.text(self.owner._mods_folder + ": " + str(len(self.owner._mod_list)))
                    
                        
                    
                    #Toggle Hide
                    
                    imgui.same_line()
               
                    imgui.indent(imgui.get_window_size()[0]-200 - self.config.selected_size * 2)
                        

                    if imgui.radio_button("Collapse##Hide ~mods",self.toggle_hide__mods):
                        self.toggle_hide__mods = not self.toggle_hide__mods
                        self.config.config_setting("Preset")



                    # Open button
                    imgui.same_line()        
                   
                    if imgui.button("Open##Open ~mods Folder"):
                        if sys.platform == "win32":

                            subprocess.Popen(['explorer', "{0}".format(self.owner.path + "\{0}".format(self.owner._mods_folder))])

                        if sys.platform == "linux":
                            os.system('xdg-open "%s"' % self.path + "/{0}".format(self.__mods_folder))

                    imgui.unindent(imgui.get_window_size()[0]-200 -self.config.selected_size * 2)




                    imgui.separator()
                    



                
                    if self.toggle_hide__mods == False:

                                        
                        for i in self.owner._mod_list:
                            
                            if self.show_thumbnail == True :

            
                                imgui.image(i.icon[0],self.config.thumbnail_size,self.config.thumbnail_size)    
                                if imgui.is_item_hovered():  
                                    if imgui.begin_tooltip(): 
                                            
                                            imgui.image(i.icon[0],i.icon[1],i.icon[2])
                                        
                                    imgui.end_tooltip()
                            


                                imgui.same_line()
                            
                            _, i.active = imgui.checkbox(i.name, i.active)
                          
                            if imgui.is_item_hovered():
                                    self.highlight = i
                                    

                            if imgui.is_item_edited:
                                self.activation_list(i.active,i.location) 
                            

                        if len(self.owner._mod_list) == 0:
                            imgui.text(self.no_mod_message.format(self.__mods_folder))
                            imgui.text(self.tip_message)
                                
                                

                            


            
                #mods ui list
                if os.path.isdir(self.owner.path + "/" + self.owner.mods_folder) == True:
                
                    imgui.separator()
                    imgui.text(self.owner.mods_folder + ": " + str(len(self.owner.mod_list)))

                    

                    #Hide
                    imgui.same_line()
                    imgui.indent(imgui.get_window_size()[0]-200  - self.config.selected_size * 2)
                    if imgui.radio_button("Collapse##Hide mods",self.toggle_hide_mods):
                        self.toggle_hide_mods = not self.toggle_hide_mods
                        self.config.config_setting("Preset")

                    imgui.unindent(imgui.get_window_size()[0]-200  - self.config.selected_size * 2)
                    




                    #Open button  
                    
                    imgui.same_line() 
                    if imgui.button("Open##Open mods Folder"):
                        if sys.platform == "win32":

                            subprocess.Popen(['explorer', "{0}".format(self.owner.path + "\{0}".format(self.owner.mods_folder))])

                        if sys.platform == "linux":
                            os.system('xdg-open "%s"' % self.owner.path + "/{0}".format(self.owner.mods_folder))
    
                      
                    
        

                    imgui.separator() 





                    if self.toggle_hide_mods == False:
                        
                            #imgui.indent(20)
                        for i in self.owner.mod_list:

                            if self.show_thumbnail == True:
                                
                                
                                imgui.image(i.icon[0],self.config.thumbnail_size,self.config.thumbnail_size)  
                                if imgui.is_item_hovered():  
                                    if imgui.begin_tooltip():   

                                        imgui.image(i.icon[0],i.icon[1],i.icon[2])

                                    imgui.end_tooltip()


                                imgui.same_line()
                    
                            _, i.active = imgui.checkbox(i.name, i.active)
                            if imgui.is_item_hovered():
                                self.highlight = i

                            self.activation_list(i.active,i.location) 
                                                


                        if len(self.owner.mod_list) == 0:
                            imgui.text(self.no_mod_message.format(self.owner.mods_folder))
                            imgui.text(self.tip_message)
                            
                            
                





                #logicmods ui list
                if os.path.isdir(self.owner.path + "/" + self.owner.logicmods_folder) == True:
                    imgui.separator()
                    imgui.text(self.owner.logicmods_folder + ": " + str(len(self.owner.logicmods_list)))
                    
                    
                


                    #Hide 
                    imgui.same_line()
                    imgui.indent(imgui.get_window_size()[0]-200  - self.config.selected_size * 2)
                    if imgui.radio_button("Collapse##Hide logicmods",self.toggle_hide_logicmods):
                            self.toggle_hide_logicmods = not self.toggle_hide_logicmods
                            self.config.config_setting("Preset")
                    imgui.unindent(imgui.get_window_size()[0]-200 - self.config.selected_size * 2)




                    #Open button
                    imgui.same_line()          
                    
                    if imgui.button("Open##Open logicmods Folder"):
                        if sys.platform == "win32":
                            subprocess.Popen(['explorer', "{0}".format(self.owner.path + "\{0}".format(self.owner.logicmods_folder))])

                        if sys.platform == "linux":
                            os.system('xdg-open "%s"' % self.owner.path + "/{0}".format(self.owner.logicmods_folder))

                        
                   
                                
            


                    imgui.separator()
                        





                    if self.toggle_hide_logicmods == False:

                        #imgui.indent(20)
                        for i in self.owner.logicmods_list:
                                
                            if self.show_thumbnail == True:
                                
                                imgui.image(i.icon[0],self.config.thumbnail_size,self.config.thumbnail_size)   
                                
                                if imgui.is_item_hovered():  
                                    if imgui.begin_tooltip():   

                                        imgui.image(i.icon[0],i.icon[1],i.icon[2])

                                        
                                    imgui.end_tooltip()

                                imgui.same_line()


                            _, i.active = imgui.checkbox(i.name, i.active)
                            if imgui.is_item_hovered():
                               
                                self.highlight = i


                            self.activation_list(i.active,i.location) 
                                                


                        if len(self.owner.logicmods_list) == 0:
                            imgui.text(self.no_mod_message.format("logicmods folder"))
                            imgui.text(self.tip_message)
                        

        
        


        def activation_list(self,state,dir):



                if os.path.isdir(dir) == True:
                    for file in os.listdir(dir):
                        if file.endswith("pak") | file.endswith("pak-x") | file.endswith("ucas") | file.endswith("ucas-x") | file.endswith("utoc") | file.endswith("utoc-x"):
                                                        
                            if state == True:
                                if file.endswith("-x"):
                                    os.rename(dir +"/" + file, dir +"/" + file.strip("-x"))
                                    
                            elif state == False:
                                if not file.endswith("-x"):
                                    os.rename(dir +"/" + file, dir +"/" + file +"-x")
            
        




        def ui_treeview(self, directory, indent=0):


                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    

                
                    if item.lower() == self.owner._mods_folder.lower():
                            
                        _,self.toggle__mods = imgui.checkbox("##"+"mm",self.toggle__mods)
                        if imgui.is_item_edited():
            
                            self.activation_tree(self.toggle__mods,self.path +"/{0}".format(self.__mods_folder)) 
                        imgui.same_line()

                
                    if item.lower() == self.owner.mods_folder.lower():

                        _,self.toggle_mods = imgui.checkbox("##"+"m",self.toggle_mods)
                        if imgui.is_item_edited():
                                        
                                
                            self.activation_tree(self.toggle_mods,self.owner.path +"/{0}".format(self.owner.mods_folder)) 
                        imgui.same_line()
                                

                    if item.lower() == self.owner.logicmods_folder.lower():

                        _,self.toggle_logicmods = imgui.checkbox("##"+"l",self.toggle_logicmods)
                        if imgui.is_item_edited():
                                        
                                
                            self.activation_tree(self.toggle_logicmods,self.owner.path +"/{0}".format(self.owner.logicmods_folder)) 
                        imgui.same_line()
                        
                            
                



                    if os.path.isdir(item_path):
                        
                            
                            for i in self.owner._mod_list:
                                    
                                    if item == i.name:
                                        
                                        _,i.active = imgui.checkbox("##"+i.name,i.active)
                                        
                                        if imgui.is_item_edited():
                                            
                                            self.toggle__mods  = True
                                            self.activation_tree(i.active,i.location) 
                                        imgui.same_line()

                        
                            for i in self.owner.mod_list:
                                
                                    if item == i.name:
                                    
                                        _,i.active = imgui.checkbox("##"+i.name,i.active)
                                        
                                        if imgui.is_item_edited():
                                            
                                            self.toggle_mods = True
                                            self.activation_tree(i.active,i.location) 
                                        imgui.same_line()

                        


                            for i in self.owner.logicmods_list:
                                    
                                    if item == i.name:
                                        
                                        _,i.active = imgui.checkbox("##"+i.name,i.active)
                                        
                                        if imgui.is_item_edited():
                                            
                                            self.toggle_logicmods = True
                                            self.activation_tree(i.active,i.location) 
                                        imgui.same_line()



                            
                            

                        
                            
                            if imgui.tree_node( "Directory: " + item, imgui.TREE_NODE_OPEN_ON_ARROW ):
                                imgui.indent(5)
                            
                                #files
                                for i in os.listdir(item_path):
                                        
                                        if os.path.isfile(item_path +"/" + i):
                                            imgui.indent(33)
                                            imgui.text("File: " + i)
                                        
                                            imgui.indent(-33)
                                
                            
                                self.ui_treeview(item_path, indent+1)
                        

                                imgui.tree_pop()
                                imgui.indent(-5)
                            
                        


        
        def activation_tree(self,state,directory, indent = 0):
            
        
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
            
                    

                if os.path.isdir(item_path):
                    
                    
                    for i in self.owner._mod_list:
                            
                            if item == i.name:
                                
                                i.active = state


                    
                    for i in self.owner.mod_list:
                            
                            if item == i.name:
                                
                                i.active = state  
                

                    
                    for i in self.owner.logicmods_list:
                            
                            if item == i.name:
                                
                                i.active = state



                    #print(f"{'  ' * indent}Directory: {item}")
                    
                
                    for i in os.listdir(item_path):
                        if os.path.isfile(item_path +"/" + i):
                            #print(f"{'  ' * (indent+1)}File: {i}")
                            pass

                
                    self.activation_tree(state,item_path)



            
                else:
                    

                    
                
                    if os.path.isfile(item_path):
                            file = item
                            if file.endswith("pak") | file.endswith("pak-x") | file.endswith("ucas") | file.endswith("ucas-x") | file.endswith("utoc") | file.endswith("utoc-x"):
                                                                    
                                if state == True:
                                        if file.endswith("-x"):
                                            os.rename(directory +"/" + file, directory +"/" + file.strip("-x"))
                                                
                                        else:
                                            pass
                                    
                                if state == False:
                                        if file.endswith("-x"):
                                            pass
                                        else:
                                            
                                            os.rename(directory +"/" + file, directory +"/" + file +"-x")

    
        



        def main_infoviewbox(self):
            
            
            
            #imgui.set_next_window_position(glfw.get_window_size(self.window)[0]-200,0)
            with imgui.begin("" + "Info",False | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS  |imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE):
              
                if self.highlight == None:
                    pass
                else:
                    
                    imgui.indent(50)
                    imgui.image(self.highlight.icon[0],self.highlight.icon[1]*1.5,self.highlight.icon[2]*1.5)


                    imgui.unindent(50)
                    imgui.separator()
                    imgui.push_font(self.config.fonts[2][1][12][1])
                    #imgui.set_window_font_scale(3)   
                    imgui.text("Name: " + self.highlight.description.name)    
                    imgui.text("Aurther: " + self.highlight.description.aurther)
                    imgui.text("Description: " + self.highlight.description.description)
                    imgui.text("URL: " + self.highlight.description.url)
                    imgui.text("Type: " + self.highlight.description._type)
                    imgui.pop_font()
           





        def main_window_box(self):

            
            win_w, win_h = glfw.get_window_size(self.window)
            fb_w, fb_h = glfw.get_framebuffer_size(self.window)
            scaling = max(float(fb_w) / win_w, float(fb_h) / win_h)






            imgui.set_next_window_size(scaling * (glfw.get_window_size(self.window)[0]),scaling *  (glfw.get_window_size(self.window)[1]-26))
            imgui.set_next_window_position(0,26)
            

            imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE,0.0)
            
            with imgui.begin("##" + "manager",False,imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE):
         
            
                imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING,12)  

                if self.toggle_viewmode == True:
                    self.ui_treeview(self.owner.path)
                
                else:

                    self.ui_listview()
                imgui.pop_style_var()    
            imgui.pop_style_var()    




            
            




        def run(self):
            
            
            imgui.push_style_color(imgui.COLOR_TEXT,*self.config.font_colour)
            imgui.push_style_color(imgui.COLOR_BUTTON,*self.config.button_colour)
            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED,*self.config.button_colour)
            imgui.push_style_color(imgui.COLOR_CHECK_MARK,1,1,1)
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,*self.config.bg_colour)

            
            imgui.push_font(self.config.selected_font) 

            if os.path.isdir(self.owner.path) == True:


                #self.main_filter_bar()
                self.main_window_bar()
                self.main_window_box()
                #self.main_infoviewbox()
                
            
            else:
              
                imgui.begin("Error")
                imgui.text(self.path_error_message)
                if imgui.button("Close##Close Window"):
                    glfw.set_window_should_close(self.window,glfw.TRUE)
                imgui.end()
                
            imgui.pop_font()


            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
         





         


    def key_callback( self, window,key, scancode, action, mods):

        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.terminate()



    def framebuffer_size_callback(self, window,w,h):
        glViewport(0, 0, w, h)
      


    
    
    def ui_images(self, image = None):

            if image == None:
                image = self.window_icon
            

            img = Image.open(image).convert("RGBA")
            size = (400,400)
            img.thumbnail(size)


            imdata = img.tobytes() 
            width, height = img.size
            
            texname = glGenTextures(1)

            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            glBindTexture(GL_TEXTURE_2D, texname)
            glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width, height,0,GL_RGBA,GL_UNSIGNED_BYTE,imdata)
            glGenerateMipmap(GL_TEXTURE_2D)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glBindTexture(GL_TEXTURE_2D,0)





        
        

            return [texname,width,height]

        



    def clear_images(self):

           
        for i in self._mod_list:
            if i.icon != None:
                glDeleteTextures([i.icon[0]])
                i.icon = None

        for i in self.mod_list:
            if i.icon != None:
                glDeleteTextures([i.icon[0]])
                i.icon = None

        for i in self.logicmods_list:
            if i.icon != None:
                glDeleteTextures([i.icon[0]])
                i.icon = None





    def main(self):
            
            # Initialize the library
            if not glfw.init():
                return


            #configuation
            config = self.configs(self)
            config.window_check()

            # Create a windowed mode window and its OpenGL context
            glfw.window_hint(glfw.RESIZABLE,glfw.TRUE)
            glfw.window_hint(glfw.MAXIMIZED, config.maximised)
           
        
            window = glfw.create_window(600, 600, "Tekken 8 Mod Manager " , None, None)

            
            glfw.set_framebuffer_size_callback(window,self.framebuffer_size_callback)
            glfw.set_key_callback(window,self.key_callback)
            

                

            #Check if the program is run from binary or srcipt and which platform.
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                print('running in a PyInstaller bundle')
                
                if sys.platform == "win32":
                    self.path = os.path.dirname(sys.executable) + "\Polaris\Content\Paks"
                    self.pure_dir = os.path.dirname(sys.executable)
                elif sys.platform == "linux":
                    self.path = os.path.dirname(sys.executable) + "/Polaris/Content/Paks"
                    self.pure_dir = os.path.dirname(sys.executable)

            else:
                
                print('running in a normal Python process')
                
                if sys.platform == "win32":
                    self.path =  os.path.dirname(os.path.abspath(__file__)) + "\Polaris\Content\Paks"
                    self.pure_dir = "None"
                elif sys.platform == "linux":
                    self.path =  os.path.dirname(os.path.abspath(__file__)) + "/Polaris/Content/Paks"
                    self.pure_dir = "None"
                
            



            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                    
                    self.window_icon = os.path.abspath(os.path.dirname(__file__)) + "\\assets\\branding\icon.ico"
                    self.banner = os.path.abspath(os.path.dirname(__file__)) + "\\assets\\branding\\banner.png"
                
            else:
                
                    
                    if sys.platform == "win32":
                        self.window_icon =  os.path.dirname(os.path.abspath(__file__)) +"/assets/branding/icon.ico"
                        self.banner = os.path.abspath(os.path.dirname(__file__)) + "/assets/branding/banner.png"

                    elif sys.platform == "linux":

                        self.window_icon =  os.path.dirname(os.path.abspath(__file__)) +"/assets/branding/icon.ico"
                        self.banner = os.path.abspath(os.path.dirname(__file__)) + "/assets/branding/banner.png"
                        





            img = Image.open(self.window_icon)
            glfw.set_window_icon(window,1,img)
            






            if not window:
                glfw.terminate()
                return



            # Make the window's context current
            glfw.make_context_current(window)
            glfw.swap_interval(1)
            


            # initilize imgui context (see documentation)
            imgui.create_context()
            impl = GlfwRenderer(window)




            
            #setup
            config.window = window
            config.get_font_collection()
     

            #ui class
            self.ui = self.windows_ui(self,window,impl,config)
            
            #apply setting to ui
            config.ui_check()
            impl.refresh_font_texture()
            
            # Generate mods list before program starts
            self.ui.generate_modlist()
           
            


          
            # Loop until the user closes the window
            while not glfw.window_should_close(window):
                # Render here, e.g. using pyOpenGL

                
                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)

                
                
            
                imgui.new_frame()
              
                
                
                self.ui.run()
                
          

                #imgui.show_demo_window()
               

                #Rendering
                imgui.render()
                impl.render(imgui.get_draw_data())
                





                # Swap front and back buffers
                glfw.swap_buffers(window)
                

                # Poll for and process events
                glfw.poll_events()
                impl.process_inputs()


            #clean up
            impl.shutdown()
            


            glfw.destroy_window(window)
            glfw.terminate()
            





program = mod_manager()


if __name__ == "__main__":
    program.main()



