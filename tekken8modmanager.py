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
import numpy



class mod_list_format:
        name : str = ""
        location : str = ""
        _type : str = ""
        active : bool = True
        icon  =  None
        

   

    
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
        

        self.toggle_about : bool = False
        self.toggle_view : bool = False


        self.toggle_mods : bool = True
        self.toggle__mods : bool = True
        self.toggle_logicmods : bool = True


        self.version = 1.3
        self.about_message : str = "Created by Beanman"
        self.no_mod_message : str = "No mods were found inside the {0} folder"
        self.folder_message : str = " Folder not present."
        self.tip_message : str = "Tip: Please make sure that each mod has its own separate folder."
        self.path_error : str = "This program was not placed in Steam\steamapps\common\Tekken 8."


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
            
        
       




    def generate_modlist_with_subfolders(self):

        self._mod_list.clear()
        self.mod_list.clear()
        self.logicmods_list.clear()
        


        if os.path.isdir(self.path):
            

            for folder in os.listdir(self.path):
                
                #checking for root mod folders.
                if os.path.isdir(self.path + "/" + folder):

                    if folder == "~mods" or folder == "mods" or folder == "logicmods":


                        # look through the root mod folders.
                        for root, dirnames, filenames  in os.walk(self.path +"/" + folder):

                                for mod_folder in dirnames:

                                    if os.path.isdir(root + "/" + mod_folder):
                                
                                        if os.listdir(root  + "/" + mod_folder) != []:
                                            
                                            if self.toggle_view == False:
                                                for i in os.listdir(root  + "/" + mod_folder):
                                                    if i.endswith("pak") | i.endswith("pak-x") | i.endswith("ucas") | i.endswith("ucas-x") | i.endswith("utoc") | i.endswith("utoc-x"):
                                                        

                                                        new = mod_list_format()
                                                        new._type = folder
                                                        new.name = mod_folder
                                                        new.location = root  + "/" + mod_folder
                                                        #new.icon.append(self.ui_images())
                                                        
                                                        for filecheck in os.listdir(root  + "/" + mod_folder):
                                                            #if filecheck.startswith("thumbnail"):
                                                                #new.icon = [self.ui_images(root  + "/" + mod_folder + "/" + filecheck)]
                                                            
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
                                                        break
                                            
                                            else:
                                                        new = mod_list_format()
                                                        new._type = folder
                                                        new.name = mod_folder
                                                        new.location = root  + "/" + mod_folder
                                                        #new.icon.append(self.ui_images())
                                                        
                                                        for filecheck in os.listdir(root  + "/" + mod_folder):
                                                            #if filecheck.startswith("thumbnail"):
                                                                #new.icon = [self.ui_images(root  + "/" + mod_folder + "/" + filecheck)]
                                                            
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
           
    




    def activation_list(self,state,dir):



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
    
    

    

    def ui_listview(self):
            
        self.generate_modlist_with_subfolders()

            
        imgui.push_style_color(imgui.COLOR_TEXT,1,1,1,1)
        imgui.push_style_color(imgui.COLOR_CHECK_MARK,1,1,1)

     
        
        
      
                
        if os.path.isdir(self.path) == True:
                    
            
                
            #~mods ui list
            imgui.separator()
            imgui.text("~mods" + ":" + str(len(self._mod_list)))
            
                

            imgui.same_line()
            imgui.indent(417)

                    # button
            if os.path.isdir(self.path + "/" + "~mods") == True:
                            
                imgui.push_style_color(imgui.COLOR_BUTTON,radians(11),radians(22),radians(76.5))
                if imgui.button("Open ~mods Folder"):
                            if sys.platform == "win32":

                                subprocess.Popen(['explorer', "{0}".format(self.path + "\~mods")])

                            if sys.platform == "linux":
                                os.system('xdg-open "%s"' % self.path + "/~mods")

                imgui.pop_style_color()   
            else:
                        
                if os.path.isdir(self.path + "/" + "~mods") == False:
                            imgui.text(" Folder not present.")

               
            imgui.indent(-417)
            imgui.separator()
                    

            if os.path.isdir(self.path + "/" + "~mods") == True:
                        
                        
                for i in self._mod_list:
                    """
                    glBindTexture(GL_TEXTURE_2D, i.icon[0])     
                    imgui.image(i.icon[0],50,50)    
                    if imgui.is_item_hovered():  
                        if imgui.begin_tooltip():   
                            imgui.image(i.icon[0],250,200)
                        imgui.end_tooltip()
                                
                    imgui.same_line()
                    """      
                    _, i.active = imgui.checkbox(i.name, i.active)
                    if imgui.is_item_edited:
                        self.activation_list(i.active,i.location) 
                                    


                if len(self._mod_list) == 0:
                    imgui.text(self.no_mod_message.format(~mods))
                    imgui.text(self.tip_message)
                       
                    

                 


                

            #mods ui list
            imgui.separator()
            imgui.text("mods" + ":" + str(len(self.mod_list)))

                

            imgui.same_line()
            imgui.indent(417)

            # button
            if os.path.isdir(self.path + "/" + "mods") == True:
                            
                imgui.push_style_color(imgui.COLOR_BUTTON,radians(11),radians(22),radians(76.5))  
                if imgui.button("Open mods Folder"):
                    if sys.platform == "win32":

                        subprocess.Popen(['explorer', "{0}".format(self.path + "\mods")])

                    if sys.platform == "linux":
                        os.system('xdg-open "%s"' % self.path + "/mods")

                
                imgui.pop_style_color()       
            else:
                        
                if os.path.isdir(self.path + "/" + "mods") == False:
                    imgui.text(self.folder_message)

                    
            imgui.indent(-417)
            imgui.separator()
                

            if os.path.isdir(self.path + "/" + "mods") == True:
                #imgui.indent(20)
                for i in self.mod_list:
                    """
                    glBindTexture(GL_TEXTURE_2D, i.icon[0])     
                    imgui.image(i.icon[0],50,50)    
                    if imgui.is_item_hovered():  
                        if imgui.begin_tooltip():
                                            
                            imgui.image(i.icon[0],250,200)
                        imgui.end_tooltip()
                             
                    imgui.same_line()
                    """
                    _, i.active = imgui.checkbox(i.name, i.active)
                    self.activation_list(i.active,i.location) 
                                    


                if len(self.mod_list) == 0:
                    imgui.text(self.no_mod_message.format("mods"))
                    imgui.text(self.tip_message)
                 
                    

                        




            #logicmods ui list
            imgui.separator()
            imgui.text("logicmods" + ":" + str(len(self.logicmods_list)))

                

            imgui.same_line()
            imgui.indent(417)

            # button
            if os.path.isdir(self.path + "/" + "logicmods") == True:
                            
                imgui.push_style_color(imgui.COLOR_BUTTON,radians(11),radians(22),radians(76.5))  
                if imgui.button("Open logicmods Folder"):
                    if sys.platform == "win32":

                        subprocess.Popen(['explorer', "{0}".format(self.path + "\logicmods")])

                    if sys.platform == "linux":
                        os.system('xdg-open "%s"' % self.path + "/logicmods")

                
                
                imgui.pop_style_color()    
            else:
                        
                if os.path.isdir(self.path + "/" + "logicmods") == False:
                    imgui.text(self.folder_message)

                    
            imgui.indent(-417)
            imgui.separator()
                

            if os.path.isdir(self.path + "/" + "logicmods") == True:
                #imgui.indent(20)
                for i in self.logicmods_list:
                    """
                    glBindTexture(GL_TEXTURE_2D, i.icon[0])     
                    imgui.image(i.icon[0],50,50)    
                    if imgui.is_item_hovered():  
                        if imgui.begin_tooltip():              
                            imgui.image(i.icon[0],250,200)
                            imgui.text("Hello")
                        imgui.end_tooltip()

                            

                    imgui.same_line()
                    """           
                    _, i.active = imgui.checkbox(i.name, i.active)
                    self.activation_list(i.active,i.location) 
                                    


                if len(self.logicmods_list) == 0:
                    imgui.text(self.no_mod_message.format("logicmods folder"))
                    imgui.text(self.tip_message)
              

                

                        


        else:

            imgui.text(self.path_error)
            
            

        imgui.pop_style_color()
        imgui.pop_style_color()
                
        
    
    """

    def ui_listview_Test(self):
            
        self.generate_modlist_with_subfolders()

            
        imgui.push_style_color(imgui.COLOR_TEXT,1,1,1,1)
        imgui.push_style_color(imgui.COLOR_CHECK_MARK,1,1,1)

     
        flags = imgui.TABLE_BORDERS_VERTICAL| imgui.TABLE_BORDERS_OUTER_HORIZONTAL| imgui.TABLE_RESIZABLE | imgui.TABLE_ROW_BACKGROUND | imgui.TABLE_NO_BORDERS_IN_BODY | imgui.TABLE_SCROLL_Y | imgui.TABLE_COLUMN_NO_RESIZE | imgui.WINDOW_NO_MOVE

        with imgui.begin_table("Hello",4,flags):
            imgui.table_setup_column("Name",imgui.TABLE_COLUMN_NO_HIDE)
            imgui.table_setup_column("Version",imgui.TABLE_COLUMN_NO_HIDE)
            imgui.table_setup_column("Creater",imgui.TABLE_COLUMN_NO_HIDE)
            imgui.table_setup_column("Location",imgui.TABLE_COLUMN_NO_HIDE)
            imgui.table_setup_scroll_freeze(0,1) 
            imgui.table_headers_row()
            

            imgui.table_next_row()
            imgui.table_next_column()
            
       
        
                    
            if os.path.isdir(self.path) == True:
                        
                
                    
                #~mods ui list
               

                # button
                if os.path.isdir(self.path + "/" + "~mods") == True:
                                
                    pass
             
                
                if os.path.isdir(self.path + "/" + "~mods") == True:
                    
                
                                
                        for i in self._mod_list:
                            
                              
                            _, i.active = imgui.checkbox(i.name, i.active)
                            if imgui.is_item_edited:
                                self.activation_list(i.active,i.location) 
                            
                            imgui.table_next_column()
                            imgui.text_disabled("--")
                            imgui.table_next_column()
                            imgui.text_disabled("--")
                            imgui.table_next_column()
                            imgui.text(i._type) 
                            
                             
                            imgui.same_line()
                            if imgui.button("##"+"Open ~mods Folder"):
                                if sys.platform == "win32":

                                    subprocess.Popen(['explorer', "{0}".format(self.path + "\~mods")])

                                if sys.platform == "linux":
                                    os.system('xdg-open "%s"' % self.path + "/~mods")
                            
                            
                            imgui.table_next_column()                


                 
                            

                        


                    

                #mods ui list
               
        
                # button
                if os.path.isdir(self.path + "/" + "mods") == True:
                                
                    pass
             
               
                    

                if os.path.isdir(self.path + "/" + "mods") == True:
                    #imgui.indent(20)
                    for i in self.mod_list:
                        

                        _, i.active = imgui.checkbox(i.name, i.active)
                        self.activation_list(i.active,i.location) 
                        imgui.table_next_column()
                        imgui.text_disabled("--")
                        imgui.table_next_column()
                        imgui.text_disabled("--")
                        imgui.table_next_column()
                        imgui.text(i._type) 
                       


                         
                        imgui.same_line()
                        if imgui.button("##"+"Open mods Folder"):
                            if sys.platform == "win32":

                                subprocess.Popen(['explorer', "{0}".format(self.path + "\mods")])

                            if sys.platform == "linux":
                                os.system('xdg-open "%s"' % self.path + "/mods")
                        
                        
                        imgui.table_next_column()          



                            




                #logicmods ui list
            
    


                # button
                if os.path.isdir(self.path + "/" + "logicmods") == True:
                   pass
               
                        
             

                if os.path.isdir(self.path + "/" + "logicmods") == True:
                    #imgui.indent(20)
                    for i in self.logicmods_list:
                       

                        _, i.active = imgui.checkbox(i.name, i.active)
                        self.activation_list(i.active,i.location) 
                        imgui.table_next_column()
                        imgui.text_disabled("--")
                        imgui.table_next_column()
                        imgui.text_disabled("--")
                        imgui.table_next_column()             
                        imgui.text(i._type) 
                        

                            
                        imgui.same_line()
                        if imgui.button("##"+"Open logicmods Folder"):
                            if sys.platform == "win32":

                                subprocess.Popen(['explorer', "{0}".format(self.path + "\logicmods")])

                            if sys.platform == "linux":
                                os.system('xdg-open "%s"' % self.path + "/logicmods")
                        
                        
                        imgui.table_next_column()    

                            


            else:

                imgui.text(self.path_error)
                
            

        imgui.pop_style_color()
        imgui.pop_style_color()
                
        
    """




    
    def activation_tree(self,state,directory, indent = 0):
        
       
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
        
                

            if os.path.isdir(item_path):
                
                
                for i in self._mod_list:
                        
                        if item == i.name:
                            
                            i.active = state


                
                for i in self.mod_list:
                        
                        if item == i.name:
                            
                            i.active = state  
               

                
                for i in self.logicmods_list:
                        
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

  
       


    def ui_treeview(self, directory, indent=0):

        self.generate_modlist_with_subfolders()
    
        
        imgui.push_style_color(imgui.COLOR_TEXT,1,1,1,1)
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            match  item:
                    
                    
                    case "~mods":

                        _,self.toggle__mods = imgui.checkbox("##"+"mm",self.toggle__mods)
                        if imgui.is_item_edited():
     
                            self.activation_tree(self.toggle__mods,self.path +"/~mods") 
                        imgui.same_line()
                    case "mods":

                        _,self.toggle_mods = imgui.checkbox("##"+"m",self.toggle_mods)
                        if imgui.is_item_edited():
                                
                           
                            self.activation_tree(self.toggle_mods,self.path +"/mods") 
                        imgui.same_line()
                    case "logicmods":

                        _,self.toggle_logicmods = imgui.checkbox("##"+"l",self.toggle_logicmods)
                        if imgui.is_item_edited():
                                
                           
                            self.activation_tree(self.toggle_logicmods,self.path +"/logicmods") 
                        imgui.same_line()

            
          



            if os.path.isdir(item_path):
                
              
                    
                    for i in self._mod_list:
                            
                            if item == i.name:
                                
                                _,i.active = imgui.checkbox("##"+i.name,i.active)
                                
                                if imgui.is_item_edited():
                                    #print(i.active)
                                    self.toggle__mods  = True
                                    self.activation_tree(i.active,i.location) 
                                imgui.same_line()

                    
                    for i in self.mod_list:
                            
                            if item == i.name:
                                
                                _,i.active = imgui.checkbox("##"+i.name,i.active)
                                
                                if imgui.is_item_edited():
                                    #print(i.active)
                                    self.toggle_mods = True
                                    self.activation_tree(i.active,i.location) 
                                imgui.same_line()

                    
                    for i in self.logicmods_list:
                            
                            if item == i.name:
                                
                                _,i.active = imgui.checkbox("##"+i.name,i.active)
                                
                                if imgui.is_item_edited():
                                    #print(i.active)
                                    self.toggle_logicmods = True
                                    self.activation_tree(i.active,i.location) 
                                imgui.same_line()



                    #print(f"{'  ' * indent}Directory: {item}") 
                    

                
                
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
                    
                

                
               

        imgui.pop_style_color()

        
       
   

    """
    def ui_images(self, image = "assets/icon.ico"):
        

        img = Image.open(image).convert("RGBA")
        imdata = numpy.array(list(img.getdata()),numpy.uint8)
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
        

       

        return texname

    """



    def main_window_bar(self):

        #https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html#imgui.core.listbox_header
        
        with imgui.begin_main_menu_bar():
            
           

        
            
            #view modes
            if imgui.begin_menu("View"):
                
                _, list_view = imgui.menu_item("List View")
                _, tree_view = imgui.menu_item("Tree View")
                
                if list_view:
                    self.toggle_view = False
                    self.generate_modlist_with_subfolders()
                    #print("list view")
                

                if tree_view:
                    self.toggle_view  = True
                    self.generate_modlist_with_subfolders()
                    #print("tree view")
                
      
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
                
                imgui.set_next_window_size(150,150)
                imgui.begin("About",False,imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
            
            
                imgui.indent(10)
                imgui.text_wrapped(self.about_message)
                imgui.indent(-10)
                imgui.indent(50)
                for i in range(5):
                    imgui.spacing() 
                    pass
                    
                if imgui.button("Close"):
                    self.toggle_about = False
                imgui.end()
            


            """
            #Refresh
            imgui.indent(400)
            if imgui.button("Refresh"):
                self.generate_modlist_with_subfolders()
            """  
             




    def main_window_box(self,window):


        
    
             
        mod_title = " "
        if os.path.isdir(self.path) == False:
            mod_title = " "
        else:
            mod_title = " Total:" + str( len(program._mod_list) + len(program.logicmods_list) + len(program.mod_list)) 




        imgui.set_next_window_size(glfw.get_window_size(window)[0],glfw.get_window_size(window)[1]-20)
        imgui.set_next_window_position(0,20)
        imgui.push_style_color(imgui.COLOR_TEXT,0.1,0.1,0.1,1)




        with imgui.begin("##" + mod_title,False,imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE):
                        
            
            if self.toggle_view == True:
                self.ui_treeview(self.path)
            
            else:

                self.ui_listview()
            
                    
                

        imgui.pop_style_color()
        




    def main(self):
            
            # Initialize the library
            if not glfw.init():
                return

            # Create a windowed mode window and its OpenGL context
            glfw.window_hint(glfw.RESIZABLE,glfw.FALSE)
            window = glfw.create_window(600, 600, "Tekken 8 Mod Manager " , None, None)
            

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
            imgui.style_colors_dark()



            #font
            
            """
            window_font = os.path.abspath(os.path.dirname(__file__)) + "/arial.ttf"
            io = imgui.get_io()
            font_scaling_factor = 1
            font_size_in_pixels = 16
            fonts = io.fonts.add_font_from_file_ttf(window_font, font_size_in_pixels * font_scaling_factor)
            io.font_global_scale /= font_scaling_factor
            impl.refresh_font_texture()
            """

                   
             
        

            
           
            self.generate_modlist_with_subfolders()
           
            

            # Loop until the user closes the window
            while not glfw.window_should_close(window):
                # Render here, e.g. using pyOpenGL

                
                glClearColor(0, 0, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT)

                
                imgui.new_frame()
                
                   
                
                imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND,0.05,0.05,0.05)
                imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE,radians(11),radians(22),radians(76.5))
                imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND,radians(11),radians(22),radians(76.5))
                
               
                
                #with imgui.font(fonts):
                self.main_window_bar()
                self.main_window_box(window)
                    
                """
                    imgui.set_next_window_size(glfw.get_window_size(window)[0],glfw.get_window_size(window)[1]-20)
                    imgui.set_next_window_position(0,20)
                    imgui.push_style_color(imgui.COLOR_TEXT,0.1,0.1,0.1,1)
                    with imgui.begin("Test", False, imgui.WINDOW_NO_TITLE_BAR):
                        self.ui_listview_Test()

                    imgui.pop_style_color()
                """

                """
                flags = imgui.TABLE_BORDERS_VERTICAL| imgui.TABLE_BORDERS_OUTER_HORIZONTAL| imgui.TABLE_RESIZABLE | imgui.TABLE_ROW_BACKGROUND | imgui.TABLE_NO_BORDERS_IN_BODY

                with imgui.begin_table("Hello",2,flags):
                    imgui.table_setup_column("Name",imgui.TABLE_COLUMN_NO_HIDE)
                    imgui.table_setup_column("Creater",imgui.TABLE_COLUMN_NO_HIDE)
                    imgui.table_headers_row()

                    imgui.table_next_column()
                    imgui.table_next_row()
                """
        
                imgui.pop_style_color()
                imgui.pop_style_color()
                imgui.pop_style_color()
               

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


