from tkinter import ttk
from tkinter import PhotoImage
import mysql.connector as s
from tkinter import *
from random import *
from datetime import *
import csv
mycon=s.connect(host='localhost',user='root', password='mysql', database='housekeepers')
cur=mycon.cursor()

def create_main_screen():
    global main_window,table
    main_window = Tk()
    main_window.title("ThunderBird")
    main_window.geometry("500x500")

    app_logo = PhotoImage(file=r"C:\Sreedivya\Sreedivya_12th\CS\12th Project\ThunderBird Logo.png")  
    logo_label = Label(main_window, text="THUNDERBIRD",font=("Lucida Bright",16),image=app_logo)
    logo_label.image = app_logo
    logo_label.pack(pady=20)

    table='users'

    signup_button = Button(main_window, text="Signup", width=20, command=lambda:create_signup_screen(table),font=('Garamond',14,'bold'),
                               activebackground='white',activeforeground='#228B22',fg='white',bg='#000080')
    signup_button.pack(pady=10)

    login_button = Button(main_window, text="Login", width=20, command=lambda:create_login_screen(table),font=('Garamond',14,'bold'),
                              activebackground='white',activeforeground='#228B22',fg='white',bg='#000080')
    login_button.pack(pady=10)

    global selection
    selection = StringVar(main_window, "User")


    # Create radio buttons with customized font
    user_radio = Radiobutton(main_window, text="User", variable=selection, value="User", command=choice_selected, font=("Lucida Bright", 14, "bold"))
    provider_radio = Radiobutton(main_window, text="Service Provider", variable=selection, value="Service Provider", command=choice_selected, font=("Lucida Bright", 14, "bold"))

    # Pack the radio buttons
    user_radio.pack(pady=10)
    provider_radio.pack(pady=10)
    main_window.mainloop()

def choice_selected():
    global table,selection
    selected_table=selection.get()
    if selected_table=='User':
        table='users'
    elif selected_table=='Service Provider':
        table='service_provider'
    print(selected_table,table)
    
def create_signup_screen(table):
    main_window.withdraw()

    signup_window = Toplevel()
    signup_window.title("Signup")
    signup_window.geometry("400x400")
    signup_window.configure(bg="black")

    Label(signup_window, text="Signup Form", font=("Lucida Bright", 20), pady=20, bg="black", fg="white").pack()

    Label(signup_window, text="Gmail", font=("Lucida Bright", 12), bg="black", fg="white").pack()
    gmail_entry = Entry(signup_window)
    gmail_entry.pack(pady=5)

    Label(signup_window, text="UserID", font=("Lucida Bright", 12), bg="black", fg="white").pack()
    userid_entry = Entry(signup_window)
    userid_entry.pack(pady=5)

    Label(signup_window, text="Password", font=("Lucida Bright", 12), bg="black", fg="white").pack()
    password_entry = Entry(signup_window, show="*")
    password_entry.pack(pady=5)

    Label(signup_window, text="Confirm Password", font=("Lucida Bright", 12), bg="black", fg="white").pack()
    confirm_password_entry = Entry(signup_window, show="*")
    confirm_password_entry.pack(pady=5)

    def confirm_signup():
        gmail = gmail_entry.get()  # Get user input when button is clicked
        user_id = userid_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()


        if password == confirm_password:
            if table=='users':
                query1="select user_id from users;"
                cur.execute(query1)
                unavailable_ids=cur.fetchall()
                un_ids=[i[0] for i in unavailable_ids]
                print(un_ids)
                if user_id in un_ids:
                    Label(signup_window, text="Unavailable ID. Try another.", font=("Lucida Bright", 12), bg="black", fg="red").pack()
                else: 
                    query='insert into users (gmail,user_id,password) values (%s,%s,%s);'
                    values=(gmail,user_id,password)   
                    cur.execute(query,values)
                    mycon.commit()
                    signup_window.destroy()
                    create_login_screen(table)
                
                
            else:
                query1="select provider_id from service_provider;"
                cur.execute(query1)
                unavailable_ids=cur.fetchall()
                un_ids=[i[0] for i in unavailable_ids]
                if user_id in un_ids:
                    Label(signup_window, text="Unavailable ID. Try another.", font=("Lucida Bright", 12), bg="black", fg="red").pack()
                else: 
            
                    query='insert into service_provider (gmail,provider_id,password) values (%s,%s,%s);'
                    values=(gmail,user_id,password)   
                    cur.execute(query,values)
                    mycon.commit()
                    signup_window.destroy()
                    create_login_screen(table)
        else:
            Label(signup_window, text="Passwords do not match!", font=("Lucida Bright", 12), bg="black", fg="red").pack()

    confirm_button = Button(
        signup_window,
        text="Confirm",
        width=20,
        command=confirm_signup, 
        activebackground='white',
        activeforeground='#000080',
        bg='purple',
        fg='white',)
    confirm_button.pack(pady=20)

