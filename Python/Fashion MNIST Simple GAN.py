import torch.nn
import torch.optim
import torchvision.transforms
from torch.utils.data import DataLoader
from torch.utils.data import ConcatDataset
from datetime import datetime

class Generator(torch.nn.Module):
    def __init__(self, latent_dim=100):
        super(Generator, self).__init__()
        self.main = torch.nn.Sequential(
            # First Dense Layer
            torch.nn.Linear(latent_dim, 256),
            torch.nn.BatchNorm1d(256),
            torch.nn.LeakyReLU(0.2, inplace=True),

            # Second Dense Layer
            torch.nn.Linear(256, 512),
            torch.nn.BatchNorm1d(512),
            torch.nn.LeakyReLU(0.2, inplace=True),

            # Third Dense Layer (Core Layer)
            torch.nn.Linear(512, 1024),
            torch.nn.BatchNorm1d(1024),
            torch.nn.LeakyReLU(0.2, inplace=True),

            # Optional Fourth Dense Layer
            torch.nn.Linear(1024, 2048),
            torch.nn.BatchNorm1d(2048),
            torch.nn.LeakyReLU(0.2, inplace=True),

            # Output Dense Layer
            torch.nn.Linear(2048, 784),
            torch.nn.Tanh() # Tanh for image generation, scales output to [-1, 1]
        )

    def forward(self, input):
        img = self.main(input)
        img = img.view(-1, 28, 28) # Reshape to (batch_size, 28, 28)
        return img

class Discriminator(torch.nn.Module):
    def __init__(self, img_dim=784, hidden_dim=256, dropout_rate=0.3):
        super(Discriminator, self).__init__()
        self.main = torch.nn.Sequential(
            torch.nn.Flatten(), # Input will be 28x28 images, Flatten converts to 784-dimensional vector
            torch.nn.Linear(img_dim, hidden_dim),
            torch.nn.LeakyReLU(0.2), # Uses Leaky ReLU activation, helpful in preventing dying ReLU problem
            torch.nn.BatchNorm1d(hidden_dim), # Batch normalization stabilizes training and may reduce overfitting
            torch.nn.Dropout(dropout_rate), # Dropout regularization for preventing overfitting

            torch.nn.Linear(hidden_dim, hidden_dim // 2),  # Halving the hidden dimension for each subsequent layer
            torch.nn.LeakyReLU(0.2),
            torch.nn.BatchNorm1d(hidden_dim // 2),
            torch.nn.Dropout(dropout_rate),

            torch.nn.Linear(hidden_dim // 2, hidden_dim // 4),
            torch.nn.LeakyReLU(0.2),
            torch.nn.BatchNorm1d(hidden_dim // 4),
            torch.nn.Dropout(dropout_rate),

            torch.nn.Linear(hidden_dim // 4, 1), # Outputting a single value as probability (real/fake)
            torch.nn.Sigmoid()  # Sigmoid activation to squash output to [0, 1] for binary classification
        )

    def forward(self, x):
        return self.main(x)

class CombinedModel(torch.nn.Module):
    def __init__(self, generator, discriminator):
        super(CombinedModel, self).__init__()
        self.Generator = generator
        self.Discriminator = discriminator


    def forward(self, x):
        x = self.Generator(x)
        x = self.Discriminator(x)
        return x
    
class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data_tensors):
        self.data = data_tensors

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], 0

InputTransform = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor(),  # Convert PIL Image to PyTorch Tensor
    torchvision.transforms.Resize((28,28)),
    torchvision.transforms.Normalize((0.5,), (0.5,)) # Normalize pixel values to range [-1, 1]
])

if torch.cuda.is_available():
    device = torch.device("cuda")
    with open("simplemodeloutput.txt", "w") as file:
        file.write(f"device properties: {torch.cuda.get_device_properties(device=device)}\n")
    with open("cnnmodeloutput.txt", "w") as file:
        file.write(f"device properties: {torch.cuda.get_device_properties(device=device)}\n")
    print("device properties: ",torch.cuda.get_device_properties(device=device))
else:
    with open("simplemodeloutput.txt", "w") as file:
        file.write(f"using cpu\n")
    with open("cnnmodeloutput.txt", "w") as file:
        file.write(f"using cpu\n")
    device = torch.device("cpu")
print(f"Using device: {device}")

# Training dataset
train_dataset = torchvision.datasets.FashionMNIST(
    root='./data',        # Directory to store the dataset
    train=True,           # Specify training dataset
    download=True,        # Download if not already present
    transform=InputTransform   # Apply the defined transformations
)

# Test dataset
test_dataset = torchvision.datasets.FashionMNIST(
    root='./data',
    train=False,          # Specify test dataset
    download=True,
    transform=InputTransform
)

#relabel train_dataset and test_dataset from classifer integer to 1 for "real image"
train_dataset.targets[:] = 1
test_dataset.targets[:] = 1

genModel=Generator().to(device)
genOptimizer = torch.optim.Adam(genModel.parameters(), lr=0.001)
discModel=Discriminator().to(device)
discOptimizer = torch.optim.Adam(discModel.parameters(), lr=0.001)
fullGAN=CombinedModel(genModel,discModel).to(device)
fullGANOptimizer = torch.optim.Adam(fullGAN.parameters(), lr=0.001)
criterion = torch.nn.BCELoss()
#fullGAN.compile()

num_epochs=100
batch_size = 32
latent_dim = 100

train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True, # Shuffle data for better training
    pin_memory=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False, # No need to shuffle test data
    pin_memory=True
)

