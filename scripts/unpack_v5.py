import sys
import os
import struct
import blackboxprotobuf
import imageio.v3 as imageio

import json
import cv2
import numpy as np 
from PIL import Image
from enum import Enum

unpack_debug = False
display_undistort = False


class LINE_TYPE(Enum):
    LINE_LEFT = 1 << 0
    LINE_RIGHT = 1 << 1
    LINE_LEFT_LEFT = 1 << 2
    LINE_RIGHT_RIGHT = 1 << 3 
    LINE_LEFT_OUTER = 1 << 4
    LINE_RIGHT_OUTER = 1 << 5
    LINE_LEFT_LEFT_LEFT = 1 << 6
    LINE_RIGHT_RIGHT_RIGHT = 1 << 7

    LINE_RAMP = 1 << 8
    LINE_DOUBLE = 1 << 9
    LINE_DASH = 1 << 10
    LINE_SOLID = 1 << 11

    LINE_WHITE = 1 << 12
    LINE_YELLOW = 1 << 13
    LINE_BLUE = 1 << 14
    LINE_GREEN = 1 << 15

    LINE_FENCE =  1 << 16
    LINE_ROAD_HEIGHT = 1 << 17
    LINE_DIVERSION_INSIDE = 1 << 18

    LINE_BARRIER = 1 << 19
    LINE_DIVERSION_OUTSIDE = 1 << 20

    LINE_PERCEPTION = 1 << 21
    LINE_TRACKING = 1 << 22
    LINE_RAW = 1 << 23
    LINE_ROAD = 1 << 24
    LINE_POLE = 1 << 25
    LINE_ROAD_UNPARALLEL = 1 << 26

class OBSTACLE_TYPE(Enum):
     OBSTACLE_TYPE_VEHICLEREAR = 0
     OBSTACLE_TYPE_VEHICLEFULL = 1
     OBSTACLE_TYPE_PEDESTRIAN = 2
     OBSTACLE_TYPE_TRAFFICSIGN = 3
     OBSTACLE_TYPE_TRAFFICLIGHT = 4
     OBSTACLE_TYPE_ROADSIGN = 6
     OBSTACLE_TYPE_CROSSWALKLINE = 7
     OBSTACLE_TYPE_TRAFFICARROW = 8
     OBSTACLE_TYPE_TRAFFICCONE = 9
     OBSTACLE_TYPE_BARREL = 10
     OBSTACLE_TYPE_YIELDMARK = 11
     OBSTACLE_TYPE_SPEEDMARK = 12
     OBSTACLE_TYPE_CHARACTER = 13
     OBSTACLE_TYPE_STOPLINE = 14
     OBSTACLE_TYPE_DIAMOND = 15
     OBSTACLE_TYPE_BICYCLESIGN = 16
     OBSTACLE_TYPE_SPEEDBUMPS = 17
     OBSTACLE_TYPE_CYCLIST = 18
     OBSTACLE_TYPE_PARKINGLOCK = 19
     OBSTACLE_TYPE_SPEEDCAMERA = 20
     OBSTACLE_TYPE_TRAFFICLIGHTLENS = 21


