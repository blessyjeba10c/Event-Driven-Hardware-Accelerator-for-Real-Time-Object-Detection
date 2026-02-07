import torch
import torch.nn as nn
import torch.nn.functional as F

class CNN_Model(nn.Module):
    """
    Lightweight CNN for edge inference on Xilinx Zynq SoC.
    Designed for HW/SW co-design where convolution layers
    are intended for FPGA acceleration.
    """

    def __init__(self):
        super(CNN_Model, self).__init__()

        # --------------------
        # Convolutional Layers
        # --------------------

        # Input: 1 x 100 x 100
        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=32,
            kernel_size=5,
            stride=1,
            padding=0
        )
        # Output: 32 x 96 x 96 → MaxPool → 32 x 48 x 48

        self.conv2 = nn.Conv2d(
            in_channels=32,
            out_channels=64,
            kernel_size=5,
            stride=1,
            padding=0
        )
        # Output: 64 x 44 x 44 → MaxPool → 64 x 22 x 22

        self.conv3 = nn.Conv2d(
            in_channels=64,
            out_channels=128,
            kernel_size=5,
            stride=1,
            padding=0
        )
        # Output: 128 x 18 x 18

        # --------------------
        # Fully Connected Layers
        # --------------------

        self.fc1 = nn.Linear(
            in_features=18 * 18 * 128,
            out_features=2048
        )

        # Output: bounding box (x, y, width, height)
        self.fc2 = nn.Linear(
            in_features=2048,
            out_features=4
        )

    def forward(self, x):
        """
        Forward pass optimized for inference.
        """

        # Conv Layer 1
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, kernel_size=2, stride=2)

        # Conv Layer 2
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, kernel_size=2, stride=2)

        # Conv Layer 3
        x = F.relu(self.conv3(x))

        # Flatten
        x = x.view(x.size(0), -1)

        # Fully Connected Layers
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x
