import os
import sys
import subprocess

import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
from OpenGL.GL import *
import OpenGL.GL as gl
from PIL import Image
from math import radians




class mod_list_format:
        name : str = ""
        location : str = ""
        _type : str = ""
        active : bool = True
        

   

    
def name_sort(mod_list):
    return mod_list.name.title()
   


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



class mod_manager:
    


    def __init__(self):

        self._mod_list : mod_list_format = []
        self.mod_list : mod_list_format = []
        self.logicmods_list : mod_list_format = []
        self.path : str = ""
        self.toggle_view = False


        #check path
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            print('running in a PyInstaller bundle')
            
            if sys.platform == "win32":
                self.path = os.path.dirname(sys.executable) + "\Polaris\Content\Paks"
            elif sys.platform == "linux":
                self.path = os.path.dirname(sys.executable) + "/Polaris/Content/Paks"

        else:
            print('running in a normal Python process')
            
            if sys.platform == "win32":
                self.path =  os.path.dirname(os.path.abspath(__file__)) + "\Polaris\Content\Paks"
            elif sys.platform == "linux":
                self.path =  os.path.dirname(os.path.abspath(__file__)) + "/Polaris/Content/Paks"
            
        
       

    
    def generate_modlist(self):

        self._mod_list.clear()
        self.mod_list.clear()
        self.logicmods_list.clear()


        if os.path.isdir(self.path):
                
            for folder in os.listdir(self.path):

                if os.path.isdir(self.path + "/" + folder):

                    if folder == "~mods" or folder == "mods" or folder == "logicmods":
                        
                        for mod_folder in os.listdir(self.path + "/" + folder):
                            
                            if os.path.isdir(self.path + "/" + folder   + "/" + mod_folder):
                                
                                if os.listdir(self.path + "/" + folder   + "/" + mod_folder) != [] :

                                   
                                    new = mod_list_format()
                                    new._type = folder
                                    new.name = mod_folder
                                    new.location = self.path + "/" + folder + "/" + mod_folder
                                    
                                    for filecheck in os.listdir(self.path + "/" + folder + "/" + mod_folder):
                                            
                                        if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                
                                            if filecheck.endswith("-x"):
                                                new.active = False
                                            else:
                                                new.active = True


                                    if folder == "~mods":        
                                        self._mod_list.append(new)

                                    if folder == "mods":        
                                        self.mod_list.append(new)

                                    if folder == "logicmods":
                                        self.logicmods_list.append(new)

            
            self._mod_list.sort(reverse=False,key=name_sort)
            self.mod_list.sort(reverse=False,key=name_sort)
            self.logicmods_list.sort(reverse=False,key=name_sort)
           
    
    

    """
    def generate_modlist2(self):

        self._mod_list.clear()
        self.mod_list.clear()
        self.logicmods_list.clear()

        if os.path.isdir(self.path):
     
            for folder in os.listdir(self.path):

                if os.path.isdir(self.path + "/" + folder):

                    if folder == "~mods" or folder == "mods" or folder == "logicmods":

                        for root, dirnames, filenames  in os.walk(self.path +"/" + folder):

                                for mod_folder in dirnames:

                                    if os.path.isdir(root + "/" + mod_folder):
                                
                                        if os.listdir(root  + "/" + mod_folder) != []:
                                            

                                            new = mod_list_format()
                                            new._type = folder
                                            new.name = mod_folder
                                            new.location = root  + "/" + mod_folder
                                            
                                            for filecheck in os.listdir(root  + "/" + mod_folder):
                                                    
                                                if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                        
                                                    if filecheck.endswith("-x"):
                                                            new.active = False
                                                    else:
                                                            new.active = True
                                                
                                            if folder == "~mods":        
                                                self._mod_list.append(new)

                                            if folder == "mods":        
                                                self.mod_list.append(new)

                                            if folder == "logicmods":
                                                self.logicmods_list.append(new)



        
            self._mod_list.sort(reverse=False,key=name_sort)
            self.mod_list.sort(reverse=False,key=name_sort)
            self.logicmods_list.sort(reverse=False,key=name_sort)
           
    """


    def activation(self,state,dir):

            if os.path.isdir(dir) == True:
                for file in os.listdir(dir):
                    if file.endswith("pak") | file.endswith("pak-x") | file.endswith("ucas") | file.endswith("ucas-x") | file.endswith("utoc") | file.endswith("utoc-x"):
                                                    
                        if state == True:
                            if file.endswith("-x"):
                                os.rename(dir +"/" + file, dir +"/" + file.strip("-x"))
                                
                            else:
                                pass
                    
                        if state == False:
                            if file.endswith("-x"):
                                pass
                            else:
                            
                                os.rename(dir +"/" + file, dir +"/" + file +"-x")
    
   

 
    """
    def ui_treeview(self,directory, indent=0):
        self.generate_modlist2()

        imgui.push_style_color(imgui.COLOR_TEXT,1,1,1,1)
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            for i in self._mod_list:

                if item == i.name:
                    
                    
                    _,i.active =imgui.checkbox(i.name,i.active)
                    imgui.text
                    self.activation(i.active,i.location) 
                    imgui.same_line()
            
            
            for i in self.mods_list:

                if item == i.name:
                    #print(i.name)
                    _,i.active =imgui.checkbox(i.name,i.active)
                    self.activation(i.active,i.location) 
                    imgui.same_line()

                    
            for i in self.logicmods_list:

                if item == i.name:
                    #print(i.name)
                    _,i.active =imgui.checkbox(i.name,i.active)
                    self.activation(i.active,i.location) 
                    imgui.same_line()

            
            if os.path.isdir(item_path):
                
               
                if imgui.tree_node(item):

                    
                    #print(f"{'  ' * indent}Directory: {item}")
                
                    #elif os.path.isfile(item_path):
                
                    #print(f"{'  ' * (indent+1)}File: {item}")

                    self.ui_treeview(item_path, indent+1)
                    imgui.tree_pop()
           
        imgui.pop_style_color()

    
    """


    

    def ui_checklist(self):
            
            self.generate_modlist()

            
            imgui.push_style_color(imgui.COLOR_TEXT,1,1,1,1)
            imgui.push_style_color(imgui.COLOR_CHECK_MARK,1,1,1)

            if os.path.isdir(self.path) == True:
                

                #~mods ui list
                imgui.separator()
                imgui.text("~mods" + ":" + str(len(self._mod_list)))

             

                imgui.same_line()
                imgui.indent(420)

                # button
                if os.path.isdir(self.path + "/" + "~mods") == True:
                        
                
                    if imgui.button("open ~mods folder"):
                        if sys.platform == "win32":

                            subprocess.Popen(['explorer', "{0}".format(self.path + "\~mods")])

                        if sys.platform == "linux":
                            os.system('xdg-open "%s"' % self.path + "/~mods")

                
                else:
                    
                    if os.path.isdir(self.path + "/" + "~mods") == False:
                        imgui.text(" Folder Not Present.")

                
                imgui.indent(-420)
                imgui.separator()
            

                if os.path.isdir(self.path + "/" + "~mods") == True:
                    imgui.indent(20)
                    for i in self._mod_list:
                            
                        _, i.active = imgui.checkbox(i.name, i.active)
                        self.activation(i.active,i.location) 
                                


                    if len(self._mod_list) == 0:
                        imgui.text("No mods found inside the ~mods folder")
                        imgui.text("Tip: " +"Please make sure that each mod has its own separate folder.")
                    imgui.indent(-20)
                

                




                #mods ui list
                imgui.separator()
                imgui.text("mods" + ":" + str(len(self.mod_list)))

             

                imgui.same_line()
                imgui.indent(420)

                # button
                if os.path.isdir(self.path + "/" + "mods") == True:
                        
                
                    if imgui.button("open mods folder"):
                        if sys.platform == "win32":

                            subprocess.Popen(['explorer', "{0}".format(self.path + "\mods")])

                        if sys.platform == "linux":
                            os.system('xdg-open "%s"' % self.path + "/mods")

                
                else:
                    
                    if os.path.isdir(self.path + "/" + "mods") == False:
                        imgui.text(" Folder Not Present.")

                
                imgui.indent(-420)
                imgui.separator()
            

                if os.path.isdir(self.path + "/" + "mods") == True:
                    imgui.indent(20)
                    for i in self.mod_list:
                            
                        _, i.active = imgui.checkbox(i.name, i.active)
                        self.activation(i.active,i.location) 
                                


                    if len(self.mod_list) == 0:
                        imgui.text("No mods found inside the mods folder")
                        imgui.text("Tip: " +"Please make sure that each mod has its own separate folder.")
                    imgui.indent(-20)
                



                    
                #logicmods ui list
                imgui.separator()
                imgui.text("logicmods" + ":" + str(len(self.logicmods_list)))

             

                imgui.same_line()
                imgui.indent(420)

                # button
                if os.path.isdir(self.path + "/" + "logicmods") == True:
                        
                
                    if imgui.button("open logicmods folder"):
                        if sys.platform == "win32":

                            subprocess.Popen(['explorer', "{0}".format(self.path + "\logicmods")])

                        if sys.platform == "linux":
                            os.system('xdg-open "%s"' % self.path + "/logicmods")

                
                else:
                    
                    if os.path.isdir(self.path + "/" + "logicmods") == False:
                        imgui.text(" Folder Not Present.")

                
                imgui.indent(-420)
                imgui.separator()
            

                if os.path.isdir(self.path + "/" + "logicmods") == True:
                    imgui.indent(20)
                    for i in self.logicmods_list:
                            
                        _, i.active = imgui.checkbox(i.name, i.active)
                        self.activation(i.active,i.location) 
                                


                    if len(self.logicmods_list) == 0:
                        imgui.text("No mods found inside the logicmods folder")
                        imgui.text("Tip: " +"Please make sure that each mod has its own separate folder.")
                    imgui.indent(-20)







            else:

                imgui.text("This program was not placed in Steam\steamapps\common\Tekken 8.")
                


            imgui.pop_style_color()
            imgui.pop_style_color()
            
            


    

    def main(self):

            # Initialize the library
            if not glfw.init():
                return

            # Create a windowed mode window and its OpenGL context
            glfw.window_hint(glfw.RESIZABLE,glfw.FALSE)
            window = glfw.create_window(600, 600, "Tekken 8 Mod Manager", None, None)
            


            #windows icon
            window_icon = None
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                #print('running in a PyInstaller bundle')
                window_icon = os.path.abspath(os.path.dirname(__file__)) + "\icon.ico"
                img = Image.open(window_icon)
                glfw.set_window_icon(window,1,img)

            else:
                #print('running in a normal Python process')
                    
                if sys.platform == "linux":
                    pass
                elif sys.platform == "win32":
                    #window_icon =  os.path.dirname(os.path.abspath(__file__)) +"/assets/icon.ico"
                    #img = Image.open(window_icon)
                    #glfw.set_window_icon(window,1,img)
                    pass
                   

           
            

            if not window:
                glfw.terminate()
                return


            # Make the window's context current
            glfw.make_context_current(window)
            glfw.swap_interval(2)
            


            # initilize imgui context (see documentation)
            imgui.create_context()
            impl = GlfwRenderer(window)

            """
            io = imgui.get_io()
            font_scaling_factor = 1
            font_size_in_pixels = 30
            io.fonts.add_font_from_file_ttf("assets/arial.ttf", font_size_in_pixels * font_scaling_factor)
            io.font_global_scale /= font_scaling_factor
            """


            #function
            program = mod_manager()
            program.generate_modlist()
            

            

            # Loop until the user closes the window
            while not glfw.window_should_close(window):
                # Render here, e.g. using pyOpenGL

                glClearColor(1, 1, 1, 1)
                glClear(GL_COLOR_BUFFER_BIT)


                
                imgui.new_frame()
                
                
                
                mod_title = " "
                if os.path.isdir(self.path) == False:
                    mod_title = " "
                else:
                    mod_title = " Total:" + str( len(program._mod_list) + len(program.logicmods_list) + len(program.mod_list)) 


                   
            
                imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,0.05,0.05,0.05)
                imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE,radians(24.3),radians(33.4),radians(76.5))
                imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND,1,0,0)
                
                
                #with imgui.begin_main_menu_bar():
                    

                    #_,self.toggle_view = imgui.checkbox("View Toggle",self.toggle_view)
                        
                    #imgui.button("About")

                imgui.set_next_window_size(glfw.get_window_size(window)[0],glfw.get_window_size(window)[1])
                imgui.set_next_window_position(0,0)
                imgui.push_style_color(imgui.COLOR_TEXT,0.1,0.1,0.1,1)

                with imgui.begin(mod_title,False,imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE):
                        
                        #if self.toggle_view:
                            #program.ui_treeview(self.path)
                        #else:
                        program.ui_checklist()
                       
                    
                        
                    
                imgui.pop_style_color()
                    

                imgui.pop_style_color()
                imgui.pop_style_color()
                imgui.pop_style_color()
        
                #imgui.show_demo_window()

                
                imgui.render()
                impl.render(imgui.get_draw_data())




                # Swap front and back buffers
                glfw.swap_buffers(window)
                

                # Poll for and process events
                glfw.poll_events()
                glfw.wait_events()
                impl.process_inputs()



            impl.shutdown()
            glfw.terminate()
            




program = mod_manager()
if __name__ == "__main__":
  
    program.main()


