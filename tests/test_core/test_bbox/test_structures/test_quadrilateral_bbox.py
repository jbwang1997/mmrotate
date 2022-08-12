# Copyright (c) OpenMMLab. All rights reserved.
from math import sqrt
from unittest import TestCase

import numpy as np
import torch
from mmengine.testing import assert_allclose

from mmrotate.core.bbox.structures import QuadriBoxes


class TestQuadriBoxes(TestCase):

    def test_propoerty(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        bboxes = QuadriBoxes(th_bboxes)

        # Centers
        centers = torch.Tensor([17, 15]).reshape(1, 1, 2)
        assert_allclose(bboxes.centers, centers)
        # Areas
        areas = torch.Tensor([100]).reshape(1, 1)
        assert_allclose(bboxes.areas, areas)
        # widths
        widths = torch.Tensor([10]).reshape(1, 1)
        assert_allclose(bboxes.widths, widths)
        # heights
        heights = torch.Tensor([10]).reshape(1, 1)
        assert_allclose(bboxes.heights, heights)

    def test_flip(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        img_shape = [50, 85]
        bboxes = QuadriBoxes(th_bboxes)

        # horizontal flip
        flipped_bboxes_th = torch.Tensor([75, 10, 65, 10, 61, 20, 71,
                                          20]).reshape(1, 1, 8)
        flipped_bboxes = bboxes.flip(img_shape, direction='horizontal')
        assert_allclose(flipped_bboxes.tensor, flipped_bboxes_th)
        # vertical flip
        flipped_bboxes_th = torch.Tensor([10, 40, 20, 40, 24, 30, 14,
                                          30]).reshape(1, 1, 8)
        flipped_bboxes = bboxes.flip(img_shape, direction='vertical')
        assert_allclose(flipped_bboxes.tensor, flipped_bboxes_th)
        # diagonal flip
        flipped_bboxes_th = torch.Tensor([75, 40, 65, 40, 61, 30, 71,
                                          30]).reshape(1, 1, 8)
        flipped_bboxes = bboxes.flip(img_shape, direction='diagonal')
        assert_allclose(flipped_bboxes.tensor, flipped_bboxes_th)

    def test_translate(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        bboxes = QuadriBoxes(th_bboxes)

        translated_bboxes = bboxes.translate([23, 46])
        translated_bboxes_th = torch.Tensor([33, 56, 43, 56, 47, 66, 37,
                                             66]).reshape(1, 1, 8)
        assert_allclose(translated_bboxes.tensor, translated_bboxes_th)
        # negative
        translated_bboxes = bboxes.translate([-6, -2])
        translated_bboxes_th = torch.Tensor([4, 8, 14, 8, 18, 18, 8,
                                             18]).reshape(1, 1, 8)
        assert_allclose(translated_bboxes.tensor, translated_bboxes_th)

    def test_clip(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        img_shape = [13, 14]
        bboxes = QuadriBoxes(th_bboxes)

        cliped_bboxes = bboxes.clip(img_shape)
        cliped_bboxes_th = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                         20]).reshape(1, 1, 8)
        assert_allclose(cliped_bboxes.tensor, cliped_bboxes_th)
        self.assertIsNot(cliped_bboxes.tensor, th_bboxes)

    def test_rotate(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 20, 20, 10,
                                  20]).reshape(1, 1, 8)
        center = (15, 15)
        angle = 45
        bboxes = QuadriBoxes(th_bboxes)

        rotated_bboxes = bboxes.rotate(center, angle)
        rotated_bboxes_th = torch.Tensor([
            15 - 5 * sqrt(2), 15, 15, 15 - 5 * sqrt(2), 15 + 5 * sqrt(2), 15,
            15, 15 + 5 * sqrt(2)
        ]).reshape(1, 1, 8)
        assert_allclose(rotated_bboxes.tensor, rotated_bboxes_th)

    def test_project(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        matrix = np.random.rand(3, 3)
        bboxes = QuadriBoxes(th_bboxes)
        bboxes.project(matrix)

    def test_rescale(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        scale_factor = [0.4, 0.8]
        bboxes = QuadriBoxes(th_bboxes)

        rescaled_bboxes = bboxes.rescale(scale_factor)
        rescaled_bboxes_th = torch.Tensor([4, 8, 8, 8, 9.6, 16, 5.6,
                                           16]).reshape(1, 1, 8)
        assert_allclose(rescaled_bboxes.tensor, rescaled_bboxes_th)
        rescaled_bboxes = bboxes.rescale(scale_factor, mapping_back=True)
        rescaled_bboxes_th = torch.Tensor([25, 12.5, 50, 12.5, 60, 25, 35,
                                           25]).reshape(1, 1, 8)
        assert_allclose(rescaled_bboxes.tensor, rescaled_bboxes_th)

    def test_resize_bboxes(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        bboxes = QuadriBoxes(th_bboxes)

        with self.assertRaises(AssertionError):
            resized_bboxes = bboxes.resize_bboxes([0.4, 0.8])
        resized_bboxes = bboxes.resize_bboxes([0.4, 0.4])
        resized_bboxes_th = torch.Tensor(
            [14.2, 13, 18.2, 13, 19.8, 17, 15.8, 17]).reshape(1, 1, 8)
        assert_allclose(resized_bboxes.tensor, resized_bboxes_th)

    def test_is_bboxes_inside(self):
        th_bboxes = torch.Tensor([[10, 10, 20, 10, 24, 20, 14, 20],
                                  [20, 10, 30, 10, 34, 20, 24, 20],
                                  [25, 10, 35, 10, 39, 20, 29,
                                   20]]).reshape(1, 3, 8)
        img_shape = [30, 30]
        bboxes = QuadriBoxes(th_bboxes)

        index = bboxes.is_bboxes_inside(img_shape)
        index_th = torch.BoolTensor([True, True, False]).reshape(1, 3)
        self.assertEqual(tuple(index.size()), (1, 3))
        assert_allclose(index, index_th)

    def test_find_inside_points(self):
        th_bboxes = torch.Tensor([10, 10, 20, 10, 24, 20, 14,
                                  20]).reshape(1, 1, 8)
        bboxes = QuadriBoxes(th_bboxes)
        points = torch.Tensor([[9, 15], [11, 15], [12.5, 15], [17, 15]])
        index = bboxes.find_inside_points(points)
        index_th = torch.BoolTensor([False, False, True, True]).reshape(4, 1)
        self.assertEqual(tuple(index.size()), (4, 1))
        assert_allclose(index, index_th)
