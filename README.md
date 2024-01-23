# 1.first:
概要：
Overview:<br>
This add-on has just been released and is not yet compatible with all rigs in all situations, but we will do our best to make it compatible.
<br>

 　However, we cannot guarantee that it will retarget correctly depending on the orientation and configuration of the bones.
　If you would like to request a response or report an error, please contact us oshigoto@makeinufilm.com (it may take some time to respond, and we may charge a fee for corporate clients, depending on the size of the project).
<br><br> Errors may occur depending on the environment, operating procedures, and rig configuration.
(If you send us the operation procedures and error messages, we will do our best to respond to your request.)
<br>**Bone layer and bone collection APIs are different between blender 3.6 and blender 4.0, so support for blender 4.0 and later will start after blender 4.3 LTS is released.
The operation has been verified with blender 3.6.2.

<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/1a9aeebd-f8ad-4b23-a2b8-584625388d8b" width="768">

*The images are bvh data of Chiyo, the original character, and text to motion with MoMask.
# 2.UI description:
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/18bd42b6-112e-4824-b4c9-d132726f3606" width="768">
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/faefc9f3-efe2-49a2-8313-2749b594a71c" width="768">

# 3.process description:

Setting Example:<br>
#### １．Registration of various armatures and bone names
<br>　I think the UI will look like the picture when it's done.
<br>　The *arms_group and *legs_group are partially blank, but with momaskBVH, they are blank because the wrist is oriented in the ZUP direction (if the wrist portion is blank, it is set to face the X axis).
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/d155d704-df2c-4f41-8166-ae14438b0cb3" width="768"><br>

#### ２．retarget_setting(FK_only)

Pressing the button assigns the constraint and at the same time the influence value of the constraint is displayed in the RetargetOffsetPanel
<br><br>
**If the image jumps in the Z direction, uncheck the Offset checkbox**.
　　root_offsetZ is for vertical correction and root_offsetXY is for horizontal correction.
<br>
The names and influences of other bones will be displayed, and you can adjust where you do not want the rotation to be reflected (e.g., turn off Neck and Head to reduce neck and head shake)<br><br>.
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/3bd9cda6-02be-4161-9a57-ccc2e2e21a11" width="768">
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/790326c8-951d-4c60-861a-7b5415881612" width="768"><br>

#### ２－clear_setting

Press the button to return to the original settings.
　If you have a bone with the same name, please rename it beforehand.

#### ３．Bake_Animation

<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/e9b169d3-b6ab-4614-a87d-e1721102f00a" width="768"><br>
Burn animation only on the registered target bones, done!

#### ４．IK_offset(Features not completed)
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/27eff023-ad47-43ea-8b6c-91581a59c4d3" width="768"><br>
I will do ...... when 4.3LTS comes. ......
I have a lot of things unorganized, but for now I have a function ...... that allows you to adjust the Root position, foot and hand position (_OFST_), but it is unstable at the moment.
<br>Bake_Animation will only bake the registered FK (deform) bones, not the IK, and the IK-related bones will be deleted.

## Operations that lead to errors:

Errors may occur depending on the operating procedure.<br>
1. do not hide (hide) the source and target bones [shortcut: H]<br>
2. if you have a control rig, do not check use IK offset<br>
3. IK offset is also deprecated in cases where there is no control rig and there is a twisting joint twist joint mechanism, etc. (This will be addressed in the future.)<br>
If you have no choice but to retarget with a scale of 0.01, please select Apply: (Apply) and apply delta scale.<br>
However, even in the above case, the coordinate position may jump, so **use the equal magnification setting** if possible.<br>
<img src="https://github.com/makeinufilm/mk_simple_retarget_addon/assets/157425559/8ae4db7b-8d6b-4cc9-92c5-a8adab491f59" width="384"><br>
<br>The above is for reference when importing FBXs exported by other DCC, scale is 100, check Automatic Bone Orientation<br>.
　After the import is complete, manually select all the FBX objects imported and match the scale: Apply: (Apply) All Transoform to normalize them.


## How to register blender for extras by AI

This add-on has just been released and is not compatible with all rigs in all situations. We will do our best, but we cannot guarantee that it will retarget correctly depending on the orientation and configuration of the bones.
　If you would like to request a response (although it may take some time), please contact us at oshigoto@makeinufilm.com (for corporate clients, depending on the size of the project, there may be a possibility of a paid response).
 　Please note that errors may occur depending on the environment, operating procedures, and rig configuration, and we cannot guarantee the operation of the rig (if you send us the operating procedures and error messages, we will do our best to respond).
**Because the bone layer and bone collection APIs are different between blender 3.6 and blender 4.0, we plan to start supporting blender 4.0 and later after blender 4.3 LTS is released.
The operation has been verified with blender 3.6.2.
Hello, Blender users! We are excited to introduce a new add-on developed to make your animation work in Blender easier and more efficient. It’s called “MK Simple Retarget”.

The main feature of this add-on is animation retargeting. This means you can apply one animation to another character. This allows you to reuse an animation you’ve created and apply it to various characters.

Here’s how to register this add-on in Blender:

Open Blender and click on “Edit” in the top menu.
Select “Preferences”.
From the menu on the left side of the window that opens, click on “Add-ons”.
Click on the “Install…” button at the top right.
Select the downloaded “mk_simple_retarget_00.py” and click the “Install Add-on” button.
The installed add-on will appear in the list. Enable it by checking the checkbox.
With that, you’ve successfully installed and enabled “MK Simple Retarget”. Now you can fully utilize the power of animation retargeting. Try using this add-on to make your animation creation more enjoyable and efficient.

For more details, please check the GitHub link below: GitHub Link

Happy Blending!

*The above greeting is written by bingAI What is happyblending, please tell me.

# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details
