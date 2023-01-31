from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
from .models import User, WeeklyRanking, MonthlyRanking, AllSeasonRanking, RankSelecter
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

    #ランキングテーブル登録処理
    result_weekly = weekly_ranking_submit(name, UserInf, blockcount)
    result_monthly = monthly_ranking_submit(name, UserInf, blockcount)
    result_allseason = allseason_ranking_submit(name, UserInf, blockcount)

    #画面に返す値を格納
    result_json = {'result': result_weekly}

    if result_monthly != "not_submit":
        result_json = {'result': result_monthly}
    
    if result_allseason != "not_submit":
        result_json = {'result': result_allseason}
    
    return JsonResponse(result_json)


#RANKING出力処理
def ranking(request):
    name = request.POST.get('name')
    ranking_type = request.POST.get('ranking_type')

    #本日日付を取得
    dt1 = make_aware(datetime.datetime.now())

    #直近の月曜日0時0分を取得
    dayweek = dt1.weekday()
    dt2 = dt1 + datetime.timedelta(days=-dayweek)
    Monday = dt2.replace(hour=0, minute=0, second=0, microsecond=0)

    #今月の1日の日付を取得
    ThisMonthDay1 = dt1.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    #rankingを取得
    if ranking_type == 'weekly':
        ranking_List = WeeklyRanking.objects.filter(date__gte=Monday).order_by('blockcount').reverse()
    elif ranking_type == 'monthly':
        ranking_List = MonthlyRanking.objects.filter(date__gte=ThisMonthDay1).order_by('blockcount').reverse()
    elif ranking_type == 'allseason':
        ranking_List = AllSeasonRanking.objects.all().order_by('blockcount').reverse()
    
    #ランク決定用リストを作成
    rankselect = RankSelecter.objects.all()

    #画面用listの作成
    screen_list = []
    
    #画面用listに値を格納　⇒　名前、ブロック数、獲得ランク、称号、日付
    for ranking_item in ranking_List:
        item_dict = {}
        item_dict["name"] = ranking_item.user.name
        item_dict["blockcount"] = ranking_item.blockcount
        for rank_item in rankselect:
            if ranking_item.blockcount < rank_item.underblocks:
                 item_dict["rank"] = rank_item.rank
                 item_dict["syougou"] = rank_item.syougou
                 break
        item_dict["date"] = ranking_item.date.strftime('%Y年%m月%d日 %a')

        screen_list.append(item_dict)
                
    return render(request, 'tetris/ranking.html', {'screen_list': screen_list, 'name': name, 'ranking_kind': ranking_type})

#ランキング画面からの戻り処理
def redisp_tetris(request):
  
    #画面項目を変数へ格納
    name = request.POST['name']

    # DB検索
    UserInf = User.objects.filter(name=name).first()

    # テトリス画面へ
    return render(request, 'tetris/tetris.html', {'userInf': UserInf})


#遊び方表示
def HowToEnjoy(request):
  
    #画面項目を変数へ格納
    name = request.POST['name']

    # テトリス画面へ
    return render(request, 'tetris/HowToEnjoy.html', {'name': name})

#お知らせ表示
def Osirase(request):
  
    #画面項目を変数へ格納
    name = request.POST['name']

    # テトリス画面へ
    return render(request, 'tetris/Osirase.html', {'name': name})


def weekly_ranking_submit(name, UserInf, blockcount):

    #直近の月曜日0時0分を取得
    dt1 = make_aware(datetime.datetime.now())
    dayweek = dt1.weekday()
    dt2 = dt1 + datetime.timedelta(days=-dayweek)
    Monday = dt2.replace(hour=0, minute=0, second=0, microsecond=0)

    #今週の最大落下ブロック数を取得
    weekly_max = UserInf.weeklyranking_set.filter(date__gte=Monday).order_by('blockcount').reverse().first()

    #今週登録されたデータが存在する場合 = / 今週の最高記録の場合-最高記録をupdateする / 今週の最高記録でない場合-登録しない /
    if weekly_max:
        weekly_max_blocks = weekly_max.blockcount
        
        if blockcount > weekly_max_blocks:
            weekly_max.blockcount = blockcount
            weekly_max.date = make_aware(datetime.datetime.now())
            weekly_max.save()
            result_text = "weekly_max"
        else:
            result_text = "not_submit"
    
    #今週登録されたデータが存在しない場合 = 登録する
    else:
        UserInf.weeklyranking_set.create(
                user = name,
                blockcount = blockcount,
                date = datetime.datetime.now()
            )
        result_text = "weekly_fs"
    
    return result_text


#monthlyランキング登録処理
def monthly_ranking_submit(name, UserInf, blockcount):

    #今月の1日の日付を取得
    dt1 = make_aware(datetime.datetime.now())
    ThisMonthDay1 = dt1.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    #今月の最大落下ブロック数を取得
    monthly_max = UserInf.monthlyranking_set.filter(date__gte=ThisMonthDay1).order_by('blockcount').reverse().first()

    #今月登録されたデータが存在する場合 = / 今月の最高記録の場合-最高記録をupdateする / 今月の最高記録でない場合-登録しない /
    if monthly_max:
        monthly_max_blocks = monthly_max.blockcount
        
        if blockcount > monthly_max_blocks:
            monthly_max.blockcount = blockcount
            monthly_max.date = make_aware(datetime.datetime.now())
            monthly_max.save()
            result_text = "monthly_max"
        else:
            result_text = "not_submit"
    
    #今月登録されたデータが存在しない場合 = 登録する
    else:
        UserInf.monthlyranking_set.create(
                user = name,
                blockcount = blockcount,
                date = datetime.datetime.now()
            )
        result_text = "monthly_fs"
    
    return result_text


#AllSeasonランキング登録処理
def allseason_ranking_submit(name, UserInf, blockcount):

    #オールシーズンの最大落下ブロック数を取得
    all_season_max = UserInf.allseasonranking_set.all().order_by('blockcount').reverse().first()

    #登録されたデータが存在する場合 = / 最高記録の場合-最高記録をupdateする / 最高記録でない場合-登録しない /
    if all_season_max:
        all_season_max_blocks = all_season_max.blockcount
        
        if blockcount > all_season_max_blocks:
            all_season_max.blockcount = blockcount
            all_season_max.date = make_aware(datetime.datetime.now())
            all_season_max.save()
            result_text = "allseason_max"
        else:
            result_text = "not_submit"
    
    #登録されたデータが存在しない場合 = 登録する
    else:
        UserInf.allseasonranking_set.create(
                user = name,
                blockcount = blockcount,
                date = datetime.datetime.now()
            )
        result_text = "allseason_fs"
    
    return result_text