def user_homescreen(user_id):
    global mycon,cur,custom_font,search_screen,open_screens,new_request_canvas
    open_screens=[]
    search_screen=Tk()
    search_screen.configure(background='white')
    search_screen.title("Home Screen")
    search_screen.geometry("1500x700")
    open_screens.append(search_screen)
    
    custom_font="Lucida Bright"
    if mycon.is_connected():
        print("connected")
    #create request frame
    new_request_canvas=Frame(search_screen,width=800,height=700,bg='white')
    pending_request_frame=Frame(search_screen,width=400,height=700,bg='white')
    
    
    #pending request frame
    pending_request_canvas = Canvas(pending_request_frame, width=400, height=700)

    vertical_scrollbar = Scrollbar(
        pending_request_frame, orient='vertical', command=pending_request_canvas.yview)
    horizontal_scrollbar = Scrollbar(
        pending_request_frame, orient='horizontal', command=pending_request_canvas.xview)

    scrollable_frame = Frame(pending_request_canvas, width=400)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: pending_request_canvas.configure(
            scrollregion=pending_request_canvas.bbox("all")))

    canvas_frame = pending_request_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")


    pending_request_canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    vertical_scrollbar.pack(side="right", fill="y")
    horizontal_scrollbar.pack(side="bottom", fill="x")
    pending_request_canvas.pack(side="left", fill="both", expand=True)

    
    pending_request_canvas.pack(side='left',fill='both',expand=True)
    pending_request_frame.pack(side='left',fill='both',expand=True)
    new_request_canvas.pack(side='left',fill='both',expand=True)

    pending_request_label=Label(scrollable_frame,text="YOUR REQUESTS",bg='#000080',fg='white',font=('Lucida Bright',16,'bold'),height=3,justify='center',width=20)
    pending_request_label.pack(pady=10,fill='x',expand=True)
    pending_query='select * from bookings where user_id=%s order by status desc,start_time;'
    cur.execute(pending_query,(user_id,))
    pending_requests=cur.fetchall()


    for i in pending_requests:
        user_id = i[1]
        pending_service=i[8]
        booking_date = i[3]
        pending_start_time = i[4]
        pending_end_time = i[5]
        extra_details = i[7]
        status=i[10]
        booked="Yes"
        
        if status=="completed":
            frame_colour="white"
            
        else:
            frame_colour="#87CEEB"
        

        
        frame = Frame(scrollable_frame, bg=frame_colour, height=200, width=1000)
        frame.pack(pady=10, fill='x',expand=True)
        
        pending_service_label = Label(frame, text=pending_service, bg=frame_colour,font=('Lucida Bright',16,"bold"))
        pending_service_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        booking_date_label = Label(frame, text="Date: "+str(booking_date), bg=frame_colour,font=('Lucida Bright',14))
        booking_date_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        time_label = Label(frame, text="Time: "+str(pending_start_time)+"-"+str(pending_end_time), bg=frame_colour,font=('Lucida Bright',14))
        time_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        view_button=Button(frame,
                  text="VIEW",
                  activebackground='white',
                  activeforeground='#228B22',
                  command=lambda booking_date=booking_date,user_id=user_id,status=status,booked=booked,start_time=pending_start_time,end_time=pending_end_time,pending_service=pending_service:view(booking_date,user_id,status,booked,start_time,end_time,pending_service),
                  bg='#228B22',
                  fg='white',
                  font=('Garamond',14,"bold"),
                  height=1,
                  width=6,
                  justify='center')
        view_button.grid(row=2, column=0,padx=50,pady=5,sticky='w')
    
    new_service_request_label=Label(new_request_canvas,text="NEW REQUEST",font=('Lucida Bright',16,'bold'),bg='#000080',fg='white',width=80,height=3,justify='center')
    new_service_request_label.grid(row=0,column=1,columnspan=2,padx=10,pady=10,sticky='w')
    search_text=StringVar()
    search_text.set("Select the Desired Service")
    search_label=Label(new_request_canvas,
                       textvariable=search_text,
                       bg='white',
                       height=2,
                       width=80,
                       bd=0,
                       font=('Lucida Bright',16),
                       fg="#000080",
                       justify='center')
    search_label.grid(row=1,column=1,columnspan=2,padx=10,pady=10,sticky='w')
    global row,column
    row=2
    column=1
    fetch_data()


