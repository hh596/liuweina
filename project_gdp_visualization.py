#coding:utf-8
"""
综合项目:世行历史数据基本分类及其可视化
作者：刘维娜
日期: 6.1

"""

import csv
import math
import pygal
import pygal_maps_world  #导入需要使用的库


def read_csv_as_nested_dict(filename, keyfield, separator, quote): #读取原始csv文件的数据，格式为嵌套字典
    """
    输入参数:
      filename:csv文件名
      keyfield:键名
      separator:分隔符
      quote:引用符

    输出:
      读取csv文件数据，返回嵌套字典格式，其中外层字典的键对应参数keyfiled，内层字典对应每行在各列所对应的具体值
    """
    result={}
    with open(filename,newline="")as csvfile:
        csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csvreader:
            rowid=row[keyfield]
            result[rowid]=row

    return result

pygal_countries = pygal.maps.world.COUNTRIES #读取pygal.maps.world中国家代码信息（为字典格式），其中键为pygal中各国代码，值为对应的具体国名(建议将其显示在屏幕上了解具体格式和数据内容）

def reconcile_countries_by_name(plot_countries, gdp_countries): #返回在世行有GDP数据的绘图库国家代码字典，以及没有世行GDP数据的国家代码集合
    """
    
    输入参数:
    plot_countries: 绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
    gdp_countries:世行各国数据，嵌套字典格式，其中外部字典的键为世行国家代码，值为该国在世行文件中的行数据（字典格式)
    
    输出：
    返回元组格式，包括一个字典和一个集合。其中字典内容为在世行有GDP数据的绘图库国家信息（键为绘图库各国家代码，值为对应的具体国名),
    集合内容为在世行无GDP数据的绘图库国家代码
    """
    no_datas=set() #创建一个集合，为在世行无GDP数据的绘图库国家代码
    datas={} #创建一个字典，为在世行有GDP数据的绘图库国家信息
 
    for key1,value1 in plot_countries.items():
        if value1 in gdp_countries:
            data=gdp_countries[value1]
            i=0
            for key2,value2 in data.items():
                i=i+1
                if i>=5: #isp_gdp.csv文件从第五列开始为GDP数据
                    if value2!='':
                        datas[key1]=value1
                        break
                    else:
                        continue
            if i==61:
                no_datas.add(key1)
        else:
            no_datas.add(key1)
    return no_datas,datas


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    输入参数:
    gdpinfo: 
	plot_countries: 绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
	year: 具体年份值
	
    输出：
    输出包含一个字典和二个集合的元组数据。其中字典数据为绘图库各国家代码及对应的在某具体年份GDP产值（键为绘图库中各国家代码，值为在具体年份（由year参数确定）所对应的世行GDP数据值。为
    后续显示方便，GDP结果需转换为以10为基数的对数格式，如GDP原始值为2500，则应为log2500，ps:利用math.log()完成)
    2个集合一个为在世行GDP数据中完全没有记录的绘图库国家代码，另一个集合为只是没有某特定年（由year参数确定）世行GDP数据的绘图库国家代码

   """
    no_data=set() #在世行GDP数据中完全没有记录的绘图库国家代码
    year_no_data=set() #只是没有某特定年（由year参数确定）世行GDP数据的绘图库国家代码
    year_data={} #绘图库各国家代码及对应的在某具体年份GDP产值
    gdp_countries=read_csv_as_nested_dict(gdpinfo["gdpfile"], 'Country Name', ',', '"')
    no_datas,datas=reconcile_countries_by_name(plot_countries, gdp_countries)
    no_data=no_datas
    for key1,value1 in datas.items():
        per_country_data=gdp_countries[value1]
        year_gdp=per_country_data[year]
        if year_gdp!='':
            year_gdp=float(year_gdp)
            gdp=math.log(year_gdp,10)
            year_data[key1]=gdp
        else:
            year_no_data.add(key1)
    tuple1=(year_data,no_data,year_no_data)
    return tuple1


def render_world_map(gdpinfo, plot_countries, year, map_file): #将具体某年世界各国的GDP数据(包括缺少GDP数据以及只是在该年缺少GDP数据的国家)以地图形式可视化
    """
    Inputs:
      
      gdpinfo:gdp信息字典
      plot_countires:绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
      year:具体年份数据，以字符串格式程序，如"1970"
      map_file:输出的图片文件名
    
    目标：将指定某年的世界各国GDP数据在世界地图上显示，并将结果输出为具体的的图片文件
    提示：本函数可视化需要利用pygal.maps.world.World()方法
    
    
    """
    world_map=pygal.maps.world.World()
    world_map.title='全球GDP分布图'
    tuple2=build_map_dict_by_name(gdpinfo, plot_countries, year)
    dict_a=tuple2[0]
    dict_b={}
    for i in tuple2[1]:
        dict_b[i]='not found data'
    dict_c={}
    for i in tuple2[2]:
        dict_c[i]='not found data'
    world_map.add('{0}'.format(year),dict_a)
    world_map.add('missing from world bank', dict_b)
    world_map.add('no data at this year', dict_c)
    world_map.render_to_file(map_file)


def test_render_world_map(year):  #测试函数
    """
    对各功能函数进行测试
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    } #定义数据字典


    pygal_countries = pygal.maps.world.COUNTRIES   # 获得绘图库pygal国家代码字典

    # 测试时可以1970年为例，对函数继续测试，将运行结果与提供的svg进行对比，其它年份可将文件重新命名
    render_world_map(gdpinfo, pygal_countries, year, "isp_gdp_world_name_2010.svg")








#程序测试和运行
print("欢迎使用世行GDP数据可视化查询")
print("----------------------")
year=input("请输入需查询的具体年份:")
test_render_world_map(year)
