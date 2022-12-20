from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import User
from .forms import LoginForm
from django.template import loader

#ログイン処理
def Login(request):

    #GET時/初期画面を返す
    if request.method == 'GET':
        return render(request,'tetris/login.html') 

    #POST時/ログイン処理を行う
    elif request.method == 'POST':
        
        #画面項目を変数へ格納
        name = request.POST['name']
        password = request.POST['password']

        # DB検索
        UserInf = User.objects.filter(name=name).first()

        # DB検索結果チェック
        if not UserInf:
            error_message = "登録されていないユーザ名です。"
            return render(request, 'tetris/login.html', {'error_message': error_message})
        
        if UserInf.password != password:
            error_message = "パスワードが違います。"
            return render(request, 'tetris/login.html', {'error_message': error_message})

        # エラーがない場合：テトリス画面へ
        return render(request, 'tetris/tetris.html', {'userInf': UserInf})


#ユーザ新規登録処理
def UserCreate(request):

    #GET時/初期画面を返す
    if request.method == 'GET':
        return render(request,'tetris/UserCreate.html') 

    #POST時/ユーザ登録処理を行う
    elif request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            error_message = "パスワードを正しく入力してください。"
            return render(request, 'tetris/UserCreate.html', {'error_message': error_message})
        
        # DB検索
        ExistUser = User.objects.filter(name=name).first()

        if ExistUser:
            error_message = "すでに登録済みのユーザ名です。別のユーザ名をご使用ください。"
            return render(request, 'tetris/UserCreate.html', {'error_message': error_message})

        # DB登録
        try:
            User.objects.create(name=name, password=password)
        except:
            raise Http404("ERROR")    

        error_message = "ユーザ登録が完了しました。ログインしてください。"
        return render(request, 'tetris/login.html', {'error_message': error_message})

def login2(request, login_name):
    user_list = User.objects.order_by('name')[:5]
    output = ', '.join([q.name for q in user_list])
    return HttpResponse(output)

def login_test(request, login_name):
    user_list = User.objects.order_by('name')[:5]
    template = loader.get_template('tetris/test.html')
    #画面側の変数とview側の変数を紐づける
    context = {
        'User_list': user_list,
    }
    return HttpResponse(template.render(context, request))
    
    #↓これでもOK(かっこいいやり方？)
    #return render(request, 'tetris/test.html', context)

#DBを検索してユーザが登録されていれば、テトリス画面へ
def login_DB(request, login_name):
    try:
        username = User.objects.get(name=login_name)
    except User.DoseNotExist:
        raise Http404("User dose not exist")
    return render(request, 'tetris/tetris.html', {'username': username})

# Create your views here.
