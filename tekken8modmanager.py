import os


import sys


import subprocess

import configparser


import math


import weakref
import webbrowser


import shutil

import re

import logging


import glfw

import imgui


from imgui.integrations.glfw import GlfwRenderer


from OpenGL.GL import *


from PIL import Image







class DescriptionFormat:


    """Description format for displaying information on mods"""


    name: str = ""


    author: str = "" 


    description: str = ""


    url: str = ""


    version: str = ""


    date: str = ""


    category: str = ""


    presets: list = []


    override_parameter: list = []






class ModListFormat:


    """Modlist format for storing mod list"""


    name: str = ""


    location: str = ""


    folder: str = ""

    is_mod_folder: bool = False


    active: bool = False


    icon: list = []


    description: DescriptionFormat = None


    conflict: list = []





def name_sort(mod_list: list):
    return mod_list.name.title()





class ConflictManagement:

    """ This class compares mod list and finds the same string values to determine what mod conflict with one another."""

    def __init__(self, owner: object):


        self.owner = owner


        self.modlist_ref: list = []
        

        self.history: list = []



    def demo(self):

        """ Test function """
        

        mod1 = ModListFormat()


        mod1.name = "Sindel Zafina"


        mod1.description = DescriptionFormat()


        mod1.description.override_parameter = []


        mod1.description.override_parameter.append("zafina::preset1")


        mod1.description.override_parameter.append("zafina::preset2")


        mod1.description.override_parameter.append("zafina::preset4")



        mod2 = ModListFormat()


        mod2.name = "Zafina"


        mod2.description = DescriptionFormat()


        mod2.description.override_parameter = []


        mod2.description.override_parameter.append("zafina::preset1")


        mod2.description.override_parameter.append("zafina::preset2")




        self.modlist_ref = [mod1, mod2]




    def generate_conflict_list(self):


        self.history = []

        for mod in self.modlist_ref:


            mod.conflict = []

            temp_conflicts  = []
            
            if mod.is_mod_folder is True:

                for sug in mod.description.override_parameter:

                    if sug not in self.history and sug != "":

                        self.history.append(sug)
            

            for compare in self.modlist_ref:

                if mod.is_mod_folder is True and compare.is_mod_folder is True:
                   

                    if (mod != compare) and (mod.active is True and compare.active is True):


                        sim1 = []





                        if mod.description.override_parameter!= []:
                            
                            


                            if compare.description.override_parameter != []:




                                sim1 = list(set(mod.description.override_parameter) & set(compare.description.override_parameter))




                                if sim1 != []:

                                    temp_conflicts.append([compare, sim1.copy()])


                                    sim1.clear()


                            sim1.clear()







            mod.conflict = temp_conflicts




    def show(self):



        for i in self.modlist_ref:


            if i.is_mod_folder is True:

                print(i.name)




                print("conflict mods:")


                for info in i.conflict:
                    print(info)

             


                    print("  " + info[0].name)
    


                    print("    " + "similar:")
    


                    for r in info[1]:


                        print("    " + str(r))
              


                print("\n")




    def ui_conflict_warning(self, mod: ModListFormat):

        



            if len(mod.conflict) != 0:

                imgui.same_line()


                imgui.push_style_color(imgui.COLOR_TEXT, 0, 0, 0, 1)


                imgui.push_style_color(imgui.COLOR_BUTTON, 214, 220, 0, 1)


                if imgui.button("!##" + mod.name + "conflicts"):


                    for c in mod.conflict:




                        for j in self.owner.config.mod_list:




                            if c[0].name == j.name:


                                j.active = False


                                self.owner.ui.activation_list(j)
                                


                    self.generate_conflict_list()



                imgui.pop_style_color()


                imgui.pop_style_color()


                if imgui.is_item_hovered():


                    with imgui.begin_tooltip():


                        imgui.text("Possible Conflicting Mods:")
                        imgui.separator()





                        for info in mod.conflict:
                          

                            imgui.image(info[0].icon[0][0], self.owner.ui.thumbnail_size*0.5, self.owner.ui.thumbnail_size*0.5)
                            imgui.same_line()

                            imgui.text(info[0].name)


                            imgui.indent(40)


                            imgui.text("Reasons:")



                            for r in info[1]:


                                imgui.bullet_text(r)
                                imgui.spacing()
                                imgui.spacing()


                            imgui.indent(-40)
                        imgui.spacing()
                        imgui.spacing()
                        imgui.separator()


                        imgui.text("Optional: ")
                        imgui.same_line()


                        imgui.text_colored("Click the button to disable conflicting mods",214, 220, 0, 1)






