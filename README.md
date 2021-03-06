# Document Orientation

When dealing with a big amount of scanned documents, some are scanned in the wrong direction. The goal of this code is to detect if the document has been scanned in the right way and if not, to rotate it so it can be used properly. As it's scanned documents the rotation applied will be 90, 180 or 270 degrees and not a skew from 0 to 359 degrees.

 - [Project Description](#prd)
 - [Installation](#ins)
 - [Usage](#use)


## <a name="prd"></a> Project Description

In order to detect the right orientation we first detect words one by one (or by group) and use a rectangle to plot its/their contour(s). This box is then cut horizontally into two parts and a mean of pixels' value is computed for each part. Part with the biggest mean (most ink displayed in the box) is declared as the upper part of the word. This is an assumption made for the french language as statistically in sentences there will be more letters with an upper part (b d f h i k l t é è à ù) than letters with a lower part (g j p q). We then rotate the image in order to have the upper part of the word orientated the right way.

## <a name="ins"></a> Installation

You need to install al dependencies and just clone the repo or copy paste the python file and run as described in [Usage](#use)

### Dependencies

Python packages used : numpy, argparse, cv2, time


## <a name="use"></a> Usage

You need to place documents to parse in the same directory than the python file and use this command to run :
```
python orientationDetectorOpenCV.py -i YOUR_INPUT_DIRECTORY -o YOUR_OUTPUT_DIRECTORY
```

# Contributing

We would love for you to contribute to help make it even better than it is today!
As a contributor, here are the guidelines we would like you to follow :

 - [Code of Conduct](#coc)
 - [Any Question](#aqu)
 - [Reporting Bugs](#rb)
 - [Suggesting Enhancements](#sa)
 - [Style Guide](#stg)

## <a name="coc"></a> Code of Conduct

Like many other projects, we have adopted [Contributor Covenant] https://www.contributor-covenant.org/ as our code of conduct and we hope that participants will adhere to it. 

Instances inacceptable behavior may be reported to the community leaders responsible for enforcement at guillaume.laulom@labanquepostale.fr 

## <a name="aqu"></a>Any question
If you have any question or issues you can post it in the [Issue Section](https://github.com/labanquepostale/DocumentOrientation/issues) with a proper label.

#### <a name="rb">Reporting bugs

Before reporting a bug, please make sure it hasn't already been reported by visiting the
[issue section](https://github.com/labanquepostale/DocumentOrientation/issues).

If the bug you found hasn't been reported yet, create a new issue and assign it the proper label(s).
Besides this, there isn't any specific guideline on how the bugs should be reported, Just be sure
to be as clear as possible when describing it.

#### <a name="sa"></a>Suggesting enhancements

Same as the bug reporting. First of all, check if the enhancement has already been suggested.
If it doesn't exist, create a new issue and give it the `enhancement` label, plus any other proper label.

Keep in mind that what you may find useful might be completely useless for other users,
so please, make sure that the enhancement can actually be useful for everyone before proposing it.
If you find that it is actually useful only for you, consider forking the project and implementing that
enhancement just for yourself.

#### <a name="stg"></a>Style Guide
Just use classic Python style and add comment to make it understandable if needed

# License
You can consult [the license in this section](https://github.com/labanquepostale/DocumentOrientation/blob/master/LICENSE)
