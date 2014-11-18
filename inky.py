import os
import sys
import getopt
import subprocess

from PIL import Image

#--------------------------------------
#python inky_tmp.py "mapb.txt" "id" "mapb test" ------ uses [mapb.txt] to export [id] paths only from [mapb].svg file to [test] subfolder
#--------------------------------------
def help():
    s = ''
    s+= '#'*74+'\n'
    s+= 'usage:\n'
    s+= '\n'
    s+= 'REQUIRED:\n'
    s+= '---------\n'
    s+= '\n'
    s+= '-e --extract        file to extract from data from\n'
    s+= '\n'
    s+= '     pass in either .svg file or .txt file. if a .svg file\n'
    s+= '     is supplied a txt file will be generated for easier\n'
    s+= '     repeated use. if a .txt file is passes in without any\n'
    s+= '     optional parameters, nothing will occur, just parsing\n'
    s+= '     of the file, with nothing being done from there.\n'
    s+= '\n'
    s+= 'OPTIONAL:\n'
    s+= '---------\n'
    s+= '\n'
    s+= '-a --action         what to do with data after extraction\n'
    s+= '\n'
    s+= '     single function actions:\n'
    s+= '     -------------------\n'
    s+= '     id i         image  - id extraction only\n'
    s+= '     visible v    image  - all visible within id borders\n'
    s+= '     position p   string - automate ethanon variable string id x,y positions\n'
    s+= '     size s       string - automate ethanon variable string id w,h size\n'
    s+= '     name n       string - automate ethanon variable string id name\n'
    s+= '     loadsprite l string - automate ethanon variable string\n'
    s+= '     drawsprite d string - automate ethanon variable string\n'
    s+= '\n'
    s+= '     multi function actions:\n'
    s+= '     -------------------\n'
    s+= '\n'
    s+= '-i --in           what file or folder to act on, .svg file only\n'
    s+= '-o --out          what folder to save images from svg into\n'
    s+= '-p --pre          prefix to attach to saved images\n'
    s+= '\n'
    s+= 'EXAMPLES:\n'
    s+= '---------\n'
    s+= '\n'
    s+= 'python inky.py -e mapb.svg    -will extract mapb.svg into mapb.txt, and exit\n'
    s+= '\n'
    s+= 'python inky.py -e mapb.svg -a id -o test\n'
    s+= 'python inky.py -e mapb.svg -a id -o test -p test\n'
    s+= 'python inky.py -e mapb.txt -a id -i mapb.svg -o test -p test\n'
    s+= '\n'
    s+= '     the three above examples will saves images from mapb.svg, into the test\n'
    s+= '     folder with a \'test_\' prefix. The difference is, eg 3, will read from\n'
    s+= '     a txt while 1 and 2 will read from svg file with no need for txt, but\n'
    s+= '     will also save a txt file. eg 1 also make no use of a prefix on save\n'
    s+= '\n'
    s+= 'python inky.py -e mapb.txt -i mapb.svg -a visibile -o test -p vis\n'
    s+= '\n'
    s+= '     exports into the text folder, all visible in mapb.svg based on mapb.txt\n'
    s+= '     with an added prefix of \'vis_\' on image files\n'
    s+= '\n'
    s+= '#'*74+'\n'
    return s