class Configs:



    def __init__(self, owner: object):


        self.owner = owner



        # font setting vars


        self.selected_font = None


        self.selected: int = 6


        self.selected_size: int = 9


        self.fonts: list = []


        self.font_colour: tuple = 1, 1, 1, 1



        self.style: imgui.styled = None


        self.dpi_scale: float = 1.0



        # mod data


        self.mod_list: list = []



        # window


        self.maximised: bool = False



        # conflict


        self.conflict = ConflictManagement(self.owner)







    def window_check(self):


        configfile = configparser.ConfigParser()


        filecheck = configfile.read('tekken8modmanager.ini')

        header = ""

        if filecheck:



            for i in configfile.sections():


                if i == "Manager":

                    header = "Manager"

                if i == "Preset":

                    header = "Preset"


            self.maximised = configfile.getboolean(header, 'maximised', fallback=False)






    def ui_check(self):


        configfile = configparser.ConfigParser()


        file_check = configfile.read('tekken8modmanager.ini')


        if file_check:

            #convert header

            header = ""

            for i in configfile.sections():


                    if i == "Manager":

                        header = "Manager"

                    if i == "Preset":

                        header = "Preset"


            self.owner.ui.toggle_viewmode = configfile.getboolean(header, 'viewmode', fallback=False)


            self.owner.ui.show_thumbnail = configfile.getboolean(header, 'thumbnail', fallback=True)



            self.owner.ui.thumbnail_size = configfile.getint(header, 'thumbnail_size', fallback=50)



            # colours


            temp = configfile.get(header, 'font_colour', fallback=(1, 1, 1, 1))


            if temp != (1, 1, 1, 1):


                temp2 = temp.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "").split()


                self.font_colour = list(map(float, temp2))



            temp = configfile.get(header, 'button_colour', fallback=(0, 0.290, 0.783, 1))


            if temp != (0, 0.290, 0.783, 1):


                temp2 = temp.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "").split()


                self.owner.ui.button_colour = list(map(float, temp2))



            temp = configfile.get(header, 'bg_colour', fallback=(0, 0, 0, 1))


            if temp != (0, 0, 0, 1):


                temp2 = temp.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(",", "").split()


                self.owner.ui.bg_colour = list(map(float, temp2))



            # font


            self.selected = configfile.getint(header, 'font_index', fallback=4)


            self.selected_size = configfile.getint(header, 'font_size_index', fallback=9)


            self.config_font_type()



            # UI Scale(WIP)


            self.dpi_scale = configfile.getfloat(header, 'dpi_scale', fallback=1.0)


            self._imgui_scale_all_sizes(self.style, self.dpi_scale, self.dpi_scale)




            #warning


            self.owner.ui.conflict_notification = configfile.getboolean(header, 'warning', fallback=True)



            # docked


            self.owner.ui.docked = configfile.getboolean(header, 'docked', fallback=False)



            #presets


            self.owner.ui.presets = configfile.get(header, 'presets', fallback="Default").split()




    def config_save_app_setting(self):


        configfile = configparser.ConfigParser()


        listToStr = ' '.join([str(elem) for elem in self.owner.ui.presets])


        with open('tekken8modmanager.ini', 'w') as config:



            configfile['Manager'] = {'viewmode': str(self.owner.ui.toggle_viewmode),


                                    'Thumbnail': str(self.owner.ui.show_thumbnail),


                                    'maximised': str(self.maximised),


                                    "font_index": str(self.selected),


                                    "font_size_index": str(self.selected_size),


                                    "thumbnail_size": str(self.owner.ui.thumbnail_size),


                                    "font_colour": str(self.font_colour),


                                    "button_colour": str(self.owner.ui.button_colour),


                                    "bg_colour": str(self.owner.ui.bg_colour),


                                    'dpi_scale': str(self.dpi_scale),


                                    'docked': str(self.owner.ui.docked),


                                    'presets': listToStr,


                                    'warning': str(self.owner.ui.conflict_notification)


                                    }

          

            configfile.write(config)
            



    def get_font_collection(self):



        imgui.get_font_size()


        io = imgui.get_io()



        win_w, win_h = glfw.get_window_size(self.owner.window)


        fb_w, fb_h = glfw.get_framebuffer_size(self.owner.window)


        font_scaling_factor = max(float(fb_w) / win_w, float(fb_h) / win_h)


        font_size_in_pixels = 2


        io.font_global_scale /= font_scaling_factor

        

        _path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets"),"fonts")

        for i in os.listdir(_path):


            font = []



            if i.endswith(".otf") or i.endswith(".ttf"):


                for jj in range(15):


                    font_path = os.path.join(_path,i)

                    font.append((i + " " + str(font_size_in_pixels) + "px", io.fonts.add_font_from_file_ttf(font_path,font_size_in_pixels * font_scaling_factor)))


                    font_size_in_pixels += 2



                font_size_in_pixels = 2


                self.fonts.append([i, font])




        if sys.platform == "win32":
           

            # hack for user custom fonts

            _path = os.path.join(os.path.join(self.owner.pure_dir,"assets"),"fonts")

            if os.path.isdir(_path):


                for i in os.listdir(_path):


                    font = []


                    if i.endswith(".otf") or i.endswith(".ttf"):


                        for jj in range(15):

                            font_path = os.path.join(_path, i)

                            font.append((i + " " + str(font_size_in_pixels) + "px", io.fonts.add_font_from_file_ttf(font_path,font_size_in_pixels * font_scaling_factor)))


                            font_size_in_pixels += 2


                        font_size_in_pixels = 2


                        self.fonts.append([i, font])




        #layout = [font][fontset][fontsizeindex][fontfile]


        self.selected_font = self.fonts[6][1][9][1]




    def config_font_type(self):


        for i in self.fonts[self.selected][1][self.selected_size]:


            self.selected_font = i





    def _imgui_scale_all_sizes(self, style: imgui.styled, hscale: float, vscale: float) -> None:


        """pyimgui is missing ImGuiStyle::ScaleAllSizes(); this is a reimplementation of it.


            #https://github.com/ocornut/imgui/issues/6967#issuecomment-1793465530"""



        scale = max(hscale, vscale)



        def scale_it(attrname: str) -> None:


            value = getattr(style, attrname)



            if isinstance(value, imgui.Vec2):


                value = imgui.Vec2(math.trunc(value.x * hscale), math.trunc(value.y * vscale))



                setattr(style, attrname, value)


            else:


                setattr(style, attrname, math.trunc(value * scale))



        # scale_it("window_padding")


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



        self.selected = 6


        self.selected_size = 9


        self.selected_font = self.fonts[6][1][9][1]


        self.font_colour = 1, 1, 1, 1


        self.maximised = False


        self.dpi_scale = 1.0


        self.owner.ui.docked = True


        self.owner.ui.show_thumbnail = True


        self.owner.ui.button_colour = 0, 0.290, 0.783, 1


        self.owner.ui.bg_colour = 0, 0, 0, 1


        self.owner.ui.thumbnail_size = 50


        self.owner.ui.conflict_notification = True



        self.config_save_app_setting()






    def get_description(self, location: str):



        description = configparser.ConfigParser()


        description_info = DescriptionFormat()

        description_info.presets = []



        # create profile folder

        for file in os.listdir(location):
                 

            if (file.endswith("pak") or file.endswith("pak-x") or file.endswith("ucas") or file.endswith("ucas-x") or file.endswith("utoc") or file.endswith("utoc-x")):

                if os.path.exists(os.path.join(location,"profile")):
                    pass

                    #valid_folder = os.path.join(location, "profile")

                    #logging.warning("Profile folder exists in {0}".format(valid_folder))

                else:

                    #logging.warning("Profile folder will be created in {0}".format(location))

                    os.mkdir(os.path.join(location,"profile"))

                    if os.path.exists(os.path.join(location,"profile")):

                        #logging.warning("Profile folder was created!")
                        pass


                break   


        


        #convert to new location format

        if os.path.exists(os.path.join(location, "profile")):
            

            if os.path.isfile(os.path.join(location, "mod.ini")):


                shutil.move(os.path.join(location, "mod.ini"), os.path.join(os.path.join(location,"profile"),"mod.ini"))
            
           

            for filecheck in os.listdir(location):



                if filecheck.endswith(".jpg") or filecheck.endswith( ".jpeg") or filecheck.endswith(".png") or filecheck.endswith(".webp") or filecheck.endswith(".bmp"):
                    

                    shutil.move(os.path.join(location, filecheck), os.path.join(os.path.join(location, "profile"), filecheck))

            

            

            #normal operation

            if description.read(os.path.join(os.path.join(location,"profile"),"mod.ini")):


                description_info.name = description.get("Mod", "name", fallback="").replace('"', "")



                description_info.author = description.get("Mod", "author", fallback="").replace('"', "")
        


                description_info.date = description.get("Mod", "date", fallback="").replace('"', "")



                description_info.version = description.get("Mod", "version", fallback="").replace('"', "")



                description_info.description = description.get("Mod", "description", fallback="").replace('"', "")
    


                description_info.url = description.get("Mod", "url", fallback="").replace('"', "")
        


                description_info.category = description.get("Mod", "category", fallback="").replace('"', "")
        



                if description.get("Mod", "override_parameter", fallback="") == "":


                    description_info.override_parameter = []


                else:


                    description_info.override_parameter = description.get("Mod", "override_parameter", fallback="").lower().split()
                
                


                if description.get("Mod", "presets",fallback="") == "":


                    description_info.presets = []
                

                else:


                    description_info.presets = description.get("Mod", "presets").split()



        return description_info






    def update_description(self, location: str, mod: ModListFormat):


        description = configparser.ConfigParser()


        listToStr = ' '.join([str(elem) for elem in mod.description.presets])


        listToStr2 = ' '.join([str(elem) for elem in mod.description.override_parameter])



        if os.path.exists(os.path.join(os.path.join(location, "profile"),"mod.ini")):


            with open(os.path.join(os.path.join(location, "profile"),"mod.ini"), 'w') as descrp:


                description['Mod'] = {


                    'name': '"' + str(mod.description.name) + '"',


                    'author': '"' + str(mod.description.author) + '"',


                    'description': '"' + str(mod.description.description) + '"',


                    'url': '"' + str(mod.description.url) + '"',


                    'date': '"' + str(mod.description.date) + '"',


                    'version': '"' + str(mod.description.version) + '"',


                    'category': '"' + str(mod.description.category) + '"',


                    'presets': listToStr,


                    'override_parameter': listToStr2

                }

                





                description.write(descrp)






    def generate_modlist(self):
      



        self.owner.clear_images()
        self.mod_list.clear()



        """default image for thumbnails and icons"""

        default_icon = self.owner.ui_images()

    

        if os.path.isdir(self.owner.path):



            # look through the root mod folders.


            for root, dirnames, filenames in os.walk(self.owner.path):
                   


                for i in os.listdir(root):



                    if os.path.isdir(os.path.join(root, i)) and i != "profile":
                              

                        new_mod = ModListFormat()


                        new_mod.folder = root


                        new_mod.name = i
                         

                        new_mod.location = os.path.join(root, i)


                        new_mod.icon = [default_icon]


                        new_mod.description = self.owner.config.get_description(os.path.join(root, i))


                        new_mod.is_mod_folder = False


                        new_mod.active = False
                        
                     

                        # check  if folder is empty with no files.
                        for file in os.listdir(os.path.join(root, i)):


                            if (file.endswith("pak") or file.endswith("pak-x") or file.endswith("ucas") or file.endswith("ucas-x") or file.endswith("utoc") or file.endswith("utoc-x")):


                                    new_mod.is_mod_folder = True
                                    break

                            else:

                               new_mod.is_mod_folder = False
                               break

                                    

                       
                      



                        # image collection


                        temp_image_collection = []


                        if os.path.exists(os.path.join(os.path.join(root, i), "profile")):


                            if os.path.isdir(os.path.join(os.path.join(root, i), "profile")):
                                    

                                for filecheck in os.listdir(os.path.join(os.path.join(root, i), "profile")):


                                    if filecheck.endswith(".jpg") or filecheck.endswith(".jpeg") or filecheck.endswith(".png") or filecheck.endswith(".webp") or filecheck.endswith(".bmp"):


                                        temp_image_collection.append(self.owner.ui_images(os.path.join(os.path.join(os.path.join(root, i), "profile"),filecheck)))



                            if temp_image_collection != []:


                                new_mod.icon = temp_image_collection 

                            



                        # check active mod


                        for filecheck in os.listdir(os.path.join(root, i)):
                            

                            if filecheck.endswith("pak") or filecheck.endswith("pak-x") or filecheck.endswith("ucas") or filecheck.endswith("ucas-x") or filecheck.endswith("utoc") or filecheck.endswith("utoc-x"):


                                if filecheck.endswith("-x"):


                                    new_mod.active = False 

                                    break 


                                else:


                                    new_mod.active = True

                                    break 

                 



                        self.mod_list.append(new_mod)



        self.mod_list.sort(reverse=False, key=name_sort)


        self.conflict.modlist_ref =  self.mod_list
        self.conflict.generate_conflict_list()
        #self.conflict.show()





