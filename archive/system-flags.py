import sysconfig

keys = ('CC', 'CXX', 'CCSHARED', 'CFLAGS', 'LDSHARED')
for key in keys:
    value = sysconfig.get_config_var(key)
    print(key, value)