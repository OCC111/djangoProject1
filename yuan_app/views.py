from django.shortcuts import render, redirect
from yuan_app.models import Department, UserInfo, PrettyNum
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from yuan_app.utils.paginstion import Paginstion


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
    # user_set = UserInfo.objects.all()
    # return render(request, 'user_list.html', {'user_set': user_set})

    user_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        user_dict["name__contains"] = search_data

    queryset = UserInfo.objects.filter(**user_dict)
    page_object = Paginstion(request, queryset, page_size=5)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html,  # 页码
    }

    return render(
        request,
        'user_list.html',
        context
    )


# def user_add(request):
#     """ 添加用户  原始方法"""
#     if request.method == "GET":
#         context = {
#             'gender_choies': UserInfo.gender_choices,
#             'depart_list': Department.objects.all()
#         }
#         return render(request, 'user_add.html', context)
#
#     name = request.POST.get('name')
#     password = request.POST.get('password')
#     age = request.POST.get('age')
#     account = request.POST.get('account')
#     ctime = request.POST.get('ctime')
#     gender = request.POST.get('gd')
#     depart_id = request.POST.get('dp')
#
#     # 添加数据到数据库中
#     UserInfo.objects.create(
#         name=name,
#         password=password,
#         age=age,
#         account=account,
#         create_time=ctime,
#         gender=gender,
#         depart_id=depart_id
#
#     )
#
#     return redirect('/user/list/')


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="姓名")
    password = forms.CharField(min_length=8, label="密码")
    age = forms.CharField(min_length=2, label="年龄")
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

        # 钩子方法

    def clean_name(self):

        # self.instance.pk
        # 用户输入的所有的值
        txt_name = self.cleaned_data["name"]
        exists = UserInfo.objects.filter(name=txt_name).exists()
        if exists:
            raise ValidationError("用户已存在")
        # 验证通过  用户输入的值返回
        return txt_name


def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {'form': form})

    # 用户POST提交数据  数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # UserInfo.objects.create()

        # 保存用户输入的值
        form.save()
        return redirect('/user/list/')

    # 校验失败  在页面上显示错误信息
    return render(request, "user_model_form_add.html", {'form': form})


def user_model_form_edit(request, nid):
    """编辑用户"""
    if request.method == "GET":
        # 查询并展示默认的数据
        row_object = UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, "user_model_form_edit.html", {'form': form})
    row_object = UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 保存用户输入的值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_model_form_edit.html', {"form": form})


def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(request):
    """靓号列表"""
    # mob = 13812347894
    # for i in range(100):
    #     mobile = mob + 1
    #     PrettyNum.objects.create(mobile=mobile,price=10,level=2,status=1)

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = PrettyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Paginstion(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html,  # 页码
    }

    return render(
        request,
        'pretty_list.html',
        context
    )


class PrettyModelForm(forms.ModelForm):
    # 验证方式1  正则表达式校验
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$',
                                   "手机号格式错误")]
    )

    class Meta:
        model = PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 钩子方法
    def clean_mobile(self):

        # self.instance.pk
        # 用户输入的所有的值
        txt_mobile = self.cleaned_data["mobile"]
        exists = PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("手机号必须是11位")
        # 验证通过  用户输入的值返回
        return txt_mobile


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # UserInfo.objects.create()

        # 保存用户输入的值
        form.save()
        return redirect('/pretty/list/')

    # 校验失败  在页面上显示错误信息
    return render(request, "pretty_add.html", {'form': form})


class PrettyEditModelForm(forms.ModelForm):
    # 验证方式1  正则表达式校验
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$',
                                   "手机号格式错误")]
    )

    class Meta:
        model = PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 钩子方法
    def clean_mobile(self):

        # self.instance.pk
        # 用户输入的所有的值
        txt_mobile = self.cleaned_data["mobile"]
        # 排除自己以外的 其他手机号是否重复
        exists = PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("手机号必须是11位")
        # 验证通过  用户输入的值返回
        return txt_mobile


def pretty_edit(request, nid):
    """修改靓号"""
    # 查询出默认数据并显示
    row_object = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        # 查询并展示默认的数据
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 保存用户输入的值
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