def fixfloat(int_value):
    return struct.unpack('f',struct.pack('I',int_value))[0]

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     sys.exit(0)
    # f = open(sys.argv[1], 'rb')
    f = open(r'F:\ADAS_20231008-100118_678_5.pack', 'rb')
    ovideo = cv2.VideoWriter(r'f:\aaa.avi',cv2.VideoWriter_fourcc('m','p','e','g'), 30, (3840,2160))
    f.seek(0, 2) 
    eof = f.tell() 
    f.seek(0, 0)
    f.read(4)

    ui_w = 1280
    ui_h = 720

    frame_index = 0
    firstIFrameHasReached = False
    video_encode_data = b''
    video_encode_data_I = b''
    video_encode_index = 0

    gt = [1930.8148193359375, -2403.518798828125, -3832.2744140625, 1096.7318115234375, 11.465042114257812, 1535.2890625, 0.9999794363975525, 0.0015858577098697424, -1.992562174797058]
    while True:
        box_size_bin = f.read(4)  
        box_size = struct.unpack('I', box_size_bin)[0]
        print("frame {} size {}".format(frame_index,box_size))
        box_data = f.read(box_size)  

        #f_tmp = open('test_pack.tmp', 'wb')
        #f_tmp.write(box_data)
        #f_tmp.close()

        if firstIFrameHasReached:
            a, b = blackboxprotobuf.protobuf_to_json(box_data)
            box_data_json = json.loads(a)
            print("---------frame_id:{}".format(box_data_json['2']))
            org_image_width = box_data_json['4']['1']
            org_image_height = box_data_json['4']['2']
            camera_matrix_vcsgnd2img = []
            camera_matrix_gnd2img = []

            if True:
                camera_matrix = box_data_json['3']
                print("camera_matrix gnd2img 3")
                for i in range(0,9):
                    print(fixfloat(camera_matrix['1'][i]))
                print("camera_matrix img2gnd 3")
                for i in range(0,9):
                    print(fixfloat(camera_matrix['2'][i]))
                print("camera_matrix vcsgnd2img 3")
                for i in range(0,9):
                    camera_matrix_vcsgnd2img.append(fixfloat(camera_matrix['3'][i]))
                    print(fixfloat(camera_matrix['3'][i]))
                print("camera_matrix img2vcsgnd 3")
                for i in range(0,9):
                    print(fixfloat(camera_matrix['4'][i]))
                print("camera_matrix local2img 3")
                for i in range(0,9):
                    print(fixfloat(camera_matrix['5'][i]))
                print("camera_matrix img2local 3")
                for i in range(0,9):
                    print(fixfloat(camera_matrix['6'][i]))

                #img_frame = box_data_json['4']
                #print("image width {} height {} ".format(img_frame['1'],img_frame['2']))
                #print("image channel {} time_stamp {} ".format(img_frame['3'],img_frame['4']))
                #print("image send_mode  {} format  {} ".format(img_frame['5'],img_frame['6']))
            if True:
                print("camera_matrix gnd2img 7-160 lane_camera_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['160']['1'][i]))
                print("camera_matrix img2gnd 7-160 lane_camera_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['160']['2'][i]))
                print("camera_matrix vcsgnd2img 7-160 lane_camera_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['160']['3'][i]))
                print("camera_matrix img2vcsgnd 7-160 lane_camera_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['160']['4'][i]))
                print("camera_matrix local2img 7-160 lane_camera_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['160']['5'][i]))

                print("camera_matrix img2local 7-160 lane_camera_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['160']['6'][i]))

            if True:
                print("camera_matrix gnd2img 7-12 unkown_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['12']['1'][i]))
                print("camera_matrix img2gnd 7-12 unkown_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['12']['2'][i]))
                print("camera_matrix vcsgnd2img 7-12 unkown_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['12']['3'][i]))
                print("camera_matrix img2vcsgnd 7-12 unkown_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['12']['4'][i]))
                print("camera_matrix local2img 7-12 unkown_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['12']['5'][i]))

                print("camera_matrix img2local 7-12 unkown_matrix")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['12']['6'][i]))
            if True:
                print("camera_matrix gnd2img 7-10-30 unkown_matrix2")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['10']['30']['1'][i]))
                print("camera_matrix img2gnd 7-10-30 unkown_matrix2")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['10']['30']['2'][i]))
                print("camera_matrix vcsgnd2img 7-10-30 unkown_matrix2")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['10']['30']['3'][i]))
                print("camera_matrix img2vcsgnd 7-10-30 unkown_matrix2")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['10']['30']['4'][i]))
                print("camera_matrix local2img 7-10-30 unkown_matrix2")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['10']['30']['5'][i]))
                print("camera_matrix img2local 7-10-30 unkown_matrix2")
                for i in range(0,9):
                    print(fixfloat(box_data_json['7']['10']['30']['6'][i]))  
            # continue

            # if True:
            #     camera_matrix = box_data_json['3']
            #     # camera_matrix = box_data_json['7']['160']
            #     print("camera_matrix gnd2img ")
            #     for i in range(0,9):
            #         camera_matrix_gnd2img.append(fixfloat(camera_matrix['1'][i]))
            #         print(fixfloat(camera_matrix['1'][i]))
            #     print("camera_matrix img2gnd ")
            #     for i in range(0,9):
            #         print(fixfloat(camera_matrix['2'][i]))
            #     print("camera_matrix vcsgnd2img ")
            #     for i in range(0,9):
            #         camera_matrix_vcsgnd2img.append(fixfloat(camera_matrix['3'][i]))
            #         print(fixfloat(camera_matrix['3'][i]))
            #     print(camera_matrix_vcsgnd2img)
            #     diff = np.array(camera_matrix_vcsgnd2img) - np.array(gt)
            #     # diff[0]=1
            #     if np.any(diff!=0):
            #         print(diff)
            #         print('aaa')
            #         assert False
            #     print("camera_matrix img2vcsgnd ")
            #     for i in range(0,9):
            #         print(fixfloat(camera_matrix['4'][i]))

            #     print("camera_matrix local2img ")
            #     for i in range(0,9):
            #         print(fixfloat(camera_matrix['5'][i]))

            #     print("camera_matrix img2local ")
            #     for i in range(0,9):
            #         print(fixfloat(camera_matrix['6'][i]))

            #     img_frame = box_data_json['4']
            #     print("image width {} height {} ".format(img_frame['1'],img_frame['2']))
            #     print("image channel {} time_stamp {} ".format(img_frame['3'],img_frame['4']))

            #     print("image send_mode  {} format  {} ".format(img_frame['5'],img_frame['6']))


            frame_v1 = box_data_json['7']
            #print("motion:{}".format(frame_v1['11']))
            obstacles_raw_frame_v1_30_1_2 = frame_v1['30']['1']['2']
            obstacles_frame_v1_30_10_2 = frame_v1['30']['10']['2']

            print("-------------------------------------------------roi ")

            roi_2_rect = frame_v1['3']['16'][1]['2']
            roi_2_rect = [int(fixfloat(roi_2_rect['1'])),int(fixfloat(roi_2_rect['2'])),int(fixfloat(roi_2_rect['3'])),int(fixfloat(roi_2_rect['4']))]
            print(roi_2_rect)
            roi_3_rect = frame_v1['3']['16'][2]['2']
            roi_3_rect = [int(fixfloat(roi_3_rect['1'])),int(fixfloat(roi_3_rect['2'])),int(fixfloat(roi_3_rect['3'])),int(fixfloat(roi_3_rect['4']))]
            print(roi_3_rect)

            g_obstacles_raw_rect = []
            for i in range(0,len(obstacles_raw_frame_v1_30_1_2)):
                obstacles_rect_ = obstacles_raw_frame_v1_30_1_2[i]['1']
                obstacles_rect = [int(fixfloat(obstacles_rect_['1'])),int(fixfloat(obstacles_rect_['2'])),int(fixfloat(obstacles_rect_['3'])),int(fixfloat(obstacles_rect_['4']))]
                g_obstacles_raw_rect.append(obstacles_rect)

            g_obstacles_rect = []
            g_obstacles_rect_sta = []
            for i in range(0,len(obstacles_frame_v1_30_10_2)):
                print("---------obstacle {:02d} S---------".format(i))
                print("obstacle id {}".format(obstacles_frame_v1_30_10_2[i]['1']))
                rect_ = obstacles_frame_v1_30_10_2[i]['6']['1']
                obstacles_rect = [int(fixfloat(rect_['1'])),int(fixfloat(rect_['2'])),int(fixfloat(rect_['3'])),int(fixfloat(rect_['4']))]
                g_obstacles_rect.append(obstacles_rect)

                rect_ = obstacles_frame_v1_30_10_2[i]['6']['2']
                obstacles_rect_sta = [int(fixfloat(rect_['1'])),int(fixfloat(rect_['2'])),int(fixfloat(rect_['3'])),int(fixfloat(rect_['4']))]
                g_obstacles_rect_sta.append(obstacles_rect_sta)

                #obstacles_frame_v1_30_10_2[i]['7']['1']
                if '1' in obstacles_frame_v1_30_10_2[i]['7']:
                    yaw = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['1'])
                    print("yaw {} ".format(yaw))
                if '2' in obstacles_frame_v1_30_10_2[i]['7']:
                    vx = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['2']['1'])
                    vy = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['2']['1'])
                    print("velocity {} {} ".format(vx,vy))
                if '14' in obstacles_frame_v1_30_10_2[i]['7']:
                    acc = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['14'])
                    print("acc {} ".format(acc))
                if '10' in obstacles_frame_v1_30_10_2[i]['7']:
                    ttc = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['10'])
                    print("ttc {} ".format(ttc))   
                if '7' in obstacles_frame_v1_30_10_2[i]['7']:
                    px = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['7']['1'])
                    py = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['7']['2'])
                    print(" position {} {}".format(px,py))  
                if '12' in obstacles_frame_v1_30_10_2[i]['7']:
                    px = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['12']['1'])
                    py = fixfloat(obstacles_frame_v1_30_10_2[i]['7']['12']['2'])
                    print(" position_obs {} {}".format(px,py))               
                print("---------obstacle {:02d} E---------".format(i))


            g_lines_type = []
            g_lines_coeffs = []
            g_lines_endpoint = []       
            if '2' in frame_v1['30']['11']:
                lines_frame_v1_30_10_2 = frame_v1['30']['11']['2']            
                for i in range(0,len(lines_frame_v1_30_10_2)):
                    #print("line type:{:x}".format(lines_frame_v1_30_10_2[i]['9']))
                    print("---------Line {:02d} S---------".format(i))
                    print("line id {}".format(lines_frame_v1_30_10_2[i]['1']))
                    line_type_value = lines_frame_v1_30_10_2[i]['9']

                    for line_type in LINE_TYPE:
                        if (line_type.value & line_type_value) != 0:
                            print(line_type.name)

                    g_lines_type.append(line_type_value)
                    line_endpoint = [[fixfloat(lines_frame_v1_30_10_2[i]['8'][0]['1']),fixfloat(lines_frame_v1_30_10_2[i]['8'][0]['2'])],[fixfloat(lines_frame_v1_30_10_2[i]['8'][1]['1']),fixfloat(lines_frame_v1_30_10_2[i]['8'][1]['2'])]]
                    g_lines_endpoint.append(line_endpoint)
                    print("end point:{}".format(line_endpoint))
                    line_coeffs = [fixfloat(lines_frame_v1_30_10_2[i]['7'][0]),fixfloat(lines_frame_v1_30_10_2[i]['7'][1]),fixfloat(lines_frame_v1_30_10_2[i]['7'][2]),fixfloat(lines_frame_v1_30_10_2[i]['7'][3])]
                    g_lines_coeffs.append(line_coeffs)
                    print("coeffs:{}".format(line_coeffs))
                    #y = line_coeffs[0] + x * line_coeffs[1] + (x**2) * line_coeffs[2] + (x**3) * line_coeffs[3]   
                    #print("x {} y {}".format(x,y))     
                    print("---------Line {:02d} E---------".format(i))    


            scanpoints_frame_v1_30_10_2 = frame_v1['30']['30']

            g_ScanPoints_pts = [] 
            print("---------Scan Point S---------")    
            for i in range(0,len(scanpoints_frame_v1_30_10_2['5'])):
                pts_ = scanpoints_frame_v1_30_10_2['5'][i]
                pts = [fixfloat(pts_['1']),fixfloat(pts_['2'])]
                #print(pts)
                g_ScanPoints_pts.append(pts)
            print("---------Scan Point E---------")    


            print("---------Camera Inner S---------")  
            fx = fixfloat(frame_v1['10']['1'])
            fy = fixfloat(frame_v1['10']['2'])
            cx = fixfloat(frame_v1['10']['3'])
            cy = fixfloat(frame_v1['10']['4'])

            print("fx {}".format(fx))
            print("fy {}".format(fy))
            print("cx {}".format(cx))
            print("cy {}".format(cy))
            opencv_matrix_c = np.zeros([3,3],np.float32)
            opencv_matrix_c[0][0] = fx
            opencv_matrix_c[0][1] = 0
            opencv_matrix_c[0][2] = cx

            opencv_matrix_c[1][0] = 0
            opencv_matrix_c[1][1] = fy
            opencv_matrix_c[1][2] = cy

            opencv_matrix_c[2][0] = 0
            opencv_matrix_c[2][1] = 0
            opencv_matrix_c[2][2] = 1

            print("---------Camera Inner S1---------")  

            k1 = fixfloat(frame_v1['10']['20']['1'][0])
            k2 = fixfloat(frame_v1['10']['20']['1'][1])
            p1 = fixfloat(frame_v1['10']['20']['1'][2])
            p2 = fixfloat(frame_v1['10']['20']['1'][3])
            k3 = fixfloat(frame_v1['10']['20']['1'][4])
            k4 = fixfloat(frame_v1['10']['20']['1'][5])
            k5 = fixfloat(frame_v1['10']['20']['1'][6])
            k6 = fixfloat(frame_v1['10']['20']['1'][7])

            print("k1 {}".format(k1))
            print("k2 {}".format(k2))
            print("p1 {}".format(p1))
            print("p2 {}".format(p2))
            print("k3 {}".format(k3))
            print("k4 {}".format(k4))
            print("k5 {}".format(k5))
            print("k6 {}".format(k6))

            opencv_dist_c = np.zeros([8],np.float32)
            opencv_dist_c[0] = k1
            opencv_dist_c[1] = k2
            opencv_dist_c[2] = p1
            opencv_dist_c[3] = p2
            opencv_dist_c[4] = k3
            opencv_dist_c[5] = k4
            opencv_dist_c[6] = k5
            opencv_dist_c[7] = k6        

            print("---------Camera Inner E---------")  

            opencv_newMatrix, undistort_roi = cv2.getOptimalNewCameraMatrix(opencv_matrix_c, opencv_dist_c, (org_image_width, org_image_height), 1, (org_image_width, org_image_height))
            print("undistort_roi {}".format(undistort_roi))
            h = undistort_roi[3]
            h = int(h-112)
            w = int(h*3840/2160)
            x = int(undistort_roi[0]+(undistort_roi[2]/2)-(w/2))
            y = int(undistort_roi[1]+(undistort_roi[3]/2)-(h/2))
            undistort_adjust_roi = [x,y,w,h]
            print("undistort_adjust_roi {}".format(undistort_adjust_roi))

            mapx, mapy = cv2.initUndistortRectifyMap(opencv_matrix_c, opencv_dist_c, None, opencv_newMatrix, (org_image_width,org_image_height), 5)


            if False:
                f_tmp = open('test_protobuf_{:04d}_perception_info.txt'.format(frame_index), 'w')
                f_tmp.write(json.dumps(box_data_json))
                f_tmp.close()

            if False:
                f_tmp = open('test_pack_{:04d}_info_.bin'.format(frame_index), 'wb')
                f_tmp.write(box_data)
                f_tmp.close()

        box_size_bin = f.read(4)  
        box_size = struct.unpack('I', box_size_bin)[0]
        box_data = f.read(box_size)  

        frameType = "P"
        isIFrame = False
        if box_data[8] == 0x40:
            frameType = "I"
            isIFrame = True
        if not firstIFrameHasReached:
            if isIFrame:
                subbox_size = struct.unpack('I', box_data[0:4])[0]
                subbox_data = box_data[4:4+subbox_size]
                video_encode_data_I = subbox_data

                f.seek(4, 0)
                frame_index = 0;
                firstIFrameHasReached = True
            else:
                frame_index = frame_index + 1
            continue

        if False:
            f_tmp = open('test_pack_{:04d}_video_{}.bin'.format(frame_index,frameType), 'wb')
            f_tmp.write(box_data)
            f_tmp.close()

        subbox_offset = 0
        subbox_image_index = 0

        while True:
            #print('{}/{} S'.format(subbox_offset,box_size))
            subbox_size = struct.unpack('I', box_data[0+subbox_offset:4+subbox_offset])[0]
            subbox_data = box_data[4+subbox_offset:4+subbox_offset+subbox_size]


            if subbox_image_index == 0:
                if isIFrame:
                    video_encode_index = 0
                    video_encode_data = subbox_data
                    video_encode_data_I = subbox_data
                else:
                    video_encode_index = 1
                    video_encode_data = video_encode_data_I + subbox_data

                cur_image = imageio.imread(video_encode_data, index=video_encode_index)
                cv2.namedWindow("ADAS", 0)
                cv2.resizeWindow("ADAS", ui_w, ui_h)

 
                if display_undistort:
                    cur_image = cv2.undistort(cur_image, opencv_matrix_c, opencv_dist_c, None, opencv_newMatrix)
                    if False: 
                        cv2.rectangle(cur_image,  (undistort_roi[0],undistort_roi[1]), (undistort_roi[0]+undistort_roi[2],undistort_roi[1]+ undistort_roi[3]),  (255,0,0),2)
                        cv2.rectangle(cur_image,  (undistort_adjust_roi[0],undistort_adjust_roi[1]), (undistort_adjust_roi[0]+undistort_adjust_roi[2],undistort_adjust_roi[1]+ undistort_adjust_roi[3]),  (255,0,0),2)
                    else:
                        cur_image = cur_image[undistort_adjust_roi[1]:undistort_adjust_roi[1]+undistort_adjust_roi[3], undistort_adjust_roi[0]:undistort_adjust_roi[0]+undistort_adjust_roi[2],:]
                        cur_image = cv2.resize(cur_image,(org_image_width,org_image_height))
                        for i in range(0,len(g_lines_coeffs)):
                            line_endpoint = g_lines_endpoint[i]
                            coeff = g_lines_coeffs[i]
                            x = np.linspace(line_endpoint[0][0], line_endpoint[1][0], 101)
                            y = coeff[0] + x * coeff[1] + (x**2) * coeff[2] + (x**3) * coeff[3]
                            local_sample_points = []
                            for j in range(0,101):
                                bev_x = x[j]
                                bev_y = y[j]
          
                                undistort_x = bev_x*camera_matrix_vcsgnd2img[0]+bev_y*camera_matrix_vcsgnd2img[1]+camera_matrix_vcsgnd2img[2]
                                undistort_y = bev_x*camera_matrix_vcsgnd2img[3+0]+bev_y*camera_matrix_vcsgnd2img[3+1]+camera_matrix_vcsgnd2img[3+2]
                                undistort_z = bev_x*camera_matrix_vcsgnd2img[6+0]+bev_y*camera_matrix_vcsgnd2img[6+1]+camera_matrix_vcsgnd2img[6+2]
                                undistort_x = int(undistort_x/undistort_z)
                                undistort_y = int(undistort_y/undistort_z)

                                if undistort_x > 0 and undistort_x < org_image_width and undistort_y > 0 and undistort_y < org_image_height:
                                    local_sample_points.append([undistort_x,undistort_y])
                            cv2.polylines(cur_image,np.int32([np.array(local_sample_points)]),False,(0,0,255),3)

                        local_sample_points = []
                        for i in range(0,len(g_ScanPoints_pts)):
                            bev_x = g_ScanPoints_pts[i][0]
                            bev_y = g_ScanPoints_pts[i][1]
                            undistort_x = bev_x*camera_matrix_vcsgnd2img[0]+bev_y*camera_matrix_vcsgnd2img[1]+camera_matrix_vcsgnd2img[2]
                            undistort_y = bev_x*camera_matrix_vcsgnd2img[3+0]+bev_y*camera_matrix_vcsgnd2img[3+1]+camera_matrix_vcsgnd2img[3+2]
                            undistort_z = bev_x*camera_matrix_vcsgnd2img[6+0]+bev_y*camera_matrix_vcsgnd2img[6+1]+camera_matrix_vcsgnd2img[6+2]
                            undistort_x = int(undistort_x/undistort_z)
                            undistort_y = int(undistort_y/undistort_z)

                            if undistort_x > 0 and undistort_x < org_image_width and undistort_y > 0 and undistort_y < org_image_height:
                                local_sample_points.append([undistort_x,undistort_y])
                        cv2.polylines(cur_image,np.int32([np.array(local_sample_points)]),False,(0,255,0),2)

                        for i in range(0,len(g_obstacles_rect)):
                            cv2.rectangle(cur_image,  (g_obstacles_rect[i][0], g_obstacles_rect[i][1]), (g_obstacles_rect[i][2], g_obstacles_rect[i][3]),  (255,0,0),2)

                else:
                    cv2.rectangle(cur_image,  (roi_2_rect[0], roi_2_rect[1]), (roi_2_rect[2], roi_2_rect[3]),  (0,0,128),2)
                    cv2.rectangle(cur_image,  (roi_3_rect[0], roi_3_rect[1]), (roi_3_rect[2], roi_3_rect[3]),  (0,0,128),2)   
                    for i in range(0,len(g_obstacles_raw_rect)):
                       cv2.rectangle(cur_image,  (g_obstacles_raw_rect[i][0], g_obstacles_raw_rect[i][1]), (g_obstacles_raw_rect[i][2], g_obstacles_raw_rect[i][3]),  (0,255,0),2)
                    for i in range(0,len(g_lines_coeffs)):
                        line_endpoint = g_lines_endpoint[i]
                        line_type_value = g_lines_type[i]
                        coeff = g_lines_coeffs[i]

                        x = np.linspace(line_endpoint[0][0], line_endpoint[1][0], 101)
                        y = coeff[0] + x * coeff[1] + (x**2) * coeff[2] + (x**3) * coeff[3]
                        local_sample_points = []
                        for j in range(0,101):
                            bev_x = x[j]
                            bev_y = y[j]
                            
                            undistort_x = bev_x*camera_matrix_vcsgnd2img[0]+bev_y*camera_matrix_vcsgnd2img[1]+camera_matrix_vcsgnd2img[2]
                            undistort_y = bev_x*camera_matrix_vcsgnd2img[3+0]+bev_y*camera_matrix_vcsgnd2img[3+1]+camera_matrix_vcsgnd2img[3+2]
                            undistort_z = bev_x*camera_matrix_vcsgnd2img[6+0]+bev_y*camera_matrix_vcsgnd2img[6+1]+camera_matrix_vcsgnd2img[6+2]
                            undistort_x = undistort_x/undistort_z
                            undistort_y = undistort_y/undistort_z

                            if undistort_x > 0 and undistort_x < org_image_width and undistort_y > 0 and undistort_y < org_image_height:
                                org_point_in0 = [undistort_x*undistort_adjust_roi[2]/3840.0+undistort_adjust_roi[0],undistort_y*undistort_adjust_roi[3]/2160.0+undistort_adjust_roi[1]]
                                org_point_out0 = [0,0]

                                distort_x = int(mapx[int(org_point_in0[1]),int(org_point_in0[0])])
                                distort_y  = int(mapy[int(org_point_in0[1]),int(org_point_in0[0])])

                                if distort_x > 0 and distort_x < org_image_width and distort_y > 0 and distort_y < org_image_height:
                                    local_sample_points.append([distort_x,distort_y])
                        isRaw = False
                        for line_type in LINE_TYPE:
                            if (line_type.value & line_type_value) != 0:
                                print(line_type.name)
                                if line_type.name == 'LINE_RAW':
                                    isRaw = True
                        if isRaw:
                            cv2.polylines(cur_image,np.int32([np.array(local_sample_points)]),False,(0,0,255),3)
                        else:
                            cv2.polylines(cur_image,np.int32([np.array(local_sample_points)]),False,(255,0,0),3)

                    # local_sample_points = []
                    # for i in range(0,len(g_ScanPoints_pts)):
                    #     bev_x = g_ScanPoints_pts[i][0]
                    #     bev_y = g_ScanPoints_pts[i][1]
                    #     undistort_x = bev_x*camera_matrix_vcsgnd2img[0]+bev_y*camera_matrix_vcsgnd2img[1]+camera_matrix_vcsgnd2img[2]
                    #     undistort_y = bev_x*camera_matrix_vcsgnd2img[3+0]+bev_y*camera_matrix_vcsgnd2img[3+1]+camera_matrix_vcsgnd2img[3+2]
                    #     undistort_z = bev_x*camera_matrix_vcsgnd2img[6+0]+bev_y*camera_matrix_vcsgnd2img[6+1]+camera_matrix_vcsgnd2img[6+2]
                    #     undistort_x = undistort_x/undistort_z
                    #     undistort_y = undistort_y/undistort_z
                    #     if undistort_x > 0 and undistort_x < org_image_width and undistort_y > 0 and undistort_y < org_image_height:
                    #         org_point_in0 = [undistort_x*undistort_adjust_roi[2]/3840.0+undistort_adjust_roi[0],undistort_y*undistort_adjust_roi[3]/2160.0+undistort_adjust_roi[1]]
                    #         org_point_out0 = [0,0]

                    #         distort_x = int(mapx[int(org_point_in0[1]),int(org_point_in0[0])])
                    #         distort_y  = int(mapy[int(org_point_in0[1]),int(org_point_in0[0])])

                    #         if distort_x > 0 and distort_x < org_image_width and distort_y > 0 and distort_y < org_image_height:
                    #             local_sample_points.append([distort_x,distort_y])
                    # cv2.polylines(cur_image,np.int32([np.array(local_sample_points)]),False,(0,255,0),2)

                    # for i in range(0,len(g_obstacles_rect)):

                    #     undistort_x = g_obstacles_rect[i][0]
                    #     undistort_y = g_obstacles_rect[i][1]

                    #     org_point_in0 = [undistort_x*undistort_adjust_roi[2]/3840.0+undistort_adjust_roi[0],undistort_y*undistort_adjust_roi[3]/2160.0+undistort_adjust_roi[1]]
                    #     org_point_out0 = [0,0]

                    #     org_point_out0[0] = int(mapx[int(org_point_in0[1]),int(org_point_in0[0])])
                    #     org_point_out0[1] = int(mapy[int(org_point_in0[1]),int(org_point_in0[0])])

                    #     undistort_x = g_obstacles_rect[i][2]
                    #     undistort_y = g_obstacles_rect[i][3]
                    #     org_point_in1 = [undistort_x*undistort_adjust_roi[2]/3840.0+undistort_adjust_roi[0],undistort_y*undistort_adjust_roi[3]/2160.0+undistort_adjust_roi[1]]
                    #     org_point_out1 = [0,0]
                    #     org_point_out1[0] = int(mapx[int(org_point_in1[1]),int(org_point_in1[0])])
                    #     org_point_out1[1] = int(mapy[int(org_point_in1[1]),int(org_point_in1[0])])
                        
                    #     cv2.rectangle(cur_image,  (org_point_out0[0], org_point_out0[1]), (org_point_out1[0], org_point_out1[1]),  (255,0,0),2)

                cur_image = cur_image[:,:,::-1]
                cv2.imshow("ADAS", cur_image)
                #cv2.waitKey()
                cv2.waitKey(1)
                #cv2.destroyAllWindows()
                ovideo.write(cur_image)

            if subbox_image_index == 1:
                flat_data = b''
                item_num = int((len(subbox_data)-8)/3)
                sub_image_height = int.from_bytes(subbox_data[4:4+2], "big")
                sub_image_width = int.from_bytes(subbox_data[6:8], "big") 

                for i in range(0,item_num):
                    repeat_count = int.from_bytes(subbox_data[8+1+i*3:8+3+i*3], "little")
                    repeat_byte = subbox_data[8+i*3:8+i*3+1]
                    flat_data = flat_data + (repeat_byte*repeat_count)

                vis_mask_Image = (np.frombuffer(flat_data, dtype=np.uint8)*16).reshape((sub_image_height,sub_image_width,1))

                #cv2.imwrite("vis_mask_Image_{}.png".format(frame_index), vis_Image)

                cv2.namedWindow("ADAS Parser1", 0)
                cv2.resizeWindow("ADAS Parser1", sub_image_width, sub_image_height)
                cv2.imshow("ADAS Parser1", vis_mask_Image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

            if subbox_image_index == 2:
                flat_data = b''
                item_num = int((len(subbox_data)-8)/3)
                sub_image_height = int.from_bytes(subbox_data[4:4+2], "big")
                sub_image_width = int.from_bytes(subbox_data[6:8], "big") 

                for i in range(0,item_num):
                    repeat_count = int.from_bytes(subbox_data[8+1+i*3:8+3+i*3], "little")
                    repeat_byte = subbox_data[8+i*3:8+i*3+1]
                    flat_data = flat_data + (repeat_byte*repeat_count)
                vis_lane_Image = (np.frombuffer(flat_data, dtype=np.uint8)*32).reshape((sub_image_height,sub_image_width,1))
                
                #cv2.imwrite("vis_lane_Image_{}.png".format(frame_index), vis_lane_Image)
                
                cv2.namedWindow("ADAS Parser2", 0)
                cv2.resizeWindow("ADAS Parser2", sub_image_width, sub_image_height)
                cv2.imshow("ADAS Parser2", vis_lane_Image)
                cv2.waitKey(1)
                #cv2.destroyAllWindows()

            if False:
                f_tmp = open('test_pack_{:04d}_video_part_{}_{}.bin'.format(frame_index,subbox_offset,frameType), 'wb')
                f_tmp.write(subbox_data)
                f_tmp.close()


            subbox_offset = subbox_offset + 4+subbox_size
            subbox_image_index = subbox_image_index + 1
            if subbox_offset >= box_size:
                break

        frame_index = frame_index + 1
        #if frame_index > 100:
        #   sys.exit(0)
        if f.tell() >= eof: 
            break
    f.close()
    ovideo.release()
    sys.exit(0)