#def main(filename,action,args):
def main(argv):
    out=''
    
    #handle the arguments

    try:
        opts,args = getopt.getopt(argv,"he:a:i:o:p:",["help","extract=","action=","in=","out=","pre="])
    except getopt.GetoptError:
        s = '!'*74+'\n'
        s+= "you've encountered an error\n"
        s = '!'*74+'\n\n'
        s+=help()
        print s
        sys.exit(2)

    #first store inputs that are used durring actions
    
    fin = ''
    fout = ''
    prefix = ''

    data = ''

    for opt,arg in opts:
        if opt in ("-i" , "--in"):
            fin = arg
        elif opt in ("-o" , "--out"):
            fout = arg
        elif opt in ("-p" , "--pre"):
            prefix = arg+'_'

    #save file names
    extract_file_name = ''
    extract_file_parts = ''

    #now run the actions

    for opt,arg in opts:

        if opt in ("-h" , "--help"):
            print  help()
            sys.exit()

        #extract data
        elif opt in ("-e" , "--extract"):
            extract_file_name = arg
            extract_file_parts = remove_file_extension(arg)
            #part one, read the file, be it svg or txt
            if(extract_file_parts[1]=='svg'):
                #out = extract_svg(arg)
                print 'read svg'
                data = split_text_data(extract_svg(arg))
            elif(extract_file_parts[1]=='txt'):
                #out = extract_txt(arg)
                print 'read txt'
                data = split_text_data(extract_txt(arg))
            else:
                print 'please give a svg or txt file'
                sys.exit(2)

        #perform action
        elif opt in ("-a" , "--action"):

            if arg in ("id" , "i"):
                #if we extracted a svg, then we can just use that to export images from, no need for inut file
                use_file = ''
                if(extract_file_parts[1] == 'svg' and fin == ''):
                    use_file = extract_file_name
                elif(len(fin)>0):#we should validate fin as a file that we can use
                    fin_parts = remove_file_extension(fin)
                    if(len(fin_parts)>1):
                        if(fin_parts[1]=='svg'):
                            use_file = fin
                if(use_file==''):#we have no vaild file to use
                    print 'no valid file given to saves id images from'
                    sys.exit(2)
                    break
                #now we need to get the folder to save in
                if(len(fout)<=0):
                    print 'must provide a folder to save to'
                    sys.exit(2)
                    break

                save_paths_as_images(data,use_file,fout,prefix)
                print 'do id'

            elif arg in ('visible','v'):
                #check that the use file is valid
                use_file = ''
                fin_parts = remove_file_extension(fin)
                if(len(fin_parts)>1):
                    if(fin_parts[1]=='svg'):
                        use_file = fin
                if(use_file==''):#we have no vaild file to use
                    print 'no valid file given to saves id images from'
                    sys.exit(2)
                    break
                #now we need to get the folder to save in
                if(len(fout)<=0):
                    print 'must provide a folder to save to'
                    sys.exit(2)
                    break

                save_visible_as_images(data,use_file,fout,prefix)
                print 'do visible'

            elif arg in ('composite','comp','c'):
                composite(data,fin,prefix,fout)
                print 'do composite'

            elif arg in ('position','p'):
                print 'do position'
            elif arg in ('size','s'):
                print 'do size'
            elif arg in ('name','n'):
                print 'do name'
            elif arg in ('loadsprite','l'):
                print 'do loadsprite'
            elif arg in ('drawsprite','d'):
                print 'do drawsprite'
            else:
                print 'unknown action, unable to continue'
                sys.exit(2)
        #    inputfile = arg
        #elif opt in ("-o","--ofile"):
        #    outputfile = arg
    #print 'inputfile is: ',inputfile
    #print 'outputfile is: ',outputfile

    #--------------------
    #--------------------
    

    #part two, now that we have our data, we can operate our chosen action
    '''if(action=="position" or action=="positions"):
        out="private vector2[] positions = {"

    if(action=="size" or action=="sizes"):
        out="private vector2[] sizes = {"

    if(action=="name" or action=="names"):
        out="private string[] names = {"
    '''

    print out

#------------------------------------------
#this function reads a svg filem and can save the contents to a text file, named the same as the svg.txt
#or it can just return the data as a string for immediat usage
def extract_svg(svg_filename,save=True):
    out=""
    name = remove_file_extension(svg_filename)
    if(name[1]=='svg'):
        f = open(svg_filename,"r")
        cmd=['inkscape',svg_filename,'-S']
        out = subprocess.check_output(cmd)
        if(save):
            nf = open(name[0]+'.txt',"w")
            nf.write(out)
            nf.close()
            #out='saved to: '+name[0]+'.txt'
        f.close()
    else:
        out = 'only svg files are supported'
    return out

#this basically just reads the text file and returns the text inside, for immediat usage
def extract_txt(txt_filename):
    out=""
    name = remove_file_extension(txt_filename)
    if(name[1]=='txt'):
       # with open(txt_filename,"r") as f:
        f = open(txt_filename,"r")
        out = f.read()
        f.close();
    else:
        out = 'we are expecting a txt file'
    return out
#------------------------------------------

#------------------------------------------
#parse the data that we've read in
def split_text_data(data):
    count=0
    lines = data.split("\n")
    for l in lines:
        lines[count] = l.split(',')
        #insert type and id
        tai = get_type_and_id(lines[count][0])
        lines[count].insert(0,tai[1])
        lines[count].insert(0,tai[0])
        count+=1
    return lines

#this does the spliting off of digits from a string,and returns the digits and the string in an array
#now we have an array of each object split into
# 0:TYPE, 1:ID, 2,TYPEID, 3:X, 4:Y, 5:WIDTH, 6:HEIGHT
def get_type_and_id(s):
    no_digits = []
    digits = []
    # Iterate through the string, adding non-numbers to the no_digits list
    for i in s:
            if not i.isdigit():
                    no_digits.append(i)
            else:
                    digits.append(i)

    # Now join all elements of the list with '',
    # which puts all of the characters together.
    type = ''.join(no_digits)
    id = ''.join(digits)
    return [type,id]

