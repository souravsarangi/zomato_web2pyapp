# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


#db(db.constants.id>0).insert(t="")
def index2():
    
    
    flag=0
    
    
    if request.vars: 
    	j=request.vars.text

    	j=j.lower()
    	query = (db.general_info.fname.lower()==j) | (db.general_info.city.lower()==j)
	message = db(query).select(orderby=db.general_info.Ratings)

	
    	if len(message)>0:
		flag=2
		
	
    	if flag==2:
		flag=0
		
		return dict(message=message)
				

    	else:
				return dict(message="Entry not available")
    else:
	return dict(message="")




def index3():
        return dict()

def get_search2():
        textx=request.vars['x'].lower()
        texty=request.vars['y'].lower()
        rows=db((db.theaters.fname.lower().startswith(textx)) & (db.theaters.city.lower().startswith(texty))).select(orderby=db.theaters.price_range)
        s='{"fname":['
	for row in rows:
	    print row
            s=s+'"'+row['fname']+'"'+","
	s=s[0:-1]+'],'
	
	s=s+'"id":['
	for row in rows:
            s=s+'"'+str(row['id'])+'"'+","
	s=s[0:-1]+'],'
	
	
	s=s+'"city":['
	for row in rows:
            s=s+'"'+row['city']+'"'+","
	s=s[0:-1]+'],'
	
	
	s=s+'"Address":['
	for row in rows:
            s=s+'"'+row['Address']+'"'+","
	s=s[0:-1]+'],'
	
	
	s=s+'"price_range":['
	for row in rows:
            s=s+'"'+row['price_range']+'"'+","
	s=s[0:-1]+']}'
 
        if s=='{"fname":],"id":],"city":],"Address":],"price_range":]}':
            s='{"fname":[],"id":[],"City":[],"Address":[],"price_range":[]}'
        return dict(names=s)
          
def entry2():
	import time
	tyme=time.strftime("%m-%d")
	tyme=tyme.split("-")
	z=request.args[0]
	note=db.theaters(request.args[0])
        form=SQLFORM(db.theaters,note,deletable=True)
        if form.validate():
                if form.deleted:
                        db(db.theaters.id==note.id).delete()
                        redirect(URL(index3))
                else:
                        note.update_record(**dict(form.vars))


	

	message={}
	query=db(db.theaters.id==int(z)).select()
	message["movie_id"]=int(z)
	message["fname"]=query[0].fname
	message["Address"]=query[0].Address
	f=query[0].datei.split(",")
	message["city"]=query[0].city
	message["email"]=query[0].email
	message["price_range"]=query[0].price_range
	z=query[0].show_time.split("-")
	
	c=query[0].movie.split(",")
	
	t=0
	for i in c:
		t+=1

	l=[]
	
	for i in range(t):
		
		q=db(db.movie.id==int(c[i])).select()
		
		
		
		print q[0].fname
		t=t+1
		k=f[i].split(":")
                print "#",k,tyme
		if ( (int(k[0][3:])<=int(tyme[1])) and (int(k[1][3:])>=int(tyme[1]))  and (int(k[0][0:2])==int(k[1][0:2]))and (int(k[0][0:2])==int(tyme[0]))) or ((int(k[0][0:2]))<=int(tyme[0]) and (int(k[1][0:2])>=int(tyme[0]))and (int(k[0][0:2])!=int(k[1][0:2]))): 
			print k	
			l.append(q[0])

	
	return dict(message=message,l=l,z=z,form=form)
	
	

	#return dict(query=query)
	
		
			
		
		    

def user():
    """    
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
""" 
    #mail.send(to=['nikhildaliya@gmail.com'],
     #     subject='hiii',
          # If reply_to is omitted, then mail.settings.sender is used
      #    reply_to='nikhil.daliya@students.iiit.ac.in',
       #   message='Thanks for being part of our Family'
        #  )
   
    return dict(form=auth())


