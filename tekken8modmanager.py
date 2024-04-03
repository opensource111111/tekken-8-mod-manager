import os
import sys

import glfw
import imgui
import OpenGL
from OpenGL.GL import *
from imgui.integrations.glfw import GlfwRenderer





class mod_manager:
    
    def __init__(self):
        self.mod_list : mod_list_format = []
        self.path : str = ""
        
        if getattr(sys,"frozen", False):
            self.path = os.path.dirname(sys.executable) + "/Polaris/Content/Paks"
        else:
            self.path =  os.path.dirname(os.path.abspath(__file__)) + "/Polaris/Content/Paks"
        print(self.path)


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
        if len(self.mod_list) == 0 and os.path.isdir(self.path) == True:
            imgui.text("No Mods.....")

        if os.path.isdir(self.path) == False:
            imgui.text("This program was not placed in the Tekken 8 game folder.")


        

    def main(self):

        # Initialize the library
        if not glfw.init():
            return

        # Create a windowed mode window and its OpenGL context
        glfw.window_hint(glfw.RESIZABLE,glfw.FALSE)
        window = glfw.create_window(480, 480, "Tekken 8 Mod Manager", None, None)
        
       
        
        #glfw.set_window_icon(window,1,d)

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
                mod_title = str(len(program.mod_list)) + " Mods"


            imgui.set_next_window_size(480,480)
            imgui.set_next_window_position(0,0)
            imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,0.05,0.05,0.05)
            imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE,1,0,0)
            imgui.push_style_color(imgui.COLOR_TEXT,0,0,0,1)
            imgui.begin(mod_title,False,imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE)
            imgui.pop_style_color()
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