import numpy as np

def compute_iou(gt_boxes, pred_boxes):
    """
    Computes Intersection over Union (IoU) between
    ground-truth and predicted bounding boxes.

    Parameters:
    gt_boxes   : numpy array of shape (N, 4)
                 Each box = [x, y, width, height]
    pred_boxes : numpy array of shape (N, 4)

    Returns:
    avg_iou    : Average IoU across all samples
    iou_list   : List of IoU values per sample
    """

    assert len(gt_boxes) == len(pred_boxes), "Mismatch in number of boxes"

    iou_sum = 0.0
    iou_list = []

    for i in range(len(gt_boxes)):

        gt = gt_boxes[i]
        pred = pred_boxes[i]

        # Intersection rectangle
        x_left   = max(gt[0], pred[0])
        y_top    = max(gt[1], pred[1])
        x_right  = min(gt[0] + gt[2], pred[0] + pred[2])
        y_bottom = min(gt[1] + gt[3], pred[1] + pred[3])

        # Intersection area
        inter_width  = max(0, x_right - x_left)
        inter_height = max(0, y_bottom - y_top)
        inter_area   = inter_width * inter_height

        # Union area
        gt_area   = gt[2] * gt[3]
        pred_area = pred[2] * pred[3]
        union_area = gt_area + pred_area - inter_area

        # IoU computation (safe division)
        if union_area == 0:
            iou = 0.0
        else:
            iou = inter_area / union_area

        iou = np.clip(iou, 0.0, 1.0)

        iou_sum += iou
        iou_list.append(iou)

    avg_iou = iou_sum / len(gt_boxes)

    return avg_iou, iou_list
