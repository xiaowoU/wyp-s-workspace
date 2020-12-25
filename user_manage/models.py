from django.db import models

# Create your models here.
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from db.base_model import BaseModel
import uuid

class Company(BaseModel):
    # id = models.AutoField(primary_key=True)
    # company_id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(verbose_name='单位名', max_length=64)
    address = models.CharField(verbose_name='地址', max_length=64, null=True, blank=True)
    key_person = models.CharField(verbose_name='关键人物', max_length=64, null=True, blank=True)
    contacts = models.CharField(verbose_name='联系人', max_length=64, null=True, blank=True)
    manager = models.CharField(verbose_name='负责人', max_length=64, null=True, blank=True)
    contract_number = models.CharField(verbose_name='合同编号', max_length=64, null=True, blank=True)

    def __str__(self):  # str才行
        return self.name

    class Meta:
        db_table = 't_company'
        verbose_name = u'单位表'
        verbose_name_plural = verbose_name



# # AUTH_USER_MODEL = 'user_manage.User'  # 在设置中声明
class User(AbstractUser, BaseModel):
    # help_text="xx", validators=[validators.RegexValidator(regex=r"^1111$", message="xxx！")], error_messages={"unique": "已存在！", "required": "非空！"}
    real_name = models.CharField(verbose_name='真实姓名', max_length=64, blank=True, null=True)
    tel = models.CharField(verbose_name='联系电话', max_length=64, blank=True, null=True)
    wechat = models.CharField(verbose_name='微信', max_length=64, blank=True, null=True)
    # mail = models.CharField(verbose_name='邮箱', max_length=64, blank=True, null=True)
    company = models.ForeignKey(Company, verbose_name='所属单位', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True)
# class User(models.Model):
#     username = models.CharField(verbose_name='用户名', max_length=64)
#     real_name = models.CharField(verbose_name='真实姓名', max_length=64, blank=True, null=True)
#     password = models.CharField(verbose_name='密码', max_length=64)
#     limit = models.IntegerField(verbose_name='权限', blank=True, null=True)
#     tel = models.CharField(verbose_name='联系电话', max_length=64, blank=True, null=True)
#     wechat = models.CharField(verbose_name='微信', max_length=64, blank=True, null=True)
#     mail = models.CharField(verbose_name='邮箱', max_length=64, blank=True, null=True)
#     company = models.CharField(verbose_name='所属单位', max_length=128, blank=True, null=True)
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_user'
        verbose_name = u'用户表'
        verbose_name_plural = verbose_name


class Project(BaseModel):
    name = models.CharField(verbose_name='隧道名', max_length=128)
    owner_company = models.CharField(verbose_name='业主单位', max_length=128, null=True, blank=True)
    manage_company = models.CharField(verbose_name='运营单位', max_length=128, null=True, blank=True)
    province = models.CharField(verbose_name='所属省', max_length=32)
    city = models.CharField(verbose_name='所属市', max_length=32)
    district = models.CharField(verbose_name='所属区/县', max_length=32)
    position = models.CharField(verbose_name='位置', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_project'
        verbose_name = u'项目表'
        verbose_name_plural = verbose_name


class OperateCompany(BaseModel):
    manage_company = models.CharField(verbose_name='运营单位', max_length=128)
    superior_company = models.CharField(verbose_name='上级', max_length=128, null=True, blank=True)
    contacts = models.CharField(verbose_name='联系人', max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_operate_company'
        verbose_name = u'运营单位表'
        verbose_name_plural = verbose_name


class Section(BaseModel):
    name = models.CharField(verbose_name='隧道边幅名称', max_length=64)
    mileage = models.CharField(verbose_name='里程', max_length=64)
    project = models.ForeignKey(Project, verbose_name='所属工程', to_field='id', on_delete=models.DO_NOTHING, default='', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_section'
        verbose_name = u'断面表'
        verbose_name_plural = verbose_name


class Device(BaseModel):
    device_name = models.CharField(verbose_name='设备名称', max_length=128, null=True, blank=True)
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    firmware_version = models.CharField(verbose_name='固件版本', max_length=32, null=True, blank=True)
    type = models.IntegerField(verbose_name='设备类型', null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=32, null=True, blank=True)
    ip = models.CharField(verbose_name='逻辑ID', max_length=64, null=True, blank=True)
    mac = models.CharField(verbose_name='MAC地址', max_length=64, blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='所属断面', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True, default='')


    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_device'
        verbose_name = u'设备表'
        verbose_name_plural = verbose_name




class Position(BaseModel):
    # todo: circular arc position
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    position = models.CharField(verbose_name='安装位置', max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_position'
        verbose_name = u'设备位置表'
        verbose_name_plural = verbose_name


class OutLine(BaseModel):
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    angle = models.FloatField(verbose_name='监测角度', max_length=64)
    range = models.FloatField(verbose_name='监测距离', max_length=64)
    turns_flag = models.IntegerField(verbose_name='圈数标志')
    times = models.IntegerField(verbose_name='次数编号')
    timestamp = models.DateTimeField(verbose_name='测量的时间戳')
    section = models.ForeignKey(Section, verbose_name='所属断面', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_outline'
        verbose_name = u'轮廓记录表'
        verbose_name_plural = verbose_name
        app_label = 'data_display'


class Result(BaseModel):
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    timestamp = models.DateTimeField(verbose_name='测量的时间戳')
    convergence = models.FloatField(verbose_name='收敛值', max_length=64)
    sedimentation = models.FloatField(verbose_name='沉降值', max_length=64)
    section = models.ForeignKey(Section, verbose_name='所属断面', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_result'
        verbose_name = u'数据处理结果表'
        verbose_name_plural = verbose_name
        app_label = 'data_display'

class Param(BaseModel):
    device_sn = models.CharField(verbose_name='设备编号', max_length=128)
    scan_resolution = models.FloatField(verbose_name='扫面分辨率', max_length=64)
    start_angle = models.FloatField(verbose_name='起始角度', max_length=64)
    end_angle = models.FloatField(verbose_name='终止角度', max_length=64)
    re_times = models.IntegerField(verbose_name='单点重复测量次数')
    turns_flag = models.IntegerField(verbose_name='圈数标志')
    cycle = models.FloatField(verbose_name='采集周期', max_length=64)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_param'
        verbose_name = u'设置参数表'
        verbose_name_plural = verbose_name
        app_label = 'test_install'



class Warning(BaseModel):
    name = models.CharField(verbose_name='预警名', max_length=128)
    # Ⅳ级（一般）、Ⅲ级（较重）、Ⅱ级（严重）、Ⅰ级（特别严重）
    level = models.IntegerField(verbose_name='预警级别', choices=[
                                                                (4, 'Ⅳ级：一般'),
                                                                (3, 'Ⅲ级：较重'),
                                                                (2, 'Ⅱ级：严重'),
                                                                (1, 'Ⅰ级：特别严重'),
                                                            ], default=4)
    notify_obj = models.CharField(verbose_name='通知对象', max_length=128)
    desc = models.CharField(verbose_name='预警信息描述', max_length=256)
    project = models.ForeignKey(Project, verbose_name='所属工程', to_field='id', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_warning'
        verbose_name = u'预警信息表'
        verbose_name_plural = verbose_name
        app_label = 'warning_manage'









class SectionRefPosition(BaseModel):
    section_id = models.IntegerField(verbose_name='断面id,t_section表的id')
    position_id = models.IntegerField(verbose_name='设备位置id,position表的id')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 't_section_ref_position'
        verbose_name = u'断面&位置关系表'
        verbose_name_plural = verbose_name

