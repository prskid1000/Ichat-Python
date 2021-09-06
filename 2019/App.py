from tkinter import *
import requests
import urllib.request
import urllib.parse

root = Tk()
username=StringVar()
stranger_del=StringVar()
stranger_add=StringVar()
stranger_data=StringVar()

def main_account_screen():
    root.geometry("600x600")
    root.configure(background='white')
    destroy(root)
    Label(root, text="Username:",font=("Times", 40, "bold italic"),fg='green',bg='white').place(bordermode=OUTSIDE,relx=0.25,rely=0.3)
    Entry(root, textvariable=username,font=("Times", 20, "bold italic"),fg='black',bg='white').place(bordermode=OUTSIDE, relx=0.25,rely=0.4)
    Button(root, text="Login", width=10, height=2, bg='green',font=("Helvetica", 20),command=get_contact).place(bordermode=OUTSIDE,relx=0.45,rely=0.5)

def destroy(parent):
    for child in parent.winfo_children():
        child.destroy()


def get_contact():
    destroy(root)

    Label(root, text="Add Contact:",font=("Times", 30, "bold italic"),fg='green',bg='white').place(bordermode=OUTSIDE,relx=0.25,rely=0.23)
    Entry(root, textvariable=stranger_add,font=("Times", 20, "bold italic"),fg='black',bg='white').place(bordermode=OUTSIDE, relx=0.25,rely=0.30)
    Button(root, text="Add", width=9, height=2, bg='green',font=("Helvetica", 15),command=add_contact).place(bordermode=OUTSIDE,relx=0.40,rely=0.37)

    Label(root, text="Delete Contact:",font=("Times", 30, "bold italic"),fg='green',bg='white').place(bordermode=OUTSIDE,relx=0.25,rely=0.50)
    Entry(root, textvariable=stranger_del,font=("Times", 20, "bold italic"),fg='black',bg='white').place(bordermode=OUTSIDE, relx=0.25,rely=0.57)
    Button(root, text="Delete", width=9, height=2, bg='green',font=("Times", 15, "bold italic"),command=delete_contact).place(bordermode=OUTSIDE,relx=0.40,rely=0.64)

    Button(root,text="Go Back",font=("Times", 20, "bold italic"),width=20,height=3,bg='red',command=lambda:main_account_screen()).place(bordermode=OUTSIDE,relheight=0.1,relwidth=0.5,relx=0,rely=0.9)


    Button(root,text='View Contact',font=("Times", 20, "bold italic"),width=20,height=3,bg='green',command=lambda:view_contact()).place(bordermode=OUTSIDE,relheight=0.1,relwidth=0.5,relx=0.5,rely=0.9)

def view_contact():
     destroy(root)
     URL = 'http://progwithme.dx.am/app/get_contact.php'
     data = {'userid': username.get()}
     x = requests.get(url=URL,params=data)
     arr=[str(i) for i in x.text.split()]

     frame=Frame(root)
     frame.place(relheight=0.9,relwidth=1,rely=0)

     scrollbar = Scrollbar(frame)
     scrollbar.pack( side = RIGHT, fill = Y )
     mylist = Listbox(frame, font=("Times", 30, "bold italic"),activestyle="none",bg='white',fg='green',highlightcolor='white',selectbackground='red',yscrollcommand = scrollbar.set )

     for i in range(0,len(arr)):
         mylist.insert(i, arr[i])

     mylist.place(relheight=1,relwidth=0.98,relx=0,rely=0)

     scrollbar.config( command = mylist.yview )

     Button(root,text="Go Back",font=("Times", 20, "bold italic"),width=20,height=3,bg='red',command=lambda:get_contact()).place(bordermode=OUTSIDE,relheight=0.1,relwidth=0.5,relx=0,rely=0.9)


     Button(root,text="Start Chating",font=("Times", 20, "bold italic"),width=20,height=3,bg='green',command=lambda:open_chat(mylist.get(ACTIVE))).place(bordermode=OUTSIDE,relheight=0.1,relwidth=0.5,relx=0.5,rely=0.9)

