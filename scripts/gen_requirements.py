import pkg_resources
 
# 获取所有已安装的包及其版本
installed_packages = [(dist.key, dist.version, dist.location) for dist in pkg_resources.working_set]
 
# 写入requirements.txt
with open('requirements.txt', 'w') as f:
    for package in installed_packages:
        f.write('{}=={}\n'.format(package[0], package[1]))