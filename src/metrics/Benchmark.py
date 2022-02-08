from typing import Callable, List

import numpy as np
import numpy.typing as npt

from src.utils.metrics import group_indices_by_labels


def mean(
    pc_points: npt.NDArray[np.float64],
    pred_labels: npt.NDArray[np.int32],
    gt_labels: npt.NDArray[np.int32],
    metrics: List[
        Callable[
            [npt.NDArray[np.float64], npt.NDArray[np.int32], npt.NDArray[np.int32]],
            np.float64,
        ]
    ],
) -> List[np.float64]:
    """
    :param pc_points: source point cloud
    :param pred_labels: labels of points obtained as a result of segmentation
    :param gt_labels: reference labels of point cloud
    :param metrics: list of metric functions for which you want to get the mean value
    :return: list of mean value for each metric
    """
    assert pc_points.shape[1] == 3, "Dimension of the array of points should be (n, 3)"
    assert (
        pc_points.shape[0] == pred_labels.size
    ), "Number of points does not match the array of predicted labels"
    assert (
        pc_points.shape[0] == gt_labels.size
    ), "Number of points does not match the array of ground truth labels"

    plane_predicted_dict = group_indices_by_labels(pred_labels)
    plane_gt_dict = group_indices_by_labels(gt_labels)
    unique_labels = np.unique(pred_labels)
    metrics_mean = []

    for metric in metrics:
        mean_array = np.empty((1, 0), np.float64)
        for label in unique_labels:
            if label in plane_gt_dict:
                mean_array = np.append(
                    mean_array,
                    metric(
                        pc_points, plane_predicted_dict[label], plane_gt_dict[label]
                    ),
                )

        if mean_array.size == 0:
            metrics_mean.append(0)
        else:
            metrics_mean.append(mean_array.mean())

    return metrics_mean