def add_contact():
    destroy(root)
    URL = 'http://progwithme.dx.am/app/add_contact.php'
    data = {'userid': username.get(),'receiver':stranger_add.get()}
    x = requests.get(url=URL,params=data)
    person=stranger_add.get()+" is added"
    Label(root, text=person,font=("Times", 30, "bold italic"),fg='green',bg='white').place(bordermode=OUTSIDE,relx=0.25,rely=0.4)

    Button(root,text="Go Back",font=("Times", 20, "bold italic"),width=20,height=3,bg='red',command=lambda:get_contact()).place(bordermode=OUTSIDE,relheight=0.1,relwidth=1,relx=0,rely=0.9)

def delete_contact():
    destroy(root)
    URL = 'http://progwithme.dx.am/app/remove_contact.php'
    data = {'userid': username.get(),'receiver':stranger_add.get()}
    x = requests.get(url=URL,params=data)
    person=stranger_del.get()+" is deleted"
    Label(root, text=person,font=("Times", 30, "bold italic"),fg='green',bg='white').place(bordermode=OUTSIDE,relx=0.25,rely=0.4)

    Button(root,text="Go Back",font=("Times", 20, "bold italic"),width=20,height=3,bg='red',command=lambda:get_contact()).place(bordermode=OUTSIDE,relheight=0.1,relwidth=1,relx=0,rely=0.9)


def send_message(data,person):
    destroy(root)
    URL = 'http://progwithme.dx.am/app/send_message.php'
    data = {'userid': username.get(),'data':data,'receiver':person}
    x = requests.get(url=URL,params=data)
    open_chat(person)

def open_chat(person):
    destroy(root)
    frame=Frame(root)
    frame.configure(bg='white')
    frame.place(relheight=0.9,relwidth=1,rely=0)
    scrollbar = Scrollbar(frame)
    scrollbar.pack( side = RIGHT, fill = Y )

    data = urllib.parse.urlencode({'userid': username.get(),'receiver':person})
    URL = 'http://progwithme.dx.am/app/receive_message.php?%s'%data

    dat=""
    with urllib.request.urlopen(URL) as f:
        data=f.read().decode('utf-8')

    tmp1,tmp2=data.replace('list','').split('&')

    per1=[str(i) for i in tmp1.split()]
    per2=[str(i) for i in tmp2.split()]

    mylist = Listbox(frame, font=("Times", 18, "bold italic"),activestyle="none",bg='white',fg='green',highlightcolor='white',selectbackground='red',yscrollcommand = scrollbar.set )



    for i in range(0,len(per1)):
        mylist.insert(i,username.get().upper()+": "+per1[i].replace('~',' '))

    for i in range(len(per1),len(per2)+len(per1)):
        mylist.insert(i,person.upper()+": "+per2[i-len(per1)].replace('~',' '))

    mylist.place(relheight=1,relwidth=0.98,relx=0,rely=0)
    scrollbar.config( command = mylist.yview )

    Entry(root, textvariable=stranger_data,font=("Times", 20, "bold italic"),fg='black',bg='lightgreen').place(bordermode=OUTSIDE,relwidth=1,relheight=0.1,relx=0,rely=0.8)

    Button(root,text="Go Back",font=("Times", 20, "bold italic"),width=20,height=3,bg='red',command=lambda:view_contact()).place(bordermode=OUTSIDE,relheight=0.1,relwidth=0.25,relx=0,rely=0.9)

    Button(root,text='Send',font=("Times", 20, "bold italic"),width=20,height=3,bg='green',command=lambda:send_message(stranger_data.get(),person)).place(bordermode=OUTSIDE,relheight=0.1,relwidth=0.5,relx=0.25,rely=0.9)

    Button(root,text='Refresh',font=("Times", 20, "bold italic"),width=20,height=3,bg='red',command=lambda:open_chat(person)).place(bordermode=OUTSIDE,relheight=0.1,relwidth=0.25,relx=0.75,rely=0.9)


if __name__ == '__main__':
    main_account_screen()
    root.mainloop()
