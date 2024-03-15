from django.db import models

class Department(models.Model):
    # 部门表
    # 自动创建id，为主键，自增
    title = models.CharField(verbose_name="标题", max_length=32)
    #显示部门名称而不是部门Department object(3)
    def __str__(self):
        return self.title
# Create your models here.
class USerInfo(models.Model):
    # verbose_name为注释内容,可写可不写
    name = models.CharField(verbose_name="姓名", max_length=16)
    passwd = models.CharField(verbose_name="密码111", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    # 账户长度为10，小数点有两位
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    creat_time = models.DateTimeField(verbose_name="入职时间")
    #下面的时间格式没有时分秒，一般用作入职时间
    #creat_time = models.DateField(verbose_name="入职时间")
    # 给部门ID加上约束，员工所属部门ID只能是已经存在的,to表示要与那个表关联，to_field表示与表中的哪一列关联，生成的列名字是depart_id
    # 一般用ID相关联，大公司有时候用名字比如销售部门，运维部门
    # 级联删除---  on_delete=models.CASCADE 表示部门被删除，所属该部门的员工也会被删除，叫级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

    # 置空---  null=True,blank=True,on_delete=models.SET_NULL 表示部门删除后，员工所属部门号为null
    # depart=models.ForeignKey(to="Department",to_field="id",null=True,blank=True,on_delete=models.SET_NULL)

    # 设置性别,属于django的约束
    gender_choice = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)

#手机号表格
class PhoneTable(models.Model):
    """ 靓号表"""
    #id = models.IntegerField(verbose_name="ID", primary_key=True)
    #CharField后面一定要跟max_length,存储成charfiled方便后面正则查找
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    #decimal_places=2 小数点后两位
    #null=True, blank=True 允许为空
    price = models.DecimalField(verbose_name="价格", max_digits=5, decimal_places=2)
    level_choice=(
        (1,"高级"),
        (2,"普通")
    )
    leval=models.SmallIntegerField(verbose_name="等级", choices=level_choice,default=2)
    status_choice=(
        (1,"空闲"),
        (2,"售出")
    )
    status=models.SmallIntegerField(verbose_name="状态", choices=status_choice,default=1)
