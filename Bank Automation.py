from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox 
from tkintertable import TableCanvas,TableModel
import time,random,sqlite3,gmail,project_tables,os,shutil
from PIL import Image,ImageTk

#file=open('gmail_login.txt')
#email,apppass=file.read().split(',')
#file.close()

win=Tk()
win.title('Banking Automation')
win.state('zoomed')
win.resizable(width=False,height=False)
win.configure(bg='navyblue')

title=Label(win,text="Banking Automation",font=("algerian",60,'bold','underline'),bg='navyblue',fg='yellow')
title.pack()

date=time.strftime("%d-%B-%Y")
currdate=Label(win,text=date,font=("algerian",20),bg='navyblue',fg='red')
currdate.pack(pady=10)

img=Image.open("logo.jpg").resize((300,150))
bitmap_img=ImageTk.PhotoImage(img,master=win)

lbl_img=Label(win,image=bitmap_img)
lbl_img.place(relx=0,rely=0.003)

footer=Label(win,text="By Som Dutt Sharma @ +91 9761398726\n Meerut_U.P",font=("algerian",20,'bold','underline'),bg='navyblue',fg='yellow')
footer.pack(side='bottom')

def main_screen():
    frm=Frame(win,highlightbackground='white',highlightthickness=2)
    frm.configure(bg='black')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.7)

    code_cap=""
    for i in range(3):
        i=random.randint(65,90)
        c=chr(i)
        j=random.randint(0,9)
        code_cap=code_cap+str(j)+c

    def forgot_pass():
        frm.destroy()
        forgotpass_screen()

    def login():
        acn_type=cb_type.get()
        acno=e_acn.get()
        pwd=e_pass.get()
        user_cap=e_captcha.get()

        if acno=="" or pwd=="" or user_cap=="":
            messagebox.showerror("login","Empty fields are not allowed")
            return

        if acn_type=="admin" and acno=="0" and pwd=="admin":
            if user_cap==code_cap:
                frm.destroy()
                welcome_admin_screen()
            else:
                messagebox.showerror("login","invalid calptcha")
        elif acn_type=="user":
            if user_cap==code_cap:
                conobj=sqlite3.connect("bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("select * from users where users_acno=? and users_pass=?",(acno,pwd))
                tup=curobj.fetchone()
                if tup==None:
                    messagebox.showerror("Login","Invalid ACNO/Pass")
                    return
                else:
                    global welcome_user,user_acno
                    welcome_user=tup[1]
                    user_acno=tup[0]
                    frm.destroy()
                    welcome_user_screen()
        else:
            messagebox.showerror("login","invalid acn or password")


    lbl_type=Label(frm,text="ACN Type",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_type.place(relx=.3,rely=.15)

    cb_type=Combobox(frm,values=["----select acn type----","user","admin"],font=('algerian',17,'bold'))
    cb_type.current(0)
    cb_type.place(relx=.43,rely=.15)

    lbl_acn=Label(frm,text="ACN No.",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_acn.place(relx=.43,rely=.25)
    e_acn.focus()

    e_pass=Entry(frm,font=("algerian",17,"bold"),bd=5,show="*")
    e_pass.place(relx=.43,rely=.35)

    lbl_pass=Label(frm,text="Password",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_pass.place(relx=.3,rely=.35)

    def refresh():
        frm.destroy()
        main_screen()

    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_captcha.delete(0,"end")
        e_acn.focus(0,"end")


    lbl_captcha=Label(frm,text="Captcha :-",font=('algerian',20,'bold'),bg="black",fg='#FFD700')
    lbl_captcha.place(relx=.35,rely=.45)

    lbl_captcha=Label(frm,text=f"{code_cap}",font=('arial',20,'bold'),bg="black",fg='#FFD700')
    lbl_captcha.place(relx=.5,rely=.45)

    lbl_captcha2=Label(frm,text="Enter\ncaptcha",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_captcha2.place(relx=.3,rely=.55)

    e_captcha=Entry(frm,font=("arial",19,"bold"),bd=5)
    e_captcha.place(relx=.43,rely=.55)

    btn_refresh=Button(frm,text="⟳",font=("algerian",15,'bold'),bd=3,command=refresh,fg="green")
    btn_refresh.place(relx=.595,rely=.45)

    btn_login=Button(frm,text="login",font=("algerian",18,'bold'),bd=5,command=login)
    btn_login.place(relx=.439,rely=.7)

    btn_reset=Button(frm,text="Reset",font=("algerian",18,'bold'),bd=5,command=reset)
    btn_reset.place(relx=.539,rely=.7)

    btn_forgotpass=Button(frm,text="Forgot Password",font=("algerian",18,'bold'),bd=5,command=forgot_pass)
    btn_forgotpass.place(relx=.43,rely=.85,relwidth=.19)

def forgotpass_screen():
    frm=Frame(win,highlightbackground='white',highlightthickness=2)
    frm.configure(bg='black')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.7)

    frm_title=Label(frm,text="Password Recovery screen",font=("algerian",30,'bold','underline'),bg='black',fg='light green')
    frm_title.pack()

    def back():
        frm.destroy()
        main_screen()
    
    def reset():
        e_acn.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_acn.focus(0,"end")

    def forgotpass_db():
        uacno=e_acn.get()
        umob=e_mob.get()
        uemail=e_email.get()

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select users_name, users_pass from users where users_acno=? and users_email=? and users_mob=?",(uacno,uemail,umob))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("Login","Invalid Details")
            return
        else:
            global upass
            uname=tup[0]
            upass=tup[1]
            otp=random.randint(1000,9999)

            try:
                con=gmail.GMail('somduttsharma2592002@gmail.com','ssuc wyza rvnu cinx')
                utext=f'''Hello,{uname},
            OTP to recover password is {otp}

            Thanks
            SDS Bank Corp
            '''
                msg=gmail.Message(to=uemail,subject="OTP for password recovery",text=utext)
                con.send(msg)
                messagebox.showinfo('New User','Mail sent seccessfully')

                lbl_otp=Label(frm,text="Email",font=('algerian',20,'bold'),bg="black",fg='white')
                lbl_otp.place(relx=.3,rely=.7)

                e_otp=Entry(frm,font=("algerian",17,"bold"),bd=5)
                e_otp.place(relx=.43,rely=.7)

                def verify_otp():
                    if otp==int(e_otp.get()):
                        messagebox.showinfo('Forgot Pass',f'Your Pass is \t:\t{upass}')
                    else:
                        messagebox.showerror('Forgot Pass',f'Invalid OTP')

                btn_otp=Button(frm,text="Verify",font=("algerian",18,'bold'),bd=5,command=verify_otp)
                btn_otp.place(relx=.6,rely=.7)
            except:
                messagebox.showerror("Network Problem","Something went wrong with network")


    btn_back=Button(frm,text="Back",font=("algerian",18,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="ACN No.",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_acn.place(relx=.43,rely=.25)
    e_acn.focus()

    lbl_mob=Label(frm,text="Mob",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_mob.place(relx=.3,rely=.35)

    e_mob=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_mob.place(relx=.43,rely=.35)

    lbl_email=Label(frm,text="Email",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_email.place(relx=.3,rely=.45)

    e_email=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_email.place(relx=.43,rely=.45)
    
    btn_submit=Button(frm,text="Submit",font=("algerian",18,'bold'),bd=5,command=forgotpass_db)
    btn_submit.place(relx=.439,rely=.6)

    btn_reset=Button(frm,text="Reset",font=("algerian",18,'bold'),bd=5,command=reset)
    btn_reset.place(relx=.539,rely=.6)

def welcome_admin_screen():
    frm=Frame(win,highlightbackground='white',highlightthickness=2)
    frm.configure(bg='black')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.7)

    frm_title=Label(frm,text="Admin Home screen",font=("algerian",30,'bold','underline'),bg='black',fg='light green')
    frm_title.pack()

    def logout():
        frm.destroy()
        main_screen()

    def newuser():
        frm.destroy()
        newuser_screen()

    def delteuser():
        frm.destroy()
        deleteuser_screen()

    def viewuser():
        frm.destroy()
        viewuser_screen()

    btn_logout=Button(frm,text="Logout",font=("algerian",18,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    btn_newuser=Button(frm,text="Open user acn",font=("algerian",18,'bold'),bd=5,command=newuser,background="green",fg="white" )
    btn_newuser.place(relx=0,rely=.1,relwidth=.2)

    btn_deleteuser=Button(frm,text="Delete user acn",font=("algerian",18,'bold'),bd=5,command=delteuser,background="red",fg="white")
    btn_deleteuser.place(relx=0,rely=.3,relwidth=.2)

    btn_viewuser=Button(frm,text="view user acn",font=("algerian",18,'bold'),bd=5,command=viewuser)
    btn_viewuser.place(relx=0,rely=.5,relwidth=.2)

def newuser_screen():
    frm=Frame(win,highlightbackground='white',highlightthickness=2)
    frm.configure(bg='black')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.7)

    frm_title=Label(frm,text="Open New account",font=("algerian",30,'bold','underline'),bg='black',fg='light green')
    frm_title.pack()

    def logout():
        frm.destroy()
        main_screen()

    def back():
        frm.destroy()
        welcome_admin_screen()

    def newuser_db():
        uname=e_name.get()
        umob=e_mob.get()
        umail=e_email.get()
        uadhar=e_adhar.get()
        ubal=0
        upass=""
        for i in range(3):
            i=random.randint(65,90)
            c=chr(i)
            j=random.randint(0,9)
            upass=upass+str(j)+c

        conobj=sqlite3.connect("Bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into users(users_name,users_pass,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)",(uname,upass,umob,umail,ubal,uadhar,date))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect("Bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute('select max(users_acno) from users')
        uacn=curobj.fetchone()[0]
        conobj.close()

        messagebox.showinfo('New User',f'ACN Created with ACN:{uacn} & PASS:{upass}')
        #app_password="ssuc wyza rvnu cinx"
        try:
            con=gmail.GMail('somduttsharma259202@gmail.com','ssuc wyza rvnu cinx')
            utext=f'''Hello,{uname},
            Your account has been opened successfully with SDS Bank
            Your Account No is {uacn}
            Your Passsword is {upass}

            Kindly change your passsword when you login to app

            Thanks
            SDS Bank Corp
            '''

            
            msg=gmail.Message(to=umail,subject="Account Opened Successfully",text=utext)
            con.send(msg)
            messagebox.showinfo('New User','Mail sent seccessfully')
        except:
            messagebox.showerror("Network Problem","Something went wrong with network")

    btn_logout=Button(frm,text="Logout",font=("algerian",18,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    btn_back=Button(frm,text="Back",font=("algerian",18,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_name=Label(frm,text="Name",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_name.place(relx=.3,rely=.25)

    e_name=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_name.place(relx=.43,rely=.25)
    e_name.focus()

    lbl_mob=Label(frm,text="Mob",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_mob.place(relx=.3,rely=.35)

    e_mob=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_mob.place(relx=.43,rely=.35)

    lbl_email=Label(frm,text="Email",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_email.place(relx=.3,rely=.45)

    e_email=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_email.place(relx=.43,rely=.45)

    lbl_adhar=Label(frm,text="Adhar",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_adhar.place(relx=.3,rely=.55)

    e_adhar=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_adhar.place(relx=.43,rely=.55)
    
    btn_submit=Button(frm,text="Submit",font=("algerian",18,'bold'),bd=5,command=newuser_db)
    btn_submit.place(relx=.439,rely=.7)

    btn_reset=Button(frm,text="Reset",font=("algerian",18,'bold'),bd=5)
    btn_reset.place(relx=.539,rely=.7)


def deleteuser_screen():
    frm=Frame(win,highlightbackground='white',highlightthickness=2)
    frm.configure(bg='black')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.7)

    frm_title=Label(frm,text="Delete user account",font=("algerian",30,'bold','underline'),bg='black',fg='light green')
    frm_title.pack()

    def logout():
        frm.destroy()
        main_screen()

    def back():
        frm.destroy()
        welcome_admin_screen()

    def delete():
        uacn=e_acno.get()
        uadhar=e_adhar.get()
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('delete from users where users_acno=? and users_adhar=?',(uacn,uadhar))
        curobj.execute('delete from txn where txn_acno=?',(uacn,))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Delete User","Account deleted")

    btn_logout=Button(frm,text="Logout",font=("algerian",18,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    btn_back=Button(frm,text="Back",font=("algerian",18,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acno=Label(frm,text="Acno",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_acno.place(relx=.3,rely=.25)

    e_acno=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_acno.place(relx=.43,rely=.25)
    e_acno.focus()

    lbl_adhar=Label(frm,text="Adhar",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_adhar.place(relx=.3,rely=.35)

    e_adhar=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_adhar.place(relx=.43,rely=.35)
    
    btn_submit=Button(frm,text="Submit",font=("algerian",18,'bold'),bd=5,command=delete)
    btn_submit.place(relx=.439,rely=.5)

    btn_reset=Button(frm,text="Reset",font=("algerian",18,'bold'),bd=5)
    btn_reset.place(relx=.539,rely=.5)

def viewuser_screen():
    frm=Frame(win,highlightbackground='white',highlightthickness=2)
    frm.configure(bg='black')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.7)

    frm_title=Label(frm,text="View user account",font=("algerian",30,'bold','underline'),bg='black',fg='light green')
    frm_title.pack()

    def logout():
        frm.destroy()
        main_screen()

    def back():
        frm.destroy()
        welcome_admin_screen()

    def view():
        uacn=e_acno.get()

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acno=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("View","Account does not exist")
            return
        
        lbl_acn=Label(frm,text="ACNo",font=('algerian',20,'bold'),bg='black',fg='silver')
        lbl_acn.place(relx=.1,rely=.25)

        lbl_acn_val=Label(frm,text=tup[0],font=('algerian',17,'bold'),bg='black',fg='#FFD500')
        lbl_acn_val.place(relx=.25,rely=.25)

        lbl_name=Label(frm,text="Name",font=('algerian',20,'bold'),bg='black',fg='silver')
        lbl_name.place(relx=.55,rely=.25)

        lbl_name_val=Label(frm,text=tup[1],font=('algerian',17,'bold'),bg='black',fg='#FFD500')
        lbl_name_val.place(relx=.7,rely=.25)

        lbl_mob=Label(frm,text="Mob",font=('algerian',20,'bold'),bg='black',fg='silver')
        lbl_mob.place(relx=.1,rely=.45)

        lbl_mob_val=Label(frm,text=tup[3],font=('algerian',17,'bold'),bg='black',fg='#FFD500')
        lbl_mob_val.place(relx=.25,rely=.45)

        lbl_adhar=Label(frm,text="Adhar",font=('algerian',20,'bold'),bg='black',fg='silver')
        lbl_adhar.place(relx=.55,rely=.45)

        lbl_adhar_val=Label(frm,text=tup[6],font=('algerian',17,'bold'),bg='black',fg='#FFD500')
        lbl_adhar_val.place(relx=.7,rely=.45)

        lbl_opendate=Label(frm,text="Open date",font=('algerian',20,'bold'),bg='black',fg='silver')
        lbl_opendate.place(relx=.1,rely=.65)

        lbl_opendate_val=Label(frm,text=tup[7],font=('algerian',17,'bold'),bg='black',fg='#FFD500')
        lbl_opendate_val.place(relx=.25,rely=.65)

        lbl_bal=Label(frm,text="Bal",font=('algerian',20,'bold'),bg='black',fg='silver')
        lbl_bal.place(relx=.55,rely=.65)

        lbl_bal_val=Label(frm,text=tup[5],font=('algerian',17,'bold'),bg='black',fg='#FFD500')
        lbl_bal_val.place(relx=.7,rely=.65)



    btn_logout=Button(frm,text="Logout",font=("algerian",18,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    btn_back=Button(frm,text="Back",font=("algerian",18,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acno=Label(frm,text="Acno",font=('algerian',20,'bold'),bg="black",fg='white')
    lbl_acno.place(relx=.33,rely=.15)

    e_acno=Entry(frm,font=("algerian",17,"bold"),bd=5)
    e_acno.place(relx=.4,rely=.15)

    btn_search=Button(frm,text="Search",font=("algerian",18,'bold'),bd=5,command=view)
    btn_search.place(relx=.65,rely=.15)

def welcome_user_screen():
    frm=Frame(win,highlightbackground='white',highlightthickness=2)
    frm.configure(bg='black')
    frm.place(relx=0,rely=.19,relwidth=1,relheight=.7)
    screen_title="User Home screen"

    frm_title=Label(frm,text=screen_title,font=("algerian",30,'bold','underline'),bg='black',fg='light green')
    frm_title.place(relx=.45,rely=.035)

    lbl_wel=Label(frm,text=f"Welcome, {welcome_user}",font=("algerian",20,'bold'),bg='black',fg='pink')
    lbl_wel.place(relx=0,rely=0)

    def logout():
        frm.destroy()
        main_screen()
    
    def deposit_screen():
        screen_title="User Deposit Screen"
        frm_title.configure(text=screen_title)
        
        def deposit():
            uamt=int(e_amt.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update users set users_bal=users_bal+? where users_acno=?",(uamt,user_acno))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_bal from users where users_acno=?",(user_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Cr',uamt,ubal,date))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit",f"{uamt} deposited,updated Bal:{ubal}")

        ifrm=Frame(frm,highlightbackground='white',highlightthickness=2)
        ifrm.configure(bg='black')
        ifrm.place(relx=.25,rely=.12,relwidth=.7,relheight=.8)

        lbl_amt=Label(ifrm,text="Amount",font=('algerian',20,'bold'),bg="black",fg='white')
        lbl_amt.place(relx=.25,rely=.25)

        e_amt=Entry(ifrm,font=("algerian",17,"bold"),bd=5)
        e_amt.place(relx=.45,rely=.25)
        e_amt.focus()

        btn_submit=Button(frm,text="Submit",font=("algerian",18,'bold'),bd=5,command=deposit)
        btn_submit.place(relx=.65,rely=.5)
    
    def withdraw_screen():
        screen_title="User Withdraw Screen"
        frm_title.configure(text=screen_title)
        ifrm=Frame(frm,highlightbackground='white',highlightthickness=2)
        ifrm.configure(bg='black')
        ifrm.place(relx=.25,rely=.12,relwidth=.7,relheight=.8)

        def withdraw():
            uamt=int(e_amt.get())

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_bal from users where users_acno=?",(user_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()
            if ubal>uamt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update users set users_bal=users_bal-? where users_acno=?",(uamt,user_acno))
                conobj.commit()
                conobj.close()


                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Dr',uamt,ubal-uamt,date))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdraw",f"{uamt} withdrawn,Updated Bal:{ubal-uamt}")
            else:
                messagebox.showerror("withdraw",f"Insufficient Bal:{ubal}")
  

        lbl_amt=Label(ifrm,text="Amount",font=('algerian',20,'bold'),bg="black",fg='white')
        lbl_amt.place(relx=.25,rely=.25)

        e_amt=Entry(ifrm,font=("algerian",17,"bold"),bd=5)
        e_amt.place(relx=.45,rely=.25)
        e_amt.focus()

        btn_submit=Button(frm,text="Submit",font=("algerian",18,'bold'),bd=5,command=withdraw)
        btn_submit.place(relx=.65,rely=.5)

    def transfer_screen():
        screen_title="User Transfer Screen"
        frm_title.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='black')
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.7)

        def transfer():
            uamt=int(e_amt.get())
            utoacn=int(e_to.get())

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select * from users where users_acno=?',(utoacn,))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Transfer","Invalid To ACN")
            else:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
                ubal=curobj.fetchone()[0]
                conobj.close()
                if ubal>uamt:
                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,user_acno))
                    curobj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,utoacn))
                    conobj.commit()
                    conobj.close()

                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Dr',uamt,ubal-uamt,date))
                    curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(utoacn,'Cr',uamt,ubal+uamt,date))
                    
                    conobj.commit()
                    conobj.close()

                    messagebox.showinfo("Transfer",f"{uamt} transferd,Updated Bal:{ubal-uamt}")
                else:
                    messagebox.showerror("Transfer",f"Insufficient Bal:{ubal}")

        lbl_to=Label(ifrm,text="To Acno",font=('algerian',20,'bold'),bg='black',foreground='white')
        lbl_to.place(relx=.25,rely=.25)

        e_to=Entry(ifrm,font=('algerian',20,'bold'),bd=5)
        e_to.place(relx=.4,rely=.25)
        e_to.focus()

        lbl_amt=Label(ifrm,text="Amt",font=('algerian',20,'bold'),bg='black',foreground='white')
        lbl_amt.place(relx=.25,rely=.45)

        e_amt=Entry(ifrm,font=('algerian',20,'bold'),bd=5,fg='black')
        e_amt.place(relx=.4,rely=.45)

        btn_submit=Button(ifrm,text="submit",font=('algerian',20,'bold'),bd=5,command=transfer)
        btn_submit.place(relx=.4,rely=.7)
      
    def update_screen():
        screen_title="User Update Screen"
        frm_title.configure(text=screen_title)

        def update_db():
            upass=e_pass.get()
            umob=e_mob.get()
            uemail=e_email.get()
            conobj=sqlite3.connect("Bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute('update users set users_pass=?,users_mob=?,users_email=?',(upass,umob,uemail))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Details","Updated")

        ifrm=Frame(frm,highlightbackground='white',highlightthickness=2)
        ifrm.configure(bg='black')
        ifrm.place(relx=.25,rely=.12,relwidth=.7,relheight=.8)

        lbl_pass=Label(ifrm,text="Pass",font=('algerian',20,'bold'),bg="black",fg='white')
        lbl_pass.place(relx=.25,rely=.15)

        e_pass=Entry(ifrm,font=("algerian",17,"bold"),bd=5)
        e_pass.place(relx=.4,rely=.15)
        e_pass.focus()

        lbl_mob=Label(ifrm,text="Mob",font=('algerian',20,'bold'),bg="black",fg='white')
        lbl_mob.place(relx=.25,rely=.3)

        e_mob=Entry(ifrm,font=("algerian",17,"bold"),bd=5)
        e_mob.place(relx=.4,rely=.3)

        lbl_email=Label(ifrm,text="Email",font=('algerian',20,'bold'),bg="black",fg='white')
        lbl_email.place(relx=.25,rely=.45)

        e_email=Entry(ifrm,font=("algerian",17,"bold"),bd=5)
        e_email.place(relx=.4,rely=.45)

        btn_submit=Button(frm,text="Submit",font=("algerian",18,'bold'),bd=5,command=update_db)
        btn_submit.place(relx=.6,rely=.6)

        conobj=sqlite3.connect("Bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select users_pass,users_mob,users_email from users where users_acno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        e_pass.insert(0,tup[0])
        e_mob.insert(0,tup[1])
        e_email.insert(0,tup[2])

    def history_screen():
        screen_title="User Txn History Screen"
        frm_title.configure(text=screen_title)
        ifrm=Frame(frm,highlightbackground='white',highlightthickness=2)
        ifrm.configure(bg='black')
        ifrm.place(relx=.25,rely=.12,relwidth=.7,relheight=.8)

        data={}
        conobj=sqlite3.connect("Bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from txn where txn_acno=?",(user_acno,))
        tups=curobj.fetchall()
        i=1
        for tup in tups:
            data[str(i)]={"Txn Amt":tup[3],"Txn Type":tup[2],"Updated Bal":tup[4],"Txn Date":tup[5],"Txn Id":tup[0]}
            i+=1
        model = TableModel()
        model.importDict(data)

        table_frm=Frame(ifrm)
        table_frm.place(relx=.2,rely=.2)

        table = TableCanvas(table_frm, model=model,editable=False)
        table.show()
         
   

    def details_screen():
        screen_title="User Details Screen"
        frm_title.configure(text=screen_title)
        
        ifrm=Frame(frm,highlightbackground='white',highlightthickness=2)
        ifrm.configure(bg='black')
        ifrm.place(relx=.25,rely=.12,relwidth=.7,relheight=.8)

        conobj=sqlite3.connect("Bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        lbl_acno=Label(ifrm,text=f"Acno",font=("algerian",20,'bold'),bg='black',fg="#FFD700")
        lbl_acno.place(relx=.05,rely=.15)

        lbl_acno_val=Label(ifrm,text=tup[0],font=("algerian",17,'bold'),bg='black',fg="silver")
        lbl_acno_val.place(relx=.2,rely=.15)

        lbl_name=Label(ifrm,text=f"Name",font=("algerian",20,'bold'),bg='black',fg="#FFD700")
        lbl_name.place(relx=.65,rely=.15)

        lbl_name_val=Label(ifrm,text=tup[1],font=("algerian",17,'bold'),bg='black',fg="silver")
        lbl_name_val.place(relx=.8,rely=.15)

        lbl_mob=Label(ifrm,text=f"Mob",font=("algerian",20,'bold'),bg='black',fg="#FFD700")
        lbl_mob.place(relx=.05,rely=.35)
        
        lbl_mob_val=Label(ifrm,text=tup[3],font=("algerian",17,'bold'),bg='black',fg="silver")
        lbl_mob_val.place(relx=.2,rely=.35)

        lbl_adhar=Label(ifrm,text=f"Adhar",font=("algerian",20,'bold'),bg='black',fg="#FFD700")
        lbl_adhar.place(relx=.65,rely=.35)

        lbl_adhar_val=Label(ifrm,text=tup[6],font=("algerian",17,'bold'),bg='black',fg="silver")
        lbl_adhar_val.place(relx=.8,rely=.35)

        lbl_opendate=Label(ifrm,text=f"Open Date",font=("algerian",20,'bold'),bg='black',fg="#FFD700")
        lbl_opendate.place(relx=.05,rely=.55)

        lbl_opendate_val=Label(ifrm,text=tup[7],font=("algerian",17,'bold'),bg='black',fg="silver")
        lbl_opendate_val.place(relx=.2,rely=.55)

        lbl_bal=Label(ifrm,text=f"Bal",font=("algerian",20,'bold'),bg='black',fg="#FFD700")
        lbl_bal.place(relx=.65,rely=.55)

        lbl_bal_val=Label(ifrm,text=tup[5],font=("algerian",17,'bold'),bg='black',fg="silver")
        lbl_bal_val.place(relx=.8,rely=.55)

    def update_photo():
        img_path=filedialog.askopenfilename()
        shutil.copy(img_path,f'{user_acno}.png')

        pro_img=Image.open(f"{user_acno}.png").resize((310,150))
        pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

        prolbl_img=Label(frm,image=pro_bitmap_img)
        prolbl_img.image=pro_bitmap_img
        prolbl_img.place(relx=0,rely=.05)

    btn_logout=Button(frm,text="Logout",font=("algerian",18,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    if os.path.exists(f'{user_acno}.png'):
        pro_img=Image.open(f'{user_acno}.png').resize((310,150))
    else:
        pro_img=Image.open("default.jpg").resize((310,150))
    pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

    prolbl_img=Label(frm,image=pro_bitmap_img)
    prolbl_img.image=pro_bitmap_img
    prolbl_img.place(relx=0,rely=.05)

    btn_update_pro=Button(frm,text="Update photo",command=update_photo,font=("algerian",18,'bold'),bd=5 )
    btn_update_pro.place(relx=0.032,rely=.32,relheight=.05)

    btn_details=Button(frm,text="Check details",command=details_screen,font=("algerian",18,'bold'),bd=5,background="yellow",fg="red" )
    btn_details.place(relx=0,rely=.4,relwidth=.2)

    btn_deposit=Button(frm,text="Deposit",command=deposit_screen,font=("algerian",18,'bold'),bd=5,background="green",fg="white")
    btn_deposit.place(relx=0,rely=.5,relwidth=.2)

    btn_withdraw=Button(frm,text="Withdraw",command=withdraw_screen,font=("algerian",18,'bold'),bd=5,bg="red",fg="white")
    btn_withdraw.place(relx=0,rely=.6,relwidth=.2)

    btn_update=Button(frm,text="Update",command=update_screen,font=("algerian",18,'bold'),bd=5)
    btn_update.place(relx=0,rely=.7,relwidth=.2)

    btn_transfer=Button(frm,text="Transfer",command=transfer_screen,font=("algerian",18,'bold'),bd=5,bg="magenta",fg="white")
    btn_transfer.place(relx=0,rely=.8,relwidth=.2)

    btn_history=Button(frm,text="Txn History",command=history_screen,font=("algerian",18,'bold'),bd=5,bg="light green",fg="white")
    btn_history.place(relx=0,rely=.9,relwidth=.2)

main_screen()
win.mainloop()
