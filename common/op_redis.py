# encoding: utf-8

# python连接redis
import redis

class OpRedis(object):
    # 连接阿里云redis实例下的某个库
    def __init__(self, host, port, password, db):
        password = None if password == '' else password
        # decode_responses=True，写入键值对中的value为str类型，不加这个参数写入的则为字节类型
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=db, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    # 获取账号3.0登录、注册等验证码，value为hash类型
    # 获取账号2.0登录、注册等验证码，value为string类型
    def get_captcha_account(self, account_version, captcha_type, phone_number):
        captcha_value = None
        if account_version == 'v3':
            key_name = 'platform:account:captcha:'+str(captcha_type)+':'+str(phone_number)
            h_key = 'captcha'
            captcha_value = self.r.hget(key_name, h_key)
        elif account_version == 'v2':
            key_name = 'tiger:account:captcha:'+str(captcha_type)+':'+str(phone_number)
            captcha_value = self.r.get(key_name)
        else:
            print('错误的账号版本：{}'.format(account_version))
        return captcha_value

    # 获取产品信息
    # return: List
    def get_product_info(self, pid):
        key_name = 'platform:account:product_info:'+str(pid)
        pid_info = self.r.hmget(key_name, ['id', 'name', 'description'])
        if pid_info[0] != None:
            return pid_info


if __name__ == '__main__':
    op_redis = OpRedis(host='dev.codemao.cn', port=7000, db=1)
    print(op_redis.get_product_info('-8ZfYfLG'))