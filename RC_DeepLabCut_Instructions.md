# Using Deep Lab Cut on Research Computing Servers

# Setup working environment on RC VIZ Servers

## Login to your account on our Viz cluster (Enginframe)

Access to EnginFrame is granted on request. Request access by sending
email to rc-help@colorado.edu.

Once access has been granted, EnginFrame is available at
https://viz.rc.colorado.edu/.

From the welcome page, select "Views" from the available interfaces
(or use [this direct link][vdi]).

[vdi]: https://viz.rc.colorado.edu/enginframe/vdi/vdi.xml

<p align="center"> 
<img src= enginframe/welcome.png format=1000w width="100%">
</p>

Provide your RC login credentials at the login prompt. You will be
promted to use a second authentication factor (e.g., the Duo mobile
app) to log in.

<p align="center"> 
<img src= enginframe/login.png format=1000w width="100%">
</p>


## Create a Remote Desktop

After logging in, select "Remote Desktop" from the list of services in
the left sidebar. (Other custom services may be configured for you as
well.)

<p align="center"> 
<img src= enginframe/vdi.png format=1000w width="100%">
</p>

When starting a Remote Desktop session you may customize the resources
allocated to the session and other characteristics of the dispatched
Slurm job. In most cases the defaults should be sufficient; however,
you may need to supply a Slurm account if you are associated with more
than one and you do not want to use your default account.

<p align="center"> 
<img src= enginframe/remote-desktop.png format=1000w width="100%">
</p>

Once the session has started, a thumbnail of the running session
appears in the Sessions list. EnginFrame will attempt to open the
session automatically, but may be blocked by the browser. In that
case, simply select the session thumbnail from the list, or use the
"click here" link in the notification text.

<p align="center"> 
<img src= enginframe/session.png format=1000w width="100%">
</p>

With the Remote Desktop session running and open, you should be able
to run standard Linux desktop applications, including 3d-acellerated
OpenGL applications.

<p align="center"> 
<img src= enginframe/glxgears.png format=1000w width="100%">
</p>

## Active Session

Once you have an active session, you'll be on a linux desktop that looks a lot like a Mac or Windows desktop. From the main menu, open a terminal. In the terminal, you can:

```
$ source /curc/sw/anaconda3/2019.03/bin/activate
$ conda activate DLCGPU_VIZ
```