def remove_file_extension(filename):
    split = filename.split('.')
    name = filename[ : -( len( split[len(split)-1])+1) ]
    ext = ''
    if(len(split)>0):
        #this is erroring out, if there is no extension
        ext = split[1]
    return [name,ext]
#------------------------------------------
#------------------------------------------

#actions
def save_paths_as_images(paths,svg,out_folder,prefix):
    for l in paths: 
        if (l[0]=="path"):
            #export each path into a png file
            cmd = "inkscape "+svg+" --export-id="+l[2]+" --export-id-only --export-png="+out_folder+"/"+prefix+l[2]+".png "
            os.system(cmd)

def save_visible_as_images(paths,svg,out_folder,prefix):
    for l in paths:
        if (l[0]=="path"):
            #export each path into a png file
            #this exports everything that is visible, so the underlying image too
            out = "inkscape "+svg+" --export-id="+l[2]+" --export-png="+out_folder+"/"+prefix+l[2]+".png "
            os.system(out)  

def composite(paths,alpha_pre,image_pre,folder):
    for l in paths:
        if (l[0]=="path"):
            ialpha = Image.open(alpha_pre+l[2]+'.png')
            iart = Image.open(image_pre+l[2]+'.png')
            inew = Image.new('RGBA',iart.size,(0,0,0,0))
            inew = Image.composite(iart,inew,ialpha)
            inew.save(folder+'/'+image_pre+l[2]+'.png')
            print "composited "+image_pre+l[2]+'.png'
#------------------------------------------
#------------------------------------------

def main_BAK(filename,action):
    	#read in the file, each line is its own entry in the array

    	f = open(filename,"r")
    	
        out=""
    	count = 0

        #we can create a text file from the data we need from the svg first
        if(action=="textfile"):
            cmd=['inkscape',filename,'-S']
            nf = open('temp.txt',"w")
            out = subprocess.check_output(cmd)
            nf.write(out)
            nf.close()
            f.close()
            #these lines below just write it straight to file without the need to open write and close it
            #with open("temp.txt","w") as txt:
            #   out = subprocess.call(cmd,stdout=txt)
        else:
            #we are using a text file we have already made
            #use data in text file to get what we want
            lines = [line.strip() for line in f]
            f.close()

            #go ahead and break out the values, so that I can use them better
            #now split the 1st value into type and id eg [path9]1 = [path, 90, path90]
            for l in lines:
                lines[count] = l.split(',')
                count+=1
            count = 0

        '''if(action=="ethanon_position_array"):
            out="private vector2[] positions = {"

        if(action=="ethanon_size_array"):
            out="private vector2[] sizes = {"

        if(action=="ethanon_name_array"):
            out="private string[] names = {"

        for l in lines:
            	tai =  get_type_and_id(l[0])
            	l.insert(0,tai[1])
            	l.insert(0,tai[0])
                #while we are in here we can start outputting crap
                if (l[0]=="path"):
                   
                    if(action=="export"):
                        #export each path into a png file
                        out = "inkscape mapb.svg --export-id="+l[2]+" --export-id-only --export-png=state_exports/"+l[2]+".png "
                        os.system(out)

                    if(action=="export all"):
                        #export each path into a png file
                        #this exports everything that is visible, so the underlying image too
                        out = "inkscape mapb.svg --export-id="+l[2]+" --export-png=state_exports/art_"+l[2]+".png "
                        os.system(out)

                    if(action=="ethanon_loadsprite"):
                        #export text file to preload sprites for anglescript
                        out+="LoadSprite(\"sprites/"+l[2]+".png\");\n"

                    if(action=="ethanon_positionvar"):
                        #export text file to preload sprites for anglescript
                        out+="private vector2 pos_"+l[2]+" = vector2("+l[3]+","+l[4]+");\n"

                    if(action=="ethanon_drawsprite"):
                        out+="DrawSprite(\"sprites/"+l[2]+".png\",pos_"+l[2]+");\n"

                    if(action=="ethanon_position_array"):
                        out+= "vector2("+l[3]+","+l[4]+"),"

                    if(action=="ethanon_size_array"):
                        out+= "vector2("+l[5]+","+l[6]+"),"

                    if(action=="ethanon_name_array"):
                        out+= "\""+l[2]+"\","

        if(action=="ethanon_position_array" or action=="ethanon_size_array" or action=="ethanon_name_array"):
            out+="};"
            '''
        print out

    	#------------------------
    	

#so i need to be giving this a text file to parse to know how to deal with the export
# that text file is made with the command from google docs
# I need to make a smarter script here that makes that text file and extpors
if __name__ == "__main__":
    main(sys.argv[1:])
    #main(sys.argv[1],sys.argv[2],sys.argv[3])
