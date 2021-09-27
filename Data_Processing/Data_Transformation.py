import os
from shutil import copyfile
import shutil
from distutils.dir_util import copy_tree
from sklearn.model_selection import train_test_split
import argparse
import json

org_path = r'C:\Users\antra\OneDrive\Máy tính\IAM db'
dest_path = r'C:\Users\antra\OneDrive\Máy tính\IAM db'

print(org_path)

#convert structure of each sample from a/b/c/d to a/b/d
def delete_parent_folder(org_path):
    for dir in os.listdir(org_path):
        dir_path = os.path.join(org_path, dir)
        for sub_dir in os.listdir(dir_path):
            subdir_path = os.path.join(dir_path, sub_dir)
            copy_tree(subdir_path, dir_path)
            shutil.rmtree(subdir_path)

#split data into 3 set train test, val
def split_data(data_dir_path, proceed_imgs, train_dest_path, val_dest_path, test_dest_path):
    data = os.listdir(data_dir_path)
    if len(data) == 0:
        return

    train, test = train_test_split(data, test_size=0.3, random_state=1, shuffle=True)
    val, test = train_test_split(test, test_size=0.5, random_state=1, shuffle=True)
    print(f'TOTAL samples: {len(data)}')
    # print(data_dir)
    print(f'TRAINSET sample: {len(train)}')
    # print(train)
    print(f'TESTSET sample: {len(test)}')
    # print(val)
    print(f'VALSET sample: {len(val)}')
    # print(test)
    for img in train:
        # print(img)
        img_org_path = os.path.join(data_dir_path, img)
        img_dest_path = os.path.join(train_dest_path, img)
        if not os.path.isfile(img_dest_path):
            shutil.copy(img_org_path, train_dest_path)
            proceed_imgs += 1
    print(f'proceed img: {proceed_imgs}')
    for img in val:
        # print(img) 
        img_org_path = os.path.join(data_dir_path, img)
        img_dest_path = os.path.join(val_dest_path, img)
        if not os.path.isfile(img_dest_path):  
            shutil.copy(img_org_path, val_dest_path)
            proceed_imgs += 1
    print(f'proceed img: {proceed_imgs}')
    for img in test:
        # print(img) 
        img_org_path = os.path.join(data_dir_path, img)
        img_dest_path = os.path.join(train_dest_path, img)
        if not os.path.isfile(img_dest_path):
            shutil.copy(img_org_path, test_dest_path)
            proceed_imgs += 1
    print(f'proceed img: {proceed_imgs}')

# delete_parent_folder(r'C:\Users\antra\OneDrive\Máy tính\IAM db\sentences')
# delete_parent_folder(r'C:\Users\antra\OneDrive\Máy tính\IAM db\lines')

# print('...')
def apply_splitted_data(org_path, dest_path):
    splitted_dir = os.path.join(dest_path,'Splitted_Data') 
    train_dir = os.path.join(splitted_dir, 'Train')
    test_dir = os.path.join(splitted_dir, 'Test')
    val_dir = os.path.join(splitted_dir, 'Val')
    proceed_imgs = 0

    #Create Spitted Data directory and Test, train, val set if they aren't existed
    # print(os.listdir(dest_path))

    if 'Splitted_Data' not in os.listdir(dest_path):
        os.mkdir(splitted_dir)
    if 'Train' not in os.listdir(splitted_dir):
        os.mkdir(train_dir)
    print('create trainset')
    if 'Test' not in os.listdir(splitted_dir):
        os.mkdir(test_dir)
    print('create testset')
    if 'Val' not in os.listdir(splitted_dir):
        os.mkdir(val_dir)
    print('create valset')

    for name_ds in os.listdir(org_path):
        print(f'name_ds: {name_ds}')
        name_ds_path = os.path.join(org_path,name_ds)
        if (name_ds == 'forms' or name_ds =='lines' or name_ds=='sentences'):
            # print('name_ds is a dir !!!')
            train_dest_path = os.path.join(train_dir, name_ds)
            test_dest_path = os.path.join(test_dir, name_ds)
            val_dest_path = os.path.join(val_dir, name_ds)

            #Create data folder in each set
            if name_ds not in os.listdir(train_dir):
                os.mkdir(train_dest_path)
            if name_ds not in os.listdir(test_dir):
                os.mkdir(test_dest_path)
            if name_ds not in os.listdir(val_dir):
                os.mkdir(val_dest_path)

            if name_ds == 'forms':
                split_data(name_ds_path, proceed_imgs=0, test_dest_path=test_dest_path, train_dest_path=train_dest_path, val_dest_path=val_dest_path)

                

            if (name_ds == 'lines' or name_ds =='sentences'):
                for data_dir in os.listdir(name_ds_path): 
                    # print(data_dir)
                    data_dir_path = os.path.join(name_ds_path, data_dir)
                    print(f'data_dir_path: {data_dir_path}') 
                    #create data folder in each data form for each dataset
                    data_train_dest_path = os.path.join(train_dest_path, data_dir)
                    data_test_dest_path = os.path.join(test_dest_path,data_dir)
                    data_val_dest_path = os.path.join(val_dest_path, data_dir)

                    if not os.path.isdir(data_train_dest_path):
                        os.mkdir(data_train_dest_path)
                    if not os.path.isdir(data_test_dest_path):
                        os.mkdir(data_test_dest_path)
                    if not os.path.isdir(data_val_dest_path):
                        os.mkdir(data_val_dest_path)

                    split_data(data_dir_path, proceed_imgs=0, test_dest_path=data_test_dest_path, train_dest_path=data_train_dest_path, val_dest_path=data_val_dest_path)


if __name__ == 'main':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--foo', help='foo help')
    argparser.add_argument('-c', '--config',  default=None, type=str, help='config file path (default: None)')
    argparser.add_argument('-p', '--path', default=None, type=str, help='Original path')
    argparser.add_argument('-d', '--destination', default=None, type=str, help='Destination path')

    args = argparser.parse_args()
    if args.config is not None and (args.path is not None and args.destination is not None):
        print('WARNING! Choose --config for configurable file or --path/--desetiation for optimal path')
    else:
        if args.config is not None:
            if not os.path.isfile(args.config): 
                print('WARNING! The path does not exist')
            else:
                configs = json.load(open(args.config))
                del_org_path = configs['delete_parent']['path']
                if del_org_path is not None:
                    delete_parent_folder(del_org_path)
                org_path = configs['split_data']['org_path']
                dest_path = configs['split_data']['dest_path']
                if org_path is not None and dest_path is not None:
                    apply_splitted_data(org_path, dest_path)
            