def create_login_screen(table):
    main_window.withdraw()

    login_window = Toplevel()
    login_window.title("Login")
    login_window.geometry("400x400")
    login_window.configure(bg="black")

    Label(login_window, text="Login Form", font=("Lucida Bright", 20), pady=20, bg="black", fg="white").pack()

    Label(login_window, text="UserID", font=("Lucida Bright", 12), bg="black", fg="white").pack()
    userid_entry = Entry(login_window)
    userid_entry.pack(pady=5)
    

    Label(login_window, text="Password", font=("Lucida Bright", 12), bg="black", fg="white").pack()
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)
    

    def confirm_login(table):
        global user_id
        user_id=userid_entry.get()
        password=password_entry.get()

        def execute():
            password_record=cur.fetchone()
            for i in password_record:
                check_password=i
            
            if password==check_password:
                 login_window.destroy()
                 if table=='users':
                     
                     user_homescreen(user_id)
                 else:
                     service_homescreen(user_id)
            else:
                Label(login_window, text="INCORRECT PASSWORD", font=("Lucida Bright", 12), bg="black", fg="red").pack()
            

        if table=='users':
            query1='select user_id from users;'
            cur.execute(query1)
            ids=cur.fetchall()
            available_ids=[i[0] for i in ids]
            if user_id in available_ids:
                query="select password from users where user_id=%s;"
                cur.execute(query,(user_id,))
                execute()
            else:
                Label(login_window, text="UserID not found.", font=("Lucida Bright", 12), bg="black", fg="red").pack()
                
        else:
            query1='select provider_id from service_provider;'
            cur.execute(query1)
            ids=cur.fetchall()
            available_ids=[i[0] for i in ids]
            if user_id in available_ids:
                query="select password from service_provider where provider_id=%s;"
                cur.execute(query,(user_id,))
                execute()
            else:
                Label(login_window, text="UserID not found.", font=("Lucida Bright", 12), bg="black", fg="red").pack()

        
    Button(login_window, text="Login", width=20, command= lambda: confirm_login(table),activebackground='white',activeforeground='#000080',bg='purple',fg='white').pack(pady=20)



def fetch_data():
    global s_name,s_service,s_rating
    query="select distinct(domain) from service_provider;"
    cur.execute(query)
    details=cur.fetchall()
    for i in details:
        s_service=i
        create_button(s_service)
    

def view(booking_date,user_id,status,booked,start_time,end_time,service):
    
    view_screen=Toplevel()
    view_screen.configure(background='white')
    view_screen.title("VIEW")
    view_screen.geometry("500x400")
    open_screens.append(view_screen)

    if status=='processing':
        if booked=="Yes":
            query="select * from bookings where user_id=%s and start_time=%s and end_time=%s and service=%s"
            cur.execute(query,(user_id,start_time,end_time,service))
            booking_details=cur.fetchall()
            for i in booking_details:
                provider_id=i[0]
                OTP=i[2]
                billable_hours=i[9]
            query="select hourlyrate from service_provider where provider_id=%s;"
            cur.execute(query,(provider_id,))
            hourly_rate=cur.fetchone()[0]
            bill_amount=hourly_rate*billable_hours

            bill_amount_label=Label(view_screen, text="Bill amount: "+str(bill_amount), bg='white', fg='#000080',font=("Lucida Bright",14,"bold"))
            bill_amount_label.grid(row=1,column=1,padx=50,pady=20)

            otp_entry=Entry(view_screen)
            otp_label=Label(view_screen, text="OTP", bg='white', fg='#000080',font=("Lucida Bright",14,"bold"))
            otp_label.grid(row=2,column=1,pady=10)
            otp_entry.grid(row=2,column=2,padx=10)

            verified_label=Label(view_screen, text="", bg='white', fg='#AEF359',font=("Lucida Bright",14,"bold"))
            verified_label.grid(row=4,column=2,padx=5)

            check_button=Button(view_screen,
                      text="CHECK",
                      activebackground='white',
                      activeforeground='#228B22',
                      command=lambda: check_otp(OTP,otp_entry,view_screen,verified_label,start_time,end_time,service),
                      bg='#228B22',
                      fg='white',
                      font=('Garamond',14,"bold"),
                      height=1,
                      width=6,
                      justify='center')
            check_button.grid(row=3,column=2,pady=5)

    elif status=="completed":
        feedback_label=Label(view_screen, text="FEEDBACK", bg='white', fg='#000080',font=("Lucida Bright",14,"bold"))
        feedback_label.pack(padx=10,pady=20)

        feedback_text=Text(view_screen,bg='white',height=9)
        feedback_text.pack(pady=20)

        submit_button=Button(view_screen,
                  text="SUBMIT",
                  activebackground='white',
                  activeforeground='#228B22',
                  command=lambda: store_feedback(feedback_text,booking_date,start_time,end_time,user_id),
                  bg='#228B22',
                  fg='white',
                  font=('Garamond',14,"bold"),
                  height=1,
                  width=30,
                  justify='center')
        submit_button.pack(pady=15)

def store_feedback(feedback_text,booking_date,start_time,end_time,user_id):
    text=feedback_text.get('1.0','end-1c')
    query="update bookings set feedback=%s where booking_date=%s and start_time=%s and end_time=%s and user_id=%s"
    values=(text,booking_date,start_time,end_time,user_id)
    cur.execute(query,values)

    mycon.commit()
            

def check_otp(otp,otp_entry,view_screen,verified_label,start_time,end_time,service):
    entered_otp=otp_entry.get()
    entered_otp=int(entered_otp)
    
    if entered_otp==otp:
        verified_label.config(text="OTP VERIFIED",fg='#AEF359')
        payment_button=Button(view_screen,
                  text="PROCEED TO PAYMENT",
                  activebackground='white',
                  activeforeground='#228B22',
                  command=lambda: payment_options(start_time,end_time,service),
                  bg='#228B22',
                  fg='white',
                  font=('Garamond',14,"bold"),
                  height=1,
                  width=30,
                  justify='center')
        payment_button.grid(row=5,column=1,pady=5,columnspan=2)

    else:
       verified_label.config(text='INCORRECT OTP',fg='red')
   

