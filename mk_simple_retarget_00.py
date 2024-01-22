# MIT License.
# author makeinufilm
# -*- coding: utf-8 -*-

import bpy
import json
from bpy_extras.io_utils import ExportHelper

bl_info = {
    "name": "Simple MKRetarget System",
    "author": "makeinufilm",
    "version": (0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Tool Shelf > mk_tools",
    "description": "simple retarget tools",
    "warning": "",
    "wiki_url": "https://github.com/makeinufilm/mkn_blender_addon",
    "category": "3D View",
}
def change_ik_const():
    armaturetemp = bpy.context.scene.MK_ArmatureTemp
    bonetemp = bpy.context.scene.MK_BoneTemp
    target_armature = armaturetemp.target
    bpy.ops.object.mode_set(mode = "OBJECT")        
    bpy.ops.object.mode_set(mode = "POSE")    
    ikarm_l=target_armature.pose.bones.get(bonetemp.ta_hand_l)
    ikarm_r=target_armature.pose.bones.get(bonetemp.ta_hand_r)
    ikleg_l=target_armature.pose.bones.get(bonetemp.ta_ankle_l)
    ikleg_r=target_armature.pose.bones.get(bonetemp.ta_ankle_r)
    ikforearm_l=target_armature.pose.bones.get(bonetemp.ta_forearm_l)
    ikforearm_r=target_armature.pose.bones.get(bonetemp.ta_forearm_r)
    ikuparm_l=target_armature.pose.bones.get(bonetemp.ta_uparm_l)
    ikuparm_r=target_armature.pose.bones.get(bonetemp.ta_uparm_r)
    
    ikupleg_l=target_armature.pose.bones.get(bonetemp.ta_upleg_l)
    ikupleg_r=target_armature.pose.bones.get(bonetemp.ta_upleg_r)
    ikmleg_l=target_armature.pose.bones.get(bonetemp.ta_leg_l)
    ikmleg_r=target_armature.pose.bones.get(bonetemp.ta_leg_r)

    bonelistarm_r = [ikuparm_r,ikforearm_r,ikarm_r]
    bonelistarm_l = [ikuparm_l,ikforearm_l,ikarm_l]
    bonelistleg_r = [ikupleg_l,ikmleg_l,ikleg_l]
    bonelistleg_l = [ikupleg_r,ikmleg_r,ikleg_r]
    bonelistgrp = bonelistarm_r+bonelistarm_l+bonelistleg_r+bonelistleg_l
    for i in bpy.context.object.pose.bones:
        i.bone.select = False
    mkpo = [i for i in bpy.context.object.pose.bones if "MK_IKS" in i.name]
    mspo = [i for i in bpy.context.object.pose.bones if "MK_PVS" in i.name]
    master = mkpo + mspo
    for i in master:
        i.bone.select = True
    bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start,
                    frame_end = bpy.context.scene.frame_end,
                    visual_keying=True,
                     clear_constraints=True, bake_types={'POSE'})
    
    for posebone in bonelistgrp:
        pbco = posebone.constraints.get("MK_Copy Rotation")
        if pbco:
            pbco.target = target_armature
            pbco.subtarget = "MK_IK_"+posebone.name
            
    
    
def create_new_ik_bones():
    bpy.ops.object.mode_set(mode = "OBJECT")
    armaturetemp = bpy.context.scene.MK_ArmatureTemp
    bonetemp = bpy.context.scene.MK_BoneTemp
    target_armature = armaturetemp.target

    bpy.context.view_layer.objects.active = target_armature
    bpy.ops.object.mode_set(mode = "EDIT")
    
    ctrlbasebone = target_armature.data.edit_bones.new("MK_BASE_"+"CTRLGRP")
    ctrlbasebone.head = (0,0,0)
    ctrlbasebone.tail = (0,0,0.1)
    ctrlbone = target_armature.data.edit_bones.new("MK_BODY_"+"CTRLGRP")
    ctrlbone.head = (0,0,0.1)
    ctrlbone.tail = (0,0,0.2)
        
    ikarm_l=target_armature.data.edit_bones.get(bonetemp.ta_hand_l)
    ikarm_r=target_armature.data.edit_bones.get(bonetemp.ta_hand_r)
    ikleg_l=target_armature.data.edit_bones.get(bonetemp.ta_ankle_l)
    ikleg_r=target_armature.data.edit_bones.get(bonetemp.ta_ankle_r)
        
    ctrarm_l = target_armature.data.edit_bones.new("MK_OFST_"+"ARM_L")
    ctrarm_l.head =ikarm_l.head
    ctrarm_l.tail =ikarm_l.tail
    ctrarm_l.parent = ctrlbasebone
    ctrarm_r = target_armature.data.edit_bones.new("MK_OFST_"+"ARM_R")
    ctrarm_r.head =ikarm_r.head
    ctrarm_r.tail =ikarm_r.tail
    ctrarm_r.parent = ctrlbasebone
    ctrleg_l = target_armature.data.edit_bones.new("MK_OFST_"+"LEG_L")
    ctrleg_l.head =ikleg_l.head
    ctrleg_l.tail =ikleg_l.tail
    ctrleg_l.parent = ctrlbasebone
    ctrleg_r = target_armature.data.edit_bones.new("MK_OFST_"+"LEG_R")
    ctrleg_r.head =ikleg_r.head
    ctrleg_r.tail =ikleg_r.tail
    ctrleg_r.parent = ctrlbasebone       
    
    ikforearm_l=target_armature.data.edit_bones.get(bonetemp.ta_forearm_l)
    ikforearm_r=target_armature.data.edit_bones.get(bonetemp.ta_forearm_r)
    ikuparm_l=target_armature.data.edit_bones.get(bonetemp.ta_uparm_l)
    ikuparm_r=target_armature.data.edit_bones.get(bonetemp.ta_uparm_r)
    
    ikupleg_l=target_armature.data.edit_bones.get(bonetemp.ta_upleg_l)
    ikupleg_r=target_armature.data.edit_bones.get(bonetemp.ta_upleg_r)
    ikmleg_l=target_armature.data.edit_bones.get(bonetemp.ta_leg_l)
    ikmleg_r=target_armature.data.edit_bones.get(bonetemp.ta_leg_r)

    bonelistarm_r = [ikuparm_r,ikforearm_r,ikarm_r]
    bonelistarm_l = [ikuparm_l,ikforearm_l,ikarm_l]
    bonelistleg_r = [ikupleg_l,ikmleg_l,ikleg_l]
    bonelistleg_l = [ikupleg_r,ikmleg_r,ikleg_r]

    shol_l=target_armature.data.edit_bones.get(bonetemp.ta_shoulder_l)
    shol_r=target_armature.data.edit_bones.get(bonetemp.ta_shoulder_r)
    ikhips=target_armature.data.edit_bones.get(bonetemp.ta_hips)
        
    # 親ボーンのリストを作成します
    parent_bones = [shol_r, shol_l, ikhips, ikhips]

    # ボーンリストのリストを作成します
    bone_lists = [bonelistarm_r, bonelistarm_l, bonelistleg_r, bonelistleg_l]

    # 各ボーンリストに対してループを行います
    for j, bonelist in enumerate(bone_lists):
        for i, bone in enumerate(bonelist):
            if bone:
                ikbone = target_armature.data.edit_bones.new("MK_IK_"+bone.name)
                ikbone.head = bone.head
                ikbone.tail = bone.tail
                ikbone.roll = bone.roll
                if i == 0:
                    if parent_bones[j]:
                        ikbone.parent = parent_bones[j]
                else:
                    if bonelist[i-1]:
                        ikbone.parent = target_armature.data.edit_bones["MK_IK_"+bonelist[i-1].name]
                        
    if ikarm_l:
        mkik_arm_l = target_armature.data.edit_bones.new("MK_IKS_"+bonetemp.ta_hand_l)
        mkik_arm_l.head = ikarm_l.head
        mkik_arm_l.tail = ikarm_l.tail
        mkik_arm_l.roll = ikarm_l.roll
        mkik_arm_l.parent = ctrarm_l
        mkpv_arm_l = target_armature.data.edit_bones.new("MK_PVS_"+bonetemp.ta_hand_l)
        mkpv_arm_l.head = ikforearm_l.head
        mkpv_arm_l.head[1] = 0.4
        mkpv_arm_l.tail = ikforearm_l.head
        mkpv_arm_l.tail[1] = 0.5       
        mkpv_arm_l.roll = ikarm_l.roll
        mkpv_arm_l.parent = ctrarm_l
    
        mkfg_arm_l = target_armature.data.edit_bones.new("MK_FKG_"+bonetemp.ta_hand_l)
        mkfg_arm_l.head = mkpv_arm_l.head
        mkfg_arm_l.tail = mkpv_arm_l.tail  
        mkfg_arm_l.parent = ikuparm_l
                         
    if ikarm_r:
        mkik_arm_r = target_armature.data.edit_bones.new("MK_IKS_"+bonetemp.ta_hand_r)
        mkik_arm_r.head = ikarm_r.head
        mkik_arm_r.tail = ikarm_r.tail
        mkik_arm_r.roll = ikarm_r.roll
        mkik_arm_r.parent = ctrarm_r  
        mkpv_arm_r = target_armature.data.edit_bones.new("MK_PVS_"+bonetemp.ta_hand_r)
        mkpv_arm_r.head = ikforearm_r.head
        mkpv_arm_r.head[1] = 0.4
        mkpv_arm_r.tail = ikforearm_r.head
        mkpv_arm_r.tail[1] = 0.5      
        mkpv_arm_r.roll = ikarm_r.roll
        mkpv_arm_r.parent = ctrarm_r         
        mkfg_arm_r = target_armature.data.edit_bones.new("MK_FKG_"+bonetemp.ta_hand_r)        
        mkfg_arm_r.head = mkpv_arm_r.head
        mkfg_arm_r.tail = mkpv_arm_r.tail  
        mkfg_arm_r.parent = ikuparm_r
                                 
                                 
    if ikleg_l:
        mkik_leg_l = target_armature.data.edit_bones.new("MK_IKS_"+bonetemp.ta_ankle_l)
        mkik_leg_l.head = ikleg_l.head
        mkik_leg_l.tail = ikleg_l.tail
        mkik_leg_l.roll = ikleg_l.roll 
        mkik_leg_l.parent = ctrleg_l
        mkpv_leg_l = target_armature.data.edit_bones.new("MK_PVS_"+bonetemp.ta_ankle_l)
        mkpv_leg_l.head = ikmleg_l.head
        mkpv_leg_l.head[1] = ikmleg_l.head[1]-0.4
        mkpv_leg_l.tail = ikmleg_l.head
        mkpv_leg_l.tail[1] = ikmleg_l.head[1]-0.5
        mkpv_leg_l.roll = ikleg_l.roll
        mkpv_leg_l.parent = ctrleg_l
        mkfg_leg_l = target_armature.data.edit_bones.new("MK_FKG_"+bonetemp.ta_ankle_l)         
        mkfg_leg_l.head = mkpv_leg_l.head
        mkfg_leg_l.tail = mkpv_leg_l.tail  
        mkfg_leg_l.parent = ikupleg_l
                                                    
    if ikleg_r:
        mkik_leg_r = target_armature.data.edit_bones.new("MK_IKS_"+bonetemp.ta_ankle_r)
        mkik_leg_r.head = ikleg_r.head
        mkik_leg_r.tail = ikleg_r.tail
        mkik_leg_r.roll = ikleg_r.roll  
        mkik_leg_r.parent = ctrleg_r    
        mkpv_leg_r = target_armature.data.edit_bones.new("MK_PVS_"+bonetemp.ta_ankle_r)
        mkpv_leg_r.head = ikmleg_r.head
        mkpv_leg_r.head[1] = ikmleg_r.head[1]-0.4
        mkpv_leg_r.tail = ikmleg_r.head
        mkpv_leg_r.tail[1] = ikmleg_r.head[1]-0.5
        mkpv_leg_r.parent = ctrleg_r
        mkfg_leg_r = target_armature.data.edit_bones.new("MK_FKG_"+bonetemp.ta_ankle_r)       
        mkfg_leg_r.head = mkpv_leg_r.head
        mkfg_leg_r.tail = mkpv_leg_r.tail  
        mkfg_leg_r.parent = ikupleg_r
                
         
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.ops.object.mode_set(mode = "POSE")

    ikconarmbone_r = target_armature.pose.bones["MK_IK_"+bonetemp.ta_forearm_r]
    ikconarmbone_l = target_armature.pose.bones["MK_IK_"+bonetemp.ta_forearm_l]
    ikconlegbone_r = target_armature.pose.bones["MK_IK_"+bonetemp.ta_leg_r]
    ikconlegbone_l = target_armature.pose.bones["MK_IK_"+bonetemp.ta_leg_l]
    pvconarmbone_r = target_armature.pose.bones["MK_PVS_"+bonetemp.ta_hand_r]
    pvconarmbone_l = target_armature.pose.bones["MK_PVS_"+bonetemp.ta_hand_l]
    pvconlegbone_r = target_armature.pose.bones["MK_PVS_"+bonetemp.ta_ankle_r]
    pvconlegbone_l = target_armature.pose.bones["MK_PVS_"+bonetemp.ta_ankle_l]
    isconarmbone_r = target_armature.pose.bones["MK_IKS_"+bonetemp.ta_hand_r]
    isconarmbone_l = target_armature.pose.bones["MK_IKS_"+bonetemp.ta_hand_l]
    isconlegbone_r = target_armature.pose.bones["MK_IKS_"+bonetemp.ta_ankle_r]
    isconlegbone_l = target_armature.pose.bones["MK_IKS_"+bonetemp.ta_ankle_l]
    pvlistaget = ["MK_FKG_"+bonetemp.ta_hand_r,"MK_FKG_"+bonetemp.ta_hand_l,"MK_FKG_"+bonetemp.ta_ankle_r,"MK_FKG_"+bonetemp.ta_ankle_l,
                bonetemp.ta_hand_r,bonetemp.ta_hand_l,bonetemp.ta_ankle_r,bonetemp.ta_ankle_l]        
    conpvlis = [pvconarmbone_r,pvconarmbone_l,pvconlegbone_r,pvconlegbone_l,
                isconarmbone_r,isconarmbone_l,isconlegbone_r,isconlegbone_l]
    coniklis = [ikconarmbone_r,ikconarmbone_l]
    coniklis_a =[ikconlegbone_r,ikconlegbone_l]

    contaget = ["MK_IKS_"+bonetemp.ta_hand_r,"MK_IKS_"+bonetemp.ta_hand_l]
    contaget_a =["MK_IKS_"+bonetemp.ta_ankle_r,"MK_IKS_"+bonetemp.ta_ankle_l]
    
    contagep = ["MK_PVS_"+bonetemp.ta_hand_r,"MK_PVS_"+bonetemp.ta_hand_l]
    contagep_a =["MK_PVS_"+bonetemp.ta_ankle_r,"MK_PVS_"+bonetemp.ta_ankle_l]
    
    for con,tage,pvage in zip(coniklis,contaget,contagep):
        co = con.constraints.new(type="IK")  
        co.target = target_armature
        co.subtarget = tage 
        co.pole_target = target_armature      
        co.pole_subtarget = pvage
        co.pole_angle = 3.14159                       
        co.chain_count = 2
        co.use_tail = True
        co.use_rotation = False

    for con,tage,pvage in zip(coniklis_a,contaget_a,contagep_a):
        co = con.constraints.new(type="IK")  
        co.target = target_armature
        co.subtarget = tage 
        co.pole_target = target_armature      
        co.pole_subtarget = pvage                           
        co.chain_count = 2
        co.use_tail = True
        co.use_rotation = False

    for con,tag in zip(conpvlis,pvlistaget):
        co = con.constraints.new(type="COPY_TRANSFORMS")
        co.target = target_armature
        co.subtarget = tag
          
            