class WindowUI:



    def __init__(self, owner: object):


        self.owner = owner



        #ui toggles


        self.toggle_about: bool = False


        self.toggle_viewmode: bool = False


        self.show_thumbnail: bool = True


        self.thumbnail_size: int = 50


        self.show_window_setting: bool = False


        self.category = ["All", "Character Customization", "Stage", "Sound", "UI/HUD", "Movesets/Animations","Miscellaneous"]


        self.filter_bar: str = self.category[0]


        self.filter_select: int = 0


        self.highlight: ModListFormat = None


        self.docked: bool = True


        self.toggle_edit_information: bool = False


        self.edit_information_select_index: int = 0


        self.button_colour: tuple = 0, 0.290, 0.783, 1


        self.bg_colour: tuple = 0, 0, 0, 1



        # ui messages


        self.about_logo = self.owner.ui_images(self.owner.banner)


        self.about_message: str = "Created by Beanman"


        self.path_error_message: str = "This program was not placed in the right location. Please close the program and place inside {0}.".format("Steam/steamapps/common/Tekken 8")


        self.source_code: str = "https://github.com/opensource111111/tekken-8-mod-manager"





        self.font_padding: int = 530 * (self.owner.config.selected_size * 0.1)



        self.image_scrollwheel: int = 0


        self.stop_scroll: bool = False



        self.presets = ["Default"]


        self.preset_input: str = ""


        self.presets_select: int = 0


        self.save: bool = True


        self.conflict_notification: bool = False




        # lerp transition

        self.t: int = 0

        self.slide: int = 0

        self.show: bool = False


        self.show_history = False

        self.x = 0

        self.y = 0



    

    def ui_slide_transition(self, a: float, b: float, t: float):
      
       

        self.t+=t

        self.slide = a + self.t *(b - a)

       

        if self.slide >= b:

            self.slide = b

            self.t = 1
        

        if self.slide <= 0:

            self.slide = 0

            self.t = 0
        

        
       
          
    

    def main_filter_bar(self):

        


        if self.toggle_viewmode == False:


            imgui.text("Filter:")
            imgui.same_line()


            _all = 0


            cc = 0


            st = 0


            s = 0


            ui = 0


            ma = 0


            m = 0
        


            # mod counter for each section


            for i in self.owner.config.mod_list:


                if i.is_mod_folder is True:


                    _all += 1


                    if i.description.category.startswith("Character Customization"):


                        cc += 1


                    if i.description.category.startswith("Stage"):


                        st += 1


                    if i.description.category.startswith("Sound"):


                        s += 1


                    if i.description.category.startswith("UI/HUD"):


                        ui += 1


                    if i.description.category.startswith("Movesets/Animations"):


                        ma += 1



                    if i.description.category.startswith("Miscellaneous"):


                        m += 1



            category = ["All: " + str(_all), "Character Customization: " + str(cc), "Stage: " + str(st),


                        "Sound: " + str(s), "UI/HUD: " + str(ui), "Movesets/Animations: " + str(ma),


                        "Miscellaneous: " + str(m)]




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

        imgui.same_line()
      






        #enable/disable buttons


        if imgui.button("Enable All##enable"):


            for i in self.owner.config.mod_list:


                i.active = True


                self.activation_list(i)

        imgui.same_line()


        if imgui.button("Disable All##disable"):


            for i in self.owner.config.mod_list:


                i.active = False


                self.activation_list(i)





        # Presets


        imgui.text("Presets: ")
        imgui.same_line()


        imgui.set_next_item_width(295)


        with imgui.begin_combo("##preset_combo", self.presets[self.presets_select]) as preset:


            if preset.opened:


                for i, item in enumerate(self.presets):


                    is_selected = (i == self.presets_select)


                    if imgui.selectable(item, is_selected)[0]:


                        self.presets_select = i





                    # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)


                    if is_selected:
                        imgui.set_item_default_focus()






        # add preset
        imgui.same_line()


        if imgui.button("+"):

            imgui.open_popup("Add New Preset")



        # add new preset popup

        imgui.set_next_window_size_constraints((400, 130), (400, 130))

        with imgui.begin_popup_modal("Add New Preset",


                                     imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_DECORATION) as select_popup:


            if select_popup.opened:

                


                if self.preset_input.find(" ") != -1:

                    colour = 0.8,0,0,1

                else:

                    colour = self.owner.config.font_colour

                imgui.push_style_color(imgui.COLOR_TEXT, *colour)

                imgui.set_next_item_width(380)

                change, self.preset_input = imgui.input_text("##presets",self.preset_input)

                imgui.pop_style_color()


                if self.preset_input.find(" ") != -1:

                    imgui.text_colored("No spacing allowed in preset name!",0.8,0,0,1)



                imgui.separator()



                show_text = False

                if imgui.button("Create"):
                   

                    if self.preset_input!= "" and self.preset_input.find(" ") ==-1:
                        self.presets.append(self.preset_input)


                        self.owner.config.config_save_app_setting()
                        imgui.close_current_popup()
                

                if imgui.is_item_hovered() and self.preset_input == "" :

                    show_text = True

                imgui.same_line()

                if imgui.button("Cancel"):
                    imgui.close_current_popup()
  
                

                if show_text:

                    imgui.text_colored("Text field is empty!",0.8,0,0,1)





        imgui.same_line()

        if imgui.button(" - "):


            if self.presets[self.presets_select] != "Default":


                imgui.open_popup("Delete Preset")



        imgui.set_next_window_size_constraints((200, 100), (200, 100))


        with imgui.begin_popup_modal("Delete Preset",imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_DECORATION) as select_popup:


            if select_popup.opened:

                imgui.separator()


                if imgui.button("Yes"):



                    for i in self.owner.config.mod_list:



                        if self.presets[self.presets_select] in i.description.presets:


                            i.description.presets.remove(self.presets[self.presets_select])


                            self.owner.config.update_description(i.location, i)



                    if self.presets[self.presets_select] in self.presets:


                        self.presets.remove(self.presets[self.presets_select])


                        self.presets_select = len(self.presets) - 1


                        self.owner.config.config_save_app_setting()

                    imgui.close_current_popup()


                imgui.same_line()


                if imgui.button("No"):
                    imgui.close_current_popup()





        imgui.same_line()


        if imgui.button("Apply"):



            for f in self.owner.config.mod_list:


                if self.presets[self.presets_select] in f.description.presets:


                    f.active = True


                    self.activation_list(f)


                else:


                    f.active = False


                    self.activation_list(f)




        imgui.same_line()



        if imgui.button("Rename"):


            if self.presets[self.presets_select] != "Default":


                imgui.open_popup("Rename")


                self.preset_input = self.presets[self.presets_select]




        imgui.set_next_window_size_constraints((400, 150), (400, 150))

        with imgui.begin_popup_modal("Rename",


                                     imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_DECORATION) as select_popup:


            if select_popup.opened:

               
                imgui.separator()
                

                if self.preset_input.find(" ") != -1:

                    colour = 0.8,0,0,1

                else:

                    colour = self.owner.config.font_colour

                imgui.push_style_color(imgui.COLOR_TEXT, *colour)

                imgui.set_next_item_width(380)

                change, self.preset_input = imgui.input_text("##rename", self.preset_input)

                imgui.pop_style_color()
             
                imgui.separator()


                if imgui.button("Change"):

                    if self.preset_input!= "" and self.preset_input.find(" ") ==-1:

                        for f in self.owner.config.mod_list:


                            if self.presets[self.presets_select] in f.description.presets:


                                f.description.presets[f.description.presets.index(self.presets[self.presets_select])] = self.preset_input


                                self.owner.config.update_description(f.location, f)


                        self.presets[self.presets_select] = self.preset_input


                        self.owner.config.config_save_app_setting()
                        imgui.close_current_popup()

                

                if self.preset_input.find(" ") != -1:

                    imgui.text_colored("No spacing allowed in preset name!",0.8,0,0,1)




        e = 0


        d = 0




        # mod counter for each section


        for i in self.owner.config.mod_list:


            if i.is_mod_folder is True:


                if i.active is False:


                    d += 1



                if i.active is True:


                    e+=1


        imgui.same_line()



        imgui.text("Enabled: " + str(e))
        imgui.same_line()


        imgui.text("Disabled: " + str(d))












    def main_window_bar(self):




        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 1.0)



        with imgui.begin_main_menu_bar():



            # Options button


            if imgui.begin_menu("Options"):


                imgui.push_style_color(imgui.COLOR_BUTTON,0,0,0,0)
                

                if imgui.button("Window Configuration"):


                    imgui.open_popup("Window Configuration")


                imgui.pop_style_color()



                # Option pop-up


                imgui.set_next_window_size_constraints((600, 580), (600, 580))


                with imgui.begin_popup_modal("Window Configuration",imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_DECORATION) as select_popup:


                    if select_popup.opened:



                        # Window & UI


                        self.ui_spacing(3)


                        imgui.text("Window & UI Settings")

                        imgui.separator()







                        # Maximised button


                        imgui.text("Start Window Maximised:")

                        imgui.same_line()


                        changed, self.owner.config.maximised = imgui.checkbox("##Maximised", self.owner.config.maximised)


                        if changed:


                            self.owner.config.config_save_app_setting()





                        # Show thumbnail button


                        imgui.text("Show Thumbnail")

                        imgui.same_line()


                        changed, self.owner.ui.show_thumbnail = imgui.checkbox("##pShow Thumbnail", self.owner.ui.show_thumbnail)


                        if changed:


                            self.owner.config.config_save_app_setting()





                        # Scale Thumbnail


                        imgui.text("Thumbnail Scale")

                        imgui.same_line()


                        self.owner.ui.thumbnail_size = imgui.slider_int("##Thumbnail_scale", self.owner.ui.thumbnail_size, 50, 100)[1]


                        if imgui.is_item_edited():


                            self.owner.config.config_save_app_setting()



                        # Docking description box


                        imgui.text("Dock Details Panel:")

                        imgui.same_line()


                        changed, self.owner.ui.docked = imgui.checkbox("##dockinformation", self.owner.ui.docked)


                        if changed:


                            self.owner.config.config_save_app_setting()

                       
                        
                        

                        imgui.text("Mod Conflict Notification:")
                        imgui.same_line()


                        changed, self.owner.ui.conflict_notification  = imgui.checkbox("##me",self.owner.ui.conflict_notification)


                        if changed:


                            self.owner.config.config_save_app_setting()
                        
                    
                       





                        self.ui_spacing(5)



                        # Font setting


                        imgui.text("Colour Setting")

                        imgui.separator()




                        # Change Button Colour


                        imgui.text("Button Colour:")

                        imgui.same_line()


                        changed, self.owner.ui.button_colour = imgui.color_edit4("##button_colour", *self.owner.ui.button_colour,imgui.COLOR_EDIT_NO_ALPHA)


                        if changed:


                            self.owner.config.config_save_app_setting()



                        # Change Background Colour


                        imgui.text("Background Colour:")

                        imgui.same_line()


                        changed, self.owner.ui.bg_colour = imgui.color_edit4("##backgound_colour",*self.owner.ui.bg_colour, imgui.COLOR_EDIT_NO_ALPHA)


                        if changed:


                            self.owner.config.config_save_app_setting()



                        self.ui_spacing(5)



                        # Font setting


                        imgui.text("Font Setting")
                        imgui.separator()


                        imgui.text("Font Style:")
                        imgui.same_line()



                        items = []


                        for i in self.owner.config.fonts:


                            items.append(i[0])



                        with imgui.begin_combo("##fontsizecombo", items[self.owner.config.selected]) as combo:


                            if combo.opened:


                                for i, item in enumerate(items):


                                    is_selected = (i == self.owner.config.selected)


                                    if imgui.selectable(item, is_selected)[0]:


                                        self.owner.config.selected = i


                                        self.owner.config.config_font_type()


                                        self.owner.config.config_save_app_setting()



                                    # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)


                                    if is_selected:

                                        imgui.set_item_default_focus()

                        items.clear()



                        imgui.text("Font Size:")

                        imgui.same_line()



                        items = []


                        for i in self.owner.config.fonts[self.owner.config.selected][1]:


                            items.append(i[0])



                        with imgui.begin_combo("##dffeef", items[self.owner.config.selected_size]) as combos:


                            if combos.opened:


                                for i, item in enumerate(items):


                                    is_selected = (i == self.owner.config.selected_size)


                                    if imgui.selectable(item, is_selected)[0]:


                                        self.owner.config.selected_size = i


                                        self.owner.config.config_font_type()


                                        self.owner.config.config_save_app_setting()
                           


                                    # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)


                                    if is_selected:
                                        imgui.set_item_default_focus()



                        imgui.text("Font Colour:")

                        imgui.same_line()


                        changed, self.owner.config.font_colour = imgui.color_edit4("##font_colour",*self.owner.config.font_colour,imgui.COLOR_EDIT_NO_ALPHA)


                        if changed:


                            self.owner.config.config_save_app_setting()




                        self.ui_spacing(5)




                        imgui.separator()


                        if imgui.button("Reset to Default"):


                            self.owner.config.config_default_settings()



                imgui.end_menu()


            #------------------------------------------------------------------------------------





            # View modes button


            if imgui.begin_menu("View"):



                _, list_view = imgui.menu_item("List View")


                _, tree_view = imgui.menu_item("Tree View")



                if list_view:


                    self.toggle_viewmode = False


                    self.owner.config.config_save_app_setting()



                if tree_view:


                    self.toggle_viewmode = True


                    self.owner.config.config_save_app_setting()

                imgui.end_menu()



            #------------------------------------------------------------------------------



            # Help button


            if imgui.begin_menu("Help"):
               



                changed, about = imgui.menu_item("About")



                if changed:


                    if self.toggle_about == True:


                        self.toggle_about = False


                    elif self.toggle_about == False:


                        self.toggle_about = True



                imgui.end_menu()








            # about box


            if self.toggle_about:


                imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 3.0)


                imgui.set_next_window_size_constraints((350, 230), (350, 230))


                imgui.begin("About", False, imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE)



                imgui.indent(imgui.get_content_region_available_width() /4)


                imgui.image(self.about_logo[0], self.about_logo[1] * 0.5, self.about_logo[2] * 0.5)


                imgui.indent(imgui.get_content_region_available_width() * 0.06)



                imgui.text_wrapped(self.about_message)



                imgui.indent(-imgui.get_content_region_available_width() /4)


                imgui.indent(imgui.get_content_region_available_width()/3.8)



                if imgui.button("Source Code"):


                    webbrowser.open(self.source_code, new=2)



                if imgui.is_item_hovered():


                    if imgui.begin_tooltip():


                        imgui.text(self.source_code)
                        imgui.end_tooltip()


              




                imgui.indent(-imgui.get_content_region_available_width() /4)


                imgui.indent(imgui.get_content_region_available_width() /3.8)
                


                self.ui_spacing(2)


                if imgui.button("Close"):


                    self.toggle_about = False



                imgui.indent(-imgui.get_content_region_available_width() * 0.3)
                imgui.end()


                imgui.pop_style_var()



            


            #-------------------------------------------------------------------------------------------



            # Refresh Button


            imgui.set_window_position(20, 0)


            if imgui.button("Refresh List"):


                self.highlight = None

                self.show = False

                self.slide = 0

                self.t = 0

                self.toggle_edit_information = False

                self.owner.config.generate_modlist()



        imgui.pop_style_var()





    def ui_spacing(self, space: int):


        for i in range(space):
            imgui.spacing()




    

    def history_box(self, pattern: str):


            if self.show_history == True:

                # Suggestions box

                imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0, 0, 0, 0.6)


                imgui.set_next_window_position(self.x, self.y + 30)

                opened = imgui.begin("History", False, imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_FOCUS_ON_APPEARING)


                for v in self.owner.config.conflict.history:

                    if re.search(pattern, v):

                        imgui.selectable(v)


                        if imgui.is_item_clicked():

                            self.highlight.description.override_parameter[self.highlight.description.override_parameter.index(pattern)] = v

                            opened = False

                            self.show_history = False

                imgui.end()

                imgui.pop_style_color()


            if imgui.is_key_pressed(glfw.KEY_ENTER):

                self.show_history = False
    



    def description_box(self):



        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, self.owner.ui.bg_colour[0] * 0.5, self.owner.ui.bg_colour[1] * 0.5, self.owner.ui.bg_colour[2] * 0.5, 1)



        if self.highlight != None:

            

            if self.docked:
        

                imgui.set_next_window_size(self.scaling() * self.font_padding, glfw.get_window_size(self.owner.window)[1] - 26)


                imgui.set_next_window_position(self.scaling() * glfw.get_window_size(self.owner.window)[0] - self.font_padding, self.scaling() * 26)



            flags: int = 0



            if self.docked:


                if self.stop_scroll == True:


                    flags =  imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_SCROLL_WITH_MOUSE


                else:


                    flags =  imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS



            else:


                if self.stop_scroll == True:



                    flags =  imgui.WINDOW_NO_SAVED_SETTINGS  | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_SCROLL_WITH_MOUSE



                else:



                    flags =  imgui.WINDOW_NO_SAVED_SETTINGS  | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_COLLAPSE



            with imgui.begin(self.highlight.name + "Details", False, flags):


                self.ui_spacing(5)


                imgui.indent(13)


                imgui.text("Details Panel")

                imgui.separator()


                imgui.unindent(13)


                self.ui_spacing(5)


                imgui.indent(13)


                imgui.image(self.highlight.icon[self.image_scrollwheel][0], self.highlight.icon[self.image_scrollwheel][1], self.highlight.icon[self.image_scrollwheel][2])


                imgui.unindent(13)



                if imgui.is_item_hovered():


                    self.stop_scroll = True


                    self.image_scrollwheel += int(self.owner.io.mouse_wheel)



                    if self.image_scrollwheel >= len(self.highlight.icon):


                        self.image_scrollwheel = 0



                    if self.image_scrollwheel <= -1:


                        self.image_scrollwheel = len(self.highlight.icon) - 1



                else:



                    self.stop_scroll = False



                self.ui_spacing(5)
                imgui.separator()



                # Open button
                imgui.same_line()
                imgui.indent(


                    self.scaling() * imgui.get_window_size()[0] - 150 * (self.owner.config.selected_size * 0.1))


                self.ui_spacing(2)



                if imgui.button("Open Folder##Openefeve_Folder"):


                    if sys.platform == "win32":


                        subprocess.Popen(['explorer', "{0}".format(self.highlight.location)])
                      


                    if sys.platform == "linux":
                       

                        os.system('xdg-open "%s"' % "{0}".format(self.highlight.location))

                imgui.unindent(


                    self.scaling() * imgui.get_window_size()[0] - 150 * (self.owner.config.selected_size * 0.1))



                if self.toggle_edit_information:



                    # edit description


                    if imgui.begin_table("cdc", 2):


                        imgui.table_next_row()


                        imgui.table_set_column_index(0)


                        imgui.text("Name:")


                        imgui.table_set_column_index(1)


                        imgui.set_next_item_width(250)


                        changed, self.highlight.description.name = imgui.input_text("##Name: ", self.highlight.description.name)



                        imgui.table_next_row()


                        imgui.table_set_column_index(0)


                        imgui.text("Created by: ")


                        imgui.table_set_column_index(1)


                        imgui.set_next_item_width(250)



                        changed, self.highlight.description.author = imgui.input_text("##Created by: ",self.highlight.description.author)



                        imgui.table_next_row()


                        imgui.table_set_column_index(0)


                        imgui.text("Description:")


                        imgui.table_set_column_index(1)


                        imgui.set_next_item_width(250)



                        changed, self.highlight.description.description = imgui.input_text_multiline("##Description: ", self.highlight.description.description, imgui.INPUT_TEXT_CALLBACK_RESIZE)



                        imgui.table_next_row()


                        imgui.table_set_column_index(0)


                        imgui.text("URL:")


                        imgui.table_set_column_index(1)


                        imgui.set_next_item_width(250)



                        changed, self.highlight.description.url = imgui.input_text("##URL: ", self.highlight.description.url)





                        imgui.table_next_row()


                        imgui.table_set_column_index(0)


                        imgui.text("Date:")


                        imgui.table_set_column_index(1)


                        imgui.set_next_item_width(250)



                        changed, self.highlight.description.date = imgui.input_text("##Date: ", self.highlight.description.date)

                       




                        imgui.table_next_row()


                        imgui.table_set_column_index(0)


                        imgui.text("Version:")


                        imgui.table_set_column_index(1)


                        imgui.set_next_item_width(250)



                        changed, self.highlight.description.version = imgui.input_text("##Version: ", self.highlight.description.version)




                        imgui.table_next_row()


                        imgui.table_set_column_index(0)


                        imgui.text("Category:")


                        imgui.table_set_column_index(1)


                        imgui.set_next_item_width(250)


                        with imgui.begin_combo("##catergory_edit",self.category[self.edit_information_select_index]) as combo:


                            if combo.opened:


                                for i, item in enumerate(self.category):


                                    is_selected = (i == self.edit_information_select_index)


                                    if imgui.selectable(item, is_selected)[0]:


                                        self.edit_information_select_index = i


                                        self.highlight.description.category = self.category[


                                            self.edit_information_select_index]



                                        # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)


                                        if is_selected:
                                            imgui.set_item_default_focus()

                     
                        

                        # override


                        imgui.table_next_row()

                        imgui.table_set_column_index(0)


                        imgui.text("Override Parameter:")

                        imgui.same_line()

                        if imgui.button("+##add-parameter"):


                            self.highlight.description.override_parameter.append("")


                        imgui.table_set_column_index(1)
                        

                        self.save = True





                        b = 0

                        for p in self.highlight.description.override_parameter:


                            if p.find(" ") != -1:


                                colour = 0.8, 0, 0, 1

                                self.save = False

                            else:

                                colour = self.owner.config.font_colour


                            imgui.push_style_color(imgui.COLOR_TEXT, *colour)

                            imgui.set_next_item_width(230)


                            changed, self.highlight.description.override_parameter[b] = imgui.input_text("##parameter-text" + str(b),self.highlight.description.override_parameter[b])


                            if imgui.is_item_clicked():

                                self.show_history = True

                                self.x, self.y = imgui.get_item_rect_min()
                            

                            if imgui.is_item_focused():

                                self.history_box(p)
                            

                            imgui.same_line()

                            if imgui.button("-##remove-parameter" + str(b)):

                                self.highlight.description.override_parameter.remove(p)


                            b+=1

                            imgui.pop_style_color()


                        


                        imgui.end_table()

                    imgui.separator()
                    



                    self.ui_spacing(5)

                    

                    if imgui.button("Save"):

                            if self.save:

                                self.owner.config.update_description(self.highlight.location,self.highlight)


                                self.toggle_edit_information = False


                                self.owner.config.conflict.generate_conflict_list()

                    imgui.same_line()



                    if imgui.button("Cancel"):


                        self.highlight.description = self.owner.config.get_description(self.highlight.location)


                        self.toggle_edit_information = False


                        self.save = True




                else:



                    # information


                    imgui.text("          Name:    " + self.highlight.description.name)

                    imgui.spacing()


                    imgui.text(" Created by:    " + self.highlight.description.author)
                    imgui.spacing()


                    imgui.text("Description:   ")
                    imgui.same_line()


                    imgui.text_wrapped(self.highlight.description.description)
                    imgui.spacing()




                    imgui.text("             URL:   ")


                    if self.highlight.description.url != "":
                        imgui.same_line()


                        if imgui.button("Open Link##" + self.highlight.description.url):


                            webbrowser.open(self.highlight.description.url, new=2)


                        if imgui.is_item_hovered():


                            if imgui.begin_tooltip():


                                imgui.text(self.highlight.description.url)

                                imgui.end_tooltip()





                    imgui.text("            Date:   " + self.highlight.description.date)
                    imgui.spacing()


                    imgui.text("       Version:    " + self.highlight.description.version)





                    imgui.text("    Category:     " + self.highlight.description.category)


                    if self.highlight.description.category != "":


                        for i in self.category:


                            if i == self.highlight.description.category:


                                self.edit_information_select_index = self.category.index(i)



                    self.ui_spacing(3)



                    if imgui.button("Edit Information##" + self.highlight.name):


                        self.toggle_edit_information = not self.toggle_edit_information

                    imgui.separator()


                    self.ui_spacing(6)



                    imgui.text("Add To Preset:")


                    imgui.same_line()


                    imgui.set_next_item_width(100)


                    with imgui.begin_combo("##preset_combo", self.presets[self.presets_select]) as preset:


                        if preset.opened:


                            for i, item in enumerate(self.presets):


                                is_selected = (i == self.presets_select)


                                if imgui.selectable(item, is_selected)[0]:


                                    self.presets_select = i



                                # Set the initial focus when opening the combo (scrolling + keyboard navigation focus)


                                if is_selected:
                                    imgui.set_item_default_focus()
                    imgui.same_line()


                    if imgui.button("+##addllgf"):


                        if self.presets[self.presets_select] in self.highlight.description.presets:
                            pass


                        else:
                           


                            self.highlight.description.presets.append(self.presets[self.presets_select])


                            self.owner.config.update_description(self.highlight.location,self.highlight)






                    if len(self.highlight.description.presets) > 0:



                        imgui.text("Attached To:")



                        for i in self.highlight.description.presets:


                            imgui.bullet_text(i)


                            imgui.same_line()


                            if imgui.button("-##wffwgf" + i):



                                if i in self.highlight.description.presets:


                                    self.highlight.description.presets.remove(i)


                                    self.owner.config.update_description(self.highlight.location,self.highlight)





                    self.ui_spacing(5)



                    if imgui.button("Close##" + self.highlight.name + "Close"):

                        self.show = False

                      


                    if imgui.is_key_pressed(glfw.KEY_ESCAPE):

                        self.show = False


                 




        imgui.pop_style_color()





    def mini_description(self, mod: ModListFormat):

        """

            Mini description for when hovering over thumbnail icon in list view.

        """


        imgui.separator()


        self.ui_spacing(2)



        imgui.text("Name: " + mod.description.name)


        imgui.text("Created by: " + mod.description.author)

        imgui.separator()


        self.ui_spacing(1)


        imgui.button("Click icon to open details panel.")



    def ui_listview(self):



        self.ui_spacing(18)



        for i in self.owner.config.mod_list:



            if (self.filter_bar == "All" or self.filter_bar.lower() == i.description.category.lower()) and i.is_mod_folder is True:
                


                if self.show_thumbnail == True:



                    imgui.push_id(i.name)


                    if imgui.image_button(i.icon[0][0], self.thumbnail_size, self.thumbnail_size):


                        if self.highlight != i:


                            self.image_scrollwheel = 0


                            self.toggle_edit_information = False



                        self.highlight = i

                        self.show = True



                    if self.highlight == None:



                        if imgui.is_item_hovered():


                            if imgui.begin_tooltip():


                                imgui.image(i.icon[0][0], i.icon[0][1], i.icon[0][2])

                                self.mini_description(i)
                            imgui.end_tooltip()

                    imgui.pop_id()

                    imgui.same_line()



                changed, i.active = imgui.checkbox(i.name, i.active)


                if changed:


                    self.activation_list(i)


                    self.owner.config.conflict.generate_conflict_list()
                
                
                
                

                if self.conflict_notification:


                    self.owner.config.conflict.ui_conflict_warning(i)
            
            
    
    


    def activation_list(self, mod: ModListFormat):



        if os.path.isdir(mod.location) == True:



            for file in os.listdir(mod.location):



                if file.endswith("pak") or file.endswith("pak-x") or file.endswith("ucas") or file.endswith(


                        "ucas-x") or file.endswith("utoc") or file.endswith("utoc-x"):



                    if mod.active == True:


                        if file.endswith("-x"):


                            os.rename(os.path.join(mod.location, file), os.path.join(mod.location, file.strip("-x")))



                    if mod.active == False:


                        if not file.endswith("-x"):


                            os.rename(os.path.join(mod.location,file), os.path.join(mod.location, file + "-x"))


        self.owner.config.conflict.generate_conflict_list()
    
    


    def ui_treeview(self, dir: str, indent: int=0):
     


        for item in os.listdir(dir):


            item_path = os.path.join(dir, item)
            
   


            if os.path.isdir(item_path):



                for i in self.owner.config.mod_list:
                    


                    if item == i.name:

                        

                        changed, i.active = imgui.checkbox("##" + i.name, i.active)
                       
                        

                        if changed:


                            self.activation_tree(i.active, i.location)

                        
                       
                           
                        

                        if self.conflict_notification:


                            self.owner.config.conflict.ui_conflict_warning(i)
                      
                        

                        imgui.same_line()


                        break
                





                #folder


                if item != "profile":


                    if imgui.tree_node("Directory: " + item, imgui.TREE_NODE_OPEN_ON_ARROW):


                        imgui.indent(13)
                    


                        self.ui_treeview(item_path, indent + 1)


                        imgui.indent(-13)
                        imgui.tree_pop()
                    
                    


                    for i in self.owner.config.mod_list:
                        

                        if self.docked:

                            if imgui.is_item_hovered():

                                if item == i.name:

                                    if i.is_mod_folder is True:


                                        self.highlight = i

                                        self.image_scrollwheel = 0

                                        self.show = True

                                        break
                                



            else:



                if not item.startswith("pakchunk") and not item.startswith("global"):


                    #files


                    imgui.indent(30)


                    imgui.text("File: " + item)


                    imgui.indent(-30)
                    







    def activation_tree(self, state: bool, directory: str, indent: int=0):



        for item in os.listdir(directory):


            item_path = os.path.join(directory, item)



            if os.path.isdir(item_path):



                for i in self.owner.config.mod_list:



                    if item == i.name:


                        i.active = state



                self.owner.config.conflict.generate_conflict_list()


                self.activation_tree(state, item_path)




            else:



                if os.path.isfile(item_path):



                    file = item


                    if file.endswith("pak") | file.endswith("pak-x") | file.endswith("ucas") | file.endswith(


                            "ucas-x") | file.endswith("utoc") | file.endswith("utoc-x"):



                        if state == True:


                            if file.endswith("-x"):


                                os.rename(os.path.join(directory, file), os.path.join(directory,file.strip("-x")))



                            else:
                                pass



                        if state == False:


                            if file.endswith("-x"):
                                pass


                            else:



                                os.rename(os.path.join(directory,file),os.path.join(directory, file + "-x"))


                self.owner.config.conflict.generate_conflict_list()







    def scaling(self):



        win_w, win_h = glfw.get_window_size(self.owner.window)


        fb_w, fb_h = glfw.get_framebuffer_size(self.owner.window)


        #fixed division by 0 error.

        scaling = max(float(max(0.1,fb_w)) / max(0.1,win_w), float(max(0.1,fb_h)) / max(0.1,win_h))

        return scaling





    def main_window_box(self):






        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0.0)



        imgui.set_next_window_position(0, 28 * (self.owner.config.selected_size * 0.1))



        with imgui.begin("##" + "filterbar", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS):



            self.main_filter_bar()
                

               


        imgui.set_next_window_size(self.scaling() * (glfw.get_window_size(self.owner.window)[0]) - self.font_padding,self.scaling() * (glfw.get_window_size(self.owner.window)[1] - 25))
        


        imgui.set_next_window_position(0, 28 * (self.owner.config.selected_size * 0.1))
        


        with imgui.begin("##" + "manager", False,imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS):



            if self.toggle_viewmode == True:


                self.ui_spacing(20)


                self.ui_treeview(self.owner.path)
               



            else:


                self.ui_spacing(4)


                self.ui_listview()



        #box


        self.description_box()



        imgui.pop_style_var()






    def run(self):


        if self.show:

            self.ui_slide_transition(0,530,0.3)

        else:

            self.ui_slide_transition(0,530,-0.3)

            if self.slide == 0:

                self.highlight = None
        



        self.font_padding = self.slide * (self.owner.config.selected_size * 0.1)
       
      

        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 54 * 0.003, 63 * 0.003, 93 * 0.003, 1)


        imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 5)


        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 5)


        imgui.push_style_color(imgui.COLOR_TEXT, *self.owner.config.font_colour)


        imgui.push_style_color(imgui.COLOR_BUTTON, *self.owner.ui.button_colour)


        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, *self.owner.ui.button_colour)


        imgui.push_style_color(imgui.COLOR_CHECK_MARK, 1, 1, 1)


        imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, *self.owner.ui.bg_colour)


        imgui.push_style_color(imgui.COLOR_HEADER_HOVERED, *self.owner.ui.button_colour)


        imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *self.owner.ui.button_colour)



        imgui.push_font(self.owner.config.selected_font)






        if os.path.isdir(self.owner.path) == True:
          

         


            self.main_window_bar()


            self.main_window_box()



        else:



            imgui.begin("Error", imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_COLLAPSE)


            imgui.text_wrapped(self.path_error_message)


            if imgui.button("Close##Close Window"):


                glfw.set_window_should_close(self.owner.window, glfw.TRUE)



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


        imgui.pop_style_var()





