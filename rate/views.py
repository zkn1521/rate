from statistics import mean

from django.http import JsonResponse
from .models import Module, Professor, ModuleInstance
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def List(request):
    ModuleInstance_list = ModuleInstance.objects.all().values('year', 'semester', 'professor__code', 'Professor2__code',
                                                              'professor__name', 'Professor2__name', 'module__code',
                                                              'module__name', 'Professor2_id', 'professor_id')

    code_list = []
    name_list = []
    year_list = []
    semester_list = []
    pro_list = []
    if ModuleInstance_list.exists():
        for i in ModuleInstance_list:
            code_list.append(i['module__code'])
            name_list.append(i['module__name'])
            year_list.append(i['year'])
            semester_list.append(i['semester'])
            if i['Professor2_id'] is not None:
                pro_list.append(str(i['professor__code'] + ', ' + i['professor__name'] + '\n'
                                    + i['Professor2__code'] + ', ' + i['Professor2__name']))
            else:
                pro_list.append(str(i['professor__code'] + ', ' + i['professor__name']))
        return JsonResponse({
            "code_list": code_list,
            "name_list": name_list,
            "year_list": year_list,
            "semester_list": semester_list,
            "pro_list": pro_list,
        }, status=200, safe=False)
    else:
        return JsonResponse({
            "message": "No Module instance yet ,call admin to add"
        }, status=404)


def Views(request):
    professor_list = (Professor.objects.all().values())
    name_list = []
    pro_id_list = []
    ave_rate = []
    if professor_list.exists():
        for i in professor_list:
            name_list.append(i['name'])
            pro_id_list.append(i['code'])
            ave_rate.append(i['ave_rate'])
        return JsonResponse({
            "name_list": name_list,
            "pro_id_list": pro_id_list,
            "ave_rate": ave_rate
        }, status=200, safe=False)
    else:
        return JsonResponse({
            "message": "No professors yet, call admin to add"
        }, status=404)


def Ave(request, pro_id, module_code):
    ave = []
    i = 0
    p = Professor.objects.filter(code=pro_id)
    mlist = Module.objects.filter(code=module_code)
    # print(mlist)
    # print(p)
    if mlist and p:
        instance = ModuleInstance.objects.filter(module_id=mlist[0].id)
        if instance:
            for ins in instance:
                # print(ins.ave_rate1)
                # print(ins.ave_rate2)
                if ins.professor_id == p[0].id:
                    ave.append(ins.ave_rate1)
                elif ins.Professor2_id == p[0].id:
                    ave.append(ins.ave_rate2)
        else:
            return JsonResponse({
                "message": "please input the right professor_id or module_code"
            }, status=404)
        if not ave:
            return JsonResponse({
                "module": mlist[0].name,
                "professor": p[0].name,
                "message": "The professor does not teach this module instance"
            }, status=203)
        else:
            ave1 = []
            for i in ave:
                if i != 0:
                    ave1.append(i)
            if not ave1:
                return JsonResponse({
                    "module": mlist[0].name,
                    "professor": p[0].name,
                    "message": "Not rated yet"
                }, status=201)
            else:
                return JsonResponse({
                    "module": mlist[0].name,
                    "professor": p[0].name,
                    "avg": round(mean(ave1))
                }, status=200)
    else:
        return JsonResponse({
            "message": "please input the right professor_id or module_code"
        }, status=404)


def rateone(request, pro_id, module_code, year, semester, rate):
    if not request.user.is_authenticated:
        return JsonResponse({
            "message": "please log in first"
        }, status=404)
    else:
        try:
            if not rate.isdigit():
                return JsonResponse({
                    "message": "please input a integer"
                }, status=404)
            rate = int(rate)
            if rate > 5 or rate < 1:
                return JsonResponse({
                    "message": "The rating must be an integer from the range of 1 to 5"
                }, status=404)
            else:
                p = Professor.objects.filter(code=pro_id)
                m = Module.objects.filter(code=module_code)
                if p and m:
                    avg_rate = 0
                    ins = ModuleInstance.objects.filter(module_id=m[0].id, semester=semester, year=year)
                    instance = None
                    if ins.filter(professor_id=p[0].id):
                        instance = ins.filter(professor_id=p[0].id)[0]
                        instance.rate_amount1 = instance.rate_amount1 + 1
                        instance.total_rate1 = instance.total_rate1 + rate
                        instance.ave_rate1 = round(instance.total_rate1 / instance.rate_amount1)
                        instance.save()
                        avg_rate = instance.ave_rate1
                    elif ins.filter(Professor2_id=p[0].id):
                        instance = ins.filter(Professor2_id=p[0].id)[0]
                        instance.rate_amount2 = instance.rate_amount2 + 1
                        instance.total_rate2 = instance.total_rate2 + rate
                        instance.ave_rate2 = round(instance.total_rate2 / instance.rate_amount2)
                        instance.save()
                        avg_rate = instance.ave_rate2
                    professor1 = p[0]
                    professor1.rate_amount = professor1.rate_amount + 1
                    professor1.total_rate = professor1.total_rate + rate
                    professor1.ave_rate = round(professor1.total_rate / professor1.rate_amount)
                    professor1.save()
                    return JsonResponse({
                        "module": m[0].name,
                        "year": year,
                        "semester": semester,
                        "professor": p[0].name,
                        "message": "rate success: ave rate score of the professor in this module instance is:",
                        "avg": avg_rate
                    }, status=200)
                else:
                    return JsonResponse({
                        "message": "no this module instance"
                    }, status=404)
        except ModuleInstance.DoesNotExist:
            return JsonResponse({
                "message": "no this module instance"
            }, status=404)


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")
    u = User.objects.filter(username=username)
    print(u)
    if u:
        return JsonResponse({
            "message": "user already exists"
        }, status=404)
    else:
        instance = User.objects.create_user(username=username, password=password, email=email)
        instance.save()
        return JsonResponse(data={
            "message": "Register Success",
            "username": instance.username,
        }, status=201)


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({
            "message": "Login Success",
            "username": username,
        }, status=201)
    else:
        return JsonResponse({
            "message": "failed, invalid username or password."
        }, status=404)


def logout_user(request):
    print(request.user)
    if not request.user.is_authenticated:
        return JsonResponse({
            "message": "failed, please login first."
        }, status=404)
    else:
        logout(request)
        return JsonResponse({
            "message": "log out succeed."
        }, status=201)
