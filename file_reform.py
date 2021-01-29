import os
import shutil
from glob import glob


def image_files_from_folder(folder, upper=False):
    extensions = ['jpg', 'jpeg', 'png']
    img_files = []
    for ext in extensions:
        img_files += glob('%s/*.%s' % (folder, ext))
        if upper:
            img_files += glob('%s/*.%s' % (folder, ext.upper()))
    return img_files


# 将分类的文件夹内的图片自动改名
def reform(src_dir, out_dir=None):
    if out_dir is None:
        out_dir = src_dir + "-img"

    # 构造 voc 数据
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    c_list = []

    for dir_n in os.listdir(src_dir):
        dir = src_dir + "/" + dir_n

        if os.path.exists(dir) is False:
            continue

        c_list.append(dir_n)

        fi = 0
        i_files = image_files_from_folder(dir)

        for file in i_files:
            if file.find('.db') >= 0 or file.find('.DS') >= 0:
                continue

            if os.path.exists(file) is False:
                continue

            file_path = os.path.join(dir, file)

            file_type = file.split('.')[1]

            s_path = "%s/%s-%s.%s" % (out_dir, dir_n, fi, file_type)

            print(file_path)

            shutil.copy(file_path, s_path)

            fi = fi + 1

    n_str = ''
    for dn in c_list:
        n_str = n_str + dn + ","

    print(n_str)


if __name__ == '__main__':
    reform('分组文件夹', None)
