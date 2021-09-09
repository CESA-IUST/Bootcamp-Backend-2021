class register(APIView):
    @csrf_exempt
    def post(self, request):
        username_=request.POST["username"]
        email_=request.POST["email"]
        password_=request.POST["password"]
        password2_=request.POST["confirmpassword"]

        if password2_!=password_:
            return JsonResponse({"status":"fail!","message":"password not equal"})

        same=User.objects.filter(username=username_)

        if  same:
            return JsonResponse({"status":"fail!","message":"username repeated!"})

        new_user=User(username=username_,email=email_)
        new_user.set_password(password_)


        new_user.save()
        token = Token.objects.create(user=new_user)
        auth.login(request, new_user,backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({"status":"True","message":f"welcome {username_} dear!", 'token':f'Token {token.key}'})

@csrf_exempt
@api_view(('POST'))
def ArchivePost(request):

    if(request.user.is_anonymous):
        return HttpResponse("you have to login first!",status=403)

    if request.method == 'POST':
        postId = request.POST["PostId"]
        collection = request.POST["Collection"]
        
        if(archivePostClass.objects.filter(UserName=request.user).filter(PostId=postId).filter(Collection=collection).count() == 0):
            if (collection == ""):
                collection = "Main"
            Obj = archivePostClass(PostId = postId,UserName=request.user,Collection = collection)
            Obj.save()
            return HttpResponse("POST was successful!",status=200)
        elif(True):
            return HttpResponse("You cant Save a post,Twice!",status=400)