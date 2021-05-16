import os
import shutil
import zipfile
import webbrowser


class stats:
    def __init__(self):
        self.nfiles=0
        self.nroots=0
        self.nsuperroots=0

# build html file, and show list of pngs
def show_png(list_roots2,list_of_lists_of_files):

    cdir=os.getcwd()
    html_file="walrus.html"
    f = open(html_file, "w")
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<body>\n")
    f.write("<h1>Select item(s). E.g. 1 3-5 15, remember your numbers, and write it in the command line</h1>\n")
    f.write("<TABLE border='1' >")

    row_count=0
    img_count=0
    for root in list_roots2:
        f.write("<TR>\n")
        for file in list_of_lists_of_files[row_count]:
            f.write("<TD>")
            root2=os.path.join(cdir,root)
            full_file2=os.path.join(root2,file)
            tmp='<img src="file:///'+full_file2+ '" alt="walrus" style="width:100px;height:100px;">\n'
            f.write(tmp)
            tmp='<p> Image number '+str(img_count)+'</p>\n'
            f.write(tmp)
            f.write("</TD>")
            img_count +=1
        f.write("</TR>\n")
        row_count +=1


    f.write("</TABLE>")
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()

    
    temp = os.path.join(cdir,html_file)
    url = 'file:///'+temp

    webbrowser.open_new(url)

def show_png2(list_roots2,list_of_lists_of_files):
    iroot=0
    ifile=0
    for root in list_roots2:
        for file in list_of_lists_of_files[iroot]:
            print(ifile,root,file)
            ifile +=1
        iroot +=1


def copy_util(source_dir,target_dir,mystats):
    # copying files
    i=0
    list_files=[]
    list_roots2=[]
    list_of_lists_of_files=[]
    
    for root, dirs, files in os.walk(source_dir, topdown=True):
        print("=======",root,dirs,files)
        if len(files)!=0:
            list_roots2.append(root)
            list_of_lists_of_files.append(files)
            mystats.nfiles +=len(files)
            mystats.nroots +=1

        # print(root)
        for file in files:
            if file.endswith(".png"):
                full_file=os.path.join(root,file)
                list_files.append(full_file)
                # print(i,full_file)
                i +=1

    mystats.nsuperroots +=1
    show_png2(list_roots2,list_of_lists_of_files)
    # it is inclusive, meaning 2 and 5 will be in it
    print("To see the images of the files type: show. To continue to selection, press ENTER.")
    temp_str2=input().lower().strip()
    if temp_str2=="show":
        show_png(list_roots2,list_of_lists_of_files)

    print("Select item(s). E.g. 1 3-5 15 ")
    temp_str = input().lower().strip()
    if temp_str=="":
        return
    temp_list=temp_str.split(" ")
    for temp in temp_list:
        if "-" in temp:
            # range
            try:
                list_files_num=temp.split("-")
                low=int(list_files_num[0])
                high=int(list_files_num[1])
            except ValueError:
                print('Non-integer input: Section IGNORED')
                return
        else:
            try:
                low = int(temp)
                high=low
            except ValueError:
                # Handle the exception
                print('Non-integer input: Section IGNORED')
                return
            
            
        if high>=len(list_files):
            print("Invalid: Too high, section IGNORED",high)
            return
        for i_c in range(low,high+1):
            shutil.copy(list_files[i_c],target_dir)
            print("Zipping file",i_c,list_files[i_c])
                
        
    print("NEW SUBSECTION!")




def main():
    print("starting")
    mystats=stats()
    sample_dir=os.path.join(".","samples")
    sword_dir=os.path.join(sample_dir,"swords")
    gui_dir=os.path.join(sample_dir,"gui")
    wool_dir=os.path.join(sample_dir,"wool")
    particle_dir=os.path.join(sample_dir,"particles")
    gapple_dir=os.path.join(sample_dir,"gapples")
    tools_dir=os.path.join(sample_dir,"tools")
    target_base =  os.path.join(".","target") 
    zipfile_name=os.path.join(".","walrus")


    # create fresh target
    if os.path.exists(target_base):
        shutil.rmtree(target_base, ignore_errors=False, onerror=None)
    os.mkdir(target_base,0o777)

    # create levels needed for overlay to work
    target_dir_temp=os.path.join(target_base,"assets")
    os.mkdir(target_dir_temp,0o777)
    target_dir_temp=os.path.join(target_dir_temp,"minecraft")
    os.mkdir(target_dir_temp,0o777)
    target_dir_temp=os.path.join(target_dir_temp,"textures")
    os.mkdir(target_dir_temp,0o777)


    target_dir=os.path.join(target_dir_temp,"items")
    os.mkdir(target_dir)
    # add swords
    copy_util(sword_dir,target_dir,mystats)
    # add gapples
    copy_util(gapple_dir,target_dir,mystats)
    # add tools
    # add gapples
    copy_util(tools_dir,target_dir,mystats)



    target_dir=os.path.join(target_dir_temp,"blocks")
    os.mkdir(target_dir)
    # add wool
    copy_util(wool_dir,target_dir,mystats)

    target_dir=os.path.join(target_dir_temp,"particle")
    os.mkdir(target_dir)
    # add particles
    copy_util(particle_dir,target_dir,mystats)

    target_dir=os.path.join(target_dir_temp,"gui")
    os.mkdir(target_dir)
    # add crosshair
    copy_util(gui_dir,target_dir,mystats)






    # add description
    full_file=os.path.join(sample_dir,"pack.mcmeta")
    shutil.copy(full_file,target_base)

    # add pack image
    full_file2=os.path.join(sample_dir,"pack.png")
    shutil.copy(full_file2,target_base)
    # create a zip file
    shutil.make_archive(zipfile_name, 'zip', root_dir=target_base)
    print("finished","superroots",mystats.nsuperroots,"roots",mystats.nroots,"files",mystats.nfiles)



# main()
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

with PyCallGraph(output=GraphvizOutput()):
    main()