from urllib import request
from app01 import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from datetime import datetime
from app01 import models
from django import forms
from app01.models import Department, USerInfo
from django.core.validators import RegexValidator


# Create your views here.
def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()
    return render(request, "depart_list.html", {"queryset": queryset})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, "depart_add.html")
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_del(request):
    # 获取id
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


def user_list(request):
    """用户管理"""
    # 获取所有用户信息
    queryset = models.USerInfo.objects.all()
    # for obj in queryset:
    #     print(obj.name, obj.account, obj.creat_time, obj.depart_id, obj.depart.title)
    return render(request, "user_list.html", {"queryset": queryset})


def user_add(request):
    if request.method == "GET":
        context = {
            "gender_choice": models.USerInfo.gender_choice,
            "depart_list": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    name = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    count = request.POST.get("count")
    time = request.POST.get("time")
    sex = request.POST.get("sex")
    bm = request.POST.get("bm")
    models.USerInfo.objects.create(
        name=name,
        passwd=pwd,
        age=age,
        account=count,
        creat_time=time,
        gender=sex,
        depart_id=bm
    )
    return redirect("/user/list/")


class UserMOdelFrom(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.USerInfo
        fields = ["name", "passwd", "age", "account", "creat_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": "哈哈哈"}


def user_model_from_add(request):
    if request.method == "GET":
        form = UserMOdelFrom()
        return render(request, "user_model_from_add.html", {"form": form})
    # 数据校验
    form = UserMOdelFrom(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_model_from_add.html", {"form": form})


def user_edit(request, nid):
    """ 编辑用户信息，使用modeform来做"""
    # 更新信息而不是新建一个信息，get和post都可以用，代表当前修改用户的id
    row_object = models.USerInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 添加默认信息,modefrom把获取的值默认显示出来
        form = UserMOdelFrom(instance=row_object)
        return render(request, "user_edit.html", {"form": form, "nid": nid})
    form = UserMOdelFrom(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存用户输入的数据
        form.save()
        return redirect('/user/list/')
    return render(request, "user_edit.html", {"form": form, "nid": nid})


def user_del(request, nid):
    models.USerInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


class PhoneModelForm(forms.ModelForm):
    # 验证一：正则表达式
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^199\d{8}$', '数字必须以199开头且为11为数字')]
    # )
    class Meta:
        model = models.PhoneTable
        # 指定获取字段
        fields = ('mobile', 'price', 'status', 'leval')
        # 获取所有
        # fields = "__all__"
        # 排除字段
        # exclude = ['phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    # 钩子方法，定义函数clean_字段名，导入RegexValidator模块
    def clean_mobile(self):
        txt_phone = self.cleaned_data['mobile']
        # 手机号不能一样，新添加时找数据库中的手机号，编辑自己时，手机号可以不用修改也能提交,exclude排除自己
        exitsts = models.PhoneTable.objects.exclude(id=self.instance.pk).filter(mobile=txt_phone).exists()
        if exitsts:
            raise ValidationError("手机号存在")
        if len(txt_phone) != 11:
            raise ValidationError("格式错误")
        return txt_phone


def phone_list(request):
    # for i in range(17):
    #    models.PhoneTable.objects.create(mobile=17613882208, price=100,leval=1,status=1)
    # for i in range(200):
    #     models.PhoneTable.objects.filter(leval=1).delete()
    # from app01 import models
    # queryset = models.PhoneTable.objects.all()
    # q1=models.PhoneTable.objects.filter(mobile='19912113111',id=8)
    # print(q1)
    # q2={"mobile":"19912113111","id":"8"}
    # q3=models.PhoneTable.objects.filter(**q2)
    # print(q3)
    # q4={}
    # q5=models.PhoneTable.objects.filter(**q4)
    # print(q5)
    # 从 GET 请求参数中获取名为 ‘page’ 的参数，如果没有提供，默认为1，并将其转换为整数类型。这个参数表示用户请求的页码。
    page = int(request.GET.get('page', 1))
    # 计算查询的起始索引和结束索引，用于分页查询数据
    start = int((page - 1) * 10)
    end = int(page * 10)
    page_size = 10
    # 从 GET 请求参数中获取名为 ‘q’ 的参数，如果没有提供，默认为空字符串。这个参数通常用于用户输入的搜索关键词。
    value = request.GET.get('q', "")
    na = {}
    if value:
        na["mobile__contains"] = value
    page_list = []
    # 根据查询条件统计符合条件的数据总数。
    count = models.PhoneTable.objects.filter(**na).order_by('-leval').count()
    # 根据数据总数和每页显示数量计算总页数。divmmod除法，求出商和余数
    total_page_count, div = divmod(count, page_size)
    print(total_page_count)
    # 计算出当前页的前5页和后5页
    plus = 3
    if total_page_count <= 2 * plus + 1:
        start_page = 1
        end_page = total_page_count + 1
    else:

        # 处理当前页面小于3时，不应该显示0，-1,最小值ing该是1
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            # 判断当前页+5>总页码时
            if (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus + 1 + 1
                end_page = total_page_count + 1 + 1

            else:
                start_page = page - plus
                end_page = page + plus
    if div:
        total_page_count += 1

    #首页
    page_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 处理上一页
    if page > 1:
        prev = '<li><a href="?page= {}">上一页</a></li>'.format(page - 1)
        page_list.append(prev)
    else:
        prev = '<li><a href="?page= {}">上一页</a></li>'.format(page)
        page_list.append(prev)

    for i in range(start_page, end_page):

        if i == page:
            ele = '<li class="active"><a href="?page= {}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page= {}">{}</a></li>'.format(i, i)

        page_list.append(ele)


    # 处理下一页
    if page < total_page_count:
        prev = '<li><a href="?page= {}">下一页</a></li>'.format(page + 1)
        page_list.append(prev)
    else:
        prev = '<li><a href="?page= {}">下一页</a></li>'.format(page)
        page_list.append(prev)

    page_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))

    page_string = mark_safe("".join(page_list))
    # 首页
    queryset = models.PhoneTable.objects.filter(**na).order_by('-leval')[start:end]
    # Choices are: id, leval, mobile, price, status
    return render(request, 'phone_list.html', {"queryset": queryset, "value": value, "page_string": page_string})


def phone_add(request):
    form = PhoneModelForm()
    if request.method == "GET":
        return render(request, 'phone_add.html', {"form": form})
    form = PhoneModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/phone/list/')
    return render(request, 'phone_add.html', {"form": form})


def phone_edit(request, nid):
    row_object = models.PhoneTable.objects.filter(id=nid).first()
    if request.method == "GET":
        # 添加默认信息,modefrom把获取的值默认显示出来
        form = PhoneModelForm(instance=row_object)
        return render(request, "phone_edit.html", {"form": form, "nid": nid})
    form = PhoneModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存用户输入的数据
        form.save()
        return redirect('/phone/list/')
    return render(request, "phone_edit.html", {"form": form, "nid": nid})


def phone_del(request, nid):
    models.PhoneTable.objects.filter(id=nid).delete()
    return redirect("/phone/list/")