def get_bone_data(armature, bone_names):
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = "EDIT")

    bone_data = []
    for bname in bone_names:
        if bname:
            bone = armature.data.edit_bones.get(bname)
            if bone:
                diff = bone.tail - bone.head
                bone_data.append((bone.head, bone.tail, bone.roll, diff))
            else:
                bone_data.append((None, None, None, None))
        else:
            bone_data.append((None, None, None, None))
    return bone_data

def create_new_bones(armature, source_bone_names, target_bone_data):
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = "EDIT")

    new_bone_names = []
    for bname, (head, tail, roll, diff) in zip(source_bone_names, target_bone_data):
        if bname and head is not None:
            source_bone = armature.data.edit_bones.get(bname)
            if source_bone:
                findbone = armature.data.edit_bones.get("MK_"+bname)
                
                if findbone:
                    new_bone = findbone
                else:
                    new_bone = armature.data.edit_bones.new("MK_"+bname)
                new_bone_names.append(new_bone.name)
                new_bone.head = source_bone.head
                new_bone.tail = new_bone.head + diff
                new_bone.roll = roll
                new_bone.parent = source_bone
            else:
                new_bone_names.append("")
        else:
            new_bone_names.append("")
    return new_bone_names

def get_root_location(target_armature,source_armature):
    bonetemp = bpy.context.scene.MK_BoneTemp
  
    bpy.ops.object.mode_set(mode = "OBJECT")


    # アクティブなオブジェクトを取得します
    obj = target_armature
    # 指定したボーンのポーズ行列を取得します
    pose_matrix = obj.pose.bones[bonetemp.ta_hips].matrix
    # ポーズ行列をグローバル座標系に変換します
    global_pose_matrix = obj.matrix_world @ pose_matrix
    # Z方向のグローバル位置座標を取得します
    tag_root_pos = global_pose_matrix.translation.z    
        
    # アクティブなオブジェクトを取得します
    obj = source_armature
    # 指定したボーンのポーズ行列を取得します
    pose_matrix = obj.pose.bones[bonetemp.so_hips].matrix
    # ポーズ行列をグローバル座標系に変換します
    global_pose_matrix = obj.matrix_world @ pose_matrix
    # Z方向のグローバル位置座標を取得します
    sou_root_pos = global_pose_matrix.translation.z    
            
    def_value = tag_root_pos * sou_root_pos
    return def_value

def get_root_invertbool(armature):
    bonetemp = bpy.context.scene.MK_BoneTemp

    # Check if the bone exists
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.ops.object.mode_set(mode = "EDIT")
    bone = armature.data.edit_bones.get(bonetemp.ta_hips)
    if bone is not None:
        root_pos = bone.tail[2] - bone.head[2]
        if root_pos >= 0.0:
            bool = True
        else:
            bool = False
    else:
        print(f"Bone '{bonetemp.ta_hips}' not found in armature '{armature.name}'")
        bool = False  # Or any other default value

    return bool

def get_root_bonehead(armature):
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = "EDIT")   
    bonetemp = bpy.context.scene.MK_BoneTemp

    root_pos = armature.data.edit_bones[bonetemp.ta_hips].head[2]
    return root_pos

def get_root_multiple(difference,root_pos,target_armature):
    bpy.ops.object.mode_set(mode = "OBJECT")    
    root_multi =  root_pos /difference
    root_multi = root_multi* -1
    return root_multi

def set_root_position(bool,difference,root_pos,target_armature):
    bpy.ops.object.mode_set(mode = "OBJECT")    
    rootfix = difference /root_pos
    if bool:
        rootfix = rootfix * -1
    bonetemp = bpy.context.scene.MK_BoneTemp

    target_armature.pose.bones[bonetemp.ta_hips].location[1] = rootfix
    return rootfix
def t_to_a_bones(armature):
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = "EDIT")
    
    new_bone_names = []
    bonetemp = bpy.context.scene.MK_BoneTemp

    sourcebone_name_l = [bonetemp.so_shoulder_l,bonetemp.so_uparm_l,bonetemp.so_forearm_l,bonetemp.so_hand_l,bonetemp.so_hand_l]
    sourcebone_name_r = [bonetemp.so_shoulder_r,bonetemp.so_uparm_r,bonetemp.so_forearm_r,bonetemp.so_hand_r,bonetemp.so_hand_r]    
    
    for i, bonename in enumerate(sourcebone_name_l):  # Exclude the last element
        if i <= 2:
            source_bone = armature.data.edit_bones.get(bonename)
            if source_bone:
                mkbone = armature.data.edit_bones.get("MK_"+bonename)
                bn = armature.data.edit_bones.get(bonename)
                tgbone = armature.data.edit_bones.get("MK_"+sourcebone_name_l[i+1])
                if mkbone and tgbone:
                    mkbone.tail = tgbone.head
                else:
                    mkbone.tail = bn.tail         
                    mkbone.tail[0] = bn.tail[0] +0.01
                    
        elif i == 3:
            source_bone = armature.data.edit_bones.get(bonename)
            if source_bone:
                mkbone = armature.data.edit_bones.get("MK_"+bonename)     
                tgbone = armature.data.edit_bones.get(sourcebone_name_l[i+1])
                if mkbone and tgbone:
                    mkbone.tail = tgbone.tail
         
    for i, bonename in enumerate(sourcebone_name_r):  # Exclude the last element
        if i <= 2:
            source_bone = armature.data.edit_bones.get(bonename)
            if source_bone:
                mkbone = armature.data.edit_bones.get("MK_"+bonename)
                bn = armature.data.edit_bones.get(bonename)     
                tgbone = armature.data.edit_bones.get("MK_"+sourcebone_name_r[i+1])
                if tgbone:
                    mkbone.tail = tgbone.head
                else:
                    mkbone.tail = bn.tail         
                    mkbone.tail[0] = bn.tail[0] +0.01
                    
        elif i == 3:
            source_bone = armature.data.edit_bones.get(bonename)
            if source_bone:
                mkbone = armature.data.edit_bones.get("MK_"+bonename)     
                tgbone = armature.data.edit_bones.get(sourcebone_name_r[i+1])
                if mkbone and tgbone:                
                    mkbone.tail = tgbone.tail                      
                    
    bpy.ops.object.mode_set(mode = "OBJECT")  


    bpy.ops.object.mode_set(mode = "OBJECT")
def add_constraints(target_armature, source_armature, target_bone_names, new_bone_names,bool,dif):
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.context.view_layer.objects.active = target_armature
    bpy.ops.object.mode_set(mode = "POSE")

    for i, (tname, nname) in enumerate(zip(target_bone_names, new_bone_names)):
        if tname and nname:
            target_bone = target_armature.pose.bones.get(tname)
            if target_bone:
                constraint = target_bone.constraints.new(type="COPY_ROTATION")
                constraint.name = "MK_"+constraint.name
                constraint.target = source_armature
                constraint.subtarget = nname
                if dif <= 0.0:
                    dif * -1.0
                if i == 0 and bool:
                    # Add two COPY_LOCATION constraints for the first bone
                    loc_constraint1 = target_bone.constraints.new(type="TRANSFORM")
                    loc_constraint1.name = "MK_"+loc_constraint1.name+"_XY"
                    loc_constraint1.target = source_armature
                    loc_constraint1.subtarget = nname
                    loc_constraint1.target_space = 'WORLD'
                    loc_constraint1.owner_space = 'WORLD'
                    loc_constraint1.from_min_x = -100
                    loc_constraint1.from_max_x = 100 
                    loc_constraint1.from_min_y = -100
                    loc_constraint1.from_max_y = 100 
                    loc_constraint1.to_min_x = 100 * dif
                    loc_constraint1.to_max_x = -100 * dif
                    loc_constraint1.to_min_y = 100 * dif
                    loc_constraint1.to_max_y = -100 * dif                    

                    loc_constraint2 = target_bone.constraints.new(type="COPY_LOCATION")
                    loc_constraint2.name = "MK_"+loc_constraint2.name+"_Z"
                    loc_constraint2.target = source_armature
                    loc_constraint2.subtarget = nname
                    loc_constraint2.use_offset = True
                    loc_constraint2.target_space = 'WORLD'
                    loc_constraint2.owner_space = 'WORLD'
                    loc_constraint2.use_x = False
                    loc_constraint2.use_y = False
                    loc_constraint2.use_z = True

