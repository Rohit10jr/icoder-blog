from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout

# html blog pages
def home(request):
    # return HttpResponse("hi world")
    return render(request, "home/home.html")

def about(request):
    messages.success(request, "this is about page")
    return render(request, "home/about.html")

def contact(request):
   
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']

        if len(name)<2 or len(email)<2 or len(phone)<2 or len(content)<4:
            messages.error(request, "please fill the form correctly")
        else:    
            contact=Contact(name=name, email=email, phone=phone, content=content )
            contact.save()
            messages.success(request, "thank you for your feedback")
    return render(request, "home/contact.html")

def search(request):
    # allposts=Post.objects.all()
    query=request.GET['query']
    if len(query)>150:
        allposts= Post.objects.none()
    else:    
        allpoststitle=Post.objects.filter(title__icontains=query)
        allpostscontent=Post.objects.filter(content__icontains=query)
        allposts = allpoststitle.union(allpostscontent)

    if allposts.count() == 0:
        messages.warning(request, "No search results found, please enter valid keywords")    
    params={'allposts': allposts, 'query': query}
    return render(request, "home/search.html", params)

# authentication apis 
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)>25:
            messages.error(request, " Your user name must be under 25 characters")
            return redirect('home')
        # check for alphanumeric
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        #check for password missmatch
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")
    
def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpass']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
