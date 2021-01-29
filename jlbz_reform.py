import os
import shutil
from os.path import basename
from xml.dom.minidom import parse

# 将精灵标注助手标注的 XML 文件转为 yolo 训练文件
def reform(src_dir, out_dir):
    if out_dir is None:
        out_dir = src_dir + "-yolo"

    # 构造 voc 数据
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    tmp_dir = src_dir + "_tmp"

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    n_set = set()

    for file in os.listdir(src_dir):
        file_path = os.path.join(src_dir, file)
        file_name = file.split('.')[0]

        dom = parse(file_path)
        root = dom.documentElement
        img_node = root.getElementsByTagName("path")[0]
        img_path = img_node.childNodes[0].data

        objects_node = root.getElementsByTagName("object")

        size_nodes = root.getElementsByTagName("size")
        if len(size_nodes) == 0:
            print(file_name + "invalid")
            continue
        size_node = size_nodes[0]
        img_w = int(size_node.getElementsByTagName("width")[0].childNodes[0].data)
        img_h = int(size_node.getElementsByTagName("height")[0].childNodes[0].data)

        tmp_file = "%s/%s.txt" % (tmp_dir, file_name)

        with open(tmp_file, "a+") as tc:
            for boxes in objects_node:
                item = boxes.getElementsByTagName("item")  # 循环所有的item()
                for box in item:
                    cls_name = box.getElementsByTagName("name")[0].childNodes[0].data
                    x1 = int(box.getElementsByTagName("xmin")[0].childNodes[0].data)
                    y1 = int(box.getElementsByTagName("ymin")[0].childNodes[0].data)
                    x2 = int(box.getElementsByTagName("xmax")[0].childNodes[0].data)
                    y2 = int(box.getElementsByTagName("ymax")[0].childNodes[0].data)

                    n_set.add(cls_name)

                    tc.write(cls_name)
                    tc.write('\t')

                    tc.write(str(0.5 * (x1 + x2) / img_w))
                    tc.write('\t')

                    tc.write(str(0.5 * (y1 + y2) / img_h))
                    tc.write('\t')

                    tc.write(str((x2 - x1) / img_w))
                    tc.write('\t')

                    tc.write(str((y2 - y1) / img_h))
                    tc.write('\t')

                    tc.write(img_path)
                    tc.write('\t')
                    tc.write('\t')
                tc.write("\n")

    # print(n_set)
    n_list = list(n_set)
    n_list.sort()
    print(len(n_list))
    print(n_list)
    n_map = {}
    n_val_count_map = {}

    for i, n in enumerate(n_list):
        n_map[n] = i
        n_val_count_map[i] = 0
    # print(n_map)

    # 构造 voc 数据
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    images_train_dir = out_dir + "/images/train/"
    images_val_dir = out_dir + "/images/val/"
    labels_train_dir = out_dir + "/labels/train/"
    labels_val_dir = out_dir + "/labels/val/"

    os.makedirs(images_train_dir)
    os.makedirs(images_val_dir)
    os.makedirs(labels_train_dir)
    os.makedirs(labels_val_dir)

    with open(out_dir + "/names.txt", "a+") as tc:
        tc.write(len(n_list).__str__())
        tc.write('\n')
        tc.write(n_list.__str__())

    # classes.txt
    with open(labels_train_dir + "classes.txt", "a+") as tc:
        for i, n in enumerate(n_list):
            tc.write(n)
            tc.write('\n')
    with open(labels_val_dir + "classes.txt", "a+") as tc:
        for i, n in enumerate(n_list):
            tc.write(n)
            tc.write('\n')

    for file in os.listdir(tmp_dir):
        file_path = os.path.join(tmp_dir, file)
        file_name = file.split('.')[0]

        save_val = False
        n_i_list = []
        n_lines = []
        img_path = ''

        lines = open(file_path).readlines()
        for l in lines:
            l_items = l.split('\t')
            n = l_items[0]
            n_i = n_map.get(n)

            n_lines.append("%s %s %s %s %s" % (n_i, l_items[1], l_items[2], l_items[3], l_items[4]))
            img_path = l_items[5]

            n_i_list.append(n_i)
            # 是否存入 val
            if n_val_count_map.get(n_i) < 1:
                save_val = True

        fname = basename(img_path)

        if save_val:
            save_img = images_val_dir + fname
            l_file = labels_val_dir + file_name + ".txt"

            for ni in n_i_list:
                ni_c = n_val_count_map.get(ni)
                n_val_count_map[ni] = ni_c + 1

        else:
            save_img = images_train_dir + fname
            l_file = labels_train_dir + file_name + ".txt"

        shutil.copy(img_path, save_img)

        with open(l_file, "a+") as tc:
            for nl in n_lines:
                tc.write(nl)
                tc.write('\n')


if __name__ == '__main__':
    reform('精灵标注助手标注的 XML文件夹', None)