@auth.requires_login()
def create():
	#mail.send(to=[auth.user.email],
        #subject='Thanks@DNS',
        # If reply_to is omitted, then mail.settings.sender is used
        #reply_to='nikhil.daliya@students.iiit.ac.in',
        #message='Thanks for sharing data with our site'
        #)

	
	response.flash='this is create page'
	form=SQLFORM(db.general_info)
	print form.vars
	
	if form.process().accepted:
		my=(db.general_info.id==form.vars.id)
		my=db(my)
		my.update(Ratings=3.00)
		mail.send(to=[auth.user.email],
        	subject='@DNS',
        	# If reply_to is omitted, then mail.settings.sender is used
        	reply_to='nikhildaliya@gmail.com',
        	message='Thanks for sharing data with our site'
        	)

		response.flash='form accepted'
		
		redirect(URL('index'))	
	elif form.errors:
		response.flash='please correct'
	
        return dict(form=form)

@auth.requires_login()
def share_image():
  form=SQLFORM(db.images)
  if form.process().accepted:
      
      my=(db.images.id==form.vars.id)
      my=db(my)
      
      my.update(place_id=request.args[0])
      my.update(person=auth.user.id)
      my.update(per=auth.user.first_name+" "+auth.user.last_name+" , "+auth.user.city)
      my.update(profile_pic=auth.user.image)
      
      response.flash="thanks"
      redirect(URL('entry',args=request.args))
      
  else:
      response.flash="try again"
  return dict(form=form)
  
   
	
@auth.requires_login()
def make_your_comment():
	z=int(request.args[0])
	q=db(db.general_info.id==z).select()
	
        if request.vars:
		  m="abc"
		  import time
		  t=str(time.strftime("%M %H %d %m %Y"))
		  

		  if type(request.vars.comment)==str and request.vars.review!="" and request.vars.comment!="":
		
			db.reviews.insert(place_id=z,person=auth.user.id,commen=request.vars.comment,review=request.vars.review,image=auth.user.image,datei=t)
			response.flash="thanks for your valuable comments"
			mail.send(to=[q[0].Email_id],
        		subject='The comments@DNS',
        	
        		reply_to='nikhil.daliya@students.iiit.ac.in',
        		message=auth.user.first_name+" "+auth.user.last_name+","+auth.user.city+" commented on your restaurent comment:"+request.vars.comment+" and  rating by him is:"+ str(request.vars.review))

                        redirect(URL('entry',args=request.args))
			return dict(Result="Fields are filled properly!!")
		  else:
			return dict(Result="Please complete fields")
	else:
		  return dict(Result="Please complete required fields")	
@auth.requires_login()
def make_comment():
        z=int(request.args[0])
        q=db(db.movie.id==z).select()

        if request.vars:
                  m="abc"
                  import time
                  t=str(time.strftime("%M %H %d %m %Y"))


                  if type(request.vars.comment)==str and request.vars.review!="" and request.vars.comment!="":

                        db.com_movie.insert(place_id=z,person=auth.user.id,commen=request.vars.comment,review=request.vars.review,image=auth.user.image,datei=t)
                        response.flash="thanks for your valuable comments"
                        #mail.send(to=[q[0].Email_id],
                        #subject='The comments@DNS',

                        #reply_to='nikhil.daliya@students.iiit.ac.in',
                        #message=auth.user.first_name+" "+auth.user.last_name+","+auth.user.city+" commented on your restaurent comment:"+request.vars.comment+" and  rating by him is:"+ str(request.vars.review))

                        redirect(URL('movie',args=request.args))
                        return dict(Result="Fields are filled properly!!")
                  else:
                        return dict(Result="Please complete fields")
        else:
                  return dict(Result="Please complete required fields")
def movie():
	z=int(request.args[0])
	import time
	query=db(db.movie.id==z).select()
	c=query[0].duration.split(":")
	print query
	ti=str(time.strftime("%M %H %d %m %Y"))
        ti=ti.split(" ")
	comments=db(db.com_movie.place_id==z).select()
	print comments
	comment_list=[]
	cal=float(query[0].rating)
	no=1
	for j in comments:

                                                comment_dict={}

                                                t=db(db.auth_user.id==int(j.person)).select()


                                                comment_dict["person"]=t[0].first_name+" "+t[0].last_name+","+t[0].city
                                                comment_dict["review"]=j.review
                                                comment_dict["comment"]=j.commen
                                                comment_dict["image"]=j.image
						comment_dict["id"]=j.person
                                                temp=j.review
                                                temp=float(temp)
                                                cal=cal+temp
                                                no=no+1
                                                
                                                



                                                y=str(j.datei)
                                                y=y.split(" ")


                                                if int(ti[4])!=int(y[4]):
                                                        ans=str(int(ti[4])-int(y[4]))+" years ago"
                                                elif int(ti[3])!=int(y[3]):
                                                        ans=str(int(ti[3])-int(y[3]))+" months ago "
                                                elif int(ti[2])!=int(y[2]):
                                                        ans=str(int (ti[2])-int(y[2]))+" days ago"
                                                elif int(ti[1])!=int(y[1]):
                                                        ans=str(int (ti[1])-int(y[1]))+" hours ago"
                                                else:
                                                        ans=str(int(ti[0])-int(y[0]))+ " minutes ago"
                                                comment_dict["time"]=ans
			
						comment_list.append(comment_dict)
			
	cal=cal/no
	comment_list.reverse()


	return dict(query=query,comment_list=comment_list,cal=cal,c=c)


