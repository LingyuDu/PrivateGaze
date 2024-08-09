# PrivateGaze: Preserving User Privacy in Black-box Mobile Gaze Tracking Services

This repository contains the introductions and the codes for IMWUT 2024 paper [PrivateGaze: Preserving User Privacy in Black-box Mobile Gaze Tracking Services](https://arxiv.org/pdf/2408.00950) by [Lingyu Du](https://github.com/LingyuDu), [Jinyuan Jia](https://jinyuan-jia.github.io/), [Xucong Zhang](https://www.ccmitss.com/zhang), and [Guohao Lan](https://guohao.netlify.app/). If you have any questions, please send an email to Lingyu.Du AT tudelft.nl.

## Description

Eye gaze contains rich information about human attention and cognitive processes. This capability makes the underlying technology, known as gaze tracking, a critical enabler for many ubiquitous applications and has triggered the development of easy-to-use gaze estimation services. Indeed, by utilizing the ubiquitous cameras on tablets and smartphones, users can readily access many gaze estimation services. In using these services, users must provide their full-face images to the gaze estimator, which is often a black box. This poses significant privacy threats to the users, especially when a malicious service provider gathers a large collection of face images to classify sensitive user attributes. In this work, we present PrivateGaze, the first approach that can effectively preserve users' privacy in black-box gaze tracking services without compromising gaze estimation performance. Specifically, we proposed a novel framework to train a privacy preserver that converts full-face images into obfuscated counterparts, which are effective for gaze estimation while containing no privacy information. Evaluation on four datasets shows that the obfuscated image can protect users' private information, such as identity and gender, against unauthorized attribute classification. Meanwhile, when used directly by the black-box gaze estimator as inputs, the obfuscated images lead to comparable tracking performance to the conventional, unprotected full-face images. 

## Real-time Video Demo

![Alt Text](https://github.com/LingyuDu/PrivateGaze/blob/main/figures/demo_new.gif)
Raw images are captured by cameras from subjects; obfuscated images are converted from raw images by the trained privacy preserver; estimated gazes visualize the gaze direction estimated from obfuscated images by the black-box gaze estimator. 


## System Overview
The illustration of PrivateGaze is shown in the following figure. The core of PrivateGaze is the privacy preserver, which transforms the original privacy-sensitive full-face image into an obfuscated version as input for the untrusted gaze estimation services. During the training stage, we train the privacy preserver with the assistance of a pre-trained surrogate gaze estimator. After training, the privacy preserve is deployed on the user's device to generate obfuscated images that can be used by the black-box gaze estimation services. This ensures accurate gaze estimation while preventing the user's private attributes, such as gender and identity, from being inferred by the service provider.

<div align=center>
<img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/teaser_figure-1.png" alt="My Image" width="800"/>
</div>

## Threat Model
### Black-box gaze estimator
We consider a more practical case where the gaze estimator $\mathcal{G}_b(\cdot)$ is performed by a black-box, deep learning-based model. Specifically, the black-box gaze estimator $\mathcal{G}_b(\cdot)$ is trained on an unknown dataset that contains raw full-face images and gaze annotations. Users can access gaze estimation services either through the cloud server or by installing the system directly on their local devices. In both cases, the user can only query and request $\mathcal{G}_b(\cdot)$ for service and has no knowledge about its implementation and 

### Capabilities and goals of the malicious service provider.
We assume the malicious service provider can stealthily collect a dataset $\mathcal{D}_p$, comprising images submitted by users for gaze estimation service, along with annotations of private user attributes such as identity and gender. Subsequently, $\mathcal{D}_p$ is used to train classifiers aimed at discerning users' private attributes from images that do not belong to $\mathcal{D}_p$.

### Our goals
In this work, we envision a trustworthy party that provides a privacy preserver $\mathcal{P}(\cdot)$ to protect the user's privacy. During the deployment stage, $\mathcal{P}(\cdot)$ converts the user's original full-face images $x$ into obfuscated images $x'$ that do not contain information related to the user's attributes, such as identity and gender. The user then directly calls the black-box gaze estimator $\mathcal{G}_b(\cdot)$ with the obfuscated image $x'$. Formally, the obfuscated image $x'$ must fulfill the objectives of preserving the user's privacy while ensuring good gaze estimation performance: 

* The obfuscated image $x'$ cannot be used to correctly classify private attributes of the user, such as identity and gender, even if the malicious service provider trains deep learning-based classifiers on $\mathcal{D}_p$, i.e., a set of $x'$ with accurate labels for these confidential user attributes.
* The obfuscated image $x'$ can be directly used by $\mathcal{G}_b(\cdot)$ without any adaption needed from the service provider's side. The gaze estimation performance of  $\mathcal{G}_b(\cdot)$ with $x'$ should be similar to the original full-face images.

## Overview of PrivateGaze
To achieve the design goals, we propose a novel framework PrivateGaze consisting of a privacy preserver, an anchor image generation module, and the surrogate gaze estimator as shown in the following figure. The privacy preserver $\mathcal{P}(\cdot)$ converts unprotected raw images $x$ into obfuscated images $x'$ to protect the private information of users, such as gender and identity contained in $x$. To achieve this goal, the privacy preserver ensures that $x'$, converted from different $x$ (images from different subjects), will exhibit similar facial appearances akin to a pre-generated average full-face image called the anchor image $\hat{x}$. We devise the anchor image generation module to generate the $\hat{x}$ from the $\mathcal{D}_{w}$.

To achieve the utility goal, the privacy preserver $\mathcal{P}(\cdot)$ is designed to extract gaze features $z$ from $x$ and generate $x'$ that maintains these features for effective gaze estimation. Specifically, $\mathcal{P}(\cdot)$ consists of the gaze-feature extractor $F(\cdot)$ and the image generator $IG(\cdot)$. $F(\cdot)$ extracts gaze features $z$ from the input $x$. $IG(\cdot)$ takes $z$ along with $\hat{x}$ as inputs to generate the privacy-preserved $x'$. The generated $x'$ has a similar appearance to $\hat{x}$ while preserving the gaze-related information $z$ from $x$ for accurate gaze estimation. To train $\mathcal{P}(\cdot)$, we construct a surrogate gaze estimator $\mathcal{G}_w(\cdot)$ trained on the public available dataset, which performs the gaze estimation training with input $x'$. In this way, we are able to maximize the information in $x'$ for the gaze estimation task. 

<div align=center>
<img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/Overview-1.png" alt="My Image" width="1000"/>
</div>

## Anchor Image Generation
We propose a novel method for generating the anchor image $\hat{x}$ from a public dataset. The anchor image serves as a template for the obfuscated images $x'$, ensuring they exhibit a facial appearance similar to $\hat{x}$. This allows us to manipulate the appearances of $x'$ to preserve user's privacy while achieving the utility goal. 

A major challenge in achieving this utility goal is training $\mathcal{P}(\cdot)$ with the surrogate gaze estimator $\mathcal{G}_w()$ while aiming for good gaze estimation performance on the black-box gaze estimator $\mathcal{G}_b(\cdot)$. To address this challenge, we carefully generate the anchor image $\hat{x}$ to ensure that both $\mathcal{G}_w(\cdot)$ and $\mathcal{G}_b(\cdot)$ yield similar gaze estimation results on $\hat{x}$. This strategy enables $\mathcal{G}_w(\cdot)$ and $\mathcal{G}_b(\cdot)$ to achieve comparable gaze estimation performance on the obfuscated images $x'$, as they share similar appearances with the anchor image. 

The anchor images generated on GazeCapture for EfficientNet, MobileNet, ResNet, ShuffleNet, and VGG respectively are shown as follows.

<div align=center>
<img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/gazecapture_average_face_efficientnet.png" alt="My Image" width="150"/>                    <img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/gazecapture_average_face_mobilenet.png" alt="My Image" width="150"/>          <img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/gazecapture_average_face_res18.png" alt="My Image" width="150"/>          <img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/gazecapture_average_face_shufflenet.png" alt="My Image" width="150"/>          <img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/gazecapture_average_face_vgg.png" alt="My Image" width="150"/> 
</div>

## Structure of the Privacy Preserver

The structure of privacy preserver $\mathcal{P}(\cdot)$ is shown in the following figure, which consists of the gaze-feature extractor $F(\cdot)$ and the image generator $IG(\cdot)$. $F(\cdot)$ extracts gaze features $z$ from the raw image $x$ of the user. $IG(\cdot)$ takes the extracted gaze features $z$ and the anchor image $\hat{x}$ as inputs to generate the privacy-preserved obfuscated image $x'$. $x'$ has a similar appearance to $\hat{x}$ while retaining the gaze features extracted from $x$. Only the components with color-coded yellow will be deployed on the user's device after training for privacy preservation.

<div align=center>
<img src="https://github.com/LingyuDu/PrivateGaze/blob/main/figures/PrivacyPreserver-1.png" alt="My Image" width="500"/>
</div>

## Codes, Pretrained Gaze Estimators, and Anchor Images

* Black-box gaze estimators trained on ETH-XGaze and the surrogate gaze estimator trained on GazeCapture are available at [black-box gaze estimators](https://drive.google.com/drive/folders/16M-xoarDf84FhGknnq6DajS4BO7wHbai?usp=drive_link).
* Anchor images are available in figures/.
* TrainPrivacyPreserver is the main file for training a privacy preserver given a black-box gaze estimator.
* unet_models_v2.py defines the architectures of the privacy preserver. 

## Citation 

Please cite the following paper in your publications if the code helps your research.

<div style="border: 1px solid #ccc; padding: 10px; background-color: #f9f9f9; border-radius: 5px;">
<pre>
@article{du2024privategaze,
  title={PrivateGaze: Preserving User Privacy in Black-box Mobile Gaze Tracking Services},
  author={Du, Lingyu and Jia, Jinyuan and Zhang, Xucong and Lan, Guohao},
  journal={Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies},
  volume={8},
  number={3},
  year={2024},
  publisher={ACM New York, NY, USA}
}
</pre>
</div>
