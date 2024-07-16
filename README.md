# PrivateGaze: Preserving User Privacy in Black-box Mobile Gaze Tracking Services

This repository contains the introductions and the codes for IMWUT 2024 paper PrivateGaze: Preserving User Privacy in Black-box Mobile Gaze Tracking Services by [Lingyu Du](https://github.com/LingyuDu), [Jinyuan Jia](https://jinyuan-jia.github.io/), [Xucong Zhang](https://www.ccmitss.com/zhang), and [Guohao Lan](https://guohao.netlify.app/). If you have any questions, please send an email to Lingyu.Du AT tudelft.nl.

## Description

Eye gaze contains rich information about human attention and cognitive processes. This capability makes the underlying technology, known as gaze tracking, a critical enabler for many ubiquitous applications and has triggered the development of easy-to-use gaze estimation services. Indeed, by utilizing the ubiquitous cameras on tablets and smartphones, users can readily access many gaze estimation services. In using these services, users must provide their full-face images to the gaze estimator, which is often a black box. This poses significant privacy threats to the users, especially when a malicious service provider gathers a large collection of face images to classify sensitive user attributes. In this work, we present PrivateGaze, the first approach that can effectively preserve users' privacy in black-box gaze tracking services without compromising gaze estimation performance. Specifically, we proposed a novel framework to train a privacy preserver that converts full-face images into obfuscated counterparts, which are effective for gaze estimation while containing no privacy information. Evaluation on four datasets shows that the obfuscated image can protect users' private information, such as identity and gender, against unauthorized attribute classification. Meanwhile, when used directly by the black-box gaze estimator as inputs, the obfuscated images lead to comparable tracking performance to the conventional, unprotected full-face images. 

## Getting Started

### Dependencies

* Pytorch

### Dataset preparation
In our implementation, to efficiently obtain DCT coefficents of the original RGB images, we proprocess the dataset by saving all the images in the format of .jpg. We then use jpeg2dct to directly read DCT coefficients from a jpg image in the training and testing stages. Moreover, we apply facial landmark detection to locate the positions of eyes and save the coordinates of periocular bounding boxes for each images as numpy arraies.

### Codes
* The file Contrastive_gaze_representation_learning.ipynb contains the main function for contrastive gaze representation learning.
* The file common_functions.py includes how to calculate the average angular error given a batch of images and gaze annotations.
* The file trans_in_rgb.py details the data augmentation we adopted in this project.

## System Overview
The illustration of PrivateGaze is shown in the folloing figure. The core of PrivateGaze is the privacy preserver, which transforms the original privacy-sensitive full-face image into an obfuscated version as input for the untrusted gaze estimation services. During the training stage, we train the privacy preserver with the assistance of a pre-trained surrogate gaze estimator. After training, the privacy preserve is deployed on the user's device to generate obfuscated images that can be used by the black-box gaze estimation services. This ensures accurate gaze estimation while preventing the user's private attributes, such as gender and identity, from being inferred by the service provider.

<img src="https://github.com/FreeGaze/FreeGaze-Source/blob/main/figures/overview.png" alt="My Image" width="500"/>
