import os
import sys
import subprocess

import glfw
import imgui
import OpenGL
from OpenGL.GL import *
from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl



class mod_list_format:
        name : str = ""
        location : str = ""
        _type : str = ""
        active : bool = True


    
def name_sort(mod_list):
    return mod_list.name.title()
   


class mod_manager:
    
    def __init__(self):

        self._mod_list : mod_list_format = []
        self.logicmods_list : mod_list_format = []


        self.path : str = ""
        
        if getattr(sys,"frozen", False):
            self.path = os.path.dirname(sys.executable) + "\Polaris\Content\Paks"
        else:
            self.path =  os.path.dirname(os.path.abspath(__file__)) + "\Polaris\Content\Paks"
        
       



    def generate_modlist(self):

        self._mod_list.clear()
        self.logicmods_list.clear()

        if os.path.isdir(self.path):
                
            for folder in os.listdir(self.path):

                if os.path.isdir(self.path + "/" + folder):

                    if folder == "~mods" or folder == "logicmods":
                        
                        for mod_folder in os.listdir(self.path + "/" + folder):
                            
                            if os.path.isdir(self.path + "/" + folder   + "/" + mod_folder):
                                
                                if os.listdir(self.path + "/" + folder   + "/" + mod_folder) != [] :

                                    if folder == "~mods":
                                        new = mod_list_format()
                                        new._type = folder
                                        new.name = mod_folder.title()
                                        new.location = self.path + "/" + folder + "/" + mod_folder
                                    
                                        for filecheck in os.listdir(self.path + "/" + folder + "/" + mod_folder):
                                            
                                            if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                
                                                if filecheck.endswith("-x"):
                                                    new.active = False
                                                else:
                                                    new.active = True
                                                
                                        self._mod_list.append(new)



                                    if folder == "logicmods":

                                        new = mod_list_format()
                                        new._type = folder
                                        new.name = mod_folder.title()
                                        new.location = self.path + "/" + folder + "/" + mod_folder
                                    
                                        for filecheck in os.listdir(self.path + "/" + folder + "/" + mod_folder):
                                            
                                            if filecheck.endswith("pak") | filecheck.endswith("pak-x") | filecheck.endswith("ucas") | filecheck.endswith("ucas-x") | filecheck.endswith("utoc") | filecheck.endswith("utoc-x"):
                                                
                                                if filecheck.endswith("-x"):
                                                    new.active = False
                                                else:
                                                    new.active = True
                                                
                                        self.logicmods_list.append(new)

        
            self._mod_list.sort(reverse=False,key=name_sort)
            self.logicmods_list.sort(reverse=False,key=name_sort)
           

            

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
                    




    def ui_checklist(self):
        
        
        self.generate_modlist()


        
        imgui.push_style_color(imgui.COLOR_TEXT,1,1,1,1)
        imgui.push_style_color(imgui.COLOR_CHECK_MARK,1,1,1)

        if os.path.isdir(self.path) == True:
            
            #~mods ui list
            imgui.separator()
            imgui.text("~mods" + ":" + str(len(self._mod_list)))
            imgui.separator()
            

            for i in self._mod_list:
                
                    _, i.active = imgui.checkbox(i.name, i.active)
                    self.activation(i.active,i.location) 
                    
                
            if len(self._mod_list) == 0:
                imgui.text("No mods found inside ~mods")
                imgui.text("Tip: " +"Please make sure that each mod has its own separate folder.")

            
        
        


            #logicmods ui list
            imgui.separator()
            imgui.text("logicmods" + ":" + str(len(self.logicmods_list)))
            imgui.separator()


            if len(self.logicmods_list) == 0:
                    imgui.text("No mods found inside logicmods")
                    imgui.text("Tip: " +"Please make sure that each mod has its own separate folder.")





            for i in self.logicmods_list:
                    
                    _, i.active = imgui.checkbox(i.name, i.active)
                    self.activation(i.active,i.location) 
                
        
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
        window = glfw.create_window(480, 480, "Tekken 8 Mod Manager", None, None)
        
       
        

        if not window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(window)
        glfw.swap_interval(2)
        
        # initilize imgui context (see documentation)
        imgui.create_context()
        impl = GlfwRenderer(window)
       

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
                mod_title = " Total:" + str(len(program._mod_list) + len(program.logicmods_list)) 

            
            imgui.set_next_window_size(glfw.get_window_size(window)[0],glfw.get_window_size(window)[1])
            imgui.set_next_window_position(0,0)
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,0.05,0.05,0.05)
            imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE,1,0,0)
            imgui.push_style_color(imgui.COLOR_TEXT,0.1,0.1,0.1,1)

            
            with imgui.begin(mod_title,False,imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE):
                

                program.ui_checklist()

            
                

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