def entry():
	
	
	z=int(request.args[0])
	
	
	comment_list=[]
	message={}
	rows=db(db.general_info.id==z).select()
        comments=db(db.reviews.place_id==z).select()
	import time
	ti=str(time.strftime("%M %H %d %m %Y"))
	ti=ti.split(" ")
	note=db.general_info(request.args[0])
	z=note.id
	form=SQLFORM(db.general_info,note,deletable=True)
	print form.vars,"eheheh"
	if form.validate():
		if form.deleted:
			db(db.general_info.id==note.id).delete()
			q=db(db.reviews.place_id==z)
			q.delete()
			p=db(db.images.place_id==z)
			p.delete()
			redirect(URL(index2))
		else:
		#	note.update(Phone=form.vars.Phone)	
			note.update_record(**dict(form.vars))
			print form.vars,"hehehe"
			redirect(URL('entry',args=request.args[0]))
			
	
	
	
	
	

	
  	
	
	
	
        

        
        
        
        

                     
	
                        
				
	for i in rows:                          
		cal=i.Ratings
		cal=float(cal)
		
		no=1
		no=float(no)        
        	message["Address"]=i.Address
		message["fname"]=i.fname
		message["city"]=i.city
		message["place_id"]=i.id
		message["menu"]=i.menu
		#print message["place_id"]
                pictures=db(db.images.place_id==i.id).select()
                                
				
				
		citi=i.city
		k=i.fname
		k=k.lower()
                message["Email_id"]=i.Email_id
                message["Phone"]=i.Phone
		if i.Pure_Veg==True:
			message["Pure_Veg"]="Pure Veg"
		else:
			message["Pure_Veg"]="Veg + Non-Veg"
		
	for j in comments:
	
                                                comment_dict={}
						
						t=db(db.auth_user.id==int(j.person)).select()
						
						
                                                comment_dict["person"]=t[0].first_name+" "+t[0].last_name+","+t[0].city
                                                comment_dict["review"]=j.review
						comment_dict["comment"]=j.commen						
						comment_dict["image"]=j.image
						temp=j.review
						temp=float(temp)
						cal=cal+temp
						no=no+1
						print("hiii")
						print ti	
						print type(ti)	
                                                #ti=ti.split(" ")
						
						
						
						y=str(j.datei)
						y=y.split(" ")
						
						
						if int(ti[4])!=int(y[4]):
							ans=str(int(ti[4])-int(y[4]))+" years ago"
						elif int(ti[3])!=int(y[3]):
							ans=str(int(ti[3])-int(y[3]))+" months ago "
						elif int(ti[2])!=int(y[2]):
							ans=str(int (ti[2])-int(y[2]))+" days ago"
						elif int(ti[1])!=int(y[1]):
							ans=str(int (ti[1])-int(y[1]))+" hours ago"
						else: 
							ans=str(int(ti[0])-int(y[0]))+ " minutes ago"
                                                comment_dict["time"]=ans

                                                comment_list.append(comment_dict)
	nearby_places=[]
	comment_list.reverse()
	m=citi.lower()
	query=(db.general_info.city.lower()==m)&(db.general_info.id!=z)
        trail=db(query).select()
	
	
		
						

						





  
        cal=cal/no
	cal=int(cal*10)/10.0                  
	message 
	message["Ratings"]=cal
        

                                

	return dict(message=message,comment_list=comment_list,nearby_places=trail,pictures=pictures,form=form)

   

