# -*-conding:utf-8-*-
import pandas as pd


def main():
    source_file = 'D:\\reversegeocode\\dim_provinces_coordinate.csv'
    t_file = 'D:\\reversegeocode\\dim_provinces_coordinate2.csv'
    # 读原文件
    sdf = pd.read_csv(source_file)
    sdf['short_lon'] = pd.Series(["{0:.2f}".format(val) for val in sdf['short_lon']], index=sdf.index)
    sdf['short_lat'] = pd.Series(["{0:.2f}".format(val) for val in sdf['short_lat']], index=sdf.index)

    # 写入到目标文件
    with open(t_file, mode='w', encoding='utf-8') as f:
        sdf.to_csv(f, index=False, encoding='utf-8')


if __name__ == '__main__':
    main()
