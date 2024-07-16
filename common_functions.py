import numpy as np
import torch


def pitchyaw_to_vector(pitchyaws):
    """Convert given yaw (:math:`\theta`) and pitch (:math:`\phi`) angles to unit gaze vectors.

    Args:
        pitchyaws (:obj:`numpy.array`): yaw and pitch angles :math:`(n\times 2)` in radians.

    Returns:
        :obj:`numpy.array` of shape :math:`(n\times 3)` with 3D vectors per row.
    """
    n = pitchyaws.shape[0]
    sin = torch.sin(pitchyaws)
    cos = torch.cos(pitchyaws)
    out = torch.empty((n, 3))
    out[:, 0] = torch.mul(cos[:, 0], sin[:, 1])
    out[:, 1] = sin[:, 0]
    out[:, 2] = torch.mul(cos[:, 0], cos[:, 1])
    return out


def angle_error(pre, real):
    """
    compute angle between two different vectors
    :param pre:
    :param real:
    :return:
    """
    dot = torch.sum(pre * real, dim=1)
    dot = torch.clamp(dot, -1, 1)
    return torch.acos(dot) * 180 / np.pi


def avg_angle_error(pre, real):
    """
    compute average angle error between prediction and labels for gaze estimation
    :param pre:
    :param real:
    :return:
    """
    pre_vector = pitchyaw_to_vector(pre)
    real_vector = pitchyaw_to_vector(real)
    avg_error = torch.mean(angle_error(pre_vector, real_vector))
    return avg_error
