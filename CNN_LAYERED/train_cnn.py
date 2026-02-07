import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np

from cnn_model import CNN_Model
from training_dataset import training_dataset
from functions import compute_iou


# ----------------------------------
# Training Function
# ----------------------------------

def train_model(model, dataloader, lr_rate, momentum, num_epochs=50):
    """
    Train CNN for bounding box regression.
    Training is CPU-only. FPGA is used only for inference.
    """

    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=lr_rate, momentum=momentum)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

    for epoch in range(num_epochs):

        scheduler.step()
        epoch_loss = 0.0
        epoch_iou = 0.0
        sample_count = 0

        for step, (inputs, labels) in enumerate(dataloader):

            # Reshape inputs
            inputs = inputs.view(inputs.size(0), 1, 100, 100)
            labels = labels.view(labels.size(0), 4)

            optimizer.zero_grad()

            outputs = model(inputs)

            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # Metrics
            preds = outputs.detach().numpy()
            gts = labels.detach().numpy()

            avg_iou, _ = compute_iou(gts, preds)

            epoch_loss += loss.item()
            epoch_iou += avg_iou
            sample_count += 1

            print(
                f"[Epoch {epoch+1:03d}, Step {step+1:03d}] "
                f"Loss: {loss.item():.6f}, IoU: {avg_iou:.4f}"
            )

        print("--------------------------------------------------")
        print(
            f"Epoch {epoch+1} Summary | "
            f"Avg Loss: {epoch_loss/sample_count:.6f}, "
            f"Avg IoU: {epoch_iou/sample_count:.4f}"
        )
        print("--------------------------------------------------")

    print("Training completed successfully.")


# ----------------------------------
# Main
# ----------------------------------

if __name__ == "__main__":

    # Hyperparameters
    learning_rate = 1e-6
    momentum = 0.9
    batch_size = 100
    num_workers = 2
    shuffle = True
    epochs = 50

    # Dataset and DataLoader
    train_dataset = training_dataset()

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers
    )

    # Model
    model = CNN_Model()
    model.train()

    # Train
    train_model(
        model=model,
        dataloader=train_loader,
        lr_rate=learning_rate,
        momentum=momentum,
        num_epochs=epochs
    )

    # Save trained weights
    torch.save(model.state_dict(), "./Model/cnn_model.pth")
    print("Model saved to ./Model/cnn_model.pth")
