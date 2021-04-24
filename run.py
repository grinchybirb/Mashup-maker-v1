import os
import shutil
import zipfile
import webbrowser

# build html file, and show list of pngs
def show_png(list_files):
    cdir=os.getcwd()
    html_file="walrus.html"
    f = open(html_file, "w")
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<body>\n")
    f.write("<h1>Select item(s). E.g. 1 3-5 15, remember your numbers, and write it in the command line</h1>\n")
    count=0
    for full_file in list_files:
        tmp='<p> Image number '+str(count)+'</p>\n'
        f.write(tmp)
        full_file2=os.path.join(cdir,full_file)
        tmp='<img src="file:///'+full_file2+ '" alt="walrus" style="width:100px;height:100px;">\n'
        f.write(tmp)
        count +=1
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()

    
    temp = os.path.join(cdir,html_file)
    url = 'file:///'+temp
    webbrowser.open_new(url)



def util(source_dir,target_dir):
    # copying files
    i=0
    list_files=[]
    for root, dirs, files in os.walk(source_dir, topdown=True):
        for file in files:
            if file.endswith(".png"):
                full_file=os.path.join(root,file)
                list_files.append(full_file)
                print(i,full_file)
                i +=1

    # it is inclusive, meaning 2 and 5 will be in it
    show_png(list_files)
    print("Select item(s). E.g. 1 3-5 15 ")
    temp_str = input().lower().strip()
    if temp_str=="":
        return
    temp_list=temp_str.split(" ")
    for temp in temp_list:
        if "-" in temp:
            # range
            list_files_num=temp.split("-")
            low=int(list_files_num[0])
            high=int(list_files_num[1])
        else:
            low=int(temp)
            high=low
        if high>=len(list_files):
            print("Invalid: Too high",high)
            return
        for i_c in range(low,high+1):
            shutil.copy(list_files[i_c],target_dir)
            print("Zipping file",i_c,list_files[i_c])
                
        
    print("NEW SUBSECTION!")





print("starting")
sample_dir=os.path.join(".","samples")
sword_dir=os.path.join(sample_dir,"swords")
gui_dir=os.path.join(sample_dir,"gui")
wool_dir=os.path.join(sample_dir,"wool")
particle_dir=os.path.join(sample_dir,"particles")
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

# add swords
target_dir=os.path.join(target_dir_temp,"items")
os.mkdir(target_dir)
util(sword_dir,target_dir)

# add wool
target_dir=os.path.join(target_dir_temp,"blocks")
os.mkdir(target_dir)
util(wool_dir,target_dir)

target_dir=os.path.join(target_dir_temp,"particle")
os.mkdir(target_dir)
util(particle_dir,target_dir)

target_dir=os.path.join(target_dir_temp,"gui")
os.mkdir(target_dir)
util(gui_dir,target_dir)





# add description
full_file=os.path.join(sample_dir,"pack.mcmeta")
shutil.copy(full_file,target_base)

# add pack image
full_file2=os.path.join(sample_dir,"pack.png")
shutil.copy(full_file2,target_base)
# create a zip file
shutil.make_archive(zipfile_name, 'zip', root_dir=target_base)
print("finished")