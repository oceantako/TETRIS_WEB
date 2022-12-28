from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from .models import User,TetrisResult
from django.db.models import Max
from .forms import LoginForm
from django.template import loader
from django.utils.timezone import make_aware
import datetime

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


#テトリス結果登録処理
def tetris_result_submit(request):

    name = request.POST.get('username')
    blockcount = int(request.POST.get('blockcounter'))

    # ユーザ情報を取得
    UserInf = User.objects.get(name=name)

    #直近の月曜日0時0分を取得
    dt1 = make_aware(datetime.datetime.now())
    dayweek = dt1.weekday()
    dt2 = dt1 + datetime.timedelta(days=-dayweek)
    Monday = dt2.replace(hour=0, minute=0, second=0, microsecond=0)

    #今種の最大落下ブロック数を取得
    weekly_max = UserInf.tetrisresult_set.filter(date__gte=Monday).order_by('blockcount').reverse().first()

    #今週登録されたデータが存在する場合 = / 今週の最高記録の場合-最高記録をupdateする / 今週の最高記録でない場合-登録しない /
    if weekly_max:
        weekly_max_blocks = weekly_max.blockcount
        
        if blockcount > weekly_max_blocks:
            weekly_max.blockcount = blockcount
            weekly_max.date = make_aware(datetime.datetime.now())
            weekly_max.save()
            result_json = {'result': 'weekly_max'}
        else:
            result_json = {'result': 'notsubmit'}
    
    #今週登録されたデータが存在しない場合 = 登録する
    else:
        UserInf.tetrisresult_set.create(
                name = name,
                blockcount = blockcount,
                date = datetime.datetime.now()
            )
        result_json = {'result': 'weekly_first'} 
    
    return JsonResponse(result_json)


#WEEKLY RANKING出力処理
def weekly_ranking(request):
    name = request.POST.get('user_name')

    #直近の月曜日0時0分を取得
    dt1 = make_aware(datetime.datetime.now())
    dayweek = dt1.weekday()
    dt2 = dt1 + datetime.timedelta(days=-dayweek)
    Monday = dt2.replace(hour=0, minute=0, second=0, microsecond=0)

    # weeklyrankingを取得
    weekly_ranking = User.objects.prefetch_related(
                        ).filter(
                            tetrisresult__date__gte=Monday
                        ).values("name").annotate(
                            weekly_MAX=Max('tetrisresult__blockcount')
                        ).order_by(
                            'weekly_MAX'
                        ).reverse()


weekly_ranking = User.objects.prefetch_related(
                        ).filter(
                            tetrisresult__date__gte=Monday
                        ).values("name").annotate(
                            weekly_MAX=Max('tetrisresult__blockcount')
                        ).values("weekly_MAX","name")


TetrisResult.objects.filter(date__gte=Monday, , blockcount=sl_blockcount)


    # 画面用listの作成
    screen_list = []

    # weeklyランキング用の日付を取得⇒画面用listに格納
    for ranking_item in weekly_ranking:
        sl_name = ranking_item["name"]
        sl_blockcount = ranking_item["weekly_MAX"]

        weekly_max_col = TetrisResult.objects.filter(date__gte=Monday, name__name=sl_name, blockcount=sl_blockcount).first()
        weekly_max_date = weekly_max_col.date
        
        date_str = weekly_max_date.strftime('%Y年%m月%d日 %a')

        ranking_item["date"] = date_str
        screen_list.append(ranking_item)


    return HttpResponse("good")



def monthly_ranking(request):
    return HttpResponse("good")

def all_season_ranking(request):
    return HttpResponse("good")



def submittest(request):
    name = "tacook"
    blockcount = 73
    date = None

    UserInf = User.objects.get(name=name)
    UserInf.tetrisresult_set.create(
        name = name,
        blockcount = blockcount,
        date = datetime.datetime.now()
    )

    return HttpResponse("good")



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
