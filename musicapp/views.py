from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import pymysql

db = pymysql.connect(host='localhost',
        user='root',
        password='',
        db='dbmusicbeats',
        charset='utf8mb4')
c=db.cursor()

######################################################################
#                           LOAD INDEX PAGE
######################################################################
def index(request):
    """ 
        The function to load index page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    return render(request,"index.html")
######################################################################
#                           LOGIN
######################################################################
def login(request):
    """ 
        The function to load login page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    msg=""
    if(request.POST):
        email=request.POST.get("txtEmail")
        pwd=request.POST.get("txtPassword")
        s="select count(*) from tbllogin where username='"+email+"'"
        c.execute(s)
        i=c.fetchone()
        if(i[0]>0):
            s="select * from tbllogin where username='"+email+"'"
            c.execute(s)
            i=c.fetchone()
            if(i[1]==pwd):
                request.session['email'] = email
                if(i[3]=="1"):
                    if(i[2]=="admin"):
                        return HttpResponseRedirect("/adminhome")
                    elif(i[2]=="company"):
                        return HttpResponseRedirect("/companyhome")
                    elif(i[2]=="user"):
                        return HttpResponseRedirect("/userhome")
                else:
                    msg="You are not authenticated to login"
            else:
                msg="Incorrect password"
        else:
            msg="User doesnt exist"
    return render(request,"login.html",{"msg":msg})
######################################################################
#                           COMPANY
######################################################################
def company(request):
    """ 
        The function to register company
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """

    msg=""
    if(request.POST):
        name=request.POST["txtName"]
        address=request.POST["txtAddress"]
        email=request.POST["txtEmail"]
        phone=request.POST["txtContact"]
        pwd=request.POST["txtPassword"]
        licens=request.POST["txtLicense"]

        s="select count(*) from tbllogin where username='"+email+"'"
        c.execute(s)
        i=c.fetchone()
        if(i[0]>0):
            msg="Email already registered"
        else:
            s="insert into tblcompany (cName,cContact,cEmail,cAddress,cLicense) values('"+name+"','"+phone+"','"+email+"','"+address+"','"+licens+"')"
            try:
                c.execute(s)
                db.commit()
            except:
                msg=s
            else:
                s="insert into tbllogin (username,password,utype,status) values('"+email+"','"+pwd+"','company','0')"
                try:
                    c.execute(s)
                    db.commit()
                except:
                    msg="Sorry login process error"
                else:
                    msg="Registered successfully. Wait for approval"

    return render(request,"company.html",{"msg":msg})
######################################################################
#                           USER
######################################################################
def user(request):
    """ 
        The function to register company
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """

    msg=""
    email=request.session["email"]
    if(request.POST):
        name=request.POST["txtName"]
        address=request.POST["txtAddress"]
        email=request.POST["txtEmail"]
        phone=request.POST["txtContact"]
        pwd=request.POST["txtPassword"]
   

        s="select count(*) from tbllogin where username='"+email+"'"
        c.execute(s)
        i=c.fetchone()
        if(i[0]>0):
            msg="Email already registered"
        else:
            s="insert into tbluser (uName,uContact,uEmail,uAddress) values('"+name+"','"+phone+"','"+email+"','"+address+"')"
            try:
                c.execute(s)
                db.commit()
            except:
                msg=s
            else:
                s="insert into tbllogin (username,password,utype,status) values('"+email+"','"+pwd+"','user','1')"
                try:
                    c.execute(s)
                    db.commit()
                except:
                    msg="Sorry login process error"
                else:
                    msg="Registered successfully."
    
    return render(request,"user.html",{"msg":msg})
######################################################################
#                                                                    #
#                                                                    #
#                           ADMIN                                    #
#                                                                    #
#                                                                    #
######################################################################
######################################################################
#                           LOAD ADMIN PAGE
######################################################################
def adminhome(request):
    """ 
        The function to load admin home page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    return render(request,"adminhome.html")
######################################################################
#                           LOAD ADMIN PAGE
######################################################################
def adminuser(request):
    """ 
        The function to load admin home page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    s="select * from tbluser where uEmail in(select username from tbllogin where status='1')"
    c.execute(s)
    data=c.fetchall()
    return render(request,"adminuser.html",{"data":data})
######################################################################
#                           LOAD ADMIN PAGE
######################################################################
def admincompany(request):
    """ 
        The function to load admin home page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    s="select * from tblcompany where cEmail in(select username from tbllogin where status='0')"
    c.execute(s)
    data=c.fetchall()
    s="select * from tblcompany where cEmail in(select username from tbllogin where status='1')"
    c.execute(s)
    data1=c.fetchall()
    return render(request,"admincompany.html",{"data":data,"data1":data1})
######################################################################
#                          ADMIN APPROVE USERS
######################################################################
def adminupdateuser(request):
    """ 
        The function to approve users
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    email=request.GET.get("id")
    status=request.GET.get("status")
    s="update tbllogin set status='"+status+"' where username='"+email+"'"
    c.execute(s)
    db.commit()
    return HttpResponseRedirect("/admincompany")
