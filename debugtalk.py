# encoding: utf-8
import os
from common import read_config
from common.util import *
from common.op_mysql import OpMysql
from common.op_redis import OpRedis

# 读取 environment 配置，用于获取config配置文件
TEST_ENV = os.environ['environment']
# 获取测试域名hosts
TIGER_API_HOST = os.environ['tiger_api_host']
PLATFORM_TIGER_API_HOST = os.environ['platform_tiger_api_host']
# 因为会发送验证码，所以最好是用自己的手机号测试
TEST_PHONE_NUMBER = os.environ['test_phone_number']
# 获取账号2.0的极验配置，用于测试验证码时是否跳过极验
GEETEST_ACCOUNT_V2 = os.environ['geetest_account_v2']

# 获取config配置文件：源用户信息
source_user = read_config.source_user(TEST_ENV)
target_user = read_config.target_user(TEST_ENV)

def source_user_id():
    return source_user.get('id')

def source_user_username():
    return source_user.get('username')

def source_user_email():
    return source_user.get('email')

def source_user_password():
    return source_user.get('password')

# 用户拥有的精灵，不拥有的精灵
def source_user_owned_sprite_id():
    return source_user.get('sprite').get('owned')

def source_user_unown_sprite_id():
    return source_user.get('sprite').get('unown')

# 获取原用户登录token，避免测试用例中多次调用登录态都初始化函数，这里先定义变量
source_user_login_token_v2 = login_token_v2(TIGER_API_HOST, source_user_username(), source_user_password())
def source_user_login_token():
    return source_user_login_token_v2

# 目标用户信息
def target_user_id():
    return target_user.get('id')

def target_user_username():
    return target_user.get('username')

def target_user_password():
    return target_user.get('password')

# 读取account库mysql配置
def get_mysql_config_account():
    if TEST_ENV != 'production':
        mysql_config_account = read_config.read_config_mysql(TEST_ENV, 'account')
        global opmysql_account
        opmysql_account = OpMysql(host=mysql_config_account['host'], user=mysql_config_account['user'], password=mysql_config_account['password'], database=mysql_config_account['database'])

# 初始化mysql配置并且跳过正式环境
get_mysql_config_account()

# 清除数据库basic_auth表的phone_number字段
def clear_phone_number(phone_number):
    opmysql_account.clear_basic_auth(column_name='phone_number', column_value=phone_number)

# 清除数据库basic_auth表的username字段
def clear_username(username):
    opmysql_account.clear_basic_auth(column_name='username', column_value=username)

# 读取redis配置
def get_redis_config():
    if TEST_ENV != 'production':
        redis_config = read_config.read_config_redis(TEST_ENV)
        global op_redis
        op_redis = OpRedis(host=redis_config['host'], port=redis_config['port'], password=redis_config['password'], db=1)

# 初始化redis配置并且跳过正式环境
get_redis_config()

# 获取账号3.0的redis中存储的验证码
def get_captcha_account_v3(catpcha_type, phone_number):
    captcha = op_redis.get_captcha_account('v3', catpcha_type, phone_number)
    return captcha

# 获取账号2.0的redi中存储的验证码
def get_captcha_account_v2(catpcha_type, phone_number):
    captcha = op_redis.get_captcha_account('v2', catpcha_type, phone_number)
    return captcha

# 获取发送图形验证码的ticket
def get_captcha_ticket():
    return get_captcha_ticket_account_v3(TIGER_API_HOST)

# dev环境判断
def is_dev():
    return True if TEST_ENV == 'dev' else False

# 判断是否是dev或者test环境
def is_dev_or_test():
    return True if TEST_ENV not in ('staging', 'production') else False

def is_production():
    return True if TEST_ENV == 'production' else False

# 判断账号2.0接口，极验是否开启
def is_geetest_account_v2_on():
    return True if GEETEST_ACCOUNT_V2 == 'on' else False

# 因为test中None会被解析为字符串，所以这里增加此函数
def is_none(source):
    return True if source == None else False

# 所有条件都是True才返回True，用于解决多个skip条件
def is_all_true(*a):
    pass