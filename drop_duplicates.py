# -*-conding:utf-8-*-
import pandas as pd


def main():
    source_file = 'D:\\reversegeocode\\LC_DISTRICT_AND_LON_LAT_MAPPING.csv'
    t_file = 'D:\\reversegeocode\\LC_DISTRICT_AND_LON_LAT_MAPPING1.csv'
    # 读原文件
    sdf = pd.read_csv(source_file)
    # 计算未完成记录
    sdf.drop_duplicates(['lon', 'lat']).to_csv(t_file, index=False)


if __name__ == '__main__':
    main()
