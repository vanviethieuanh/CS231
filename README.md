# chroma-key

Remove chroma-key backgrounds by survey ROI (which found by edge detection)

### Problem

Basically, if we want to remove chroma-key backgrounds, we will use the color range to create the mask (for removing). But the problem here is how do we know the range for any image. So in most editing software (like Adobe Photoshop or Adobe Premiere), user must manually select the _key color_ or _backgrounds region_ for calculating (because sometime backgrounds is not green). We want the computer can select ROI by it own.

### Solution

In most case, the backgrounds is a flat region. So if we get image derivative, the backgrounds region will have lower engergy than main objects. We can use that for remove main object regions, calculate the rest (pixel which is not main objects) for removing backgrounds.

When we have the pixels of background we can use standard normal distribution for create mask to remove background.
