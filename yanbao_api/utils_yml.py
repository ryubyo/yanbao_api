import os 
import yaml


def operate(file, op_data=None, mode="r", encoding="utf-8"):
    """mode: r=读取, w=覆盖, c=修改, d=删除"""
    if mode == "r":
        """读取yaml文件"""
        data = {}
        if os.path.exists(file):
            with open(file, 'r', encoding=encoding) as fr:
                data = yaml.safe_load(fr)
        return data
    elif mode == "w":
        """覆盖yaml文件"""
        with open(file, 'w', encoding=encoding) as fw:
            yaml.dump(data, fw, encoding=encoding, allow_unicode=True)
    elif mode == "c":
        """修改yaml文件"""
        data = {}
        if os.path.exists(file):
            with open(file, 'r', encoding=encoding) as fr:
                data = yaml.safe_load(fr)
        data.update(op_data)
        with open(file, 'w', encoding=encoding) as fw:
            yaml.dump(data, fw, encoding=encoding, allow_unicode=True)
    elif mode == "d":
        """删除yaml文件"""
        data = {}
        if os.path.exists(file):
            with open(file, 'r', encoding=encoding) as fr:
                data = yaml.safe_load(fr)
        for k in op_data:
            del data[k]
        with open(file, 'w', encoding=encoding) as fw:
            yaml.dump(data, fw, encoding=encoding, allow_unicode=True)
    else:
        return 