def remove_constraints(armature):
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = "POSE")

    for b in armature.pose.bones:
        if b.constraints:
            for constraint in b.constraints:
                if "MK_" in constraint.name: 
                    b.constraints.remove(constraint)
    bpy.ops.object.mode_set(mode = "OBJECT")

def remove_bones(armature):
    bpy.ops.object.mode_set(mode = "OBJECT")
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode = "EDIT")

    for bname in armature.data.edit_bones:
        if "MK_" in bname.name:
            armature.data.edit_bones.remove(bname)
            
    bpy.ops.object.mode_set(mode = "OBJECT")


class MK_OT_Retarget(bpy.types.Operator):
    bl_idname = "mkn.retarget"
    bl_label = "retarget_setting(FK only)"
    def execute(self, context):
        bpy.ops.object.mode_set(mode = "OBJECT") 
        #print("Selected file:", self.filepath)
        armaturetemp = bpy.context.scene.MK_ArmatureTemp
        target_armature = armaturetemp.target
        bpy.context.view_layer.objects.active = target_armature
        if not target_armature.data.bones.get("MK_BASE_CTRLGRP"):
            source_armature = armaturetemp.source
            bpy.ops.object.mode_set(mode = "OBJECT")            
            bpy.ops.object.mode_set(mode = "EDIT")           
            settingbone = target_armature.data.edit_bones.new("MK_BASE_CTRLGRP")
            settingbone.head=(0,0,0)
            settingbone.tail=(0,0,0.01)
            bpy.ops.object.mode_set(mode = "OBJECT")            
            bonetemp = bpy.context.scene.MK_BoneTemp

            target_bone_names = [bonetemp.ta_hips,bonetemp.ta_spine,bonetemp.ta_spine1,bonetemp.ta_chest,bonetemp.ta_neck,bonetemp.ta_head,
                bonetemp.ta_shoulder_l,bonetemp.ta_uparm_l,bonetemp.ta_forearm_l,bonetemp.ta_hand_l,
                bonetemp.ta_shoulder_r,bonetemp.ta_uparm_r,bonetemp.ta_forearm_r,bonetemp.ta_hand_r,
                bonetemp.ta_upleg_l,bonetemp.ta_leg_l,bonetemp.ta_ankle_l,bonetemp.ta_toes_l,
                bonetemp.ta_upleg_r,bonetemp.ta_leg_r,bonetemp.ta_ankle_r,bonetemp.ta_toes_r]
            source_bone_names = [bonetemp.so_hips,bonetemp.so_spine,bonetemp.so_spine1,bonetemp.so_chest,bonetemp.so_neck,bonetemp.so_head,
                bonetemp.so_shoulder_l,bonetemp.so_uparm_l,bonetemp.so_forearm_l,bonetemp.so_hand_l,
                bonetemp.so_shoulder_r,bonetemp.so_uparm_r,bonetemp.so_forearm_r,bonetemp.so_hand_r,
                bonetemp.so_upleg_l,bonetemp.so_leg_l,bonetemp.so_ankle_l,bonetemp.so_toes_l,
                bonetemp.so_upleg_r,bonetemp.so_leg_r,bonetemp.so_ankle_r,bonetemp.so_toes_r]

            if context.scene.MK_BoolTemp.fing_bool: 
                fingtemp = bpy.context.scene.MK_FingBoneTemp
                tafing_bone_names = [fingtemp.ta_index_a_l,fingtemp.ta_index_b_l,fingtemp.ta_index_c_l,fingtemp.ta_middle_a_l,fingtemp.ta_middle_b_l,fingtemp.ta_middle_c_l,
                    fingtemp.ta_ring_a_l,fingtemp.ta_ring_b_l,fingtemp.ta_ring_c_l,fingtemp.ta_pinky_a_l,fingtemp.ta_pinky_b_l,fingtemp.ta_pinky_c_l,fingtemp.ta_thumb_a_l,fingtemp.ta_thumb_b_l,fingtemp.ta_thumb_c_l,
                    fingtemp.ta_index_a_r,fingtemp.ta_index_b_r,fingtemp.ta_index_c_r,fingtemp.ta_middle_a_r,fingtemp.ta_middle_b_r,fingtemp.ta_middle_c_r,
                    fingtemp.ta_ring_a_r,fingtemp.ta_ring_b_r,fingtemp.ta_ring_c_r,fingtemp.ta_pinky_a_r,fingtemp.ta_pinky_b_r,fingtemp.ta_pinky_c_r,fingtemp.ta_thumb_a_r,fingtemp.ta_thumb_b_r,fingtemp.ta_thumb_c_r]
                sofing_bone_names = [fingtemp.so_index_a_l,fingtemp.so_index_b_l,fingtemp.so_index_c_l,fingtemp.so_middle_a_l,fingtemp.so_middle_b_l,fingtemp.so_middle_c_l,
                    fingtemp.so_ring_a_l,fingtemp.so_ring_b_l,fingtemp.so_ring_c_l,fingtemp.so_pinky_a_l,fingtemp.so_pinky_b_l,fingtemp.so_pinky_c_l,fingtemp.so_thumb_a_l,fingtemp.so_thumb_b_l,fingtemp.so_thumb_c_l,
                    fingtemp.so_index_a_r,fingtemp.so_index_b_r,fingtemp.so_index_c_r,fingtemp.so_middle_a_r,fingtemp.so_middle_b_r,fingtemp.so_middle_c_r,
                    fingtemp.so_ring_a_r,fingtemp.so_ring_b_r,fingtemp.so_ring_c_r,fingtemp.so_pinky_a_r,fingtemp.so_pinky_b_r,fingtemp.so_pinky_c_r,fingtemp.so_thumb_a_r,fingtemp.so_thumb_b_r,fingtemp.so_thumb_c_r]
                tafing_bone_data = get_bone_data(target_armature, tafing_bone_names)
                # 新しいボーンを作成
                new_fing_names = create_new_bones(source_armature, sofing_bone_names, tafing_bone_data)
                # 制約を追加
                add_constraints(target_armature, source_armature, tafing_bone_names, new_fing_names,False,0)            
                    
            # ボーンを取得
            target_bone_data = get_bone_data(target_armature, target_bone_names)
            # 新しいボーンを作成
            new_bone_names = create_new_bones(source_armature, source_bone_names, target_bone_data)
            # 制約を追加
            difloc = get_root_location(target_armature,source_armature)

            t_to_a_bones(source_armature)
            bool = get_root_invertbool(target_armature)
            location = get_root_bonehead(target_armature)
            difvalue = set_root_position(bool,difloc,location,target_armature)
            difmulti = get_root_multiple(difloc,location,target_armature)
            add_constraints(target_armature, source_armature, target_bone_names, new_bone_names,True,difmulti)
            
            context.scene['show_retarget_offset_panel'] = True
            
        return {'FINISHED'}
    
class MK_OT_IKRetarget(bpy.types.Operator):
    bl_idname = "mkn.ikretarget"
    bl_label = "retarget_setting(offset IK)"
    
    def execute(self, context):
        armaturetemp = bpy.context.scene.MK_ArmatureTemp
        target_armature = armaturetemp.target
        bpy.context.view_layer.objects.active = target_armature
        if not target_armature.data.bones.get("MK_BASE_CTRLGRP"):

            source_armature = armaturetemp.source

            bonetemp = bpy.context.scene.MK_BoneTemp
            target_bone_names = [bonetemp.ta_hips,bonetemp.ta_spine,bonetemp.ta_spine1,bonetemp.ta_chest,bonetemp.ta_neck,bonetemp.ta_head,
                bonetemp.ta_shoulder_l,bonetemp.ta_uparm_l,bonetemp.ta_forearm_l,bonetemp.ta_hand_l,
                bonetemp.ta_shoulder_r,bonetemp.ta_uparm_r,bonetemp.ta_forearm_r,bonetemp.ta_hand_r,
                bonetemp.ta_upleg_l,bonetemp.ta_leg_l,bonetemp.ta_ankle_l,bonetemp.ta_toes_l,
                bonetemp.ta_upleg_r,bonetemp.ta_leg_r,bonetemp.ta_ankle_r,bonetemp.ta_toes_r]
            source_bone_names = [bonetemp.so_hips,bonetemp.so_spine,bonetemp.so_spine1,bonetemp.so_chest,bonetemp.so_neck,bonetemp.so_head,
                bonetemp.so_shoulder_l,bonetemp.so_uparm_l,bonetemp.so_forearm_l,bonetemp.so_hand_l,
                bonetemp.so_shoulder_r,bonetemp.so_uparm_r,bonetemp.so_forearm_r,bonetemp.so_hand_r,
                bonetemp.so_upleg_l,bonetemp.so_leg_l,bonetemp.so_ankle_l,bonetemp.so_toes_l,
                bonetemp.so_upleg_r,bonetemp.so_leg_r,bonetemp.so_ankle_r,bonetemp.so_toes_r]

            if context.scene.MK_BoolTemp.fing_bool: 
                fingtemp = bpy.context.scene.MK_FingBoneTemp
                tafing_bone_names = [fingtemp.ta_index_a_l,fingtemp.ta_index_b_l,fingtemp.ta_index_c_l,fingtemp.ta_middle_a_l,fingtemp.ta_middle_b_l,fingtemp.ta_middle_c_l,
                    fingtemp.ta_ring_a_l,fingtemp.ta_ring_b_l,fingtemp.ta_ring_c_l,fingtemp.ta_pinky_a_l,fingtemp.ta_pinky_b_l,fingtemp.ta_pinky_c_l,fingtemp.ta_thumb_a_l,fingtemp.ta_thumb_b_l,fingtemp.ta_thumb_c_l,
                    fingtemp.ta_index_a_r,fingtemp.ta_index_b_r,fingtemp.ta_index_c_r,fingtemp.ta_middle_a_r,fingtemp.ta_middle_b_r,fingtemp.ta_middle_c_r,
                    fingtemp.ta_ring_a_r,fingtemp.ta_ring_b_r,fingtemp.ta_ring_c_r,fingtemp.ta_pinky_a_r,fingtemp.ta_pinky_b_r,fingtemp.ta_pinky_c_r,fingtemp.ta_thumb_a_r,fingtemp.ta_thumb_b_r,fingtemp.ta_thumb_c_r]
                sofing_bone_names = [fingtemp.so_index_a_l,fingtemp.so_index_b_l,fingtemp.so_index_c_l,fingtemp.so_middle_a_l,fingtemp.so_middle_b_l,fingtemp.so_middle_c_l,
                    fingtemp.so_ring_a_l,fingtemp.so_ring_b_l,fingtemp.so_ring_c_l,fingtemp.so_pinky_a_l,fingtemp.so_pinky_b_l,fingtemp.so_pinky_c_l,fingtemp.so_thumb_a_l,fingtemp.so_thumb_b_l,fingtemp.so_thumb_c_l,
                    fingtemp.so_index_a_r,fingtemp.so_index_b_r,fingtemp.so_index_c_r,fingtemp.so_middle_a_r,fingtemp.so_middle_b_r,fingtemp.so_middle_c_r,
                    fingtemp.so_ring_a_r,fingtemp.so_ring_b_r,fingtemp.so_ring_c_r,fingtemp.so_pinky_a_r,fingtemp.so_pinky_b_r,fingtemp.so_pinky_c_r,fingtemp.so_thumb_a_r,fingtemp.so_thumb_b_r,fingtemp.so_thumb_c_r]
                tafing_bone_data = get_bone_data(target_armature, tafing_bone_names)
                # 新しいボーンを作成
                new_fing_names = create_new_bones(source_armature, sofing_bone_names, tafing_bone_data)
                # 制約を追加
                add_constraints(target_armature, source_armature, tafing_bone_names, new_fing_names,False,0)            
                    
            # ボーンを取得
            target_bone_data = get_bone_data(target_armature, target_bone_names)
            # 新しいボーンを作成
            new_bone_names = create_new_bones(source_armature, source_bone_names, target_bone_data)
            # 制約を追加
            difloc = get_root_location(target_armature,source_armature)

            t_to_a_bones(source_armature)
            bool = get_root_invertbool(target_armature)
            location = get_root_bonehead(target_armature)
            difvalue = set_root_position(bool,difloc,location,target_armature)
            difmulti = get_root_multiple(difloc,location,target_armature)
            add_constraints(target_armature, source_armature, target_bone_names, new_bone_names,True,difmulti)
            create_new_ik_bones()
            change_ik_const()
            context.scene['show_retarget_offset_panel'] = True
            
        return {'FINISHED'}
    
