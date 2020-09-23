import numpy as np

data = np.load('0001.npz')
#print(data.files)

intrinsic_mat = data['intrinsic_mat']
print("\tCamera intrinsic mat:\n{}\n".format(intrinsic_mat))

extrinsic_mat = data['extrinsic_mat']
print("\tCamera extrinsic mat:\n{}\n".format(extrinsic_mat))

obj_pose_labels = data['object_pose_labels']
obj_pose_mats = data['object_pose_mats']
obj_poses = [{'obj_name': i, 'obj_pose_mat': j} for i, j in zip(obj_pose_labels, obj_pose_mats)]
print("\tObject poses:\n{}\n".format(obj_poses))

try:
    import cv2

    opt_flow = data['optical_flow']
    cv2.imshow("Optical flow", opt_flow)

    normals = data['normal_map']
    cv2.imshow("Surface normals", normals)

    sg_msk = data['segmentation_masks']
    height, width = sg_msk.shape
    sg_msk_img = np.zeros((height, width, 3), np.uint8)
    sg_msk_img[sg_msk == 1] = [255, 0, 0] # Draw in blue where `obj_ind = 1`
    cv2.imshow("Segmentation masks", sg_msk_img)

    depth = data['depth_map']
    INVALID_DEPTH = -1
    depth_min = np.amin(depth[depth != INVALID_DEPTH])
    """ option 1 """
    #"""
    depth_max = np.amax(depth) # if you have multiple images you can feed the min and max over all the images, to get a consistent looking depthmap
    normalized_depth = (depth - depth_min)/(depth_max - depth_min) * 255.0
    normalized_depth = normalized_depth.astype(np.uint8)
    #"""
    """ option 2 """
    """
    depth_copy = np.copy(depth)
    depth_copy[depth == INVALID_DEPTH] = depth_min
    normalized_depth = cv2.normalize(depth_copy, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1) # alternatively use CV_8UC3
    #"""
    #normalized_depth = 255.0 - normalized_depth # invert values for draw
    depth_colored = cv2.applyColorMap(normalized_depth, cv2.COLORMAP_JET)
    depth_colored[depth == INVALID_DEPTH] = [0, 0, 0] # paint in black the regions with invalid depth
    cv2.imshow("Depth map", depth_colored)

    cv2.waitKey(0)
except ImportError:
    print("\"opencv-python\" not found, please install to visualize the rest of the results.")
