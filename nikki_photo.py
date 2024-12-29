import os,json

if os.path.exists('nikki_setting.ini') == False:
    ## Read Registry
    import winreg
    import locale
    #print (locale.getdefaultlocale())
    check_language = locale.getdefaultlocale()[0]
    if 'zh_TW' in check_language :
        language = 'zh_TW'
    elif 'zh_HK' in check_language :
        language = 'zh_TW'
    elif 'ja_JP' in check_language :
        language = 'ja_JP'        
    elif 'zh_CN' in check_language :
        language = 'zh_CN'        
    else:
        language = 'en_US'
        

    ## Get Nikki install path

    key_path = 'Software\InfinityNikkiGlobal Launcher'
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        install_path = winreg.EnumValue(key, 0)[1].replace(' Launcher', '').replace('\\','\\\\')
        f = open('nikki_setting.ini', 'w')
        f.write('{"check_language":"'+language+'" , "install_path" : "'+str(install_path)+'", "backup_path" : ""}')
        f.close()
    except:
        print ('Cannot detect Infinity Nikki')

if os.path.exists('nikki_setting.ini') == True:
    f = open('nikki_setting.ini', 'r')    
    rd = json.loads(f.read())
    f.close()
    install_path = rd['install_path']
    check_language = rd['check_language']
    backup_path = rd['backup_path'].replace('\\\\', '\\')

    text_a = ["Infinity Nikki Photo Organizer", "Backup Directory: ","Total High Quality Photo Size: ",'Setting',
              "Setting Window",'Close', 'Update', 'Language:', 'Backup Path:',
              "Finish", "Please restart the program.", "Error", "Please input correct path.",
              "Select Photo Move To Backup Folder", "Delete Selected Photo", "Please setup backup directory."]
    text_b = ["インフィニットニキ写真整理", "バックアップ先フォルダ: ","高画質写真フォルダ: ",'設定',
              "プログラムの設定",'閉める', '更新', '　言語', '　バックアップ先\nフォルダ:',
              "設定完成", "プログラムを再起動してください.", "エラー発生", "正しいフォルダ名を入力してください.",
              "選択した写真をバックアップフォルダに移動する", "選択した写真を削除する",
              "バックアップ先フォルダを設定してください"]
    text_c = ["無限暖暖相片整理", "備份路徑: ","高品質照片使用空間: ",'設定',
              "軟件設定",'關閉', '更新', '　　語言', '　　備份路徑:',"完成", "請重啟軟件.",
              "發生錯誤", "請輸入正確路徑.", "選擇照片移到備份文件夾", "刪除選擇照片", "請設定備份路徑"]
    text_d = ["无限暖暖相片整理", "备份路径: ","高品质照片使用空间: ",'设定',"软件设定",'关闭', '更新',
              '语言', '备份路径:',"完成", "请重启软件.", "发生错误",
              "请输入正确路径.", "选择照片移到备份文件夹", "删除选择照片", "请设定备份路径"]

    if 'zh_TW' in check_language :
        using_text = text_c
    elif 'zh_HK' in check_language :
        using_text = text_c
    elif 'ja_JP' in check_language :
        using_text = text_b       
    elif 'zh_CN' in check_language :
        using_text = text_d       
    else:
        using_text = text_a
    
    
    ## Get GamePlayPhoto Directory

    #'X6Game\Saved\GamePlayPhotos'
    subdir_temp = os.listdir((os.path.join(install_path, 'X6Game\Saved\GamePlayPhotos')))
    if len(subdir_temp) == 1:
        hq_dir = os.path.join(os.path.join(install_path, 'X6Game\Saved\GamePlayPhotos', subdir_temp[0], 'NikkiPhotos_HighQuality'))
        #print (hq_dir)    
                              
    ## Get Game Backup Photo Directory
    backup_dir = os.path.join(install_path,'X6Game\ScreenShot')
    #print (backup_dir)
                            
    ## Get content from NikkiPhotos_HighQuality
    hq_total_size = 0
    hq_list = os.listdir(hq_dir)
    for f in hq_list:
        fp = os.path.join(install_path,'X6Game\ScreenShot', f)
        hq_total_size += os.path.getsize(fp)/1048576
        
    #print (int(hq_total_size))

    ## Get content from Backup Photo
    backup_total_size = 0
    backup_list = os.listdir(backup_dir)

    #print (hq_list)
    #print (backup_list)

    ## Compare 2 Folder

    ## Choose
    ## 1. Items not in hq folder move to another backup folder?
    ## 2. Delete all items where not in hq folder
    ## 3. Preview each photo and let user to choose delete, move option

    compared_list = []
    for item in backup_list:
        if item in hq_list:
            #print (item)
            compared_list.append(item)

    #print (compared_list)

    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk
    from send2trash import send2trash
    from PIL import Image, ImageTk
    import shutil,sys
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


    def mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def change():
        #print (language_choose)
        if sbox.get() == 'English':
            rd['check_language'] = 'en_US'
        elif sbox.get() == '日本語':
            rd['check_language'] = 'ja_JP'
        elif sbox.get() == '中文(繁體)':
            rd['check_language'] = 'zh_TW'
        elif sbox.get() == '中文(简体)':
            rd['check_language'] = 'zh_CN'

        temp = stext1.get("1.0","end-1c")                
        if ':\\' in temp:
            if temp[-1] == '\\': temp = temp[:-1]
            rd['backup_path'] = temp
            with open('nikki_setting.ini', "w") as outfile:
                json.dump(rd, outfile)
            print (rd)
            messagebox.showinfo( using_text[9], using_text[10])            
        else:
            messagebox.showinfo( using_text[11], using_text[12])

    def close_setting_window():
        new.destroy()        
        
    def Setting():

        global sbox
        global stext1
        global new
        
        new = tk.Toplevel(window)
        new.geometry("450x250")
        new.resizable(False, False) 
        new.title(using_text[4])
        new.grid_rowconfigure(0, weight=1)
        new.columnconfigure(0, weight=1)

        language_choose = tk.StringVar()
        
        
        frame_setting = tk.Frame(new, bg="white")
        frame_setting.grid(sticky='news')

        # Create a frame for the canvas with non-zero row&column weights
        frame_setting_canvas = tk.Frame(frame_setting, bg="white")
        frame_setting_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')
        frame_setting_canvas.grid_rowconfigure(0, weight=1)
        frame_setting_canvas.grid_columnconfigure(0, weight=1)
        
        # Set grid_propagate to False to allow 4-by-4 buttons resizing later
        frame_setting_canvas.grid_propagate(False)

        slabel1 = tk.Label(frame_setting_canvas, text=using_text[7], font=("Arial", 12), fg="black", bg="white")#,anchor='n')
        slabel1.grid(row=0, column=0, pady=(5, 5), sticky='nw')

        sbox = ttk.Combobox(frame_setting_canvas, values=['English','日本語','中文(繁體)','中文(简体)'])
        sbox.current(0)
        sbox.grid(row=0, column=1,padx=50, pady =6 , sticky='nw')
        
        slabel2 = tk.Label(frame_setting_canvas, text=using_text[8], font=("Arial", 12), fg="black", bg="white")#,anchor='n')
        slabel2.grid(row=1, column=0, pady=(5, 5), sticky='nw')

        stext1 = tk.Text(frame_setting_canvas, height=6, width=32, font=("Arial", 12))#, height=60)
        stext1.grid(row=1, column=1, padx=1)
        stext1.insert("1.0", backup_path)

        frame_setting_canvas2 = tk.Frame(frame_setting, bg="white")
        frame_setting_canvas2.grid(row=1, column=0, pady=(5, 0), sticky='nw')
        frame_setting_canvas2.grid_rowconfigure(0, weight=1)
        frame_setting_canvas2.grid_columnconfigure(0, weight=1)
        
        # Set grid_propagate to False to allow 4-by-4 buttons resizing later
        frame_setting_canvas2.grid_propagate(False)        

        sbutton1 = tk.Button(frame_setting_canvas2, text=(using_text[6]), width = 10, command=change)
        sbutton1.grid(row=2, column=0,padx=0)

        sbutton2 = tk.Button(frame_setting_canvas2, text=(using_text[5]), width = 10, command=close_setting_window)
        sbutton2.grid(row=2, column=1,padx=60)

        frame_setting_canvas.config(width=445,height=190)#,padx=20)
        frame_setting_canvas2.config(width=445,height=40)#,padx=100)
        
        """
        tk.Label(new, text="new one").place(x=150, y=40)
        """
        window.wait_visibility(new)

    def showHQ():

        global compared_list
        global canvas
        # Create a frame to contain the buttons
        frame_buttons = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
        
        number = []

        i = 0
        j = 0
        while i <= (len(compared_list))-1:

            dirImg = os.path.join(backup_dir, compared_list[i])
            loading = Image.open(dirImg)
            loading.thumbnail((300,169))
            renderiza = ImageTk.PhotoImage(loading)
            number.append(tk.IntVar())
            
            imagemA = tk.Label(frame_buttons,image=renderiza)
            imagemA.image = renderiza
            imagemA.grid(column=i%4, row=i//4+j, sticky='news')
            temp_button = tk.Checkbutton(frame_buttons,text=compared_list[i], variable=number[i])#command=SelectPhoto)
            temp_button.grid(column=i%4, row=i//4+1+j, sticky='news')
            if i%4 == 3:
                j = j + 2
            i = i + 1


        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_buttons.update_idletasks()

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))

        return (frame_buttons, number)

    def Delete():
        
        if backup_path == '':
            messagebox.showinfo( using_text[11], using_text[15])            
        else:  
            global hq_total_size
            global compared_list
            #msg=messagebox.showinfo( "Hello Python", "Hello World")
            #print (number.get())
            remove_list = []
            for num in range(len(number)):
                #print (number[num].get())
                if number[num].get() == 1:
                    print (compared_list[num])
                    #print (hq_total_size)
                    
                    fp = os.path.join(hq_dir, compared_list[num])
                    hq_total_size -= os.path.getsize(fp)/1048576                
                    remove_list.append(compared_list[num])
                    #shutil.move(fp, os.path.join(backup_path, compared_list[num]))
                    send2trash(fp)
                    send2trash(os.path.join(backup_dir, compared_list[num]))

            for cc in remove_list:
                if cc in compared_list:                
                    compared_list.remove(cc)

            label1.configure(text=using_text[2]+str(int(hq_total_size))+'M')    
            frame_buttons.destroy()
            showHQ()
        
    def SelectPhoto():

        if backup_path == '':
            messagebox.showinfo( using_text[11], using_text[15])            
        else:            
            global hq_total_size
            global compared_list
            #msg=messagebox.showinfo( "Hello Python", "Hello World")
            #print (number.get())
            remove_list = []
            for num in range(len(number)):
                #print (number[num].get())
                if number[num].get() == 1:
                    print (compared_list[num])
                    #print (hq_total_size)
                    
                    fp = os.path.join(hq_dir, compared_list[num])
                    hq_total_size -= os.path.getsize(fp)/1048576                
                    remove_list.append(compared_list[num])
                    shutil.move(fp, os.path.join(backup_path, compared_list[num]))
                    send2trash(os.path.join(backup_dir, compared_list[num]))

            for cc in remove_list:
                if cc in compared_list:                
                    compared_list.remove(cc)

            label1.configure(text=using_text[2]+str(int(hq_total_size))+'M')    
            frame_buttons.destroy()
            showHQ()
        

    # Build up Window
    window = tk.Tk()
    window.title(using_text[0])
    window.geometry('1260x900')
    window.resizable(False, False)
    try:
        window.iconbitmap('photo.ico')
    except:
        window.iconbitmap(os.path.join(bundle_dir, 'photo.ico'))

    window.grid_rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    frame_main = tk.Frame(window, bg="white")
    frame_main.grid(sticky='news')

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame_main)
    frame_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 4-by-4 buttons resizing later
    frame_canvas.grid_propagate(False)

    
    
    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas, bg="white")
    canvas.grid(row=0, column=0, sticky="news")
    window.bind_all("<MouseWheel>", mouse_wheel)

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=2, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    frame_buttons, number = showHQ()

    # Resize the canvas frame to show exactly 4-by-4 buttons and the scrollbar
    first5columns_width = 1255
    first5rows_height = 770
    frame_canvas.config(width=first5columns_width,height=first5rows_height)
    
    
    ########################

    frame_canvas2 = tk.Frame(frame_main, bg="white")
    frame_canvas2.grid(row=1, column=0, pady=(5, 0), sticky='nw')
    frame_canvas2.grid_rowconfigure(0, weight=1)
    frame_canvas2.grid_columnconfigure(0, weight=1)
    frame_canvas2.grid_propagate(False)
    
    label1 = tk.Label(frame_canvas2, text=using_text[2]+str(int(hq_total_size))+'M', font=("Arial", 16), fg="black", bg="white")
    label1.grid(row=0, column=0, pady=(2, 0), sticky='nw')

    move_buttons = tk.Button(frame_canvas2, text=(using_text[13]), font=("Arial", 12), command =SelectPhoto)
    move_buttons.grid(row=0, column=1, pady=(2, 0), sticky='nw')

    frame_canvas2.config(width=1255,height=30)

    ########################

    frame_canvas3 = tk.Frame(frame_main, bg="white")
    frame_canvas3.grid(row=2, column=0, pady=(5, 0), sticky='nw')
    frame_canvas3.grid_rowconfigure(0, weight=1)
    frame_canvas3.grid_columnconfigure(0, weight=1)
    frame_canvas3.grid_propagate(False)
    
    label2 = tk.Label(frame_canvas3, text=using_text[1]+backup_path , font=("Arial", 16), fg="black", bg="white")
    label2.grid(row=0, column=0, pady=(2, 0), sticky='nw')

    delete_buttons = tk.Button(frame_canvas3, text=(using_text[14]), font=("Arial", 12), command =Delete)
    delete_buttons.grid(row=0, column=1, pady=(2, 0), sticky='nw')

    frame_canvas3.config(width=1255,height=40)
    
    #########################

    frame_canvas4 = tk.Frame(frame_main, bg="white")
    frame_canvas4.grid(row=3, column=0, pady=(2, 0), sticky='nw')
    frame_canvas4.grid_rowconfigure(0, weight=1)
    frame_canvas4.grid_columnconfigure(0, weight=1)
    frame_canvas4.grid_propagate(False)   

    setting_buttons = tk.Button(frame_canvas4, text=(using_text[3]), font=("Arial", 12), command =Setting)
    setting_buttons.grid(row=0, column=1, pady=(0, 0), sticky='nw')

    frame_canvas4.config(width=1255,height=40)    
    
    window.mainloop()
