from django.db import models


# Create your models here.

class Department(models.Model):
    """部门表"""

    title = models.CharField(verbose_name="标题", max_length=32)

    # 返回部门的数据
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)  # 准确的小数值
    create_time = models.DateTimeField(verbose_name="入职时间")

    # 在django中做约束
    gender_choices = (
        (1,"男"),
        (2,"女")
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 有约束
    # on_delete=models.CASCADE 级联删除   on_delete=models.SET_NULL置空
    depart = models.ForeignKey(verbose_name="部门",to='Department',to_field='id',on_delete=models.SET_NULL,null=True,blank=True)


class PrettyNum(models.Model):
    """英雄联盟 游戏靓号表"""
    mobile = models.CharField(verbose_name="手机号",max_length=11)
    # 想要允许为空 null=True  blank=True
    price = models.IntegerField(verbose_name="价格",default=0)

    level_choices = (
        (1,'黑铁'),
        (2,'青铜'),
        (3,'黄金'),
        (4,'铂金'),
        (5,'钻石'),
        (6,'大师'),
        (7,'王者'),
    )

    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices,default=1)

    status_choices = (
        (1,"已售出"),
        (2,"未使用"),
    )

    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=2)

























































