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
MIN_LON = 7366
MIN_LAT = 386
MAX_LON = 13505
MAX_LAT = 5355

ALL = (MAX_LON - MIN_LON) * (MAX_LAT - MIN_LAT)


def amap_regeo(location, batch):
    host = 'https://regeo.market.alicloudapi.com'
    path = '/v3/geocode/regeo'
    appcode = 'bc40cc405f3c4f5dbb2b8f967100071d'
    querys = 'batch=' + batch + '&extensions=base&location=' + location + '&output=JSON'
    url = host + path + '?' + querys
    log.info('querys:%s', querys)
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
        return '0'


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

    target_file = conf.get("path", "target_file")
    log.info('target_file:%s', target_file)

    start_lon = conf.getint("common", "start_lon")
    start_lat = conf.getint("common", "start_lat")
    sleep_millseconds = conf.getint("common", "sleep_millseconds")
    batch_size = conf.getint("common", "batch_size")

    location_arr = []
    retry = 3
    index = 0
    for i in range(start_lon, MAX_LON):
        for j in range(start_lat, MAX_LAT):
            key = format(i / 100, '.2f') + "," + format(j / 100, '.2f')
            location_arr.append(key)
            if ((index + 1) % batch_size == 0) or (i == MAX_LON and j == MAX_LAT):
                data = []
                location = '|'.join(location_arr)
                re = '0'
                jsondata = ''
                m = 0
                while re == '0' and m < retry:
                    m += 1
                    time.sleep(0.1)
                    re = amap_regeo(location, 'true')
                    if re != '0':
                        # 取json中状态码
                        jsondata = json.loads(re)
                        log.info("调用逆地理返回:%s", jsondata)
                        re = jsondata.get('status')

                if re == '0':
                    log.error('调用失败的经纬度:%s', location_arr)
                else:
                    regeocodes = jsondata.get('regeocodes')
                    regeocodes_size = len(regeocodes)

                    for j in range(0, regeocodes_size):
                        element = regeocodes[j]
                        addressComponent = element.get('addressComponent')
                        province_name = addressComponent.get('province')
                        city_name = addressComponent.get('city')
                        district_name = addressComponent.get('district')
                        district_code = addressComponent.get('adcode')

                        if district_code == '900000' or district_code == '':
                            log.info("调用逆地理未解析出地址")
                            continue
                        key = location_arr[j]
                        lonlat = key.split(',')
                        data.append(
                            ["", province_name, "", city_name, district_code, district_name, lonlat[0],
                             lonlat[1]])
                        log.info(data)

                df = pd.DataFrame(data, columns=usecols)
                conf.set("common", "start_lon", str(i))
                conf.set("common", "start_lat", str(j))
                with open(conf_path, 'w')as conf_file:
                    conf.write(conf_file)

                # 写入到目标文件
                with open(target_file, mode='a', encoding='utf-8') as f:
                    df.to_csv(f, header=f.tell() == 0, index=False, encoding='utf-8')
                location_arr.clear()
                completed = (i - MIN_LON) * (j - MIN_LAT)
                log.error("总记录：%s,已完成：%s,占比：%s", ALL, completed, completed * 100 / ALL)
            index += 1


if __name__ == '__main__':
    main()
