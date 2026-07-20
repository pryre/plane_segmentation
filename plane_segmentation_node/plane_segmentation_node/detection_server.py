
#!/usr/bin/env python3

import numpy as np

from plane_segmentation_interfaces.msg import PlaneResults, PlaneResult
from .plane_detector import detect_planes

from rclpy.node import Node
from std_msgs.msg import Header
from geometry_msgs.msg import Pose
import cv2
from message_filters import QoSProfile, TimeSynchronizer, Subscriber


from typing import Any, TypeVar
_R = TypeVar("_R")
def param_same_as_default(node:Node, param:str, default:_R) -> _R:
    p = node.declare_parameter(param, default).value
    return type(default)(p if p else default) # type: ignore

from rclpy.time import Time
from builtin_interfaces.msg import Time as TimeStamp
def time_zero():
    return Time.from_msg(TimeStamp())

from sensor_msgs.msg import Image, CameraInfo
from visualization_msgs.msg import Marker, MarkerArray
from cv_bridge import CvBridge

class DetectionServer(Node):
    def __init__(self):
        super().__init__("detection_server") # type: ignore
        self._bridge = CvBridge()

        self.target = param_same_as_default(self, "target", "base_link")
        self.geometry_scale = param_same_as_default(self, "geometry_scale", 1.0)
        # self.delay = Duration(seconds=param_same_as_default(self, "delay", 1.0))

        # self._sub_depth = self.create_subscription(Image, "depth", self._cb_depth, 10)
        # self._sub_color = self.create_subscription(Image, "color", self._cb_color, 10)
        self._pub_mask = self.create_publisher(Image, '~/mask', 10)
        self._pub_overlay = self.create_publisher(Image, '~/overlay', 10)
        self._pub_results = self.create_publisher(PlaneResults, "~/planes", 10)
        self._pub_viz = self.create_publisher(MarkerArray, '/markers', 10)

        self._ts = TimeSynchronizer(
            [
                Subscriber(self, CameraInfo, "depth/camera_info"),
                Subscriber(self, Image, "depth/image_rect_raw"),
                Subscriber(self, CameraInfo, "color/camera_info"),
                Subscriber(self, Image, "color/image_raw")
                # Subscriber(self, realsense2_camera_msgs/msg/Extrinsics, "extrinsics/depth_to_color"),
            ],
            10
        )
        self._ts.registerCallback(self.detect)

        # self._timer_status = self.create_timer(1/5.0, self._cb_status)

        # self.detector = PlaneDetector()
        # self.params = PlaneParam()

    def get_display_marker(self, header:Header, result:PlaneResult, id:int):
        marker = Marker()
        marker.header = header
        marker.ns = self.get_name()
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = 0
        marker.pose = Pose()
        marker.pose.position = result.center
        marker.scale.x = self.geometry_scale
        marker.scale.y = self.geometry_scale
        marker.scale.z = self.geometry_scale / 10.0
        marker.color.a = 1.0
        marker.color.b = (result.mask_color >> 16 & 0xFF) / 255.0
        marker.color.g = (result.mask_color >> 8 & 0xFF) / 255.0
        marker.color.r = (result.mask_color & 0xFF) / 255.0
        return marker

    def publish_viz(self, header:Header, results:list[PlaneResult]):
        if not self.geometry_scale:
            return

        markers = MarkerArray()
        markers.markers = []
        for i, r in enumerate(results):
            markers.markers.append(self.get_display_marker(header, r, i))

        self._pub_viz.publish(markers)


    def publish_results(self, header:Header, results:list[PlaneResult]):
        # for pp in plane_params:
        #     res.norms.extend(pp.w.tolist())
        #     res.center_3d.extend(pp.pts_3d_center.tolist())
        #     res.center_2d.extend(pp.pts_2d_center.tolist())
        #     res.mask_color.extend(pp.mask_color.tolist())

        msg = PlaneResults()
        msg.header = header
        msg.results = results
        self._pub_results.publish(msg)

    def publish_debug(self, header:Header, mask:np.ndarray, color:np.ndarray, results:list[PlaneResult]):
        mask_msg = self._bridge.cv2_to_imgmsg(mask, header=header)
        self._pub_mask.publish(mask_msg)

        for r in results:
            color = cv2.circle(color, center=(r.image_x, r.image_y), radius=20, color=(255,255,255), thickness=2)

        color_msg = self._bridge.cv2_to_imgmsg(color, header=header, encoding="rgb8")
        self._pub_overlay.publish(color_msg)


    def detect(self, depth_info:CameraInfo, depth_msg:Image, color_info:CameraInfo, color_msg:Image):
        # -- Detect plane.
        # self.get_logger().info("=================================================")
        # self.get_logger().info("Start plane detection")

        depth = self._bridge.imgmsg_to_cv2(depth_msg)
        color = self._bridge.imgmsg_to_cv2(color_msg)

        # results:list[PlaneResult] = list()
        results, mask = detect_planes(depth_info, depth, color)

        # self.get_logger().info("Finish plane detection")
        # # -- Print result.
        # for i, plane_param in enumerate(list_plane_params):
        #     plane_param.print_params(index=i+1)

        # self.get_logger().info("Handle results")
        header = depth_msg.header
        self.publish_results(header, results)
        self.publish_debug(color_msg.header, mask, color, results)
        self.publish_viz(header, results)


