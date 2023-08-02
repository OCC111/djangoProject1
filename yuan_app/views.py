from django.shortcuts import render, redirect
from yuan_app.models import Department, UserInfo
from django import forms


# Create your views here.

def depart_list(request):
    queryset = Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户post提交的数据
    title = request.POST.get('title')

    # 保存到数据库
    Department.objects.create(title=title)

    # 重定向部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """修改部门"""

    if request.method == "GET":
        # nid = request.GET.get('nid')
        row_object = Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})

    title = request.POST.get("title")

    Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


def user_list(request):
    """用户列表"""
    user_set = UserInfo.objects.all()

    return render(request, 'user_list.html', {'user_set': user_set})


def user_add(request):
    """ 添加用户  原始方法"""
    if request.method == "GET":
        context = {
            'gender_choies': UserInfo.gender_choices,
            'depart_list': Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    name = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加数据到数据库中
    UserInfo.objects.create(
        name=name,
        password=password,
        age=age,
        account=account,
        create_time=ctime,
        gender=gender,
        depart_id=depart_id

    )

    return redirect('/user/list/')


def user_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    Department.objects.filter(id=nid).delete()
    return redirect("/user/list/")


# -==========================================
# model form 案例


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3,label="姓名")
    password = forms.CharField(min_length=8,label="密码")
    age = forms.CharField(min_length=2,label="年龄")
    account = forms.CharField(label="余额")
    create_time = forms.DateTimeField(label="入职时间")

    class Meta:
        model = UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {'form': form})

    # 用户POST提交数据  数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # UserInfo.objects.create()
        form.save()
        return redirect('/user/list/')

    # 校验失败  在页面上显示错误信息
    return render(request, "user_model_form_add.html", {'form': form})

def user_model_form_edit(request):
    pass


