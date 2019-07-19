# -*-conding:utf-8-*-
import configparser
import json
import os
import ssl
import sys
import time
import urllib.request as urllib2

import pandas as pd

from globalLog import log

usecols = ['province_code', 'province_name', 'city_code', 'city_name', 'district_code', 'district_name', 'short_lon',
           'short_lat']


def amap_regeo(location, batch):
    host = 'https://regeo.market.alicloudapi.com'
    path = '/v3/geocode/regeo'
    appcode = 'bc40cc405f3c4f5dbb2b8f967100071d'
    querys = 'batch=' + batch + '&extensions=base&location=' + location + '&output=JSON'
    url = host + path + '?' + querys

    request = urllib2.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        response = urllib2.urlopen(request, context=ctx)
        content = response.read()
        content.decode('utf-8')

        return content
    except Exception:
        log.exception(sys.exc_info())
        return 0


def chk_file(full_path):
    # 将文件路径分割出来
    split = os.path.split(full_path)
    file_dir = split[0]
    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    # 然后再判断文件是否存在，如果不存在，则创建
    if not os.path.exists(full_path):
        open(full_path, 'a+').close()


def main():
    conf = configparser.ConfigParser()
    conf_path = os.path.abspath(os.getcwd() + "/resource/config.ini")
    conf.read(conf_path, encoding="utf-8")

    source_file = conf.get('path', 'source_file')
    target_file = conf.get("path", "target_file")

    log.info('source_file:%s', source_file)
    log.info('target_file:%s', target_file)

    skip_rows = conf.getint("common", "start_row")
    # 读原文件
    sdf = pd.read_csv(source_file, skiprows=range(1, skip_rows + 1),
                      converters={'lon': str, 'lat': str, 'city': str, 'provinces': str})
    all_rows = sdf.shape[0]
    batch_size = conf.getint("common", "batch_size")

    size = len(sdf)
    location_arr = []
    location_dic = {}
    for i in range(0, size):

        key = sdf.iloc[i]['lon'] + "," + sdf.iloc[i]['lat']
        val = (sdf.iloc[i]['city'], sdf.iloc[i]['provinces'])
        location_arr.append(key)
        location_dic[key] = val
        if ((i + 1) % batch_size == 0) or (size == i + 1):

            location = '|'.join(location_arr)
            re = 0
            jsondata = ''
            while re == 0:
                time.sleep(0.2)
                re = amap_regeo(location, 'true')
                if re != 0:
                    # 取json中状态码
                    jsondata = json.loads(re)
                    log.info("调用逆地理返回:%s", jsondata)
                    re = jsondata.get('status')
            regeocodes = jsondata.get('regeocodes')
            regeocodes_size = len(regeocodes)
            data = []
            for j in range(0, regeocodes_size):
                element = regeocodes[j]
                addressComponent = element.get('addressComponent')
                province_name = addressComponent.get('province')
                city_name = addressComponent.get('city')
                district_name = addressComponent.get('district')
                district_code = addressComponent.get('adcode')

                if district_code == '900000':
                    continue
                key = location_arr[j]
                val = location_dic.get(key)
                lonlat = key.split(',')
                data.append(
                    [val[1], province_name, val[0], city_name, district_code, district_name, lonlat[0], lonlat[1]])
                log.info(data)

            df = pd.DataFrame(data, columns=usecols)
            skip_rows += len(location_arr)
            conf.set("common", "start_row", str(skip_rows))
            with open(conf_path, 'w')as conf_file:
                conf.write(conf_file)

            # 写入到目标文件
            with open(target_file, mode='a', encoding='utf-8') as f:
                df.to_csv(f, header=f.tell() == 0, index=False, encoding='utf-8')
            location_arr.clear()
            location_dic.clear()

            log.error("总记录：%s,已完成：%s,占比：%s", all_rows, skip_rows, skip_rows * 100 / all_rows)


if __name__ == '__main__':
    main()