######################################################################
#                                                                    #
#                                                                    #
#                           MUSIC COMPANY                            #
#                                                                    #
#                                                                    #
######################################################################
######################################################################
#                           LOAD COMPANY PAGE
######################################################################
def companyhome(request):
    """ 
        The function to load company home page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    msg=""
    email=request.session["email"]
    if(request.POST):
        name=request.POST["txtName"]
        address=request.POST["txtAddress"]
        email=request.POST["txtEmail"]
        phone=request.POST["txtContact"]
        licens=request.POST["txtLicense"]
        s="update tblcompany set cName='"+name+"',cContact='"+phone+"',cAddress='"+address+"',cLicense='"+licens+"' where cEmail='"+email+"'"
        try:
            c.execute(s)
            db.commit()
        except:
            msg=s
        else:
            msg="Updation successfull"
    s="select * from tblcompany where cEmail='"+email+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"companyhome.html",{"msg":msg,"data":data}) 
######################################################################
#                           COMPANY MUSIC
######################################################################
def companymusic(request):
    """ 
        The function to load company music page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    msg=""
    email=request.session["email"]
    if(request.POST):
        name=request.POST["txtName"]
        film=request.POST["txtFilm"]
        duration=request.POST["txtDuration"]
        language=request.POST["txtLanguage"]
        release=request.POST["txtRelease"]
        album=request.POST["txtAlbum"]
        singer=request.POST["txtSinger"]
        composer=request.POST["txtComposer"]
        lyricist=request.POST["txtLyricist"]

        img=request.FILES["txtFile"]
        fs=FileSystemStorage()
        filename=fs.save(img.name,img)
        uploaded_file_url=fs.url(filename)

        s="insert into tblsongs(sName,film,duration,language,releasedate,album,singer,composer,lyricist,path,cName,status) values('"+name+"','"+film+"','"+duration+"','"+language+"','"+release+"','"+album+"','"+singer+"','"+composer+"','"+lyricist+"','"+uploaded_file_url+"','"+email+"','1')"
        try:
            c.execute(s)
            db.commit()
        except:
            msg="Sorry some error occured"
        else:
            msg="Updation successfull"
    
    return render(request,"companymusic.html",{"msg":msg}) 
######################################################################
#                           COMPANY MUSICs
######################################################################
def companysongs(request):
    """ 
        The function to load company music page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    email=request.session["email"]
    s="select * from tblsongs where status='1' and cName='"+email+"'"
    c.execute(s)
    data=c.fetchall()
    
    return render(request,"companysongs.html",{"data":data}) 
######################################################################
#                           COMPANY VIEW MORE
######################################################################
def companyviewsong(request):
    """ 
        The function to load company music page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    sid=request.GET.get("id")
    s="select * from tblsongs where sId='"+sid+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"companyviewsong.html",{"data":data}) 
######################################################################
#                   COMPANY VIEW LYRICS REQUEST
######################################################################
def companyviewlyricsrequest(request):
    """ 
        The function to load lyrics request 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    email=request.session["email"]
    s="select * from tblsongs where sId in (select sId from tbllyrics where status='0') and cName='"+email+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"companyviewlyricsrequest.html",{"data":data}) 
######################################################################
#                   COMPANY VIEW LYRICS
######################################################################
def companyviewlyrics(request):
    """ 
        The function to load lyrics request 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    sid=request.GET.get("id")
    s="select lId,lyrics from tbllyrics where sId='"+str(sid)+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"companyviewlyrics.html",{"data":data})
######################################################################
#                   COMPANY UPDATE LYRICS
######################################################################
def companyupdatelyrics(request):
    """ 
        The function to update lyrics request 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    sid=request.GET.get("id")
    status=request.GET.get("status")
    s="update tbllyrics set status='"+status+"' where lId='"+sid+"'"
    c.execute(s)
    db.commit()
    return HttpResponseRedirect("/companyviewlyricsrequest")
######################################################################
#                   COMPANY VIEW NOTES REQUEST
######################################################################
def companyviewnotesrequest(request):
    """ 
        The function to load notes request 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    email=request.session["email"]
    s="select * from tblsongs where sId in (select sId from tblnotes where status='0') and cName='"+email+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"companyviewnotesrequest.html",{"data":data}) 
