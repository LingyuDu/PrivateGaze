import os
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.io import read_image
import numpy as np
from torch.utils.data import DataLoader
from torchvision.models import resnet18, ResNet18_Weights
import torch.nn as nn
from torchvision import transforms
import h5py
import json
import cv2


class MPIIDataset(Dataset):
    def __init__(self, transform=None, target_transform=None):
        self.img_labels = np.load("/home/walter/MPIIFaceGaze_png_mix/new_labels.npy")
        self.img_dir = "/home/walter/MPIIFaceGaze_png_mix"
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return self.img_labels.shape[0]

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, str(idx)+".png")
        image = read_image(img_path)/255.
        label = self.img_labels[idx]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
   


class ETHXGaze(Dataset):
    def __init__(self, transform=None, target_transform=None):
        with open("data_index.json", 'r') as f:
            self.data_index = json.load(f)
        self.transform = transform
        self.target_transform = target_transform
        self.img_dir = '/home/walter/xgaze_224/train/'

    def __len__(self):
        return len(self.data_index)

    def __getitem__(self, idx):
        input_file = '/home/walter/xgaze_224/train/' + self.data_index[idx][0]
        fid = h5py.File(input_file, 'r')
        image = fid['face_patch'][self.data_index[idx][1], :] / 255
        image = image[:, :, [2, 1, 0]]
        image = np.transpose(image, (2, 0, 1))
        label = fid['face_gaze'][self.data_index[idx][1], :]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


class ColumbiaGaze(Dataset):
    def __init__(self, target_transform=None):

        self.transform = transforms.Resize([224, 224])
        self.target_transform = target_transform
        self.img_dir = '/home/walter/columbia_gaze_data_set_normalized/mix/'
        self.img_labels = np.load('/home/walter/columbia_gaze_data_set_normalized/mix/labels.npy')/180*np.pi
        self.gender_label = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1,
                                      1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0,
                                      0, 0])

    def __len__(self):
        return self.img_labels.shape[0]

    def __getitem__(self, idx):
        img_path = self.img_dir + str(idx) + '.png'
        image = read_image(img_path) / 255.
        label = self.img_labels[idx]
        image = self.transform(image)
        identity = int(idx/105)
        label = np.concatenate((label, np.array([identity])))
        return image, label





class GazeCapture(Dataset):
    def __init__(self, target_transform=None, subject_num=0):
        self.transform = transforms.Resize([224, 224])
        self.target_transform = target_transform
        self.data = h5py.File('/home/walter/GazeCapturePreprcessed.h5','r')
        self.image_num_per_subject = []
        self.image_num = 0
        self.subject_num = len(self.data.keys())
        self.keys_list = []
        for key in self.data.keys():
            self.image_num += self.data[key]['labels'][:].shape[0]
            self.image_num_per_subject.append(self.image_num)
            self.keys_list.append(key)
        self.image_num_per_subject = np.array(self.image_num_per_subject)

    def __len__(self):
        return self.image_num

    def __getitem__(self, idx):
        potential_subject = np.argmin(np.abs(idx-self.image_num_per_subject))
        if idx < self.image_num_per_subject[0]:
            subject = 0
            subject_img_idx = idx
        elif idx >= self.image_num_per_subject[-2]:
            subject = self.subject_num - 1
            subject_img_idx = idx - self.image_num_per_subject[subject-1]
        elif idx < self.image_num_per_subject[potential_subject]:
            subject = potential_subject
            subject_img_idx = idx - self.image_num_per_subject[subject - 1]
        else:
            subject = potential_subject + 1
            subject_img_idx = idx - self.image_num_per_subject[subject - 1]

        image = self.data[self.keys_list[subject]]['pixels'][subject_img_idx]/255.
        image = image.astype(np.float32)
        image = cv2.resize(image, (224, 224))
        image = np.transpose(image, (2, 0, 1))
        gaze_label = self.data[self.keys_list[subject]]['labels'][subject_img_idx][0:2]
        label = np.concatenate((gaze_label, np.array([subject])))

        return image, gaze_label