class MK_OT_Clear(bpy.types.Operator):
    bl_idname = "mkn.clear"
    bl_label = "clear_setting"
    def execute(self, context):
        #print("Selected file:", self.filepath)
        armaturetemp = bpy.context.scene.MK_ArmatureTemp
        target_armature = armaturetemp.target
        source_armature = armaturetemp.source
        bpy.context.view_layer.objects.active = target_armature
        # 制約を削除
        remove_constraints(target_armature)

        # ボーンを削除
        remove_bones(source_armature)
        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode = "OBJECT")
        bpy.ops.object.mode_set(mode = "POSE")
        remove_bones(target_armature)
        bpy.ops.object.mode_set(mode = "OBJECT")
        bpy.ops.object.mode_set(mode = "POSE")        
        target_armature.pose.bones[0].bone.select = True   
        bpy.ops.pose.select_all(action='SELECT')
        target_armature.animation_data_clear()
        bpy.ops.pose.transforms_clear()
        bpy.ops.object.mode_set(mode = "OBJECT")
        
        context.scene['show_retarget_offset_panel'] = False 
        return {'FINISHED'}

class MK_OT_Bake(bpy.types.Operator):
    bl_idname = "mkn.bake"
    bl_label = "bake_animation"
    def execute(self, context):
        #print("Selected file:", self.filepath)
        armaturetemp = bpy.context.scene.MK_ArmatureTemp
        target_armature = armaturetemp.target
        bpy.context.view_layer.objects.active = target_armature        

        source_armature = armaturetemp.source
        bonetemp = bpy.context.scene.MK_BoneTemp
        bpy.ops.object.mode_set(mode = "OBJECT")
        bpy.ops.object.mode_set(mode = "POSE")
 
        for pb in target_armature.pose.bones:
            pb.bone.select = False       
        target_bone_names = [bonetemp.ta_hips,bonetemp.ta_spine,bonetemp.ta_spine1,bonetemp.ta_chest,bonetemp.ta_neck,bonetemp.ta_head,
            bonetemp.ta_shoulder_l,bonetemp.ta_uparm_l,bonetemp.ta_forearm_l,bonetemp.ta_hand_l,
            bonetemp.ta_shoulder_r,bonetemp.ta_uparm_r,bonetemp.ta_forearm_r,bonetemp.ta_hand_r,
            bonetemp.ta_upleg_l,bonetemp.ta_leg_l,bonetemp.ta_ankle_l,bonetemp.ta_toes_l,
            bonetemp.ta_upleg_r,bonetemp.ta_leg_r,bonetemp.ta_ankle_r,bonetemp.ta_toes_r]

        for spb in target_bone_names:
            target_armature.pose.bones[spb].bone.select = True
        bpy.ops.nla.bake(frame_start=bpy.context.scene.frame_start,
                        frame_end=bpy.context.scene.frame_end,
                        only_selected=True,
                        visual_keying=True,
                        clear_constraints=True,
                        bake_types={'POSE'})
        remove_constraints(target_armature)
        remove_bones(target_armature)
        bpy.ops.object.mode_set(mode = "OBJECT")
        bpy.ops.object.mode_set(mode = "POSE")   
        context.scene['show_retarget_offset_panel'] = False 
        return {'FINISHED'}

class MK_OT_BoneMapRenameLR(bpy.types.Operator):
    bl_idname = "mkn.bonemap_lrchange"
    bl_label = "L to R"
    def execute(self, context):
        #print("Selected file:", self.filepath)
        bonetemp = bpy.context.scene.MK_BoneTemp
        # Define a list of bone names
        bone_names = ["shoulder", "uparm", "forearm", "hand", "upleg", "leg", "ankle", "toes"]

        # Loop over each bone name
        for bone_name in bone_names:
            # Get the left bone attribute
            left_bone_ta = getattr(bonetemp, f"ta_{bone_name}_l")
            left_bone_so = getattr(bonetemp, f"so_{bone_name}_l")

            # If ".l" is in the left bone name, replace it with ".r" and set the right bone attribute
            if ".l" in left_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace(".l", ".r"))
            elif ".L" in left_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace(".L", ".R"))
            elif "_l" in left_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace("_l", "_r"))
            elif "_L" in left_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace("_L", "_R"))
            elif "_L_" in left_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace("_L_", "_R_"))
            elif "Left" in left_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace("Left", "Right"))             
            elif "LEFT" in left_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace("LEFT", "RIGHT"))
            elif "left" in left_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_r", left_bone_ta.replace("left", "right"))               

            if ".l" in left_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace(".l", ".r"))
            elif ".L" in left_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace(".L", ".R"))
            elif "_l" in left_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace("_l", "_r"))
            elif "_L" in left_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace("_L", "_R"))
            elif "_L_" in left_bone_so:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace("_L_", "_R_"))
            elif "Left" in left_bone_so:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace("Left", "Right"))               
            elif "LEFT" in left_bone_so:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace("LEFT", "RIGHT"))               
            elif "left" in left_bone_so:
                setattr(bonetemp, f"so_{bone_name}_r", left_bone_so.replace("left", "right"))               

        fingtemp = bpy.context.scene.MK_FingBoneTemp
        fing_names = ["index_a", "index_b", "index_c", "middle_a", "middle_b", "middle_c",
                    "ring_a", "ring_b","ring_c","pinky_a","pinky_b","pinky_c","thumb_a","thumb_b","thumb_c"]
        for bone_name in fing_names:                        
            left_bone_ta = getattr(fingtemp, f"ta_{bone_name}_l")
            left_bone_so = getattr(fingtemp, f"so_{bone_name}_l")
            # If ".l" is in the left bone name, replace it with ".r" and set the right bone attribute
            if ".l" in left_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace(".l", ".r"))
            elif ".L" in left_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace(".L", ".R"))
            elif "_l" in left_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace("_l", "_r"))
            elif "_L" in left_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace("_L", "_R"))
            elif "_L_" in left_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace("_L_", "_R_"))
            elif "Left" in left_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace("Left", "Right"))             
            elif "LEFT" in left_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace("LEFT", "RIGHT"))
            elif "left" in left_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_r", left_bone_ta.replace("left", "right"))               

            if ".l" in left_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace(".l", ".r"))
            elif ".L" in left_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace(".L", ".R"))
            elif "_l" in left_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace("_l", "_r"))
            elif "_L" in left_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace("_L", "_R"))
            elif "_L_" in left_bone_so:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace("_L_", "_R_"))
            elif "Left" in left_bone_so:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace("Left", "Right"))               
            elif "LEFT" in left_bone_so:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace("LEFT", "RIGHT"))               
            elif "left" in left_bone_so:
                setattr(fingtemp, f"so_{bone_name}_r", left_bone_so.replace("left", "right"))                      

        return {'FINISHED'}
    
class MK_OT_BoneMapRenameRL(bpy.types.Operator):
    bl_idname = "mkn.bonemap_rlchange"
    bl_label = "R to L"
    def execute(self, context):
        bonetemp = bpy.context.scene.MK_BoneTemp
        # Define a list of bone names
        bone_names = ["shoulder", "uparm", "forearm", "hand", "upleg", "leg", "ankle", "toes"]

        # Loop over each bone name
        for bone_name in bone_names:
            # Get the right bone attribute
            right_bone_ta = getattr(bonetemp, f"ta_{bone_name}_r")
            right_bone_so = getattr(bonetemp, f"so_{bone_name}_r")

            # If ".r" is in the right bone name, replace it with ".l" and set the left bone attribute
            if ".r" in right_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace(".r", ".l"))
            elif ".R" in right_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace(".R", ".L"))
            elif "_r" in right_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace("_r", "_l"))
            elif "_R" in right_bone_ta[-2:]:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace("_R", "_L"))
            elif "_R_" in right_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace("_R_","_L_"))
            elif "Right" in right_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace("Right", "Left"))             
            elif "RIGHT" in right_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace("RIGHT", "LEFT"))
            elif "right" in right_bone_ta:
                setattr(bonetemp, f"ta_{bone_name}_l", right_bone_ta.replace("right", "left"))               

            if ".r" in right_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace(".r", ".l"))
            elif ".R" in right_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace(".R", ".L"))
            elif "_r" in right_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace("_r", "_l"))
            elif "_R" in right_bone_so[-2:]:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace("_R", "_L"))
            elif "_R_" in right_bone_so:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace("_R_","_L_"))
            elif "Right" in right_bone_so:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace("Right", "Left"))               
            elif "RIGHT" in right_bone_so:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace("RIGHT", "LEFT"))               
            elif "right" in right_bone_so:
                setattr(bonetemp, f"so_{bone_name}_l", right_bone_so.replace("right", "left"))               
        fingtemp = bpy.context.scene.MK_FingBoneTemp
        fing_names = ["index_a", "index_b", "index_c", "middle_a", "middle_b", "middle_c",
                      "ring_a", "ring_b","ring_c","pinky_a","pinky_b","pinky_c","thumb_a","thumb_b","thumb_c"]
        for bone_name in fing_names:                        
            right_bone_ta = getattr(fingtemp, f"ta_{bone_name}_r")
            right_bone_so = getattr(fingtemp, f"so_{bone_name}_r")

            # If ".r" is in the right bone name, replace it with ".l" and set the left bone attribute
            if ".r" in right_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace(".r", ".l"))
            elif ".R" in right_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace(".R", ".L"))
            elif "_r" in right_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace("_r", "_l"))
            elif "_R" in right_bone_ta[-2:]:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace("_R", "_L"))
            elif "_R_" in right_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace("_R_","_L_"))
            elif "Right" in right_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace("Right", "Left"))             
            elif "RIGHT" in right_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace("RIGHT", "LEFT"))
            elif "right" in right_bone_ta:
                setattr(fingtemp, f"ta_{bone_name}_l", right_bone_ta.replace("right", "left"))               

            if ".r" in right_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace(".r", ".l"))
            elif ".R" in right_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace(".R", ".L"))
            elif "_r" in right_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace("_r", "_l"))
            elif "_R" in right_bone_so[-2:]:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace("_R", "_L"))
            elif "_R_" in right_bone_so:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace("_R_","_L_"))
            elif "Right" in right_bone_so:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace("Right", "Left"))               
            elif "RIGHT" in right_bone_so:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace("RIGHT", "LEFT"))               
            elif "right" in right_bone_so:
                setattr(fingtemp, f"so_{bone_name}_l", right_bone_so.replace("right", "left"))    
        return {'FINISHED'}