def get_search():
        text=request.vars['p'].lower()
        rows=db((db.general_info.fname.lower().startswith(text)) | (db.general_info.city.lower().startswith(text))).select(orderby=db.general_info.Ratings)
        s='{"fname":['
	for row in rows:
	    print row
            s=s+'"'+row['fname']+'"'+","
	s=s[0:-1]+'],'
	
	s=s+'"id":['
	for row in rows:
            s=s+'"'+str(row['id'])+'"'+","
	s=s[0:-1]+'],'
	
	
	s=s+'"City":['
	for row in rows:
            s=s+'"'+row['city']+'"'+","
	s=s[0:-1]+'],'
	
	
	s=s+'"Address":['
	for row in rows:
            s=s+'"'+row['Address']+'"'+","
	s=s[0:-1]+'],'
	
	s=s+'"Phone":['
	for row in rows:
            s=s+'"'+row['Phone']+'"'+","
	s=s[0:-1]+'],'
	
	s=s+'"Email_id":['
	for row in rows:
	    s=s+'"'+row['Email_id']+'"'+","
	s=s[0:-1]+'],'
	
	
	s=s+'"Ratings":['
	for row in rows:
            s=s+'"'+row['Ratings']+'"'+","
	s=s[0:-1]+']}'
 
        if s=='{"fname":],"id":],"City":],"Address":],"Phone":],"Email_id":],"Ratings":]}':
            s='{"fname":[],"id":[],"City":[],"Address":[],"Phone":[],"Email_id":[],"Ratings":[]}'
        return dict(names=s)
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()



def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
@auth.requires_login()
def my_activity():
	message={}
	message["image"]=auth.user.image

	message["first_name"]=auth.user.first_name
	message["last_name"]=auth.user.last_name
        message["email"]=auth.user.email
        message["address"]=auth.user.address
        
        message["city"]=auth.user.city
        message["phone"]=auth.user.phone
	comment=db(db.reviews.person==auth.user.id).select()
	commen=db(db.com_movie.person==auth.user.id).select()
	comment_list=[]
	commen_list=[]
	for i in comment:
		place=db(db.general_info.id==i.place_id).select()
		
		info={}
		for j in place:
			m=str(j.fname)
			m=m +", "+str(j.city)
			info["place"]=m
			info["place_id"]=j.id
			
		info["commenti"]=i.commen
		info["review"]=i.review
		comment_list.append(info)
	for i in commen:
                place=db(db.movie.id==i.place_id).select()

                info={}
                for j in place:
                        m=str(j.fname)
                        
                        info["place"]=m
                        info["place_id"]=j.id

                info["commenti"]=i.commen
                info["review"]=i.review
                commen_list.append(info)

	photo=[]
	photos=db(db.images.person==auth.user.id).select()
	for i in photos:
		place=db(db.general_info.id==i.place_id).select()
		info={}
		for j in place:
			m=str(j.fname)
			m=m+" , "+str(j.city)
			info["place"]=m
			info["place_id"]=j.id
		info["picture"]=i.picture
		
		photo.append(info)
	note=db.auth_user(auth.user.id)
	form=SQLFORM(db.auth_user,note,deletable=True)
	
        if form.validate():
                if form.deleted:
                        db(db.auth_user.id==note.id).delete()
                        
                        redirect(URL(index))
                else:
                #       note.update(Phone=form.vars.Phone)      
                        note.update_record(**dict(form.vars))
                        redirect(URL('user',args='logout',    vars=dict(_next=URL(args=request.args, vars=request.vars)))) 



	
	
	
		
	
	
	
		
		
		
		
		
		
	return dict(message=auth.user,comment_list=comment_list,commen_list=commen_list,photo=photo,form=form)


#def pict_info():
#	z=request.args[0]
#	query=db(db.theaters.id==z).select()
#	return dict(query)

#def pict_search():
#	z=request.args[0].lower()
#	k=requ
#	query=(db.theaters.movie1.lower()==z|

	
	
def index():
     return dict()
def movie_list():
	query=db(db.movie.id>0).select()
	form=SQLFORM(db.movie)
	print form.vars
	if form.process().accepted:
		redirect('movie_list')
	
	return dict(query=query,form=form)