def payment_options(start_time,end_time,service):
    import tkinter as tk
    from tkinter import messagebox
    import time

    
    def show_payment_screen(payment_method):
        if payment_method == 'UPI':
            upi_screen()
        elif payment_method == 'Net Banking':
            net_banking_screen()
        elif payment_method == 'Cash':
            cash_screen()

    
    def upi_screen():
        payment_frame.pack_forget()

        upi_frame = tk.Frame(root, bg="white")
        upi_frame.pack(padx=20, pady=20)

        upi_label = tk.Label(upi_frame, text="Enter your UPI ID:", bg="white", font=('Arial', 12))
        upi_label.pack()

        upi_entry = tk.Entry(upi_frame)
        upi_entry.pack()

        def proceed_upi():
            
            upi_frame.pack_forget()
            success_screen()

        submit_button = tk.Button(upi_frame, text="Submit", command=proceed_upi, bg="navy", fg="white")
        submit_button.pack()

    
    def net_banking_screen():
        payment_frame.pack_forget()

        net_banking_frame = tk.Frame(root, bg="white")
        net_banking_frame.pack(padx=20, pady=20)

        net_banking_label = tk.Label(net_banking_frame, text="Enter Credit Card Details:", bg="white", font=('Arial', 12))
        net_banking_label.pack()

        card_number_label = tk.Label(net_banking_frame, text="Card Number:", bg="white")
        card_number_label.pack()
        card_number_entry = tk.Entry(net_banking_frame)
        card_number_entry.pack()

        cvv_label = tk.Label(net_banking_frame, text="CVV:", bg="white")
        cvv_label.pack()
        cvv_entry = tk.Entry(net_banking_frame, show="*")
        cvv_entry.pack()

        def proceed_net_banking():
            
            net_banking_frame.pack_forget()
            success_screen()

        submit_button = tk.Button(net_banking_frame, text="Submit", command=proceed_net_banking, bg="navy", fg="white")
        submit_button.pack()

    
    def cash_screen():
        messagebox.showinfo("Complete","Service Completed")
        query="update bookings set status='completed' where user_id=%s and start_time=%s and end_time=%s;"
        values=(user_id,start_time,end_time)
        cur.execute(query,values)
        mycon.commit()

        homelander()
           
    def success_screen():
        time.sleep(7)

        messagebox.showinfo("Payment", "Payment Successful")
        query="update bookings set status='completed' where user_id=%s and start_time=%s and end_time=%s and service=%s;"
        values=(user_id,start_time,end_time,service)
        cur.execute(query,values)
        mycon.commit()

        homelander()


    root = tk.Toplevel()
    root.title("Payment Options")
    open_screens.append(root)

    root.configure(bg="white")


    payment_frame = tk.Frame(root, bg="white")
    payment_frame.pack(padx=20, pady=20)


    payment_label = tk.Label(payment_frame, text="Choose Payment Option", font=('Arial', 14), bg="white")
    payment_label.pack(pady=10)


    upi_button = tk.Button(payment_frame, text="UPI", width=20, command=lambda: show_payment_screen('UPI'), bg="navy", fg="white")
    upi_button.pack(pady=5)

    net_banking_button = tk.Button(payment_frame, text="Net Banking", width=20, command=lambda: show_payment_screen('Net Banking'), bg="navy", fg="white")
    net_banking_button.pack(pady=5)

    cash_button = tk.Button(payment_frame, text="Cash", width=20, command=lambda: show_payment_screen('Cash'), bg="navy", fg="white")
    cash_button.pack(pady=5)

    root.mainloop()

    
def create_button(buttext):
    global row,column
    button=Button(new_request_canvas,
                  text=buttext,
                  activebackground='white',
                  activeforeground='#228B22',
                  command=lambda: button_clicked(buttext),
                  bg='#228B22',
                  fg='white',
                  font=('Garamond',14,"bold"),
                  height=2,
                  width=30,
                  justify='center')
    button.grid(row=row,column=column,padx=5,pady=10,sticky='w')
    if column>1:
        column=1
        row+=2
    else:
        column+=1
def button_clicked(screentext):
    global s_details, provider_list_screen,open_screens
    
    provider_list_screen=Toplevel()
    provider_list_screen.configure(background='white')
    provider_list_screen.title(screentext)
    provider_list_screen.geometry("1000x600")
    open_screens.append(provider_list_screen)
    query="select * from service_provider where domain=%s order by service;"
    cur.execute(query,screentext)
    s_details=cur.fetchall()
    detail_display()