class ModManager:



    def __init__(self):



        # system path


        self.path: str = ""


        self.pure_dir: str = ""


        self.window_icon: str = None


        self.banner: str = None
     



        # main classes


        self.ui: WindowUI = None


        self.window = None


        self.config: Configs = None


        self.io = None


        self.impl = None


        self.version: str= "2.0.1"




    def ui_images(self, image: str = ""):



        if image == "":


            image = self.window_icon



        img = Image.open(image).convert("RGBA")


        size = (400, 400)


        img.thumbnail(size)



        imdata = img.tobytes()


        width, height = img.size



        texname = glGenTextures(1)



        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)


        glBindTexture(GL_TEXTURE_2D, texname)


        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imdata)


        glGenerateMipmap(GL_TEXTURE_2D)


        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)


        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)


        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)


        glBindTexture(GL_TEXTURE_2D, 0)



        return [texname, width, height]





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



        # Configuration


        self.config = Configs(self)


        self.config.window_check()



        # Create a windowed mode window and its OpenGL context


        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)


        glfw.window_hint(glfw.MAXIMIZED, self.config.maximised)



        self.window = glfw.create_window(810, 800, "Tekken 8 Mod Manager", None, None)



        # Check if the program is run from binary or script and which platform.


        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):


            print('running in a PyInstaller bundle')


            import pyi_splash

            pyi_splash.close()

        


            if sys.platform == "win32":


                self.path = os.path.dirname(sys.executable) + "\\Polaris\\Content\\Paks"


                self.pure_dir = os.path.dirname(sys.executable)


                self.window_icon = os.path.abspath(os.path.dirname(__file__)) + "\\assets\\branding\\icon.ico"


                self.banner = os.path.abspath(os.path.dirname(__file__)) + "\\assets\\branding\\banner.png"



            elif sys.platform == "linux":


                self.path = os.path.dirname(sys.executable) + "/Polaris/Content/Paks"


                self.pure_dir = os.path.dirname(sys.executable)
                

                self.window_icon = os.path.dirname(os.path.abspath(__file__)) + "/assets/branding/icon.ico"


                self.banner = os.path.abspath(os.path.dirname(__file__)) + "/assets/branding/banner.png"



        else:



            print('running in a normal Python process')



            if sys.platform == "win32":


                self.path = os.path.dirname(os.path.abspath(__file__)) + "\\Polaris\\Content\\Paks"

                self.window_icon = os.path.abspath(os.path.dirname(__file__)) + "\\assets\\branding\\icon.ico"

                self.banner = os.path.abspath(os.path.dirname(__file__)) + "\\assets\\branding\\banner.png"



            elif sys.platform == "linux":


                self.path = os.path.dirname(os.path.abspath(__file__)) + "/Polaris/Content/Paks"

                self.window_icon = os.path.dirname(os.path.abspath(__file__)) + "/assets/branding/icon.ico"

                self.banner = os.path.abspath(os.path.dirname(__file__)) + "/assets/branding/banner.png"

        

           






        img = Image.open(self.window_icon)


        glfw.set_window_icon(self.window, 1, img)



        if not self.window:


            glfw.terminate()
            return



        # Make the window's context current


        glfw.make_context_current(self.window)


        glfw.swap_interval(1)



        # Initilize imgui context (see documentation)


        imgui.create_context()


        self.impl = GlfwRenderer(self.window)


        self.io = imgui.get_io()



        # Config fonts


        self.config.style = imgui.get_style()
        self.config.get_font_collection()


        self.impl.refresh_font_texture()



        # UI class


        self.ui = WindowUI(self)

   


        # Apply setting to ui


        self.config.ui_check()

        self.config.config_save_app_setting()



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



            # Rendering
            imgui.render()


            self.impl.render(imgui.get_draw_data())



            # Swap front and back buffers


            glfw.swap_buffers(self.window)

            self.impl.process_inputs()



            # Poll for and process events


            glfw.poll_events()





        # Clean up


        self.impl.shutdown()


        glfw.destroy_window(self.window)


        glfw.terminate()
        



program = ModManager()



if __name__ == "__main__":
    program.main()








