import os
import sys

import glfw
import imgui
import OpenGL
from OpenGL.GL import *
from imgui.integrations.glfw import GlfwRenderer





""" 
    Tekken 8 Mod Manager

    Inspinerd by CDDTreborn's Tekken 8 Mod On / Off Switch (Version 2) at https://tekkenmods.com/mod/3312/tekken-8-mod-on-off-switch-version-2


    Dependences
    - Python: https://www.python.org/
    - glfw: pip install glfw
    - numpy: pip install numpy
    - PyOpenGL : pip install PyOpenGL
    - imgui: pip install imgui

    ***Instruction***
    1. Place script inside the Tekken 8 game folder.

    Linux - Open terminal and type "python3" or "python". Drag and drop script onto the terminal and press enter.
    Window - Right click file and Open with Python



   How it works.
   - Searches for folder ~mods and logicmods inside the Tekken 8 folder
   - Adds or removes "-x" at the end of the files to enabled/disabled a mod.
    - Enabled = Filenames not ending with "-x"
    - Disabled = Filenames ending with "-x"

"""





class mod_manager:
    
    def __init__(self):
        self.mod_list : mod_list_format = []
        self.path : str = os.path.dirname(os.path.abspath(__file__)) + "/Polaris/Content/Paks"

    class mod_list_format:
        name : str = ""
        location : str = ""
        active : bool = True

        
    
    def getname(self,mod_list):
        return mod_list.name.upper()
   


    def find_mods(self):


        if os.path.isdir(self.path):
                
            for folder in os.listdir(self.path):
                if os.path.isdir(self.path + "/" + folder):
                    if folder == "~mods" or folder == "logicmods":
                        
                        for mod_folder in os.listdir(self.path + "/" + folder):
                                
                            new = mod_manager.mod_list_format()
                            new.name = mod_folder.upper()
                            new.location = self.path + "/" + folder + "/" + mod_folder

                            for filecheck in os.listdir(self.path + "/" + folder + "/" + mod_folder):
                                if filecheck.endswith("-x"):
                                    new.active = False
                                        
                            self.mod_list.append(new)

            self.mod_list.sort(reverse=False,key=self.getname)
        
    
            


    def activation(self,state,dir):

        if os.path.isdir(dir) == True:
            for file in os.listdir(dir):
                
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
                

    def updateList(self):
 
        self.mod_list.clear()
        self.find_mods()
               


    def ui_checklist(self):
        
        
        self.updateList()

        imgui.push_style_color(imgui.COLOR_CHECK_MARK,1,1,1)
        for i in self.mod_list:
            _, i.active = imgui.checkbox(i.name, i.active)
            
            self.activation(i.active,i.location) 
                
        imgui.pop_style_color()
        


        if os.path.isdir(self.path) == True:
            if len(self.mod_list) == 0:
                imgui.text("No Mods.....")
        else:
             imgui.text("Please place this script inside the Tekken 8 folder.")
        
            
        

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
       
        program = mod_manager()
        program.find_mods()
      

        title = ""


        # Loop until the user closes the window
        while not glfw.window_should_close(window):
            # Render here, e.g. using pyOpenGL

            
            glClearColor(1, 1, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT)


            
            imgui.new_frame()

            if os.path.isdir(self.path) == True:
                title = str(len(program.mod_list)) + " Mods"
            else:
                title = " "

            imgui.set_next_window_size(480,480)
            imgui.set_next_window_position(0,0)
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,0.05,0.05,0.05)
            imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE,1,0,0)

            imgui.begin(title,False,imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE)
            imgui.pop_style_color()
            imgui.pop_style_color()
            program.ui_checklist()

            imgui.end()
            
    

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
