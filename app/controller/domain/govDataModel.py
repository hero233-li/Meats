from dataclasses import dataclass
"""这个类里面是定义查询的参数，主要是判断当前是第几层，如果是最外层，那么肯定is_parent 是true，不是的话，就可以调用具体的查询参数了
"""
@dataclass
class GetNationalMenuRequest:
    id:str
    dbcode:str
    wdcode:str
    m:str
@dataclass
class GetNationalMenuResponse:
    dbcode:str
    id:str
    isParent:bool
    name:str
    pid:str
    wdcode:str
@dataclass
class GovDataModel:
    """ 这里定义了两个类，一个是请求，一个是返回，首先我是拿到了所有的请求参数，也就是第一层目录，给一个返回出来，出现一个列表
    然后根据选择的列表，我开始再次调用查询参数，看一下有没有下级菜单，有的话，继续返回，一直到没有下一级菜单，我首先是得到最外层的参数，最顶层的数据列表
    """
    req_NationalMenu:GetNationalMenuRequest
    res_NationalMenu:GetNationalMenuResponse

