import mysql.connector
import datetime

mydb=mysql.connector.connect(host="localhost",\
                             user="root",\
                             password="swayamp123",\
                             database="library")

mycursor=mydb.cursor()

def menu():
    choice="c"
    choice=choice.lower()
    while(choice=="c"):
        print("Enter 1:To veiw a table")
        print("Enter 2:To add a book")
        print("Enter 3:To edit a book detail")
        print("Enter 4:To delete a book form the table")
        print("Enter 5:To add a member")
        print("Enter 6:To edit a member detail")
        print("Enter 7:To delete a member from the list")
        print("Enter 8:To issue a book to a member")
        print("Enter 9:To remove a book issue detail")
        choice=input("Enter your choice:")
        if(choice=="1"):
            print("Which table do you want to view books or member or rental?")
            choice=input("Enter your choice")
            if(choice.lower() in ("books","member","rental")):
                view(choice.lower())
            else:
                print("Invalid choice")
        elif(choice=="2"):
            addbook()
        elif(choice=="3"):
            editbook()
        elif(choice=="4"):
            delbook()
        elif(choice=="5"):
            addmember()
        elif(choice=="6"):
            editmember()
        elif(choice=="7"):
            delmember()
        elif(choice=="8"):
            addrental()
        elif(choice=="9"):
            delrental()
        else:
            print("Invaild choice")
        choice=input("To countinue enter 'c' or 'q' to quit.")
        choice=choice.lower()

def search(a,b):
    sql="select * from "+b
    mycursor.execute(sql)
    data=mycursor.fetchall()
    flag=False
    for x in data:
        if(x[0]==a):
           flag=True
    return flag

def datemod(a,b):
    d=int(a.day)
    m=int(a.month)
    y=int(a.year)
    if(m in (1,3,5,7,8,10)):
        if((d+b)>31):
            d=(d+b)%31
            m+=1
        else:
            d=(d+b)%31
    elif(m in (4,6,9,11)):
        if((d+b)>30):
            d=(d+b)%30
            m+=1
        else:
            d=(d+b)%30
    elif(m==12):
        if((d+b)>31):
            d=(d+b)%31
            m=1
            y+=1
        else:
            d=(d+b)%31
    else:
        if(y%4==0):
            if((d+b)>31):
                d=(d+b)%29
                m+=1
            else:
                d=(d+b)%29
        else:
            if((d+b)>31):
                d=(d+b)%28
                m+=1
            else:
                d=(d+b)%28
    nd=datetime.datetime(y,m,d)
    newdate=nd.date()
    return newdate

def view(a):
    sql="select * from "+a
    mycursor.execute(sql)
    data=mycursor.fetchall()
    for x in data:
        print(x)

def addbook():
    L=[]
    bookid=input("Enter book_id:")
    bookname=input("Enter book name:")
    writer=input("Enter name of writer:")
    price=int(input("Enter price of the book:"))
    stock=int(input("Enter stock of the book:"))
    L.append(bookid)
    L.append(bookname)
    L.append(writer)
    L.append(price)
    L.append(stock)
    newbook=(L)
    sql="insert into books(book_id,book_name,writer,price,stock)values(%s,%s,%s,%s,%s)"
    mycursor.execute(sql,newbook)
    mydb.commit()
    print("One Book added.")

def editbook():
    bookid=input("Enter book_id:")
    flag=search(bookid,"books")
    if(flag==True):
        field=input("Enter 'price' to change price or 'stock' to change stock:")
        field=field.lower()
        if(field=="price" or field=="stock"):
            new=int(input("Enter the new value:"))
            sql="update books set "+field+" = %s where book_id = %s"
            ed=(new,bookid)
            mycursor.execute(sql,ed)
            mydb.commit()
            print("Edited")
            print("Edited Record:")
            sql="select * from books where book_id=%s"
            ed=([bookid])
            mycursor.execute(sql,ed)
            rec=mycursor.fetchall()
            for x in rec:
                print(x)
        else:
            print("Invalid choice")
    else:
        print("Invalid book_id")

def delbook():
    bookid=input("Enter the book_id to be deleted:")
    flag=search(bookid,"books")
    if(flag==True):
        sql="select member_id from rental where book_id=%s"
        d=([bookid])
        mycursor.execute(sql,d)
        rec=mycursor.fetchall()
        for x in rec:
            sql="select number_books_borrowed from member where member_id=%s"
            mycursor.execute(sql,[x[0]])
            r=mycursor.fetchall()
            for i in r:
                nbb=int(i[0])-1
                sql="update member set number_books_borrowed = %s where member_id = %s"
                up=(nbb,x[0])
                mycursor.execute(sql,up)
                mydb.commit()   
        sql="delete from books where book_id=%s"
        ide=([bookid])
        mycursor.execute(sql,ide)
        mydb.commit()
        sql="delete from rental where book_id=%s"
        mycursor.execute(sql,ide)
        mydb.commit()
        print("One book deletled")
    else:
        print("Invalid book_id")

def addmember():
    L=[]
    memid=input("Enter member_id:")
    memname=input("Enter member name:")
    year=int(input("Enter year(yyyy) of membership expiry date:"))
    month=int(input("Enter month(mm) of membership expiry date:"))
    d=int(input("Enter date(dd) of membership expiry date:"))
    da=datetime.datetime(year,month,d)
    dat=da.date()
    nbook=int(input("Enter number of books borrowed:"))
    L.append(memid)
    L.append(memname)
    L.append(nbook)
    L.append(dat)
    newmem=(L)
    sql="insert into member(member_id,member_name,number_books_borrowed,member_expiry_date)values(%s,%s,%s,%s)"
    mycursor.execute(sql,newmem)
    mydb.commit()
    print("One member added.")