class MK_OT_BoneNameChecker(bpy.types.Operator):
    bl_idname = "mkn.bone_namecheck"
    bl_label = "check bonename"
    def execute(self, context):
        armaturetemp = bpy.context.scene.MK_ArmatureTemp
        target_armature = armaturetemp.target
        source_armature = armaturetemp.source
        bonetemp = bpy.context.scene.MK_BoneTemp
        fingtemp = bpy.context.scene.MK_FingBoneTemp
        sobone_names = [
            "so_hips", "so_spine", "so_spine1", "so_chest", "so_neck", "so_head",
            "so_shoulder_l", "so_uparm_l", "so_forearm_l", "so_hand_l",
            "so_shoulder_r", "so_uparm_r", "so_forearm_r", "so_hand_r",
            "so_upleg_l", "so_leg_l", "so_ankle_l", "so_toes_l",
            "so_upleg_r", "so_leg_r", "so_ankle_r", "so_toes_r"]
        tabone_names = [            
            "ta_hips", "ta_spine", "ta_spine1", "ta_chest", "ta_neck", "ta_head",
            "ta_shoulder_l", "ta_uparm_l", "ta_forearm_l", "ta_hand_l",
            "ta_shoulder_r", "ta_uparm_r", "ta_forearm_r", "ta_hand_r",
            "ta_upleg_l", "ta_leg_l", "ta_ankle_l", "ta_toes_l",
            "ta_upleg_r", "ta_leg_r", "ta_ankle_r", "ta_toes_r"]
        tabone_fingnames = [
        "ta_index_a_l","ta_index_b_l","ta_index_c_l","ta_middle_a_l","ta_middle_b_l","ta_middle_c_l","ta_ring_a_l","ta_ring_b_l","ta_ring_c_l",
        "ta_pinky_a_l","ta_pinky_b_l","ta_pinky_c_l","ta_thumb_a_l","ta_thumb_b_l","ta_thumb_c_l"
        "ta_index_a_r","ta_index_b_r","ta_index_c_r","ta_middle_a_r","ta_middle_b_r","ta_middle_c_r","ta_ring_a_r","ta_ring_b_r","ta_ring_c_r",
        "ta_pinky_a_r","ta_pinky_b_r","ta_pinky_c_r","ta_thumb_a_r","ta_thumb_b_r","ta_thumb_c_r"]
        sobone_fingnames = [        
        "so_index_a_l","so_index_b_l","so_index_c_l","so_middle_a_l","so_middle_b_l","so_middle_c_l","so_ring_a_l","so_ring_b_l","so_ring_c_l",
        "so_pinky_a_l","so_pinky_b_l","so_pinky_c_l","so_thumb_a_l","so_thumb_b_l","so_thumb_c_l",
        "so_index_a_r","so_index_b_r","so_index_c_r","so_middle_a_r","so_middle_b_r","so_middle_c_r","so_ring_a_r","so_ring_b_r","so_ring_c_r",
        "so_pinky_a_r","so_pinky_b_r","so_pinky_c_r","so_thumb_a_r","so_thumb_b_r","so_thumb_c_r"]
        so_list = [bonetemp.so_hips,bonetemp.so_spine,bonetemp.so_spine1,bonetemp.so_chest,bonetemp.so_neck,bonetemp.so_head,
            bonetemp.so_shoulder_l,bonetemp.so_uparm_l,bonetemp.so_forearm_l,bonetemp.so_hand_l,
            bonetemp.so_shoulder_r,bonetemp.so_uparm_r,bonetemp.so_forearm_r,bonetemp.so_hand_r,
            bonetemp.so_upleg_l,bonetemp.so_leg_l,bonetemp.so_ankle_l,bonetemp.so_toes_l,
            bonetemp.so_upleg_r,bonetemp.so_leg_r,bonetemp.so_ankle_r,bonetemp.so_toes_r]
        sofi_list = [fingtemp.so_index_a_l,fingtemp.so_index_b_l,fingtemp.so_index_c_l,fingtemp.so_middle_a_l,fingtemp.so_middle_b_l,fingtemp.so_middle_c_l,
            fingtemp.so_ring_a_l,fingtemp.so_ring_b_l,fingtemp.so_ring_c_l,fingtemp.so_pinky_a_l,fingtemp.so_pinky_b_l,fingtemp.so_pinky_c_l,
            fingtemp.so_thumb_a_l,fingtemp.so_thumb_b_l,fingtemp.so_thumb_c_r,
            fingtemp.so_index_a_r,fingtemp.so_index_b_r,fingtemp.so_index_c_r,fingtemp.so_middle_a_r,fingtemp.so_middle_b_r,fingtemp.so_middle_c_r,
            fingtemp.so_ring_a_r,fingtemp.so_ring_b_r,fingtemp.so_ring_c_r,fingtemp.so_pinky_a_r,fingtemp.so_pinky_b_r,fingtemp.so_pinky_c_r,
            fingtemp.so_thumb_a_r,fingtemp.so_thumb_b_r,fingtemp.so_thumb_c_r]
        ta_list = [bonetemp.ta_hips,bonetemp.ta_spine,bonetemp.ta_spine1,bonetemp.ta_chest,bonetemp.ta_neck,bonetemp.ta_head,
            bonetemp.ta_shoulder_l,bonetemp.ta_uparm_l,bonetemp.ta_forearm_l,bonetemp.ta_hand_l,
            bonetemp.ta_shoulder_r,bonetemp.ta_uparm_r,bonetemp.ta_forearm_r,bonetemp.ta_hand_r,
            bonetemp.ta_upleg_l,bonetemp.ta_leg_l,bonetemp.ta_ankle_l,bonetemp.ta_toes_l,
            bonetemp.ta_upleg_r,bonetemp.ta_leg_r,bonetemp.ta_ankle_r,bonetemp.ta_toes_r]
        tafi_list = [fingtemp.ta_index_a_l,fingtemp.ta_index_b_l,fingtemp.ta_index_c_l,fingtemp.ta_middle_a_l,fingtemp.ta_middle_b_l,fingtemp.ta_middle_c_l,
            fingtemp.ta_ring_a_l,fingtemp.ta_ring_b_l,fingtemp.ta_ring_c_l,fingtemp.ta_pinky_a_l,fingtemp.ta_pinky_b_l,fingtemp.ta_pinky_c_l,
            fingtemp.ta_thumb_a_l,fingtemp.ta_thumb_b_l,fingtemp.ta_thumb_c_l,
            fingtemp.ta_index_a_r,fingtemp.ta_index_b_r,fingtemp.ta_index_c_r,fingtemp.ta_middle_a_r,fingtemp.ta_middle_b_r,fingtemp.ta_middle_c_r,
            fingtemp.ta_ring_a_r,fingtemp.ta_ring_b_r,fingtemp.ta_ring_c_r,fingtemp.ta_pinky_a_r,fingtemp.ta_pinky_b_r,fingtemp.ta_pinky_c_r,
            fingtemp.ta_thumb_a_r,fingtemp.ta_thumb_b_r,fingtemp.ta_thumb_c_r]
                 
        bpy.ops.object.mode_set(mode = "OBJECT")
        bpy.context.view_layer.objects.active = source_armature
        bpy.ops.object.mode_set(mode = "EDIT")        
        for bone_name,bone_str in zip(so_list,sobone_names):
            if not source_armature.data.edit_bones.get(bone_name):
                
                setattr(bonetemp, bone_str, "")
                
        for bone_name,bone_str in zip(sofi_list,sobone_fingnames):
            if not source_armature.data.edit_bones.get(bone_name):
                
                setattr(fingtemp, bone_str, "")
              
        bpy.ops.object.mode_set(mode = "OBJECT")
        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode = "EDIT")
        for bone_name,bone_str in zip(ta_list,tabone_names):
            if not target_armature.data.edit_bones.get(bone_name):
                
                setattr(bonetemp, bone_str, "")
                
        for bone_name,bone_str in zip(tafi_list,tabone_fingnames):
            if not target_armature.data.edit_bones.get(bone_name):
                
                setattr(fingtemp, bone_str, "")

        bpy.ops.object.mode_set(mode = "OBJECT")                       

        return {'FINISHED'}

