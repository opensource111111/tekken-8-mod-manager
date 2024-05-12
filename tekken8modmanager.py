import os
import sys
import subprocess
import configparser
import math
import webbrowser
import ast
import glfw
import json


import imgui
from imgui.integrations.glfw import GlfwRenderer

from OpenGL.GL import *
import OpenGL.GL as gl

from PIL import Image, ImageOps




"""
class customs_overrides:
    #https://tekkenmods.com/article/78/tekken-8-general-information
    lower_body = "lower_body"
    upper_body ="upper_body"
    extra = "extra"
    face = "face"
    facial_hair = "facial_hair"
    glasses = "glasses"
    hair = "hair"
    head = "head"
    full_body = "full_body"
    shoes = "Shoe"
    full_head = "full_head"
    eyes = "eyes"
    Accessory = " Accessory"
    character = None # [All, character name]
"""  



class description_format:
    name : str = ""
    author : str = ""
    url : str = ""
    description : str = ""
    category : str = ""  
    overrides = [] 
    
    



class mod_list_format:
    name : str = ""
    location : str = ""
    folder : str = ""
    active : bool = True
    icon = []
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



        self.ui = None
        self.window = None
        self.impl = None
        self.config = None
        self.io = None
   
        self.scoll = 0

        self.version = 1.9


    class configs:

        def __init__(self,owner):
            self.owner = owner


            #fonts
            self.selected_font = None
            self.selected = 4
            self.selected_size = 9
            self.fonts = []
            self.font_colour = 1,1,1,1


            
            self.style = None
            self.dpi_scale = 1.0

                
            #mod data
            self.mod_list : mod_list_format = []


            #window
            self.maximised = False
            

            #warning (WIP)
            self.conflict_warning = False

            self.config = configparser.ConfigParser()



        def window_check(self):
            
         
            filecheck = self.config.read('tekken8modmanager.ini')
            if filecheck:
    
                for i in self.config.sections():
                    if i =="Preset":
                        self.maximised= self.config.getboolean('Preset', 'maximised',fallback=False)
                        



        def ui_check(self):
           
            filecheck = self.config.read('tekken8modmanager.ini')
            if filecheck:
    
                for i in self.config.sections():
                    if i =="Preset":
                        self.owner.ui.toggle_viewmode = self.config.getboolean('Preset', 'viewmode',fallback=False)
                        self.owner.ui.show_thumbnail = self.config.getboolean('Preset', 'thumbnail', fallback=False)
                        self.owner.ui.thumbnail_size =  self.config.getint('Preset', 'thumbnail_size', fallback=50)
                        

                        #colours
                        temp = self.config.get('Preset', 'font_colour', fallback= (1,1,1,1))
                        if temp != (1,1,1,1):
                            temp2 = temp.replace("(","").replace(")","").replace("[","").replace("]","").replace(",","").split()
                            self.font_colour = list(map(float,temp2))
                        
                        
                        temp = self.config.get('Preset', 'button_colour', fallback=(0,0.290,0.783,1))
                        if temp != (0,0.290,0.783,1):
                            temp2 = temp.replace("(","").replace(")","").replace("[","").replace("]","").replace(",","").split()
                            self.owner.ui.button_colour = list(map(float, temp2))


                        temp = self.config.get('Preset', 'bg_colour', fallback=(0,0,0,1))
                        if temp != (0,0,0,1):
                            temp2 = temp.replace("(","").replace(")","").replace("[","").replace("]","").replace(",","").split()
                            self.owner.ui.bg_colour = list(map(float, temp2))




                        #font
                        self.selected =self.config.getint('Preset', 'font_index',fallback=4)
                        self.selected_size =self.config.getint('Preset', 'font_size_index',fallback=9)
                        self.config_font_type(self.fonts[self.selected][1][self.selected_size][1])
                        

                        #UI Scale(WIP)
                        self.dpi_scale =  self.config.getfloat('Preset', 'dpi_scale', fallback=1.0)
                        self._imgui_scale_all_sizes(self.style,self.dpi_scale,self.dpi_scale)

                        
                        #conflict (WIP)
                        #self.conflict_warning =  self.config.getboolean('Preset', 'warning', fallback=False)
                        
                        #docked
                        self.owner.ui.docked=  self.config.getboolean('Preset', 'docked', fallback=False)



            
        def config_setting(self,header = "Preset"):
            
            with open('tekken8modmanager.ini', 'w') as configfile:
                self.config['Preset'] = {'viewmode': str(self.owner.ui.toggle_viewmode),'Thumbnail': str( self.owner.ui.show_thumbnail),'maximised' : str(self.maximised), "font_index" : str(self.selected),"font_size_index" : str(self.selected_size),"thumbnail_size" : str(self.owner.ui.thumbnail_size), "font_colour" : str(self.font_colour),"button_colour" : str(self.owner.ui.button_colour), "bg_colour" : str(self.owner.ui.bg_colour), 'dpi_scale' : str(self.dpi_scale) , 'warning' : str(self.conflict_warning), 'docked' : str(self.owner.ui.docked)}
                self.config.write(configfile)






        def get_font_collection(self):
                
             
                
                imgui.get_font_size()
                io = imgui.get_io()
                
                win_w, win_h = glfw.get_window_size(self.owner.window)
                fb_w, fb_h = glfw.get_framebuffer_size(self.owner.window)
                font_scaling_factor = max(float(fb_w) / win_w, float(fb_h) / win_h)
                font_size_in_pixels = 2
                io.font_global_scale /= font_scaling_factor



                for i in os.listdir(os.path.dirname(os.path.abspath(__file__)) +"/assets/fonts"):
                    font = []
                    
                    if i.endswith(".otf") or i.endswith(".ttf"):
                        for jj in range(15):
                            font.append((i + " " + str(font_size_in_pixels) + "px",io.fonts.add_font_from_file_ttf(os.path.dirname(os.path.abspath(__file__)) +"/assets/fonts/" + i , font_size_in_pixels * font_scaling_factor)))
                            font_size_in_pixels +=2
                            

                        font_size_in_pixels = 2
                        self.fonts.append([i,font])


                #hack for user custom fonts
                if os.path.isdir(self.owner.pure_dir +"/assets/fonts"):
                    for i in os.listdir(self.owner.pure_dir +"/assets/fonts"):
                        font = []
                        if i.endswith(".otf") or i.endswith(".ttf"):
                            for jj in range(15):
                                font.append((i + " " + str(font_size_in_pixels) + "px",io.fonts.add_font_from_file_ttf(self.owner.pure_dir +"/assets/fonts/" + i , font_size_in_pixels * font_scaling_factor)))
                                font_size_in_pixels +=2
                            font_size_in_pixels = 2
                            self.fonts.append([i,font])


                
               
                self.selected_font = self.fonts[4][1][9][1]
                
                
            



        def config_font_type(self,name):
            for i in self.fonts[self.selected][1][self.selected_size]:
                
                self.selected_font = i
               



        
        def _imgui_scale_all_sizes (self, style, hscale: float, vscale: float) -> None:
            """pyimgui is missing ImGuiStyle::ScaleAllSizes(); this is a reimplementation of it.
                 #How do I scale the GUI?
             #https://github.com/ocornut/imgui/issues/6967#issuecomment-1793465530"""
            
            scale = max(hscale, vscale)
           
            def scale_it (attrname: str) -> None:
                value = getattr(style, attrname)
                
                if isinstance(value, imgui.Vec2):
                    value = imgui.Vec2(math.trunc(value.x * hscale), math.trunc(value.y * vscale))
                    v = value
                    setattr(style, attrname, value)
                else:
                    setattr(style, attrname, math.trunc(value * scale))
                
            #scale_it("window_padding")
            scale_it("window_rounding")
            scale_it("window_min_size")
            scale_it("child_rounding")
            scale_it("popup_rounding")
            scale_it("frame_padding")
            scale_it("frame_rounding")
            scale_it("item_spacing")
            scale_it("item_inner_spacing")
            scale_it("cell_padding")
            scale_it("touch_extra_padding")
            scale_it("indent_spacing")
            scale_it("columns_min_spacing")
            scale_it("scrollbar_size")
            scale_it("scrollbar_rounding")
            scale_it("grab_min_size")
            scale_it("grab_rounding")
            scale_it("log_slider_deadzone")
            scale_it("tab_rounding")
            scale_it("tab_min_width_for_close_button")
            scale_it("display_window_padding")
            scale_it("display_safe_area_padding")
            scale_it("mouse_cursor_scale")




        def config_default_settings(self):
        

            
            self.selected = 4
            self.selected_size = 9
            self.selected_font = self.fonts[4][1][9][1]
            self.font_colour = 1,1,1,1
            self.maximised = False
            self.dpi_scale = 1.0
            self.conflict_warning = False
            self.owner.ui.docked = True
            self.owner.ui.show_thumbnails = True
            self.owner.ui.button_colour = 0,0.290,0.783,1
            self.owner.ui.bg_colour = 0,0,0,1
            self.owner.ui.thumbnail_size = 50


            self.config_setting()

            



        


        def get_description(self,location = None):
            
            description = configparser.ConfigParser()
            description_info = description_format()
            
            if description.read(location):
                description_info.name = description.get("Mod","name", fallback="").replace('"',"")
                #print(description_info.name)
               
                description_info.author = description.get("Mod","author", fallback="").replace('"',"")
                #print(description_info.aurther)
                
                description_info.description = description.get("Mod","description", fallback="").replace('"',"")
                #print(description_info.description)
                
                description_info.url = description.get("Mod","url", fallback="none").replace('"',"")
                #print(decription_info.url)
                
                description_info.category =  description.get("Mod","category", fallback="").replace('"',"")
                #print(description_info.category)
                        


                """
                        f = []
                        for i in description["Override"]:

                        
                            f.append([i,description["Override"][i]])

                        description_info.overrides = f
                """

            return description_info
                    
        
   

        def update_description(self,location = None):

            description = configparser.ConfigParser()
               
            
            with open(location +"/" + 'mod.ini', 'w') as descrp:
                description['Mod'] = {'name': '"' + str(self.owner.ui.highlight.description.name) + '"','author': '"' + str( self.owner.ui.highlight.description.author) + '"','url': '"' +  str( self.owner.ui.highlight.description.url) + '"' ,'description': '"' + str( self.owner.ui.highlight.description.description) + '"','category': '"' + str( self.owner.ui.highlight.description.category ) + '"'}
                description.write(descrp)
           
                    

        

        def generate_modlist(self):
            
            self.owner.clear_images()

            self.mod_list.clear()
           
            

    

            default_icon = self.owner.ui_images() 
            


            if os.path.isdir(self.owner.path):
  
                # look through the root mod folders.
                for root, dirnames, filenames  in os.walk(self.owner.path):
                        
                        if self.owner.ui.toggle_viewmode == False:
                            for i in os.listdir(root):
                                if os.path.isdir(root + "/" + i):
                                   for file in os.listdir(root + "/" + i):
                                        
                                        if file.endswith("pak") or file.endswith("pak-x") or file.endswith("ucas") or file.endswith("ucas-x") or file.endswith("utoc") or file.endswith("utoc-x"):
                                    
                                            new = mod_list_format()
                                            new.folder = root
                                            new.name = i
                                            
                                            new.location = root  + "/" + i
                                            new.icon = [default_icon]
                                            new.description = self.owner.config.get_description( root  + "/" + i + "/mod.ini")
                                            f = []
                                            for filecheck in os.listdir(root  + "/" + i):
                                                                        
                                                if filecheck.endswith(".jpg") or filecheck.endswith(".jpeg") or filecheck.endswith(".png") or filecheck.endswith(".webp") or filecheck.endswith(".bmp") :

                                                    f.append(self.owner.ui_images(root  + "/" + i + "/" + filecheck))
                                                                        
                                                if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                                                
                                                    if filecheck.endswith("-x"):
                                                        new.active = False
                                                                                    
                                                    else:
                                                        new.active = True
                                                if f != []:  
                                                    new.icon = f 
                                                                
                                                                    
                                                                        
                                            self.mod_list.append(new)
                                            break
                                                            
                        
                        else:
                            for i in os.listdir(root):               

                                if os.path.isdir(root + "/" + i):

                                    new = mod_list_format()
                                    new.folder = root
                                                     
                                    new.name = i
                                    new.location = root  + "/" + i
                                    new.icon = [default_icon]
                                    new.description = self.owner.config.get_description( root  + "/" + i + "/mod.ini")

                                    f = []                
                                    for filecheck in os.listdir(root  + "/" + i):

                   
                                        if filecheck.endswith(".jpg") or filecheck.endswith(".jpeg") or filecheck.endswith(".png") or filecheck.endswith(".webp") or filecheck.endswith(".bmp"):

                                            f.append(self.owner.ui_images(root  + "/" + i + "/" + filecheck))
                                                                        
                                

                                        if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                                        
                                            if filecheck.endswith("-x"):
                                                new.active = False
                                                                            
                                            else:
                                                new.active = True
                                                                    


                                        if f != []:  
                                            new.icon = f                     
                                                        
                                                                
                                    self.mod_list.append(new)
                                                                
                                                
                               


            self.mod_list.sort(reverse=False,key=name_sort)
               
                        


    class windows_ui:
        
        def __init__(self, owner):
            self.owner = owner
            
            self.source_code = "https://github.com/opensource111111/tekken-8-mod-manager"

            #ui toggles
            self.toggle_about : bool = False
            self.toggle_viewmode : bool = False
            self.show_thumbnail : bool = False
            self.thumbnail_size : int = 50
            self.show_window_setting : bool = False
            self.category = ["All","Character Customization","Stage","Sound","UI/HUD","Movesets/Animations","Miscellaneous"]
            self.filter_bar : str = self.category[0]
            self.filter_select = 0
            self.highlight : mod_list_format = None
            self.docked = False
            self.toggle_edit_information = False
            self.edit_information_select_index = 0

            self.button_colour = 0,0.290,0.783,1
            self.bg_colour = 0,0,0,1

   

            #ui messages
            self.about_logo = self.owner.ui_images(self.owner.banner)
            self.about_message : str = "Created by Beanman"
            self.no_mod_message : str = "No mods were found inside the {0} folder"
            self.tip_message : str = "Tip: Please make sure that each mod has its own separate folder."
            self.path_error_message : str = "This program was not placed inside {0}.".format("Steam\steamapps\common\Tekken 8")
           

            self.f =  500 * (self.owner.config.selected_size * 0.1)
            

            """
            self.override_icons = []
            for i in os.listdir(os.path.dirname(os.path.abspath(__file__)) +"/assets/override_icons"):
                self.override_icons.append([i,self.owner.ui_images(os.path.dirname(os.path.abspath(__file__)) +"/assets/override_icons/" + i)])
           
            """




        def main_filter_bar(self):
            
    
         
            
            
            imgui.text("Filter:")
            imgui.same_line()
            _all = 0
            cc = 0
            st = 0
            s = 0
            ui = 0
            ma = 0
            m = 0

            for i in self.owner.config.mod_list:
                _all+=1
                if i.description.category.startswith("Character Customization"):
                    cc+=1
                if i.description.category.startswith("Stage"):
                    st+=1
                if i.description.category.startswith("Sound"):
                    s+=1
                if i.description.category.startswith("UI/HUD"):
                    ui+=1
                if i.description.category.startswith("Movesets/Animations"):
                    ma+=1
                
                if i.description.category.startswith("Miscellaneous"):
                    m+=1



            





            category = ["All: " + str(_all),"Character Customization: " + str(cc),"Stage: " + str(st),"Sound: "+ str(s),"UI/HUD: " + str(ui),"Movesets/Animations: "+ str(ma),"Miscellaneous: " + str(m)]

            with imgui.begin_combo("##filter_combo", category[self.filter_select]) as combop:
                if combop.opened:
                    for i, item in enumerate(category):
                        is_selected = (i == self.filter_select)
                        if imgui.selectable(item, is_selected)[0]:
                            self.filter_select = i
                            self.filter_bar = self.category[i]
                           

                        # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)
                        if is_selected:
                            imgui.set_item_default_focus()
            


            
            # Open Root Directory
            imgui.same_line()        
                   
            if imgui.button("Open Root Directory##OpenFolder"):
                if sys.platform == "win32":

                    subprocess.Popen([f'explorer', "{0}".format(self.owner.path)])
                    
                if sys.platform == "linux":
                    os.system('xdg-open "%s"' % self.owner.path)

           

            

        def main_window_bar(self):
            imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE,1.0)
            
            with imgui.begin_main_menu_bar():
                
            

             
                #Options button
                if imgui.begin_menu("Options"):
    
                
                    if imgui.button("Window Configuration"):
                    
                        imgui.open_popup("Window Configuration")
                        
                    
                    #option pop-up
                    imgui.set_next_window_size_constraints((600,400), (600, 400))
                    with imgui.begin_popup_modal("Window Configuration",imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_DECORATION) as select_popup:
                        if select_popup.opened:
                            
                            #Window & UI
                            imgui.separator()
                            imgui.text("Window & UI Settings")
                            imgui.separator()


                            """
                            #dpi scale
                            imgui.text("UI Scale:")
                            imgui.same_line()
                            changed, self.owner.config.dpi_scale = imgui.input_float("##scale", self.owner.config.dpi_scale)
                            if changed:
                                self.owner.config._imgui_scale_all_sizes(self.owner.config.style,self.owner.config.dpi_scale,self.owner.config.dpi_scale)
                                self.owner.config.config_setting()
                            """
                        


                            #maximised button
                            imgui.text("Start Window Maximised:")
                            imgui.same_line()
                            changed,self.owner.config.maximised = imgui.checkbox("##m",self.owner.config.maximised)
                            if changed:
                                self.owner.config.config_setting()


                            #show thumbnail button
                            imgui.text("Show Thumbnail") 
                            imgui.same_line()
                            _, self.owner.ui.show_thumbnail = imgui.checkbox("##Show Thumbnail",self.owner.ui.show_thumbnail)
                            if imgui.is_item_edited():
                                self.owner.config.config_setting()
                            
                            #Scale Thumbnail
                            imgui.text("Thumbnail Scale") 
                            imgui.same_line()
                            self.owner.ui.thumbnail_size = imgui.slider_int("##Thumbnail_scale",self.owner.ui.thumbnail_size,50,100)[1]
                            if imgui.is_item_edited():
                                self.owner.config.config_setting()


                            
                            #docking description box
                            imgui.text("Dock Description Box:")
                            imgui.same_line()
                            changed, self.owner.ui.docked = imgui.checkbox("##dockinformation", self.owner.ui.docked)
                            if changed:
                                self.owner.config.config_setting()


                            
                            self.spacing(5)
                         



                            #font setting
                            imgui.text("Colour Setting")
                            imgui.separator()

                            #Change Button Colour 
                            imgui.text("Button Colour:")
                            imgui.same_line()
                            changed, self.owner.ui.button_colour = imgui.color_edit4("##button_colour",*self.owner.ui.button_colour,imgui.COLOR_EDIT_NO_ALPHA)
                            if changed:
                                self.owner.config.config_setting()

                            #Change Background Colour 
                            imgui.text("Background Colour:")
                            imgui.same_line()
                            changed , self.owner.ui.bg_colour = imgui.color_edit4("##backgound_colour",*self.owner.ui.bg_colour,imgui.COLOR_EDIT_NO_ALPHA)
                            if changed:
                                self.owner.config.config_setting()

                            


                        
                            

                            
                            self.spacing(5)



                            #font setting
                            imgui.text("Font Setting")
                            imgui.separator()
                            imgui.text("Font Style:")
                            imgui.same_line()
                            
                            items = []
                            for i in self.owner.config.fonts:
                        
                                items.append(i[0])
                   
                          
                            with imgui.begin_combo("##dfff",items[self.owner.config.selected]) as combo:
                                if combo.opened:
                                    for i, item in enumerate(items):
                                        is_selected = (i == self.owner.config.selected)
                                        if imgui.selectable(item, is_selected)[0]:
                                            self.owner.config.selected = i
                                            self.owner.config.config_font_type(items[i])
                                            self.owner.config.config_setting()
                                                    


                                        # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)
                                        if is_selected:
                                            imgui.set_item_default_focus()
                            items.clear()





                            imgui.text("Font Size:")
                            imgui.same_line()
                            
                            items = []
                            for i in self.owner.config.fonts[self.owner.config.selected][1]:
                                items.append(i[0])
                                
                                
                            
                            
                            with imgui.begin_combo("##dffeef",items[self.owner.config.selected_size]) as combos:
                                if combos.opened:
                                    for i, item in enumerate(items):
                                        is_selected = (i == self.owner.config.selected_size)
                                        if imgui.selectable(item, is_selected)[0]:
                                            self.owner.config.selected_size = i
                                            self.owner.config.config_font_type(items[i])
                                            self.owner.config.config_setting()
                                                    


                                        # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)
                                        if is_selected:
                                            imgui.set_item_default_focus()




                            imgui.text("Font Colour:")
                            imgui.same_line()
                            _, self.owner.config.font_colour = imgui.color_edit4("##font_colour",*self.owner.config.font_colour,imgui.COLOR_EDIT_NO_ALPHA)
                          
                            self.owner.config.config_setting()






                            self.spacing(5)



                            """
                            #Others
                            imgui.text("Others")
                            imgui.separator()

                     
                            imgui.text("Conflict Warning (WIP):")
                            imgui.same_line()
                            changed, self.owner.config.conflict_warning = imgui.checkbox("##me",self.owner.config.conflict_warning)
                            if changed:
                                self.owner.config.config_setting()
                           
                            """
                            

                            self.spacing(3)



                            imgui.separator()
                            if imgui.button("Reset to Default"):
                                self.owner.config.config_default_settings()
                            
              

                    imgui.end_menu()
                    
                
                

                #------------------------------------------------------------------------------------



                
                #view modes button
                if imgui.begin_menu("View"):
                    
                    _, list_view = imgui.menu_item("List View")
                    _, tree_view = imgui.menu_item("Tree View")
                    
                    if list_view:
                        self.toggle_viewmode = False
                        self.highlight = None
                        self.toggle_edit_information = False
                        self.owner.config.generate_modlist()
                        self.owner.config.config_setting()
                    

                    if tree_view:
                        self.toggle_viewmode  = True
                        self.highlight = None
                        self.toggle_edit_information = False
                        self.owner.config.generate_modlist()
                        self.owner.config.config_setting()
                        


                    
        
                    imgui.end_menu()



                #------------------------------------------------------------------------------




                
                #Help button
                if imgui.begin_menu("Help"):

                    changed,about = imgui.menu_item("About")

                    if changed:
                        if self.toggle_about  == True:
                            self.toggle_about = False
                        elif self.toggle_about  == False:
                            self.toggle_about  = True
            
                    imgui.end_menu()


                imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE,3.0)
                #about box
                if self.toggle_about:

                    imgui.set_next_window_size_constraints((270,215), (270, 215))
                    imgui.begin("About",False,imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
                
                    
                    imgui.indent(imgui.get_content_region_available_width()*0.1)
                    imgui.image(self.about_logo[0],self.about_logo[1]*0.5,self.about_logo[2]*0.5)
                    imgui.indent(imgui.get_content_region_available_width()*0.06)
                    imgui.text_wrapped(self.about_message)

                    imgui.indent(-imgui.get_content_region_available_width()*0.07)
                    imgui.indent(imgui.get_content_region_available_width()*0.2)
                    
                    if imgui.button("Source Code"):
                        
                        webbrowser.open(self.source_code, new=2)
                   
                    if imgui.is_item_hovered():
                        if imgui.begin_tooltip():         
                            imgui.text(self.source_code)  
                            imgui.end_tooltip()
                        

                    imgui.indent(-imgui.get_content_region_available_width()*0.2)
                    imgui.indent(imgui.get_content_region_available_width()*0.3)
                    if imgui.button("Close"):
                        self.toggle_about = False
                    
                    imgui.indent(-imgui.get_content_region_available_width()*0.3)
                    imgui.end()
                imgui.pop_style_var()



                
                #-------------------------------------------------------------------------------------------



                #Refresh Button
                imgui.set_window_position(20,0)
                if imgui.button("Refresh List"):
                    self.highlight = None
                    self.owner.config.generate_modlist()
                
                    
            imgui.pop_style_var()      
           




        def spacing(self,value):
            for i in range(value):
                imgui.spacing()
                


        """

        def check_conflict(self):

            

            for mod in self.owner._mod_list:
                b = []
                if mod.active:
                    d = mod.description.overrides
                    if len(d)!=0:
                        for i in d:
                            for compare in self.owner._mod_list:
                                if compare.name != mod.name:
                                    if compare.active:
                                        c = compare.description.overrides
                                        
                                        
                                        if len(c)!=0:
                                        
                                            
                                        
                                            for ii in c:
                                                
                                                if i == ii:
                                                    b.append(compare.name)
                                            
                    mod.conflicts = b.copy()
                    b.clear()                
                    #print(mod.conflicts)
                                 
               
        """


        """
        
        def conflict_information(self,mod):
            #conflict warning

            if self.owner.config.conflict_warning == True:
                if mod.active:
                    if len(mod.conflicts) != 0: 
                        imgui.same_line()
                        imgui.text_colored("    ?",214,220,0,1)
                        imgui.same_line()
                        imgui.push_style_color(imgui.COLOR_BUTTON,214,220,0,1)
                        imgui.button("##" + mod.name + "conflicts")
                        imgui.pop_style_color()
                        if imgui.is_item_hovered():
                            with imgui.begin_tooltip():
                                imgui.text("Possible conflicts:")
                                for c in mod.conflicts:
                                    imgui.text(c)

        """
 

     


        def description_box(self):
            

            
 
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,self.owner.ui.bg_colour[0] * 0.5,self.owner.ui.bg_colour[1] * 0.5,self.owner.ui.bg_colour[2] * 0.5,1)
            
             


            if self.highlight != None:
                
                if self.docked:
                    
                    imgui.set_next_window_size(self.scaling() *self.f ,glfw.get_window_size(self.owner.window)[1]-26)
                    imgui.set_next_window_position(self.scaling()  * glfw.get_window_size(self.owner.window)[0]-self.f , self.scaling()   *   26)

                


                f = None
                if self.docked:
                    f = imgui.WINDOW_NO_TITLE_BAR  | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
                else:

                    f = imgui.WINDOW_NO_TITLE_BAR  | imgui.WINDOW_ALWAYS_AUTO_RESIZE |  imgui.WINDOW_NO_COLLAPSE 
                
               
                with imgui.begin(self.highlight.name + "Details",False,f):
                    imgui.indent(13)
                    imgui.text("Description Panel")
                    imgui.separator()
                    imgui.unindent(13)
                    self.spacing(5)
                    imgui.indent(13)
                    imgui.image(self.highlight.icon[int(self.owner.scoll)][0],self.highlight.icon[int(self.owner.scoll)][1],self.highlight.icon[int(self.owner.scoll)][2])
                    imgui.unindent(13)
                    if imgui.is_item_hovered():
                        self.owner.scoll+=self.owner.io.mouse_wheel
                        
                                        
                        if  self.owner.scoll >= len(self.highlight.icon) :
                            self.owner.scoll = 0

                        if  self.owner.scoll <= -1 :
                            self.owner.scoll = len(self.highlight.icon)-1
                                    
                            

                    imgui.separator()




                            
                    # Open button 
                    imgui.same_line()
                    imgui.indent(self.scaling() * imgui.get_window_size()[0]-150* (self.owner.config.selected_size * 0.1))
                    self.spacing(2)

                    if imgui.button("Open Folder##Openefeve_Folder"):
                        if sys.platform == "win32":
                            #print(self.highlight.location)
                            subprocess.Popen(['explorer', "{0}".format(self.highlight.location.replace("/", "\\"))])


                        if sys.platform == "linux":
                            os.system('xdg-open "%s"' % "{0}".format(self.highlight.location.replace("\\", "/")))

                    imgui.unindent(self.scaling() * imgui.get_window_size()[0]-150* (self.owner.config.selected_size * 0.1))


                    
                    if self.toggle_edit_information :
                                
                                
                        imgui.text("Name: ")
                        imgui.same_line()
                        changed, self.highlight.description.name = imgui.input_text("##Name: ",self.highlight.description.name)
                                

                        imgui.text("Created by: ")
                        imgui.same_line()
                        changed, self.highlight.description.author = imgui.input_text("##Created by: ",self.highlight.description.author)
                        
                            
                        imgui.text("Description: ")
                        #imgui.same_line()
                        changed, self.highlight.description.description = imgui.input_text_multiline("##Description: ",self.highlight.description.description,imgui.INPUT_TEXT_CALLBACK_RESIZE )
                                
                        imgui.text("URL: ")
                        imgui.same_line()
                        changed, self.highlight.description.url = imgui.input_text("##URL: ",self.highlight.description.url)
                                
                                
                                
                        imgui.text("Category: ") 
                        imgui.same_line()
                        with imgui.begin_combo("##catergory_edit",self.category[self.edit_information_select_index]) as combo:
                            if combo.opened:
                                for i, item in enumerate(self.category):
                                    is_selected = (i == self.edit_information_select_index)
                                    if imgui.selectable(item, is_selected)[0]:
                                        self.edit_information_select_index = i
                                        self.highlight.description.category = self.category[self.edit_information_select_index]
                                                    
                                        

                                        # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)
                                        if is_selected:
                                            imgui.set_item_default_focus()
                                
                            


                                        
                        self.spacing(5)

                                
                        if imgui.button("Save##"+  self.highlight.name):
                            self.owner.config.update_description(self.highlight.location)
                            self.toggle_edit_information  = False
                        imgui.same_line()


                        if imgui.button("Cancel##"+  self.highlight.name):
                            self.highlight.description = self.owner.config.get_description(self.highlight.location +"/mod.ini")
                            #print(self.highlight.description.description)
                            self.toggle_edit_information  = False
                                

                                    
                        """
                        self.spacing(3)
                        imgui.text("overrides: ")
                        if imgui.button("+"):
                                self.highlight.description.overrides.insert(len(self.highlight.description.overrides),"")
                                

                        for i in self.highlight.description.overrides:
                                    
                            _,self.highlight.description.overrides[0] = imgui.input_text("##d"+ str(i),self.highlight.description.overrides[0])
                            #self.highlight.description.overrides[0]= f[1]
                             #self.highlight.description.overrides[self.highlight.description.overrides.index[i[1]]] = i[1]
                                    

                            imgui.same_line()

                            if imgui.button("-##-"+str(i)):
                                self.highlight.description.overrides.remove(i)
                                    
                                
                        """




                    else:

                                 
                            #information
                            imgui.text("Name: " + self.highlight.description.name)  
                       
                            imgui.spacing()  
                            imgui.text("Created by: " + self.highlight.description.author)
                            imgui.spacing()  
                            imgui.text_wrapped("Description: " + self.highlight.description.description)
                            imgui.spacing()  
                            imgui.text("URL: ")
                            if self.highlight.description.url != "":
                                imgui.same_line()
                                if imgui.button( "Open Link##"+self.highlight.description.url):
                                    webbrowser.open(self.highlight.description.url, new=2)
                                
                                
                                
                                if imgui.is_item_hovered():
                                    if imgui.begin_tooltip():    
                                    
                                        imgui.text(self.highlight.description.url)
                                
                                        imgui.end_tooltip()




                            imgui.text("Category: " + self.highlight.description.category)
                            if self.highlight.description.category != "": 
                                for i in self.category:
                                    if i == self.highlight.description.category:
                                        self.edit_information_select_index = self.category.index(i)
                                
                                
                                
                            self.spacing(3)
                        


                            if imgui.button("Edit Information##"+  self.highlight.name):
                                self.toggle_edit_information  = not self.toggle_edit_information 

            
                            self.spacing(5)


                            if imgui.button("Close##" + self.highlight.name + "Close"):
                                self.highlight.show_descripion = False
                                self.highlight = None




                            """
                                imgui.text("Overrides:")
                                for i in self.highlight.description.overrides:
                                    if i[1] != "":
                                        imgui.indent(20) 
                                        imgui.text(i[0])
                                        imgui.bullet()
                                        imgui.text(i[1])
                                        imgui.indent(-20) 
                                imgui.indent(-20) 
                                
                            """
                                    

                                    
                            """
                                    for n in self.override_icons:
                                        
                                        if n[0].lower().startswith(j.lower().replace('"',"")): 
                                            
                                            imgui.image(n[1][0],20.0,20)
                                            imgui.same_line()
                                    
                                
                                    imgui.text(j.lower().replace('"',""))
                            """



            
                           
            imgui.pop_style_color()
        




        def mini_description(self,i):
            
            imgui.separator()
            self.spacing(2)
    
            imgui.text("Name: " + i.description.name)    
            imgui.text("Created by: " + i.description.author)

            imgui.separator()
            self.spacing(1)
            imgui.button("Click icon for more details")
            
        
   

        def ui_listview(self):
                
    
            self.spacing(13)


  
                                            
            for i in self.owner.config.mod_list:
                
                if self.filter_bar == "All" or self.filter_bar.lower() == i.description.category.lower():       
                
                    if self.show_thumbnail == True :

     
                        imgui.push_id(i.name) 
                        if imgui.image_button(i.icon[0][0],self.thumbnail_size,self.thumbnail_size):
                            if self.highlight != i:
                                self.toggle_edit_information = False   
                                
                            self.highlight = i
                               

                            self.owner.scoll = 0
                            

                                            
                           
                        if  self.highlight == None:
    
                            if imgui.is_item_hovered():  
                                if imgui.begin_tooltip():    
                                    
                                    imgui.image(i.icon[0][0],i.icon[0][1],i.icon[0][2])
                                    
                                    self.mini_description(i)
                                imgui.end_tooltip()

                            
                        imgui.pop_id()
                                    

                        imgui.same_line()
                        
                                 
                  
                    changed, i.active = imgui.checkbox(i.name, i.active)
                    if changed:
                        self.activation_list(i)
                    
                                                                

        
        def activation_list(self,i):
           
            if os.path.isdir(i.location) == True:
                
                for file in os.listdir(i.location):
                    
                    if file.endswith("pak") or file.endswith("pak-x") or file.endswith("ucas") or file.endswith("ucas-x") or file.endswith("utoc") or file.endswith("utoc-x"):
                        #f = os.path.dirname(i.location)
                  
                        #if file.startswith(i.name) or os.path.basename(i.location) == i.name:             
                            if i.active == True:
                                if file.endswith("-x"):
                                   
                                    os.rename(i.location +"/" + file, i.location +"/" + file.strip("-x"))
                                    #i.files[i.files.index(file)] = i.files[i.files.index(file)].strip("-x")

                                                    
                            if i.active == False:
                                if not file.endswith("-x"):
                                    os.rename(i.location +"/" + file , i.location +"/" + file  +"-x")
                                    #i.files[i.files.index(file)] = i.files[i.files.index(file)] + "-x"



    
        
        def ui_treeview(self,dir, indent=0):
                
                for item in os.listdir(dir):
                    item_path = os.path.join(dir, item)

                       
                   
                    if os.path.isdir(item_path):
                        
                        for i in self.owner.config.mod_list:
                           
                            if item == i.name:
                                
                               
                                
                                             
                                _,i.active = imgui.checkbox("##"+i.name,i.active)

                                if self.docked:    
                                    if imgui.is_item_hovered():   
                                        
                                        self.highlight = i
                                                                            

                                        self.owner.scoll = 0
                                    
                                
                               



                                if imgui.is_item_edited():
                        
                                    #self.toggle__mods  = True
                                    self.activation_tree(i, i.active,i.location) 
                        
                                imgui.same_line()
                                break
                         
                        
                        #folder
                        if imgui.tree_node( "Directory: " + item, imgui.TREE_NODE_OPEN_ON_ARROW ):
                            imgui.indent(5)
                          
                            self.ui_treeview(item_path, indent+1)
                        

                            imgui.tree_pop()
                            imgui.indent(-5)


                        
                            
                    else:
                        if not item.startswith("pakchunk") and not item.startswith("global"):
                            #files
                            imgui.indent(33)
                            imgui.text("File: " + item)               
                            imgui.indent(-33)
                            


        
        def activation_tree(self,mod,state,directory, indent = 0):
            
        
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
            
                
               
                if os.path.isdir(item_path):
                    
          
                    
                    for i in self.owner.config.mod_list:
                        
                         
                        if item == i.name:
                        
                            i.active = state 

             
                    self.activation_tree(i,state,item_path)
               
            
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
                        
                           


        def scaling(self):
            
            win_w, win_h = glfw.get_window_size(self.owner.window)
            fb_w, fb_h = glfw.get_framebuffer_size(self.owner.window)
            scaling = max(float(fb_w) / win_w, float(fb_h) / win_h)


            return scaling




        def main_window_box(self):

            
        
            padding = 0

            if self.highlight != None and self.docked == True:
                padding = self.f 
            else:
                padding = 0




            imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE,0.0)
            
           
            imgui.set_next_window_position(0,28 * (self.owner.config.selected_size * 0.1) )
             
            with imgui.begin("##" + "filterbar",False,imgui.WINDOW_NO_TITLE_BAR  | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS):
                
                if self.toggle_viewmode == False:
    
                    self.main_filter_bar()

            
            imgui.set_next_window_size(self.scaling() * (glfw.get_window_size(self.owner.window)[0])-padding,self.scaling() *  (glfw.get_window_size(self.owner.window)[1]-25))
            imgui.set_next_window_position(0,28 * (self.owner.config.selected_size * 0.1) )
            with imgui.begin("##" + "manager",False,imgui.WINDOW_NO_TITLE_BAR  | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS):
                
                
                if self.toggle_viewmode == True:
                    self.spacing(15)
                    self.ui_treeview(self.owner.path)
                    
                else:
                    
                    
                    self.ui_listview()


  
            #box
            self.description_box()
            
            
       
            imgui.pop_style_var() 
           
             
             


            
        def run(self):
            


            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND,54*0.003,63*0.003,93*0.003,1)
            imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING,12)  
            imgui.push_style_color(imgui.COLOR_TEXT,*self.owner.config.font_colour)
            imgui.push_style_color(imgui.COLOR_BUTTON,*self.owner.ui.button_colour)
            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED,*self.owner.ui.button_colour)
            imgui.push_style_color(imgui.COLOR_CHECK_MARK,1,1,1)
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,*self.owner.ui.bg_colour)
            imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, *self.owner.ui.button_colour)
            imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *self.owner.ui.button_colour)
            


            imgui.push_font(self.owner.config.selected_font) 
            if os.path.isdir(self.owner.path) == True:

                self.main_window_bar()
                self.main_window_box()
            
            else:
              
                imgui.begin("Error")
                imgui.text(self.path_error_message)
                if imgui.button("Close##Close Window"):
                    glfw.set_window_should_close(self.owner.window,glfw.TRUE)
                imgui.end()
            imgui.pop_font()


            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_var() 
            imgui.pop_style_color()

    

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

     

        for i in self.config.mod_list:
            if len(i.icon) != 0:
            
                for ii in i.icon:
                    glDeleteTextures([ii[0]])
            i.icon = []
        
                
 

    def main(self):
            
            # Initialize the library
            if not glfw.init():
                return

            
            #configuation
            self.config = self.configs(self)
            self.config.window_check()

            # Create a windowed mode window and its OpenGL context
            glfw.window_hint(glfw.RESIZABLE,glfw.TRUE)
            glfw.window_hint(glfw.MAXIMIZED, self.config.maximised)
            
        
            self.window = glfw.create_window(600, 600, "Tekken 8 Mod Manager " , None, None)
            
             

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
                    
                elif sys.platform == "linux":
                    self.path =  os.path.dirname(os.path.abspath(__file__)) + "/Polaris/Content/Paks"
                    
                
            



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
            glfw.set_window_icon(self.window,1,img)
            


            if not self.window:
                glfw.terminate()
                return



            # Make the window's context current
            glfw.make_context_current(self.window)
            glfw.swap_interval(1)
            
            
            

            # initilize imgui context (see documentation)
            imgui.create_context()
            self.impl = GlfwRenderer(self.window)
            self.io = imgui.get_io()

            
           
            
            #config fonts
            self.config.style = imgui.get_style()
            self.config.get_font_collection()
            self.impl.refresh_font_texture()

            #ui class
            self.ui = self.windows_ui(self)
            
            #apply setting to ui
            self.config.ui_check()
            self.config.config_setting()
            
            
            # Generate mods list before program starts
            self.config.generate_modlist()


          
            # Loop until the user closes the window
            while not glfw.window_should_close(self.window):
                # Render here, e.g. using pyOpenGL

                
                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)
                
              
         
                imgui.new_frame()
              
                
                
                self.ui.run()
                
                

                #imgui.show_demo_window()
                #imgui.show_style_editor()
               

                #Rendering
                imgui.render()
                self.impl.render(imgui.get_draw_data())
                

                

                # Swap front and back buffers
                glfw.swap_buffers(self.window)

                
                self.impl.process_inputs()
                
                # Poll for and process events
                glfw.poll_events()
                
                

          

            #clean up
            self.impl.shutdown()

       

            glfw.destroy_window(self.window)
            glfw.terminate()
            




program = mod_manager()


if __name__ == "__main__":
    program.main()



