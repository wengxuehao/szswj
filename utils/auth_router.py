# __author__ : htzs
# __time__   : 19-4-15 上午10:25


class AuthRouter:
    """
    配置数据库读写分离
    """

    def db_for_read(self, model, **hints):
        return 'users'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """是否运行关联操作"""
        return True