class jsonExport(bpy.types.Operator,ExportHelper):
    bl_idname = "mkn.json_export"
    bl_label = "Export_bonemap"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext = ".json"

    def execute(self, context):
        #print("Selected file:", self.filepath)

        bonetemp = bpy.context.scene.MK_BoneTemp
        fingtemp = bpy.context.scene.MK_FingBoneTemp
        if not ".json" in self.filepath:
             self.filepath = self.filepath + ".json"
        
        d = [bonetemp.so_hips,bonetemp.so_spine,bonetemp.so_spine1,bonetemp.so_chest,bonetemp.so_neck,bonetemp.so_head,
            bonetemp.so_shoulder_l,bonetemp.so_uparm_l,bonetemp.so_forearm_l,bonetemp.so_hand_l,
            bonetemp.so_shoulder_r,bonetemp.so_uparm_r,bonetemp.so_forearm_r,bonetemp.so_hand_r,
            bonetemp.so_upleg_l,bonetemp.so_leg_l,bonetemp.so_ankle_l,bonetemp.so_toes_l,
            bonetemp.so_upleg_r,bonetemp.so_leg_r,bonetemp.so_ankle_r,bonetemp.so_toes_r,
            bonetemp.ta_hips,bonetemp.ta_spine,bonetemp.ta_spine1,bonetemp.ta_chest,bonetemp.ta_neck,bonetemp.ta_head,
            bonetemp.ta_shoulder_l,bonetemp.ta_uparm_l,bonetemp.ta_forearm_l,bonetemp.ta_hand_l,
            bonetemp.ta_shoulder_r,bonetemp.ta_uparm_r,bonetemp.ta_forearm_r,bonetemp.ta_hand_r,
            bonetemp.ta_upleg_l,bonetemp.ta_leg_l,bonetemp.ta_ankle_l,bonetemp.ta_toes_l,
            bonetemp.ta_upleg_r,bonetemp.ta_leg_r,bonetemp.ta_ankle_r,bonetemp.ta_toes_r,
            fingtemp.ta_index_a_l,fingtemp.ta_index_b_l,fingtemp.ta_index_c_l,fingtemp.ta_middle_a_l,fingtemp.ta_middle_b_l,fingtemp.ta_middle_c_l,
            fingtemp.ta_ring_a_l,fingtemp.ta_ring_b_l,fingtemp.ta_ring_c_l,fingtemp.ta_pinky_a_l,fingtemp.ta_pinky_b_l,fingtemp.ta_pinky_c_l,
            fingtemp.ta_thumb_a_l,fingtemp.ta_thumb_b_l,fingtemp.ta_thumb_c_l,
            fingtemp.ta_index_a_r,fingtemp.ta_index_b_r,fingtemp.ta_index_c_r,fingtemp.ta_middle_a_r,fingtemp.ta_middle_b_r,fingtemp.ta_middle_c_r,
            fingtemp.ta_ring_a_r,fingtemp.ta_ring_b_r,fingtemp.ta_ring_c_r,fingtemp.ta_pinky_a_r,fingtemp.ta_pinky_b_r,fingtemp.ta_pinky_c_r,
            fingtemp.ta_thumb_a_r,fingtemp.ta_thumb_b_r,fingtemp.ta_thumb_c_r,
            fingtemp.so_index_a_l,fingtemp.so_index_b_l,fingtemp.so_index_c_l,fingtemp.so_middle_a_l,fingtemp.so_middle_b_l,fingtemp.so_middle_c_l,
            fingtemp.so_ring_a_l,fingtemp.so_ring_b_l,fingtemp.so_ring_c_l,fingtemp.so_pinky_a_l,fingtemp.so_pinky_b_l,fingtemp.so_pinky_c_l,
            fingtemp.so_thumb_a_l,fingtemp.so_thumb_b_l,fingtemp.so_thumb_c_r,
            fingtemp.so_index_a_r,fingtemp.so_index_b_r,fingtemp.so_index_c_r,fingtemp.so_middle_a_r,fingtemp.so_middle_b_r,fingtemp.so_middle_c_r,
            fingtemp.so_ring_a_r,fingtemp.so_ring_b_r,fingtemp.so_ring_c_r,fingtemp.so_pinky_a_r,fingtemp.so_pinky_b_r,fingtemp.so_pinky_c_r,
            fingtemp.so_thumb_a_r,fingtemp.so_thumb_b_r,fingtemp.so_thumb_c_r]                    

        with open(self.filepath, 'w',encoding="utf-8") as f:
            json.dump(d, f,ensure_ascii=False, indent=1)
        return {'FINISHED'}

    def invoke(self, context, event):

        self.filepath = "mnr_bonemap.json"  
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class jsonImport(bpy.types.Operator,ExportHelper):
    bl_idname = "mkn.json_import"
    bl_label = "Import_bonemap"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext = ".json"
    ##0~41
    basebone_names = [
        "so_hips", "so_spine", "so_spine1", "so_chest", "so_neck", "so_head",
        "so_shoulder_l", "so_uparm_l", "so_forearm_l", "so_hand_l",
        "so_shoulder_r", "so_uparm_r", "so_forearm_r", "so_hand_r",
        "so_upleg_l", "so_leg_l", "so_ankle_l", "so_toes_l",
        "so_upleg_r", "so_leg_r", "so_ankle_r", "so_toes_r",
        "ta_hips", "ta_spine", "ta_spine1", "ta_chest", "ta_neck", "ta_head",
        "ta_shoulder_l", "ta_uparm_l", "ta_forearm_l", "ta_hand_l",
        "ta_shoulder_r", "ta_uparm_r", "ta_forearm_r", "ta_hand_r",
        "ta_upleg_l", "ta_leg_l", "ta_ankle_l", "ta_toes_l",
        "ta_upleg_r", "ta_leg_r", "ta_ankle_r", "ta_toes_r"
    ]
    ##43
    ##44~101
    bone_fingnames = [
    "ta_index_a_l","ta_index_b_l","ta_index_c_l","ta_middle_a_l","ta_middle_b_l","ta_middle_c_l","ta_ring_a_l","ta_ring_b_l","ta_ring_c_l",
    "ta_pinky_a_l","ta_pinky_b_l","ta_pinky_c_l","ta_thumb_a_l","ta_thumb_b_l","ta_thumb_c_l",
    "ta_index_a_r","ta_index_b_r","ta_index_c_r","ta_middle_a_r","ta_middle_b_r","ta_middle_c_r","ta_ring_a_r","ta_ring_b_r","ta_ring_c_r",
    "ta_pinky_a_r","ta_pinky_b_r","ta_pinky_c_r","ta_thumb_a_r","ta_thumb_b_r","ta_thumb_c_r",
    "so_index_a_l","so_index_b_l","so_index_c_l","so_middle_a_l","so_middle_b_l","so_middle_c_l","so_ring_a_l","so_ring_b_l","so_ring_c_l",
    "so_pinky_a_l","so_pinky_b_l","so_pinky_c_l","so_thumb_a_l","so_thumb_b_l","so_thumb_c_l",
    "so_index_a_r","so_index_b_r","so_index_c_r","so_middle_a_r","so_middle_b_r","so_middle_c_r","so_ring_a_r","so_ring_b_r","so_ring_c_r",
    "so_pinky_a_r","so_pinky_b_r","so_pinky_c_r","so_thumb_a_r","so_thumb_b_r","so_thumb_c_r",    
    ]

    bone_names = basebone_names + bone_fingnames
    
    def execute(self, context):
        bonetemp = bpy.context.scene.MK_BoneTemp
        with open(self.filepath, 'r') as json_open:
            json_load = json.load(json_open)
        for i, bone_name in enumerate(self.bone_names):
            if i <= 43:
                setattr(bonetemp, bone_name, json_load[i])
            elif i <= 101:

                bonetemp = bpy.context.scene.MK_FingBoneTemp                
                setattr(bonetemp, bone_name, json_load[i])

        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = "mnr_bonemap.json"  
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
class MK_RetargetOffsetPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Retarget Offset Panel"
    bl_idname = "OBJECT_PT_retarget_offset"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "mk_tools"
    @classmethod
    def poll(cls, context):
        return context.scene.get('show_retarget_offset_panel', False)

    def draw(self, context):
        layout = self.layout
        target_armature = bpy.context.scene.MK_ArmatureTemp.target
        # Ensure the object "Armature" exists and it has a bone named "Bone"
        bonetemp = bpy.context.scene.MK_BoneTemp
        if bonetemp.ta_hips:
            bone = target_armature.pose.bones[bonetemp.ta_hips]
            if bone.constraints:
                for con in bone.constraints:
                    if "MK_" in con.name:
                        if "XY" in con.name:
                            conxy = con
                        elif "Z" in con.name:
                            conz = con 

            column = layout.column(align=True)
            column.label(text="root_offsetXY")
            row = column.row(align=True)
            row.prop(conxy, "enabled")
            row.prop(conxy, "influence")
            column.label(text="root_offsetZ")
            row = column.row(align=True)
            row.prop(conz, "enabled")
            row.prop(conz, "influence")
            column.label(text="offset")
            column.prop(conz, "use_offset")
                                      
        dolist = [bonetemp.ta_hips,bonetemp.ta_spine,bonetemp.ta_spine1,bonetemp.ta_chest,bonetemp.ta_neck,bonetemp.ta_head,
            bonetemp.ta_shoulder_l,bonetemp.ta_uparm_l,bonetemp.ta_forearm_l,bonetemp.ta_hand_l,
            bonetemp.ta_shoulder_r,bonetemp.ta_uparm_r,bonetemp.ta_forearm_r,bonetemp.ta_hand_r,
            bonetemp.ta_upleg_l,bonetemp.ta_leg_l,bonetemp.ta_ankle_l,bonetemp.ta_toes_l,
            bonetemp.ta_upleg_r,bonetemp.ta_leg_r,bonetemp.ta_ankle_r,bonetemp.ta_toes_r]   
        column = layout.column(align=True)                    
        for dd in dolist:
            if dd:
                bone = target_armature.pose.bones[dd]
                if bone.constraints:
                    for con in bone.constraints:
                        if "MK_" in con.name and con.type =="COPY_ROTATION":
                            con_a = con
                            column = layout.column(align=True)
                            row = column.row(align=True)
                            row.label(text=dd)
                            row.prop(con_a, "enabled")                            
                            column.prop(con_a, "influence")

        # Add the influence property of the constraint to the panel
           

    

class MK_SimpleRetargetPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "MKSimple Retarget Panel"
    bl_idname = "OBJECT_PT_simple_retarget"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "mk_tools"

    def draw(self, context):
        props = bpy.context.scene.MK_ArmatureTemp
        layout = self.layout
        col = layout.column()
        col.prop(props,"source",text="sourceArmature")
        col.prop(props,"target",text="targetArmature")
        if props.source and props.target:
            row = layout.row()        
            row.label(text="bonemapIO")
            row = layout.row()
            #row.prop(files,"file_path")
            row.operator("mkn.json_export")
            row.operator("mkn.json_import")            
            bones = bpy.context.scene.MK_BoneTemp
            row = layout.row()   
            row.operator("mkn.bonemap_lrchange")           
            row.operator("mkn.bonemap_rlchange")
            row = layout.row()
            #row.prop(files,"file_path")
            row.operator("mkn.bone_namecheck")                            
            row = layout.row(align=True)        
            column = row.column(align=True)
            column.label(text="sourceBone")
            column.prop(bones,"so_hips", text="")
            column.prop(bones,"so_spine", text="")
            column.prop(bones,"so_spine1", text="")
            column.prop(bones,"so_chest", text="")
            column.prop(bones,"so_neck", text="")
            column.prop(bones,"so_head", text="")
            column = row.column(align=True)
            column.label(text="targetBone")
            column.prop(bones,"ta_hips", text="")
            column.prop(bones,"ta_spine", text="")
            column.prop(bones,"ta_spine1", text="")
            column.prop(bones,"ta_chest", text="")
            column.prop(bones,"ta_neck",text="")
            column.prop(bones,"ta_head", text="")
            row = layout.row(align=True)
            column = row.column(align=True)
            column.label(text="arms_group")
            row = layout.row(align=True)    
            column = row.column(align=True)
            column.prop(bones,"so_shoulder_l",text="")
            column.prop(bones,"so_uparm_l",text="")
            column.prop(bones,"so_forearm_l",text="")
            column.prop(bones,"so_hand_l",text="")
            column = row.column(align=True)        
            column.prop(bones,"ta_shoulder_l", text="")
            column.prop(bones,"ta_uparm_l",text="")
            column.prop(bones,"ta_forearm_l", text="")
            column.prop(bones,"ta_hand_l",text="")        
            
            row = layout.row(align=True)    
            column = row.column(align=True)        
            column.prop(bones,"so_shoulder_r",text="")
            column.prop(bones,"so_uparm_r",text="")
            column.prop(bones,"so_forearm_r",text="")
            column.prop(bones,"so_hand_r",text="")
            column = row.column(align=True)  
            column.prop(bones,"ta_shoulder_r",text="")
            column.prop(bones,"ta_uparm_r",text="")
            column.prop(bones,"ta_forearm_r",text="")
            column.prop(bones,"ta_hand_r", text="")
            row = layout.row(align=True)
            column = row.column(align=True)          
            column.label(text="legs_group") 
            row = layout.row(align=True)
            column = row.column(align=True) 
            column.prop(bones,"so_upleg_l", text="")
            column.prop(bones,"so_leg_l", text="")
            column.prop(bones,"so_ankle_l",text="")
            column.prop(bones,"so_toes_l",text="")
            column = row.column(align=True) 
            column.prop(bones,"ta_upleg_l",text="")
            column.prop(bones,"ta_leg_l", text="")
            column.prop(bones,"ta_ankle_l", text="")
            column.prop(bones,"ta_toes_l",text="")   
            row = layout.row(align=True)
            column = row.column(align=True)            
            column.prop(bones,"so_upleg_r", text="")
            column.prop(bones,"so_leg_r", text="")
            column.prop(bones,"so_ankle_r", text="")
            column.prop(bones,"so_toes_r",text="")
            column = row.column(align=True)          
            column.prop(bones,"ta_upleg_r", text="")
            column.prop(bones,"ta_leg_r", text="")
            column.prop(bones,"ta_ankle_r", text="")
            column.prop(bones,"ta_toes_r",text="")

            files = bpy.context.scene.MK_FileTemp
            row = layout.row() 
            row.prop(context.scene.MK_BoolTemp, "fing_bool")
            row.prop(context.scene.MK_BoolTemp, "ik_bool")

            fingbones = bpy.context.scene.MK_FingBoneTemp
            if context.scene.MK_BoolTemp.fing_bool:
                row = layout.row()
                row.label(text= "not stable")
                row = layout.row() 
                column = row.column(align=True)
                column.prop(fingbones,"so_index_a_l",text="")
                column.prop(fingbones,"so_index_b_l", text="")
                column.prop(fingbones,"so_index_c_l",text="")
                column = row.column(align=True)
                column.prop(fingbones,"ta_index_a_l",text="")
                column.prop(fingbones,"ta_index_b_l", text="")
                column.prop(fingbones,"ta_index_c_l",text="")
                row = layout.row() 
                column = row.column(align=True)                     
                column.prop(fingbones,"so_index_a_r",text="")
                column.prop(fingbones,"so_index_b_r", text="")
                column.prop(fingbones,"so_index_c_r",text="")
                column = row.column(align=True)                  
                column.prop(fingbones,"ta_index_a_r",text="")
                column.prop(fingbones,"ta_index_b_r", text="")
                column.prop(fingbones,"ta_index_c_r",text="")
                
                row = layout.row() 
                column = row.column(align=True)                
                column.prop(fingbones,"so_middle_a_l",text="")
                column.prop(fingbones,"so_middle_b_l", text="")
                column.prop(fingbones,"so_middle_c_l",text="")
                column = row.column(align=True)                
                column.prop(fingbones,"ta_middle_a_l",text="")
                column.prop(fingbones,"ta_middle_b_l", text="")
                column.prop(fingbones,"ta_middle_c_l",text="")
                row = layout.row() 
                column = row.column(align=True)                                      
                column.prop(fingbones,"so_middle_a_r",text="")
                column.prop(fingbones,"so_middle_b_r", text="")
                column.prop(fingbones,"so_middle_c_r",text="")
                column = row.column(align=True)
                column.prop(fingbones,"ta_middle_a_r",text="")
                column.prop(fingbones,"ta_middle_b_r", text="")
                column.prop(fingbones,"ta_middle_c_r",text="")
                
                row = layout.row() 
                column = row.column(align=True)
                column.prop(fingbones,"so_ring_a_l",text="")
                column.prop(fingbones,"so_ring_b_l", text="")
                column.prop(fingbones,"so_ring_c_l",text="")
                column = row.column(align=True)
                column.prop(fingbones,"ta_ring_a_l",text="")
                column.prop(fingbones,"ta_ring_b_l", text="")
                column.prop(fingbones,"ta_ring_c_l",text="")                
                row = layout.row() 
                column = row.column(align=True)      
                column.prop(fingbones,"so_ring_a_r",text="")
                column.prop(fingbones,"so_ring_b_r", text="")
                column.prop(fingbones,"so_ring_c_r",text="")
                column = row.column(align=True)
                column.prop(fingbones,"ta_ring_a_r",text="")
                column.prop(fingbones,"ta_ring_b_r", text="")
                column.prop(fingbones,"ta_ring_c_r",text="")                
                row = layout.row() 
                column = row.column(align=True)                             
                column.prop(fingbones,"so_pinky_a_l",text="")
                column.prop(fingbones,"so_pinky_b_l", text="")
                column.prop(fingbones,"so_pinky_c_l",text="")
                column = row.column(align=True) 
                column.prop(fingbones,"ta_pinky_a_l",text="")
                column.prop(fingbones,"ta_pinky_b_l", text="")
                column.prop(fingbones,"ta_pinky_c_l",text="") 
                row = layout.row()                   
                column = row.column(align=True)
                column.prop(fingbones,"so_pinky_a_r",text="")
                column.prop(fingbones,"so_pinky_b_r", text="")
                column.prop(fingbones,"so_pinky_c_r",text="")
                column = row.column(align=True)                
                column.prop(fingbones,"ta_pinky_a_r",text="")
                column.prop(fingbones,"ta_pinky_b_r", text="")
                column.prop(fingbones,"ta_pinky_c_r",text="")                 
                row = layout.row() 
                column = row.column(align=True)                               
                column.prop(fingbones,"so_thumb_a_l",text="")
                column.prop(fingbones,"so_thumb_b_l", text="")
                column.prop(fingbones,"so_thumb_c_l",text="")
                column = row.column(align=True)  
                column.prop(fingbones,"ta_thumb_a_l",text="")
                column.prop(fingbones,"ta_thumb_b_l", text="")
                column.prop(fingbones,"ta_thumb_c_l",text="")                
                row = layout.row() 
                column = row.column(align=True)                       
                column.prop(fingbones,"so_thumb_a_r",text="")
                column.prop(fingbones,"so_thumb_b_r", text="")
                column.prop(fingbones,"so_thumb_c_r",text="")
                column = row.column(align=True)
                column.prop(fingbones,"ta_thumb_a_r",text="")
                column.prop(fingbones,"ta_thumb_b_r", text="")
                column.prop(fingbones,"ta_thumb_c_r",text="")                                                                                                                   

            if context.scene.MK_BoolTemp.ik_bool:
                row = layout.row()
                row.label(text= "check wrist and ankle setting")
                row = layout.row()
                column = row.column(align=True)
                column.alignment = "RIGHT"
                column.label(text="UpperArm:")  
                column.label(text="ForeArm:")  
                column.label(text="Hand:")   
                column.label(text="Thigh:")
                column.label(text="Leg:")            
                column.label(text="Ankle:")            
                column = row.column(align=True)
                column.label(text=bones.ta_uparm_l)
                column.label(text=bones.ta_forearm_l) 
                column.label(text=bones.ta_hand_l)
                column.label(text=bones.ta_upleg_l)
                column.label(text=bones.ta_leg_l)            
                column.label(text=bones.ta_ankle_l)
                column = row.column(align=True)            
                column.label(text=bones.ta_uparm_r)
                column.label(text=bones.ta_forearm_r)
                column.label(text=bones.ta_hand_r)
                column.label(text=bones.ta_upleg_r)
                column.label(text=bones.ta_leg_r)
                column.label(text=bones.ta_ankle_r)
                row = layout.row()
                row.operator("mkn.ikretarget")
            else:                                                                                    
                row = layout.row()        
                row.operator("mkn.retarget")
            row = layout.row()   
            row.operator("mkn.clear")
            row = layout.row()   
            row.operator("mkn.bake")        
            row = layout.row()        
