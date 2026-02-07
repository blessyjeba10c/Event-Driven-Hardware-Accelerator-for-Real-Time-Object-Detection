import numpy as np
import pandas as pd
import torch

from cnn_model import CNN_Model          # Updated model class
from functions import compute_iou        # Updated IoU function

# ----------------------------
# Load Test Dataset
# ----------------------------

testX = pd.read_csv('Dataset/testData.csv', header=None).values
groundTruth = pd.read_csv('Dataset/ground-truth-test.csv', header=None).values

# Reshape input for CNN: (N, 1, 100, 100)
testX = testX.reshape(len(testX), 1, 100, 100)

# ----------------------------
# Load Model
# ----------------------------

device = torch.device("cpu")   # CPU baseline (for comparison with FPGA later)

model = CNN_Model().to(device)
model.eval()

# Load trained weights
model.load_state_dict(torch.load('Model/cnn_model.pth', map_location=device))

# ----------------------------
# Inference
# ----------------------------

with torch.no_grad():
    input_tensor = torch.tensor(testX, dtype=torch.float32).to(device)
    output = model(input_tensor)

# Convert output to numpy
pred_boxes = output.cpu().numpy()

# Convert to integer bounding boxes
pred_boxes = pred_boxes.astype(int)

# ----------------------------
# Evaluation (IoU)
# ----------------------------

avg_iou, iou_list = compute_iou(groundTruth, pred_boxes)

print("===================================")
print(" CPU-ONLY CNN INFERENCE PERFORMANCE ")
print("===================================")
print(f"Test Average IoU Score : {avg_iou:.4f}")
print("===================================")

# ----------------------------
# Save Results
# ----------------------------

np.savetxt('Results/test-result.csv', pred_boxes, delimiter=',', fmt='%d')
np.savetxt('Results/iou-scores.csv', np.array(iou_list), delimiter=',')

print("Results saved:")
print(" - Bounding boxes  → Results/test-result.csv")
print(" - IoU scores      → Results/iou-scores.csv")