...from this conda environment, you can proceed using deeplabcut in "ipython" as you normally would, and you should be able to get the GUI for the labeling step. See [Creating a project](#creating-a-project) to get started.

# Deep Lab Cut Instructions

## Creating a Project
Using the same terminal from [Active Session](#active-session), we are going to start an Ipython environment importing deeplabcut:
```
ipython
import deeplabcut
```
Next, to create a new project use the following:
```
config_path = deeplabcut.create_new_project(`Name of the project',`Name of the experimenter', [`Full path of video 1',`Full path of video2',`Full path of video3'], working_directory=`Full path of the working directory',copy_videos=True/False)
```

NOTE: Some parameters are not used or are optional when calling create_new_project

NOTE: config_path is set as a variable to easily assign config.yaml


## Configure the Project
Now is the time to edit the config.yaml file to adjust the settings
```
quit
vim fullpath/project/config.yaml
*edit the settings*
ipython
import deeplabcut
```

(Instructions about how and what to edit can be found [here](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#b-configure-the-project))

## Label Frames
First, extract frames from the given videos:
```
deeplabcut.extract_frames(config_path,‘automatic/manual’,‘uniform/kmeans’, userfeedback=False, crop=True/False)
```
Second, label the frames using a GUI:
```
deeplabcut.label_frames(config_path)
```
Click **Save**, then **Quit**.

NOTE: You can click Save at any point and then resume labeling later on using ```deeplabcut.label_frames(config_path)```

**Demo:** using the GUI to label a video from [Deep Lab Cut](http://www.mousemotorlab.org/deeplabcut)
<p align="center">
<img src=enginframe/dlcgui.gif "format=750w" width="70%">
</p>

(For help, go to [extracting frames](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#c-data-selection) or [labeling frames](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#d-label-frames))

## Check Labeled Frames:
```
deeplabcut.check_labels(config_path)
```
Checking labels returns a folder with labeled images. If the labels look good move on to [Create Training Dataset](#create-training-dataset). 

If the labels do not look correct, re-load the frames using ```deeplabcut.label_frames(config_path)```, move the labels around, and click save. 

(Help on [checking annotated frames](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#e-check-annotated-frames))

## Create Training Dataset:
***IMPORTANT:*** Only run this step where you are going to train the network.

If you label on your laptop but move your project folder to Google Colab or AWS, lab server, etc, then run the step below on that platform! If you labeled on a Windows machine but train on Linux, this is fine as of 2.0.4! You simply will be asked if you want to convert the data, and it will be done automatically!

Create a training dataset:
```
deeplabcut.create_training_dataset(config_path,num_shuffles=1)
```

(For help and to view optional parameters click [here](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#f-create-training-dataset))

## Train the Network:
***IMPORTANT:*** The time required to train the network mainly depends on the frame size of the dataset and the computer hardware. On a NVIDIA GeForce GTX 1080 Ti GPU, it takes ≈ 6 hrs to train the network for at least 200,000 iterations. On the CPU, it will take several days to train for the same number of iterations on the same training dataset.

***IMPORTANT:*** It is recommended to train for thousands of iterations until the loss plateaus (typically around 200,000). The variables display_iters and save_iters in the pose_cfg.yaml file allows the user to alter how often the loss is displayed and how often the weights are stored.

Starts training the network for the dataset created for one specific shuffle
```
deeplabcut.train_network(config_path,shuffle=1)
```

Starts training the network for the dataset created for one specific shuffle with multiple other effects(See parameter list below)
```
deeplabcut.train_network(config_path,shuffle=1,trainingsetindex=0,gputouse=None,max_snapshots_to_keep=5,autotune=False,displayiters=100,saveiters=15000, maxiters=30000)
```

(More notes on [training a network](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#g-train-the-network))

## Evaluate the Trained Network:
Now that we have a trained network, it is important that we evaluate its preformance. 

```
deeplabcut.evaluate_network(config_path, Shuffles=[1], plotting=True)
```

(Notes about evaluating the newly trained network can be found [here](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#h-evaluate-the-trained-network))

## Video Analysis and Plotting Results:
### 1. Analyze Data
NOTE: **novel videos DO NOT need to be added to the config.yaml file**. You can simply have a folder elsewhere on your computer and pass the video folder (then it will analyze all videos of the specified type (i.e. ``videotype='.mp4'``), or pass the path to the **folder** or exact video(s) you wish to analyze:

To analyze a **single** video:
```
deeplabcut.analyze_videos(config_path,[‘fullpath/analysis/project/videos/reachingvideo1.avi’], save_as_csv=True)
```
To analyze **multiple** videos:
```
deeplabcut.analyze_videos(config_path,videos,videotype='avi',shuffle=1,trainingsetindex=0,gputouse=None,save_as_csv=False, destfolder=None)
```
(Here are some tips for scaling up your analysis using [batch analysis](https://github.com/AlexEMG/DeepLabCut/wiki/Batch-Processing-your-Analysis))

### 2. Filter Data
You can also filter the predicted bodyparts by:
```
deeplabcut.filterpredictions(config_path,[`/fullpath/project/videos/reachingvideo1.avi'], shuffle=1)
```
Here are parameters you can modify and pass:
```
 deeplabcut.filterpredictions(config_path, [‘fullpath/analysis/project/videos/reachingvideo1.avi’], shuffle=1, trainingsetindex=0, comparisonbodyparts='all', filtertype='arima', p_bound=0.01, ARdegree=3, MAdegree=1, alpha=0.01)
```
NOTE: This creates a file with the ending filtered.h5 that you can use for further analysis. This filtering step has many parameters, so please see the full docstring by typing: ``deeplabcut.filterpredictions?``

Here is an example of how this can be applied to a video:
<p align="center"> 
<img src= enginframe/filterdata.png format=1000w width="80%">
</p>

### 3. Create Labeled Videos
Create labeled videos based on the extracted poses by plotting the labels on top of the frame and creating a video.

NOTE: There are two modes to create videos: FAST and SLOW (but higher quality!).

PRO TIP: The best quality videos are created when save_frames=True is passed. Therefore, when trailpoints and draw_skeleton are used, we highly recommend you also pass save_frames=True

Create multiple high-quality labeled videos:
```
deeplabcut.create_labeled_video(config_path,[‘fullpath/analysis/project/videos/reachingvideo1.avi’,‘fullpath/analysis/project/videos/reachingvideo2.avi’], save_frames=True/False)
```
Optionally, if you want to use the filtered data for a video or directory of filtered videos:
```
 deeplabcut.create_labeled_video(config_path,[‘fullpath/afolderofvideos’], videotype='.mp4', filtered=True)
```
You can also optionally add a skeleton to connect points and/or add a history of points for visualization: 
```
deeplabcut.create_labeled_video(config_path,[‘fullpath/afolderofvideos’], videotype='.mp4', draw_skeleton=True)
```
To set the "trailing points" you need to pass trailpoints:
```
deeplabcut.create_labeled_video(config_path,[‘fullpath/afolderofvideos’], videotype='.mp4', trailpoints=10) 
```
Example of a labeled skeleton video:
<p align="center"> 
<img src= enginframe/skele.gif format=1000w width="80%">
</p>

### 4. Plot the Outputs
Using *matplotlib*, plots the trajectory of the extracted poses across the analyzed video.
```
deeplabcut.plot_trajectories(config_path,[`/fullpath/project/videos/reachingvideo1.avi'],filtered=True)
```

(more details [here](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#i-video-analysis-and-plotting-results))

### 5. Analyze Skeleton Features
Extracts length and orientation of each "bone" of the skeleton as defined in the config.yaml file.
```
deeplabcut.analyzeskeleton(config, video, videotype='avi', shuffle=1, trainingsetindex=0, save_as_csv=False, destfolder=None)
```
Spooky scary [source code](https://github.com/AlexEMG/DeepLabCut/blob/master/deeplabcut/post_processing/analyze_skeleton.py)

## [Optional] Active Learning --> Network Refinement
**Complete these steps if the network was not trained properly or was not trained to your liking.**
### Extract Outlier Frames from a Video:
For generalization to large data sets, images with insufficient labeling performance can be extracted, manually corrected by adjusting the labels to increase the training set and iteratively improve the feature detectors.

NOTE: This step can be run itreatively
```
deeplabcut.extract_outlier_frames(config_path,[`videofile_path'])
```
Frame selection methods: outlieralgorithm= 'fitting', 'jump', 'uncertain', or 'manual'
* *uncertain:* select frames if the likelihood of a particular or all body parts lies below pbound (note this could also be due to occlusions rather then errors);
* *jump:* select frames where a particular body part or all body parts jumped more than \uf pixels from the last frame.
* *fitting:* select frames if the predicted body part location deviates from a state-space model fit to the time series of individual body parts. Specifically, this method fits an Auto Regressive Integrated Moving Average (ARIMA) model to the time series for each body part. Thereby each body part detection with a likelihood smaller than pbound is treated as missing data. Putative outlier frames are then identified as time points, where the average body part estimates are at least \uf pixel away from the fits. The parameters of this method are \uf, pbound, the ARIMA parameters as well as the list of body parts to average over (can also be all).
* *manual:* manually select outlier frames based on visual inspection from the user.

```
deeplabcut.extract_outlier_frames(config_path,[‘videofile_path’],outlieralgorithm='manual')
```

(To see other notes and parmaters click [here](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#j-refinement-extract-outlier-frames))

### Refinement of the Labels with our GUI:
Four scenarios are possible:
* Visible body part with accurate DeepLabCut prediction. These labels do not need any modifications.
* Visible body part but wrong DeepLabCut prediction. Move the label’s location to the actual position of the body part.
* Invisible, occluded body part. Remove the predicted label by DeepLabCut with a right click. Every predicted label is shown, even when DeepLabCut is uncertain. This is necessary, so that the user can potentially move the predicted label. However, to help the user to remove all invisible body parts the low-likelihood predictions are shown as open circles (rather than disks).
* Invalid images: In an unlikely event that there are any invalid images, the user should remove such an image and their corresponding predictions, if any. Here, the GUI will prompt the user to remove an image identified as invalid.

The labels for extracted putative outlier frames can be refined by opening the GUI:
```
deeplabcut.refine_labels(config_path)
```
Use the ‘Load Labels’ button to select one of the subdirectories, where the extracted frames are stored. 

For better chances to identify the low-confidence labels, specify the threshold of the likelihood.

Next, to adjust the position of the label, hover the mouse over the labels to identify the specific body part, left click and drag it to a different location. 

To delete a specific label, right click on the label (once a label is deleted, it cannot be retrieved).

Once done, go to [Merge](#merge-datasets)

**mini-demo:** using the refinement GUI, a user can load the file then zoom, pan, and edit and/or remove points:

<p align="center">
<img src=enginframe/dlcrefine.gif width="90%">
</p>

### Merge Datasets
After correcting the labels for all the frames in each of the subdirectories, the users should merge the data set to create a new dataset. In this step the iteration parameter in the config.yaml file is automatically updated.

To merge:
```
deeplabcut.merge_datasets(config_path)
```

(Details on merging can be found [here](https://github.com/AlexEMG/DeepLabCut/blob/master/docs/functionDetails.md#k-refine-labels-augmentation-of-the-training-dataset))

### Finished Refining Network
After you are finished refining your network, you can repeat the process starting at [create_training_dataset](#create-training-dataset) 

If after training the network generalizes well to the data, proceed to analyze new videos. Otherwise, consider labeling more data.


# Additional Resources

## About EnginFrame
NICE EnginFrame provides a 3d-accelerated remote desktop environment
on an Nvidia GPU-equipped compute node. Coupled with the proprietary
Desktop Cloud Visualization (DCV) VNC server, the EnginFrame service
supports the use of common visualization applications in a typical
desktop environment using only a modern web browser.

## Research Computing
- [https://www.nice-software.com/products/enginframe](https://www.nice-software.com/products/enginframe)
- [https://www.nice-software.com/products/dcv](https://www.nice-software.com/products/dcv)

## Deep Lab Cut (DLC)
## Help
In ipython/Jupyter notebook:
```
deeplabcut.nameofthefunction?
```
In python or pythonw:
```
help(deeplabcut.nameofthefunction)
```

### Tips for "daily" use:
<p align="center"> 
<img src= enginframe/daily.png format=1000w width="80%">
</p>

### Exiting/Returning
Linux/MacOS formatting example:
```
source activate yourdeeplabcutEnvName
ipython
import deeplabcut
config_path ='/home/yourprojectfolder/config.yaml'
```
Windows formatting example:
```
activate yourdeeplabcutEnvName
ipython
import deeplabcut
config_path = r'C:\home\yourprojectfolder\config.yaml'
```


# Credit 
* [Chase Dudas](https://github.com/ChaseD13) - Developer 
* RC - CU Boulder
* Andrew Monaghan
* [Mathis et al, 2018](https://www.nature.com/articles/s41593-018-0209-y)
* [Nath, Mathis et al, 2019](https://doi.org/10.1038/s41596-019-0176-0)