def armature_objects(self, object):
    return object.type == 'ARMATURE'
                                    
class MK_ArmatureTemp(bpy.types.PropertyGroup):
    source: bpy.props.PointerProperty(
        name="source",
        type=bpy.types.Object,  # 参照するデータ型を指定
        poll=armature_objects
    )    
    target: bpy.props.PointerProperty(
        name="target",
        type=bpy.types.Object,  # 参照するデータ型を指定
        poll=armature_objects
    )
class MK_FileTemp(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(
        name='export_path', 
        subtype='FILE_PATH', 
        default='//bonemap.json', 
        description='bonemap exportPath'
        )
class MK_BoolTemp(bpy.types.PropertyGroup):
    ik_bool: bpy.props.BoolProperty(
        name="use IK offset",
        default=False
    )
    fing_bool: bpy.props.BoolProperty(
        name="use Finger",
        default=False
    )

class MK_BoneTemp(bpy.types.PropertyGroup):
    so_hips: bpy.props.StringProperty(
        name="so_hips",
        description="so_hips",
        default="Hips"
    )
    so_spine: bpy.props.StringProperty(
        name="so_spine",
        description="so_spine",
        default="Spine"
    )
    so_spine1: bpy.props.StringProperty(
        name="so_spine1",
        description="so_spine1",
        default="Spine1"
    )
    so_chest: bpy.props.StringProperty(
        name="so_spine2",
        description="so_spine2",
        default="Spine2"
    )
    so_neck: bpy.props.StringProperty(
        name="so_neck",
        description="so_neck",
        default="Neck"
    )
    so_head: bpy.props.StringProperty(
        name="so_head",
        description="so_head",
        default="Head"
    )
    so_shoulder_l: bpy.props.StringProperty(
        name="so_shoulder_l",
        description="so_leftshoulder",
        default="LeftShoulder"
    )
    so_uparm_l: bpy.props.StringProperty(
        name="so_uparm_l",
        description="so_leftarm",
        default="LeftArm"
    )
    so_forearm_l: bpy.props.StringProperty(
        name="so_forearm_l",
        description="so_leftforearm",
        default="LeftForeArm"
    )
    so_hand_l: bpy.props.StringProperty(
        name="so_hand_l",
        description="so_lefthand",
        default="LeftHand"
    )
    so_shoulder_r: bpy.props.StringProperty(
        name="so_shoulder_r",
        description="so_rightshoulder",
        default="RightShoulder"
    )
    so_uparm_r: bpy.props.StringProperty(
        name="so_uparm_r",
        description="so_rightarm",
        default="RightArm"
    )
    so_forearm_r: bpy.props.StringProperty(
        name="so_forearm_r",
        description="so_rightforearm",
        default="RightForeArm"
    )
    so_hand_r: bpy.props.StringProperty(
        name="so_hand_r",
        description="so_righthand",
        default="RightHand"
    )
    so_upleg_l: bpy.props.StringProperty(
        name="so_upleg_l",
        description="so_leftupleg",
        default="LeftUpLeg"
    )
    so_leg_l: bpy.props.StringProperty(
        name="so_leg_l",
        description="so_leftleg",
        default="LeftLeg"
    )
    so_ankle_l: bpy.props.StringProperty(
        name="so_ankle_l",
        description="so_leftfoot",
        default="LeftFoot"
    )
    so_toes_l: bpy.props.StringProperty(
        name="so_toes_l",
        description="so_lefttoebase",
        default="LeftToeBase"
    )
    so_upleg_r: bpy.props.StringProperty(
        name="so_upleg_r",
        description="so_rightupleg",
        default="RightUpLeg"
    )
    so_leg_r: bpy.props.StringProperty(
        name="so_leg_r",
        description="so_rightleg",
        default="RightLeg"
    )
    so_ankle_r: bpy.props.StringProperty(
        name="so_ankle_r",
        description="so_rightfoot",
        default="RightFoot"
    )
    so_toes_r: bpy.props.StringProperty(
        name="so_toes_r",
        description="so_righttoebase",
        default="RightToeBase"
    )    
    ta_hips: bpy.props.StringProperty(
        name="ta_hips",
        description="ta_hips",
        default="Hips"
    )
    ta_spine: bpy.props.StringProperty(
        name="ta_spine",
        description="ta_spine",
        default="Spine"
    )
    ta_spine1: bpy.props.StringProperty(
        name="ta_spine1",
        description="ta_spine1",
        default="Spine1"
    )
    ta_chest: bpy.props.StringProperty(
        name="ta_spine2",
        description="ta_spine2",
        default="Spine2"
    )
    ta_neck: bpy.props.StringProperty(
        name="ta_neck",
        description="ta_neck",
        default="Neck"
    )
    ta_head: bpy.props.StringProperty(
        name="ta_head",
        description="ta_head",
        default="Head"
    )
    ta_shoulder_l: bpy.props.StringProperty(
        name="ta_shoulder_l",
        description="ta_leftshoulder",
        default="LeftShoulder"
    )
    ta_uparm_l: bpy.props.StringProperty(
        name="ta_uparm_l",
        description="ta_leftarm",
        default="LeftArm"
    )
    ta_forearm_l: bpy.props.StringProperty(
        name="ta_forearm_l",
        description="ta_leftforearm",
        default="LeftForeArm"
    )
    ta_hand_l: bpy.props.StringProperty(
        name="ta_hand_l",
        description="ta_lefthand",
        default="LeftHand"
    )
    ta_shoulder_r: bpy.props.StringProperty(
        name="ta_shoulder_r",
        description="ta_rightshoulder",
        default="RightShoulder"
    )
    ta_uparm_r: bpy.props.StringProperty(
        name="ta_uparm_r",
        description="ta_rightarm",
        default="RightArm"
    )
    ta_forearm_r: bpy.props.StringProperty(
        name="ta_forearm_r",
        description="ta_rightforearm",
        default="RightForeArm"
    )
    ta_hand_r: bpy.props.StringProperty(
        name="ta_hand_r",
        description="ta_righthand",
        default="RightHand"
    )
    ta_upleg_l: bpy.props.StringProperty(
        name="ta_upleg_l",
        description="ta_leftupleg",
        default="LeftUpLeg"
    )
    ta_leg_l: bpy.props.StringProperty(
        name="ta_leg_l",
        description="ta_leftleg",
        default="LeftLeg"
    )
    ta_ankle_l: bpy.props.StringProperty(
        name="ta_ankle_l",
        description="ta_leftfoot",
        default="LeftFoot"
    )
    ta_toes_l: bpy.props.StringProperty(
        name="ta_toes_l",
        description="ta_lefttoebase",
        default="LeftToeBase"
    )
    ta_upleg_r: bpy.props.StringProperty(
        name="ta_upleg_r",
        description="ta_rightupleg",
        default="RightUpLeg"
    )
    ta_leg_r: bpy.props.StringProperty(
        name="ta_leg_r",
        description="ta_rightleg",
        default="RightLeg"
    )
    ta_ankle_r: bpy.props.StringProperty(
        name="ta_ankle_r",
        description="ta_rightfoot",
        default="RightFoot"
    )
    ta_toes_r: bpy.props.StringProperty(
        name="ta_toes_r",
        description="ta_righttoebase",
        default="RightToeBase"
    )
    
class MK_FingBoneTemp(bpy.types.PropertyGroup):
    # Index finger bones
    so_index_a_l: bpy.props.StringProperty(name="so_index_a_l", description="so_index_a_l", default="LeftHandIndex1")
    so_index_b_l: bpy.props.StringProperty(name="so_index_b_l", description="so_index_b_l", default="LeftHandIndex2")
    so_index_c_l: bpy.props.StringProperty(name="so_index_c_l", description="so_index_c_l", default="LeftHandIndex3")
    # Middle finger bones
    so_middle_a_l: bpy.props.StringProperty(name="so_middle_a_l", description="so_middle_a_l", default="LeftHandMiddle1")
    so_middle_b_l: bpy.props.StringProperty(name="so_middle_b_l", description="so_middle_b_l", default="LeftHandMiddle2")
    so_middle_c_l: bpy.props.StringProperty(name="so_middle_c_l", description="so_middle_c_l", default="LeftHandMiddle3")
    # Ring finger bones
    so_ring_a_l: bpy.props.StringProperty(name="so_ring_a_l", description="so_ring_a_l", default="LeftHandRing1")
    so_ring_b_l: bpy.props.StringProperty(name="so_ring_b_l", description="so_ring_b_l", default="LeftHandRing2")
    so_ring_c_l: bpy.props.StringProperty(name="so_ring_c_l", description="so_ring_c_l", default="LeftHandRing3")
    # Pinky finger bones
    so_pinky_a_l: bpy.props.StringProperty(name="so_pinky_a_l", description="so_pinky_a_l", default="LeftHandPinky1")
    so_pinky_b_l: bpy.props.StringProperty(name="so_pinky_b_l", description="so_pinky_b_l", default="LeftHandPinky2")
    so_pinky_c_l: bpy.props.StringProperty(name="so_pinky_c_l", description="so_pinky_c_l", default="LeftHandPinky3")
    # Thumb bones
    so_thumb_a_l: bpy.props.StringProperty(name="so_thumb_a_l", description="so_thumb_a_l", default="LeftHandThumb1")
    so_thumb_b_l: bpy.props.StringProperty(name="so_thumb_b_l", description="so_thumb_b_l", default="LeftHandThumb2")
    so_thumb_c_l: bpy.props.StringProperty(name="so_thumb_c_l", description="so_thumb_c_l", default="LeftHandThumb3")
    # Right hand bones
    # Index finger bones
    so_index_a_r: bpy.props.StringProperty(name="so_index_a_r", description="so_index_a_r", default="RightHandIndex1")
    so_index_b_r: bpy.props.StringProperty(name="so_index_b_r", description="so_index_b_r", default="RightHandIndex2")
    so_index_c_r: bpy.props.StringProperty(name="so_index_c_r", description="so_index_c_r", default="RightHandIndex3")

    # Middle finger bones
    so_middle_a_r: bpy.props.StringProperty(name="so_middle_a_r", description="so_middle_a_r", default="RightHandMiddle1")
    so_middle_b_r: bpy.props.StringProperty(name="so_middle_b_r", description="so_middle_b_r", default="RightHandMiddle2")
    so_middle_c_r: bpy.props.StringProperty(name="so_middle_c_r", description="so_middle_c_r", default="RightHandMiddle3")

    # Ring finger bones
    so_ring_a_r: bpy.props.StringProperty(name="so_ring_a_r", description="so_ring_a_r", default="RightHandRing1")
    so_ring_b_r: bpy.props.StringProperty(name="so_ring_b_r", description="so_ring_b_r", default="RightHandRing2")
    so_ring_c_r: bpy.props.StringProperty(name="so_ring_c_r", description="so_ring_c_r", default="RightHandRing3")

    # Pinky finger bones
    so_pinky_a_r: bpy.props.StringProperty(name="so_pinky_a_r", description="so_pinky_a_r", default="RightHandPinky1")
    so_pinky_b_r: bpy.props.StringProperty(name="so_pinky_b_r", description="so_pinky_b_r", default="RightHandPinky2")
    so_pinky_c_r: bpy.props.StringProperty(name="so_pinky_c_r", description="so_pinky_c_r", default="RightHandPinky3")

    # Thumb bones
    so_thumb_a_r: bpy.props.StringProperty(name="so_thumb_a_r", description="so_thumb_a_r", default="RightHandThumb1")
    so_thumb_b_r: bpy.props.StringProperty(name="so_thumb_b_r", description="so_thumb_b_r", default="RightHandThumb2")
    so_thumb_c_r: bpy.props.StringProperty(name="so_thumb_c_r", description="so_thumb_c_r", default="RightHandThumb3")

    # Index finger bones
    ta_index_a_l: bpy.props.StringProperty(name="ta_index_a_l", description="ta_index_a_l", default="LeftHandIndex1")
    ta_index_b_l: bpy.props.StringProperty(name="ta_index_b_l", description="ta_index_b_l", default="LeftHandIndex2")
    ta_index_c_l: bpy.props.StringProperty(name="ta_index_c_l", description="ta_index_c_l", default="LeftHandIndex3")
    # Middle finger bones
    ta_middle_a_l: bpy.props.StringProperty(name="ta_middle_a_l", description="ta_middle_a_l", default="LeftHandMiddle1")
    ta_middle_b_l: bpy.props.StringProperty(name="ta_middle_b_l", description="ta_middle_b_l", default="LeftHandMiddle2")
    ta_middle_c_l: bpy.props.StringProperty(name="ta_middle_c_l", description="ta_middle_c_l", default="LeftHandMiddle3")
    # Ring finger bones
    ta_ring_a_l: bpy.props.StringProperty(name="ta_ring_a_l", description="ta_ring_a_l", default="LeftHandRing1")
    ta_ring_b_l: bpy.props.StringProperty(name="ta_ring_b_l", description="ta_ring_b_l", default="LeftHandRing2")
    ta_ring_c_l: bpy.props.StringProperty(name="ta_ring_c_l", description="ta_ring_c_l", default="LeftHandRing3")
    # Pinky finger bones
    ta_pinky_a_l: bpy.props.StringProperty(name="ta_pinky_a_l", description="ta_pinky_a_l", default="LeftHandPinky1")
    ta_pinky_b_l: bpy.props.StringProperty(name="ta_pinky_b_l", description="ta_pinky_b_l", default="LeftHandPinky2")
    ta_pinky_c_l: bpy.props.StringProperty(name="ta_pinky_c_l", description="ta_pinky_c_l", default="LeftHandPinky3")
    # Thumb bones
    ta_thumb_a_l: bpy.props.StringProperty(name="ta_thumb_a_l", description="ta_thumb_a_l", default="LeftHandThumb1")
    ta_thumb_b_l: bpy.props.StringProperty(name="ta_thumb_b_l", description="ta_thumb_b_l", default="LeftHandThumb2")
    ta_thumb_c_l: bpy.props.StringProperty(name="ta_thumb_c_l", description="ta_thumb_c_l", default="LeftHandThumb3")
    # Right hand bones
    # Index finger bones
    ta_index_a_r: bpy.props.StringProperty(name="ta_index_a_r", description="ta_index_a_r", default="RightHandIndex1")
    ta_index_b_r: bpy.props.StringProperty(name="ta_index_b_r", description="ta_index_b_r", default="RightHandIndex2")
    ta_index_c_r: bpy.props.StringProperty(name="ta_index_c_r", description="ta_index_c_r", default="RightHandIndex3")

    # Middle finger bones
    ta_middle_a_r: bpy.props.StringProperty(name="ta_middle_a_r", description="ta_middle_a_r", default="RightHandMiddle1")
    ta_middle_b_r: bpy.props.StringProperty(name="ta_middle_b_r", description="ta_middle_b_r", default="RightHandMiddle2")
    ta_middle_c_r: bpy.props.StringProperty(name="ta_middle_c_r", description="ta_middle_c_r", default="RightHandMiddle3")

    # Ring finger bones
    ta_ring_a_r: bpy.props.StringProperty(name="ta_ring_a_r", description="ta_ring_a_r", default="RightHandRing1")
    ta_ring_b_r: bpy.props.StringProperty(name="ta_ring_b_r", description="ta_ring_b_r", default="RightHandRing2")
    ta_ring_c_r: bpy.props.StringProperty(name="ta_ring_c_r", description="ta_ring_c_r", default="RightHandRing3")

    # Pinky finger bones
    ta_pinky_a_r: bpy.props.StringProperty(name="ta_pinky_a_r", description="ta_pinky_a_r", default="RightHandPinky1")
    ta_pinky_b_r: bpy.props.StringProperty(name="ta_pinky_b_r", description="ta_pinky_b_r", default="RightHandPinky2")
    ta_pinky_c_r: bpy.props.StringProperty(name="ta_pinky_c_r", description="ta_pinky_c_r", default="RightHandPinky3")

    # Thumb bones
    ta_thumb_a_r: bpy.props.StringProperty(name="ta_thumb_a_r", description="ta_thumb_a_r", default="RightHandThumb1")
    ta_thumb_b_r: bpy.props.StringProperty(name="ta_thumb_b_r", description="ta_thumb_b_r", default="RightHandThumb2")
    ta_thumb_c_r: bpy.props.StringProperty(name="ta_thumb_c_r", description="ta_thumb_c_r", default="RightHandThumb3")
    
def register():
    bpy.utils.register_class(jsonImport)    
    bpy.utils.register_class(jsonExport)
    bpy.utils.register_class(MK_RetargetOffsetPanel)
    bpy.utils.register_class(MK_SimpleRetargetPanel)
    bpy.utils.register_class(MK_OT_IKRetarget)    
    bpy.utils.register_class(MK_OT_Retarget)
    bpy.utils.register_class(MK_OT_Clear)
    bpy.utils.register_class(MK_OT_Bake)
    bpy.utils.register_class(MK_OT_BoneMapRenameLR)
    bpy.utils.register_class(MK_OT_BoneMapRenameRL)
    bpy.utils.register_class(MK_OT_BoneNameChecker)
    bpy.utils.register_class(MK_ArmatureTemp)
    bpy.utils.register_class(MK_BoneTemp)
    bpy.utils.register_class(MK_FileTemp)
    bpy.utils.register_class(MK_BoolTemp)    
  
    bpy.utils.register_class(MK_FingBoneTemp)

    bpy.types.Scene.MK_FileTemp = bpy.props.PointerProperty(type=MK_FileTemp)    
    bpy.types.Scene.MK_ArmatureTemp = bpy.props.PointerProperty(type=MK_ArmatureTemp)
    bpy.types.Scene.MK_BoneTemp = bpy.props.PointerProperty(type=MK_BoneTemp)
    bpy.types.Scene.MK_BoolTemp = bpy.props.PointerProperty(type=MK_BoolTemp)
    bpy.types.Scene.MK_FingBoneTemp = bpy.props.PointerProperty(type=MK_FingBoneTemp)
        
def unregister():
    bpy.utils.unregister_class(jsonImport)        
    bpy.utils.unregister_class(jsonExport)
    bpy.utils.unregister_class(MK_RetargetOffsetPanel)
    bpy.utils.unregister_class(MK_SimpleRetargetPanel)
    bpy.utils.unregister_class(MK_OT_IKRetarget)
    bpy.utils.unregister_class(MK_OT_Retarget)
    bpy.utils.unregister_class(MK_OT_Clear)
    bpy.utils.unregister_class(MK_OT_Bake)
    bpy.utils.unregister_class(MK_OT_BoneMapRenameLR)
    bpy.utils.unregister_class(MK_OT_BoneMapRenameRL)
    bpy.utils.unregister_class(MK_OT_BoneNameChecker) 
    bpy.utils.unregister_class(MK_ArmatureTemp)
    bpy.utils.unregister_class(MK_BoneTemp)
    bpy.utils.unregister_class(MK_FileTemp)    
    bpy.utils.unregister_class(MK_BoolTemp)

    bpy.utils.unregister_class(MK_FingBoneTemp)
    del bpy.types.Scene.MK_FileTemp
    del bpy.types.Scene.MK_ArmatureTemp
    del bpy.types.Scene.MK_BoneTemp
    del bpy.types.Scene.MK_BoolTemp
    del bpy.types.Scene.MK_FingBoneTemp
    
if __name__ == "__main__":
    register()