######################################################################
#                   COMPANY VIEW NOTES
######################################################################
def companyviewnotes(request):
    """ 
        The function to load notes request 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    sid=request.GET.get("id")
    s="select nId,notes from tblnotes where sId='"+str(sid)+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"companyviewnotes.html",{"data":data})
######################################################################
#                   COMPANY UPDATE NOTES
######################################################################
def companyupdatenotes(request):
    """ 
        The function to update notes request 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    sid=request.GET.get("id")
    status=request.GET.get("status")
    s="update tblnotes set status='"+status+"' where nId='"+sid+"'"
    c.execute(s)
    db.commit()
    return HttpResponseRedirect("/companyviewnotesrequest")
######################################################################
#                                                                    #
#                                                                    #
#                           USER                                     #
#                                                                    #
#                                                                    #
######################################################################
######################################################################
#                           LOAD USER PAGE
######################################################################
def userhome(request):
    """ 
        The function to load user home page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    msg=""
    email=request.session["email"]
    if(request.POST):
        name=request.POST["txtName"]
        address=request.POST["txtAddress"]
        email=request.POST["txtEmail"]
        phone=request.POST["txtContact"]
        
        s="update tbluser set uName='"+name+"',uContact='"+phone+"',uAddress='"+address+"' where uEmail='"+email+"'"
        try:
            c.execute(s)
            db.commit()
        except:
            msg=s
        else:
            msg="Updation successfull"
    s="select * from tbluser where uEmail='"+email+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"userhome.html",{"msg":msg,"data":data}) 
######################################################################
#                           USER MUSIC
######################################################################
def usermusic(request):
    """ 
        The function to load company music page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    if(request.POST):
        song=request.POST["txtSearch"]
        return HttpResponseRedirect("usersearchresult?song="+song)
    s="select * from tblsongs order by sId desc limit 10 "
    c.execute(s)
    data=c.fetchall()
    return render(request,"usermusic.html",{"data":data}) 
######################################################################
#                           USER VIEW MORE
######################################################################
def userviewsong(request):
    """ 
        The function to load company music page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    sid=request.GET.get("id")
    s="select * from tblsongs where sId='"+str(sid)+"'"
    c.execute(s)
    data=c.fetchall()
    s="select * from tbllyrics where sId='"+str(sid)+"' and status='1'"
    c.execute(s)
    lyrics=c.fetchall()
    s="select * from tblnotes where sId='"+str(sid)+"' and status='1'"
    c.execute(s)
    notes=c.fetchall()
    return render(request,"userviewsong.html",{"data":data,"lyrics":lyrics,"notes":notes,"sid":sid}) 
######################################################################
#                           USER SEARCH RESULT
######################################################################
def usersearchresult(request):
    """ 
        The function to load company music page of the project. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    song=request.GET.get("song")
    song="%"+song+"%"
    s="select * from tblsongs where sName like '"+song+"'"
    c.execute(s)
    data=c.fetchall()
    return render(request,"usersearchresult.html",{"data":data})  
######################################################################
#                           USER ADD LYRICS
######################################################################
def useraddlyrics(request):
    """ 
        The function to add lyrics. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    msg=""
    sid=request.GET.get("id")
    s="select count(*) from tbllyrics where sId='"+str(sid)+"'"
    c.execute(s)
    i=c.fetchone()
    if(i[0]>0):
        return HttpResponseRedirect("/userviewsong?id="+sid)
    if(request.POST):
        lyrics=request.POST["txtLyrics"]
        s="insert into tbllyrics (sId,lyrics,status) values('"+sid+"','"+lyrics+"','0')"
        try:
            c.execute(s)
            db.commit()
        except:
            msg="Sorry some error occured"
        else:
            msg="Lyrics added. Wait for approval"
    return render(request,"useraddlyrics.html",{"msg":msg}) 
######################################################################
#                           USER ADD NOTES
######################################################################
def useraddnotes(request):
    """ 
        The function to add notes. 
        -----------------------------------------------
        Parameters: 
            HTTP request 
          
        Returns: 
            html page
    """
    msg=""
    sid=request.GET.get("id")
    s="select count(*) from tblnotes where sId='"+str(sid)+"'"
    c.execute(s)
    i=c.fetchone()
    if(i[0]>0):
        return HttpResponseRedirect("/userviewsong?id="+sid)
    if(request.POST):
        lyrics=request.POST["txtLyrics"]
        s="insert into tblnotes (sId,notes,status) values('"+sid+"','"+lyrics+"','0')"
        try:
            c.execute(s)
            db.commit()
        except:
            msg="Sorry some error occured"
        else:
            msg="Lyrics added. Wait for approval"
    return render(request,"useraddnotes.html",{"msg":msg}) 