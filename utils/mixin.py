'''==================================================
@IDE: PyCharm
@Time : 2020/12/14 10:32
@Author : wyp
@File : mixin.py
=================================================='''
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的as_view
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