def detail_display():
    canvas=Canvas(provider_list_screen,width=1000)
    scrollbar=Scrollbar(provider_list_screen, orient='vertical', command=canvas.yview)
    scrollable_frame=Frame(canvas,width=1000)
    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_frame=canvas.create_window((0,0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left',fill='both',expand=True)
    
    global s_name,s_provider_id,s_service
    for i in s_details:
        s_name = i[0]
        s_domain = i[1]
        s_rating = i[2]
        s_hourlyrate = i[3]
        s_service = i[4]
        s_availability=i[5]
        s_provider_id=i[6]
        
        if s_availability=="available":
            frame_colour="#87CEEB"
            button_click='yes'
        else:
            button_click='no'
            frame_colour='#808080'


        frame = Frame(scrollable_frame, bg=frame_colour, height=200, width=1000)
        frame.pack(pady=10, fill='x',expand=True)
        
        service_label = Label(frame, text=s_service, bg=frame_colour,font=('Lucida Bright',16,"bold"))
        service_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        name_label = Label(frame, text="Name: "+str(s_name), bg=frame_colour,font=('Lucida Bright',14))
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        rating_label = Label(frame, text="Rating: "+str(s_rating), bg=frame_colour,font=('Lucida Bright',14))
        rating_label.grid(row=1, column=2, padx=10, pady=5, sticky='w')

        hourlyrate_label = Label(frame, text="Hourly Rate: "+str(s_hourlyrate), bg=frame_colour,font=('Lucida Bright',14))
        hourlyrate_label.grid(row=1, column=3, padx=10, pady=5, sticky='w')
        
        if button_click=='yes':
            book_button=Button(frame,
                               text='BOOK',
                               activebackground='white',
                               activeforeground='#000080',
                               command=lambda provider_id=s_provider_id,name=s_name,rating=s_rating,hourlyrate=s_hourlyrate,service=s_service: book(provider_id,name,rating,hourlyrate,service),
                               bg='#228B22',
                               fg='black',
                               font=('Garamond',12),
                               height=1,
                               width=10,
                               justify='center')
            book_button.grid(row=2,column=3,sticky='w')

        available_hours_frame=Frame(frame,bg=frame_colour)
        available_hours_frame.grid(row=2,column=0,columnspan=3,sticky='w')
        available_hours_label=Label(available_hours_frame, text="Available Hours:",bg=frame_colour,font=('Lucida Bright',14))
        available_hours_label.pack(padx=10)
        available=available_hours(s_provider_id)
        for i in available:
                label=Label(available_hours_frame, text=str(i[0])+"-"+str(i[1]),font=('Lucida Bright',14),padx=50,bg=frame_colour)
                label.pack(padx=2)

def book(provider_id,s_name,s_rating,s_hourlyrate,s_service):

    global open_screens
    booking_screen=Toplevel()
    booking_screen.configure(background='white')
    booking_screen.title("Book Service")
    booking_screen.geometry("1000x600")
    open_screens.append(booking_screen)
    details_frame=Frame(booking_screen,bg='#B2FBA5')
    details_frame.pack(side=TOP,fill=X,pady=0)
    frame_colour='#B2FBA5'

    submissions_frame=Frame(booking_screen,bg='#C7FCBD')
    submissions_frame.pack(fill=BOTH)
 
    service_label = Label(details_frame, text=s_service, bg=frame_colour,font=('Lucida Bright',16,"bold"))
    service_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    name_label = Label(details_frame, text="Name: "+str(s_name), bg=frame_colour,font=('Lucida Bright',14))
    name_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    rating_label = Label(details_frame, text="Rating: "+str(s_rating), bg=frame_colour,font=('Lucida Bright',14))
    rating_label.grid(row=1, column=2, padx=10, pady=5, sticky='w')

    hourlyrate_label = Label(details_frame, text="Hourly Rate: "+str(s_hourlyrate), bg=frame_colour,font=('Lucida Bright',14))
    hourlyrate_label.grid(row=1, column=3, padx=10, pady=5, sticky='w')

    available_hours_frame=Frame(details_frame,bg=frame_colour)
    available_hours_frame.grid(row=2,column=0,columnspan=3,sticky='w')
    available_hours_label=Label(available_hours_frame, text="Available Hours:",bg=frame_colour,font=('Lucida Bright',14))
    available_hours_label.pack(padx=10)
    available=available_hours(provider_id)
    for i in available:
            label=Label(available_hours_frame, text=str(i[0])+"-"+str(i[1]),font=('Lucida Bright',14),padx=50,bg=frame_colour)
            label.pack(padx=2)

    start_time_entry=Entry(submissions_frame)
    start_time_entry.grid(row=1,column=2,sticky='w')

    end_time_entry=Entry(submissions_frame)
    end_time_entry.grid(row=2,column=2,sticky='w')
    
    start_label=Label(submissions_frame,text="Start Time:",font=("Lucida Bright",14), fg="#000080",bg='#C7FCBD')
    start_label.grid(row=1,column=1,sticky='w',padx=10,pady=10)
    
    end_label=Label(submissions_frame,text="End Time:",font=("Lucida Bright",14), fg="#000080",bg='#C7FCBD')
    end_label.grid(row=2,column=1,sticky='w',padx=10,pady=10)

    check_button=Button(submissions_frame,
                       text='CHECK',
                       activebackground='white',
                       activeforeground='#000080',
                       command=lambda available=available, start_time_entry=start_time_entry,end_time_entry=end_time_entry,service=s_service,provider_id=provider_id: submit(available,start_time_entry,end_time_entry,extradetail_text,address_text,service,provider_id),
                       bg='#228B22',
                       fg='black',
                       font=('Garamond',12),
                       height=1,
                       width=10,
                       justify='center')
    check_button.grid(row=3,column=1, columnspan=2)

    address_label=Label(submissions_frame,text="Address:",font=("Lucida Bright",14),bg='#C7FCBD')
    address_label.grid(row=1,column=3,sticky='w')
    address_text=Text(submissions_frame,bg='white',height=6)
    address_text.grid(row=2,column=3,padx=10)

    existing_address_button=Button(submissions_frame,
                       text='Use Existing Address',
                       activebackground='white',
                       activeforeground='#000080',
                       command=lambda: existing_address(address_text),
                       bg='#228B22',
                       fg='black',
                       font=('Garamond',12,'bold'),
                       height=1,
                       width=20,
                       justify='center')
    existing_address_button.grid(row=1,column=3)
    
    extradetail_label=Label(submissions_frame,text="Any special details or requests to be given:",font=("Lucida Bright",14),bg='#C7FCBD')
    extradetail_label.grid(row=3,column=3,sticky='w')
    extradetail_text=Text(submissions_frame,bg='white',height=9)
    extradetail_text.grid(row=5,column=3,padx=10)


def existing_address(address_text):
    with open(r'address.csv','r') as f:
        rob=csv.reader(f)
        for i in rob:
            if i[0]==user_id:
                address=i[1]
                address_text.insert('1.0',address)
                break

        else:
            address_text.insert('1.0','No Saved Address')    
    
def submit(available_hours,start_time_entry,end_time_entry,extradetail_entry,address_entry,service,provider_id):
    global booking_start_time,booking_end_time,address,extradetail
    import datetime as dt
    start_time=start_time_entry.get()
    end_time=end_time_entry.get()
    extradetail=extradetail_entry.get('1.0','end-1c')
    address=address_entry.get('1.0','end-1c')
    
    if validate_time(start_time) and validate_time(end_time):
        booking_start_time=dt.datetime.strptime(start_time,'%H:%M:%S')
        booking_end_time=dt.datetime.strptime(end_time,'%H:%M:%S')
        if booking_end_time<booking_start_time:
            timemessage()
        else:
            if is_within_available_hours(booking_start_time, booking_end_time, available_hours):
                billable_time=booking_end_time-booking_start_time
                billable_hours=billable_time.total_seconds()/3600
                wait(billable_hours,service,provider_id)
            else:
                timemessage()
    else:
        timemessage()


def time_to_timedelta(time_obj):
    return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)

def is_within_available_hours(start_time, end_time, available_hours):
    if isinstance(start_time, datetime):
        start_time = time_to_timedelta(start_time)
    if isinstance(end_time, datetime):
        end_time = time_to_timedelta(end_time)
    
    
    for slot_start, slot_end in available_hours:
        if slot_start <= start_time and end_time <= slot_end:
            return True
    
    return False 

def wait(hours,service,s_provider_id):
    global open_screens
    wait_screen=Toplevel()
    wait_screen.configure(background='white')
    wait_screen.title("Wait Screen")
    wait_screen.geometry("600x600")
    open_screens.append(wait_screen)
    request_process_label=Label(wait_screen, text="Your Request is being Processed.", bg='white', fg='#000080',font=("Lucida Bright",14,"bold"))
    request_process_label.pack(pady=50)

    personnel_label=Label(wait_screen, text="Service Provider will be assigned shortly.", bg='white', fg='#000080',font=("Lucida Bright",14,"bold"))
    personnel_label.pack(pady=10)

    query="insert into bookings (provider_id,user_id,OTP,booking_date,start_time,end_time,address,extradetails,service,billable_hours) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    OTP=randint(10000,99999)
    inniku_date=date.today()
    values=(s_provider_id,user_id,OTP,inniku_date,booking_start_time.time(),booking_end_time.time(),address if address else None,extradetail if extradetail else None,service,hours)
    print(values)
    cur.execute(query,values)
    mycon.commit()
    home_screen_button=Button(wait_screen,
                       text='RETURN TO HOMESCREEN',
                       activebackground='white',
                       activeforeground='#000080',
                       command=lambda : homelander(),
                       bg='#228B22',
                       fg='black',
                       font=('Garamond',12),
                       height=1,
                       width=30,
                       justify='center')
    home_screen_button.pack(pady=50)

def homelander():
    global open_screens
    for i in open_screens:
        i.destroy()
    if table=='users':
        user_homescreen(user_id)
    else:
        service_homescreen(provider_id)

def timemessage():
    from tkinter import messagebox
    messagebox.showwarning("Incorrect Time","Enter time in the format (HH:MM:SS) or Check if Time is Within Available Hours")
            

def validate_time(time):
    if len(time)>8:
        return False
    l=time.split(":")
    if len(l)!=3:
        return False
    j=1
    for i in l:
        if i.isdigit()==False:
            return False 
        if j==1:
            if int(i)>=0 and int(i)<=23:
                j+=1
                continue
            else:
                return False

        else:
            if int(i)>=0 and int(i)<=59:
                continue
            else:
                return False
    
    return True
        
    
def available_hours(provider_id):
    from datetime import datetime,timedelta
    query="select work_start_time,work_end_time from service_provider where provider_id="+str(provider_id)+';'
    cur.execute(query)
    working_hours=cur.fetchall()
    available = []
    query="select start_time,end_time from bookings where provider_id=%s and booking_date=%s;"
    values=(provider_id,date.today())
    cur.execute(query,values)
    unavailable_slots=cur.fetchall()
    for work_start, work_end in working_hours:
        current_start = work_start
        work_end_time = work_end
        
        for un_start, un_end in unavailable_slots:
            un_start_time = un_start
            un_end_time = un_end
            
            if un_start_time >= work_end_time or un_end_time <= current_start:
                continue  
            if current_start < un_start_time:
                available.append((current_start, un_start_time))
            current_start = max(current_start, un_end_time)
        
        if current_start < work_end_time:
            available.append((current_start, work_end_time))

    return available
    
def service_homescreen(provider_id):
    global open_screens
    open_screens=[]
    home_screen=Tk()
    home_screen.configure(background='white')
    home_screen.title("Home Screen")
    home_screen.geometry("900x700")
    open_screens.append(home_screen)

    new_request_frame=Frame(home_screen,width=800,height=700,bg='white')
    pending_request_frame=Frame(home_screen,width=400,height=700,bg='white')
    
    pending_request_canvas = Canvas(pending_request_frame, width=400, height=700)

    vertical_scrollbar = Scrollbar(
        pending_request_frame, orient='vertical', command=pending_request_canvas.yview)
    horizontal_scrollbar = Scrollbar(
        pending_request_frame, orient='horizontal', command=pending_request_canvas.xview)

    pending_scrollable_frame = Frame(pending_request_canvas, width=400)

    pending_scrollable_frame.bind(
        "<Configure>",
        lambda e: pending_request_canvas.configure(
            scrollregion=pending_request_canvas.bbox("all")))

    canvas_frame = pending_request_canvas.create_window((0, 0), window=pending_scrollable_frame, anchor="nw")


    pending_request_canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    vertical_scrollbar.pack(side="right", fill="y")
    horizontal_scrollbar.pack(side="bottom", fill="x")
    pending_request_canvas.pack(side="left", fill="both", expand=True)

    
    pending_request_canvas.pack(side='left',fill='both',expand=True)
    pending_request_frame.pack(side='left',fill='both',expand=True)
    new_request_frame.pack(side='left',fill='both',expand=True)

    pending_request_label=Label(pending_scrollable_frame,text="PAST REQUESTS",bg='#000080',fg='white',font=('Lucida Bright',16,'bold'),height=3,justify='center',width=20)
    pending_request_label.pack(pady=10,fill='x',expand=True)
    pending_query='select * from bookings where provider_id=%s and status="completed" order by booking_date desc,start_time;'
    cur.execute(pending_query,(provider_id,))
    pending_requests=cur.fetchall()

    for i in pending_requests:
        provider_id=i[0]
        user_id=i[1]
        OTP=i[2]
        booking_date=i[3]   
        start_time=i[4]
        end_time=i[5]
        address=i[6]
        extradetails=i[7]
        service=i[8]
        billable_hours=i[9]
        status=i[10]     

        if status=="completed":
            frame_colour="white"
        else:
            frame_colour="#87CEEB"
        
        frame = Frame(pending_scrollable_frame, bg=frame_colour, height=200, width=1000)
        frame.pack(pady=10, fill='x',expand=True)
      
        pending_service_label = Label(frame, text=service, bg=frame_colour,font=('Lucida Bright',16,"bold"))
        pending_service_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        booking_date_label = Label(frame, text="Date: "+str(booking_date), bg=frame_colour,font=('Lucida Bright',14))
        booking_date_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        time_label = Label(frame, text="Time: "+str(start_time)+"-"+str(end_time), bg=frame_colour,font=('Lucida Bright',14))
        time_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        view_button=Button(frame,
                  text="VIEW",
                  activebackground='white',
                  activeforeground='#228B22',
                  command=lambda start_time=start_time,end_time=end_time,date=booking_date,provider_id=provider_id :new_view(start_time,end_time,date,provider_id),
                  bg='#228B22',
                  fg='white',
                  font=('Garamond',14,"bold"),
                  height=1,
                  width=6,
                  justify='center')
        view_button.grid(row=2, column=0,padx=50,pady=5,sticky='w')

    new_service_request_label=Label(new_request_frame,text="NEW REQUESTS",font=('Lucida Bright',16,'bold'),bg='#000080',fg='white',width=80,height=3,justify='center')
    new_service_request_label.pack()

    new_request_canvas = Canvas(new_request_frame, width=400, height=700)

    vertical_scrollbar = Scrollbar(
        new_request_frame, orient='vertical', command=pending_request_canvas.yview)
    horizontal_scrollbar = Scrollbar(
        new_request_frame, orient='horizontal', command=pending_request_canvas.xview)

    new_scrollable_frame = Frame(new_request_canvas, width=400)

    new_scrollable_frame.bind(
        "<Configure>",
        lambda e: new_request_canvas.configure(
            scrollregion=new_request_canvas.bbox("all")))

    canvas_frame = new_request_canvas.create_window((0, 0), window=new_scrollable_frame, anchor="nw")


    new_request_canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    vertical_scrollbar.pack(side="right", fill="y")
    horizontal_scrollbar.pack(side="bottom", fill="x")
    new_request_canvas.pack(side="left", fill="both", expand=True)

    new_query="select * from bookings where provider_id=%s and booking_date=curdate() and status='processing';"
    cur.execute(new_query,(provider_id,))

    new_requests=cur.fetchall()
    for i in new_requests:
        provider_id=i[0]
        user_id=i[1]
        OTP=i[2]
        booking_date=i[3]   
        start_time=i[4]
        end_time=i[5]
        address=i[6]
        extradetails=i[7]
        service=i[8]
        billable_hours=i[9]
        status=i[10]    

        frame_colour='white'    
        
        frame = Frame(new_scrollable_frame, bg=frame_colour, height=200, width=1000)
        frame.pack(pady=10, fill='x',expand=True)

        pending_service_label = Label(frame, text=service, bg=frame_colour,font=('Lucida Bright',16,"bold"))
        pending_service_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        booking_date_label = Label(frame, text="Date: "+str(booking_date), bg=frame_colour,font=('Lucida Bright',14))
        booking_date_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        time_label = Label(frame, text="Time: "+str(start_time)+"-"+str(end_time), bg=frame_colour,font=('Lucida Bright',14))
        time_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        new_view_button=Button(frame,
                  text="VIEW",
                  activebackground='white',
                  activeforeground='#228B22',
                  command=lambda address=address,extradetails=extradetails,OTP=OTP,start_time=start_time,end_time=end_time,provider_id=provider_id,billable_hours=billable_hours :new(address,extradetails,OTP,start_time,end_time,billable_hours,provider_id),
                  bg='#228B22',
                  fg='white',
                  font=('Garamond',14,"bold"),
                  height=1,
                  width=6,
                  justify='center')
        new_view_button.grid(row=2, column=0,padx=50,pady=5,sticky='w')


def new(address,extradetails,OTP,start_time,end_time,billable_hours,provider_id):
    new_screen=Tk()
    new_screen.configure(background='white')
    new_screen.title("Request Screen")
    new_screen.geometry("500x500")
    open_screens.append(new_screen)

    query="select hourlyrate from service_provider where provider_id=%s;"
    cur.execute(query,(provider_id,))
    for i in cur.fetchone(): 
        hourlyrate=int(i) 
    bill_amount=hourlyrate*billable_hours
    bill_amount_label=Label(new_screen, text="Bill Amount: "+str(bill_amount), bg='white',font=('Lucida Bright',14),fg='#000080')
    bill_amount_label.pack(padx=10,pady=20)

    time_label= Label(new_screen, text="Time: "+str(start_time)+"-"+str(end_time), bg='white',font=('Lucida Bright',14),fg='#000080')
    time_label.pack(pady=10)

    OTP_label=Label(new_screen, text="OTP:"+str(OTP), bg='white',font=('Lucida Bright',14),fg='#228B22')
    OTP_label.pack(pady=10)

    address_label=Label(new_screen, text="Address: "+str(address), bg='white',font=('Lucida Bright',14),fg='#228B22')
    address_label.pack(pady=10)

    extradetails_label=Label(new_screen, text="Extradetails: "+str(extradetails), bg='white',font=('Lucida Bright',14),fg='#228B22')
    extradetails_label.pack(pady=10)
    
def new_view(start_time,end_time,date,provider_id):
    feedback_screen=Toplevel()
    feedback_screen.configure(background='white')
    feedback_screen.title("View Screen")
    feedback_screen.geometry("600x600")
    open_screens.append(feedback_screen)

    query="select feedback from bookings where booking_date=%s and start_time=%s and end_time=%s and provider_id=%s and feedback is not null;"
    values=(date,start_time,end_time,provider_id)
    cur.execute(query,values)

    g=cur.fetchone()

    if g:
        for i in g:
            feedback=i
        
        feedback_title=Label(feedback_screen, text="FEEDBACK", fg="#228B22",font=('Lucida Bright',14),bg='white')
        feedback_title.pack(padx=10,pady=20)

        
        feedback_label=Label(feedback_screen, text=feedback, fg="#000080",font=('Lucida Bright',14),bg='white')
        feedback_label.pack(padx=10,pady=20)


    else:
        feedback_label=Label(feedback_screen, text="Yet to Receive Feedback on this Request.", fg="#000080",font=('Lucida Bright',14),bg='white')
        feedback_label.pack(padx=10,pady=20)        
    
create_main_screen()        
                  