def editmember():
    memid=int(input("Enter member_id:"))
    flag=search(memid,"member")
    if(flag==True):
        field=input("Enter 'exp' to change member_expiry_date or 'borrow' to change number_books_boroowed")
        field=field.lower()
        if(field=="exp"):
           year=int(input("Enter year(yyyy) of new membership expiry date:"))
           month=int(input("Enter month(mm) of new membership expiry date:"))
           d=int(input("Enter date(dd) of new membership expiry date:"))
           da=datetime.datetime(year,month,d)
           dat=da.date()
           sql="update member set member_expiry_date = %s where member_id = %s"
           ed=(dat,memid)
           mycursor.execute(sql,ed)
           mydb.commit()
           print("Edited")
           print("Edited Record:")
           sql="select * from member where member_id=%s"
           ed=([memid])
           mycursor.execute(sql,ed)
           rec=mycursor.fetchall()
           for x in rec:
                print(x)
        elif(field=="borrow"):
            new=int(input("Enter the new value"))
            sql="update member set number_books_borrowed = %s where member_id = %s"
            ed=(new,memid)
            mycursor.execute(sql,ed)
            mydb.commit()
            print("Edited")
            print("Edited Record:")
            sql="select * from member where member_id=%s"
            ed=([memid])
            mycursor.execute(sql,ed)
            rec=mycursor.fetchall()
            for x in rec:
                print(x)
        else:
            print("Invalid choice")
    else:
        print("Invalid member_id")

def delmember():
    memid=int(input("Enter the member_id to be deleted:"))
    flag=search(memid,"member")
    if(flag==True):
        sql="select book_id from rental where member_id=%s"
        d=([memid])
        mycursor.execute(sql,d)
        rec=mycursor.fetchall()
        for x in rec:
            sql="select stock from books where book_id=%s"
            mycursor.execute(sql,[x[0]])
            r=mycursor.fetchall()
            for i in r:
                nstk=int(i[0])+1
                sql="update books set stock = %s where book_id = %s"
                up=(nstk,x[0])
                mycursor.execute(sql,up)
                mydb.commit()
        sql="delete from member where member_id=%s"
        ide=([memid])
        mycursor.execute(sql,ide)
        mydb.commit()
        sql="delete from rental where member_id=%s"
        mycursor.execute(sql,ide)
        mydb.commit()
        print("One member deletled")
    else:
        print("Invalid member_id")

def addrental():
    memid=int(input("Enter member_id:"))
    d=datetime.datetime.now()
    flag=search(memid,"member")
    if(flag==True):
        L=[]
        rentalid="R."+str(d.year)+str(d.month)+str(d.day)+"."+str(d.hour)+str(d.minute)+str(d.second)
        db=d.date()
        bookid=input("Enter book_id:")
        fl=search(bookid,"books")
        if(fl==True):
              ext=int(input("Enter the number of days of rental period:"))
              dr=datemod(db,ext)
              L.append(rentalid)
              L.append(bookid)
              L.append(memid)
              L.append(db)
              L.append(dr)
              newrental=(L)
              sql="insert into rental(rental_id,book_id,member_id,date_borrow,date_return) values(%s,%s,%s,%s,%s)"
              mycursor.execute(sql,newrental)
              mydb.commit()
              sql="select stock from books where book_id=%s"
              bid=([bookid])
              mycursor.execute(sql,bid)
              stk=mycursor.fetchall()
              nstk=int(stk[0][0])-1
              sql="update books set stock=%s where book_id=%s"
              x=(nstk,bookid)
              mycursor.execute(sql,x)
              mydb.commit()
              sql="select number_books_borrowed from member where member_id=%s"
              mid=([memid])
              mycursor.execute(sql,mid)
              num=mycursor.fetchall()
              numb=int(num[0][0])+1
              sql="update member set number_books_borrowed=%s where member_id=%s"
              x=(numb,memid)
              mycursor.execute(sql,x)
              mydb.commit()
              print("One Rental Details added.")
        else:
            print("Invalid book_id")
    else:
        print("Invalid member_id")
        
def delrental():
    renid=input("Enter the rental_id to be deleted:")
    x=([renid])
    flag=search(renid,"rental")
    if(flag==True):
        sql="select book_id from rental where rental_id=%s"
        mycursor.execute(sql,x)
        bookid=mycursor.fetchall()
        sql="select stock from books where book_id=%s"
        mycursor.execute(sql,bookid[0])
        stk=mycursor.fetchall()
        nstk=int(stk[0][0])+1
        sql="update books set stock=%s where book_id=%s"
        up=(nstk,bookid[0][0])
        mycursor.execute(sql,up)
        mydb.commit()
        sql="select member_id from rental where rental_id=%s"
        mycursor.execute(sql,x)
        memid=mycursor.fetchall()
        sql="select number_books_borrowed from member where member_id=%s"
        mycursor.execute(sql,memid[0])
        num=mycursor.fetchall()
        numb=int(num[0][0])-1
        sql="update member set number_books_borrowed=%s where member_id=%s"
        up=(numb,memid[0][0])
        mycursor.execute(sql,up)
        mydb.commit()
        sql="delete from rental where rental_id=%s"
        mycursor.execute(sql,x)
        mydb.commit()
        print("One rental deletled")
    else:
        print("Invalid rental_id")

menu()