start_time = datetime.now()
with open("simplemodeloutput.txt", "a") as file:
    file.write(f"Simple model training started at {start_time}\n")
print("Simple model training started at ",start_time)
for epoch in range(num_epochs):

    for inputs, targets in train_loader:
        #move tensors to device
        inputs = inputs.to(device)
        targets = targets.to(device)
        #set correct model to train
        fullGAN.Discriminator.train()
        fullGAN.Generator.eval()
        #step 0: modify the inputs and targets
        #generate random vectors
        random_vectors = torch.randn(batch_size, latent_dim,device=device)
        #pass them through the Generator
        gen_images=genModel(random_vectors).unsqueeze(1).detach().clone()
        inputs = torch.cat((inputs,gen_images), dim=0)
        targets = torch.cat((targets,torch.zeros(batch_size,device=device)))
        #permute for randomness
        indices = torch.randperm(inputs.size(0))
        inputs = inputs[indices]
        targets = targets[indices]

        # Step 1: Zero the gradients
        fullGANOptimizer.zero_grad(set_to_none=True)

        # Step 2: Forward pass
        outputs = discModel(inputs)
        outputs = outputs.squeeze(1)
        discLoss = criterion(outputs, targets.to(dtype=torch.float32))

        # Step 3: Backward pass
        discLoss.backward()

        # Step 4: Update parameters
        fullGANOptimizer.step()

        #set other model for training
        fullGAN.Discriminator.eval()
        fullGAN.Generator.train()
        #create GAN training data
        random_vectors = torch.randn(batch_size, latent_dim,device=device)
        GAN_targets = torch.ones(batch_size,device=device)
        # Step 1: Zero the gradients
        fullGANOptimizer.zero_grad(set_to_none=True)
        # Step 2: Forward pass
        outputs = fullGAN(random_vectors).squeeze(1)
        genLoss = criterion(outputs, GAN_targets.to(dtype=torch.float32))
        # Step 3: Backward pass
        genLoss.backward()
        # Step 4: Update parameters
        fullGANOptimizer.step()
    if epoch % 10 == 0:
        end_time=datetime.now()
        time_difference = end_time - start_time
        with open("simplemodeloutput.txt", "a") as file:
            file.write(f"Epoch [{epoch+1}/{num_epochs}], Discriminator Loss: {discLoss.item():.4f}\n")
            file.write(f"Epoch [{epoch+1}/{num_epochs}], Generator Loss: {genLoss.item():.4f}\n")
            file.write(f"Epoch [{epoch+1}/{num_epochs}], completed at {end_time}, total run time so far:{time_difference.total_seconds()}\n")
        print(f"Epoch [{epoch+1}/{num_epochs}], Discriminator Loss: {discLoss.item():.4f}")
        print(f"Epoch [{epoch+1}/{num_epochs}], Generator Loss: {genLoss.item():.4f}")
        print(f"Epoch [{epoch+1}/{num_epochs}], completed at ",end_time, " total run time so far:",time_difference.total_seconds()," seconds")
    if genLoss < .0001 and discLoss < .0001:
        break

with open("simplemodeloutput.txt", "a") as file:
    file.write(f"Epoch [{epoch+1}/{num_epochs}], Discriminator Loss: {discLoss.item()}")
    file.write(f"Epoch [{epoch+1}/{num_epochs}], Generator Loss: {genLoss.item()}")

print(f"Epoch [{epoch+1}/{num_epochs}], Discriminator Loss: {discLoss.item()}")
print(f"Epoch [{epoch+1}/{num_epochs}], Generator Loss: {genLoss.item()}")