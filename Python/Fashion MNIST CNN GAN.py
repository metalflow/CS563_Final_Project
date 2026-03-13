import torch.nn
import torch.optim
import torchvision.transforms
from torch.utils.data import DataLoader
from torch.utils.data import ConcatDataset
from datetime import datetime

class CNNGenerator(torch.nn.Module):
    def __init__(self, latent_dim=100):
        super(CNNGenerator, self).__init__()
        self.fc = torch.nn.Linear(latent_dim, 7 * 7 * 128)
        self.deconv1 = torch.nn.ConvTranspose2d(128, 64, kernel_size=5, stride=2, padding=2, output_padding=1)
        self.bn1 = torch.nn.BatchNorm2d(64)
        self.deconv2 = torch.nn.ConvTranspose2d(64, 1, kernel_size=5, stride=2, padding=2, output_padding=1)
        self.relu = torch.nn.ReLU()
        self.tanh = torch.nn.Tanh()

    def forward(self, x):
        x = self.fc(x)
        x = x.view(-1, 128, 7, 7)  # Reshape to (batch_size, 128, 7, 7)
        x = self.relu(self.bn1(self.deconv1(x)))
        x = self.tanh(self.deconv2(x))
        return x

class CNNDiscriminator(torch.nn.Module):
    def __init__(self, img_dim=784, hidden_dim=256, dropout_rate=0.3):
        super(CNNDiscriminator, self).__init__()
        self.main = torch.nn.Sequential(
            # Input: (28x28x1)
            torch.nn.Conv2d(1, 64, kernel_size=5, stride=2, padding=2, bias=False),
            torch.nn.LeakyReLU(0.2, inplace=True),
            # Output of first conv: (14x14x64)

            torch.nn.Conv2d(64, 128, kernel_size=5, stride=2, padding=2, bias=False),
            torch.nn.BatchNorm2d(128),
            torch.nn.LeakyReLU(0.2, inplace=True),
            # Output of second conv: (7x7x128)

            torch.nn.Flatten(), # Flattens to 7*7*128 = 6272
            torch.nn.Linear(7 * 7 * 128, 1),
            torch.nn.Sigmoid()
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
    
genModel=CNNGenerator().to(device)
genOptimizer = torch.optim.Adam(genModel.parameters(), lr=0.001)
discModel=CNNDiscriminator().to(device)
discOptimizer = torch.optim.Adam(discModel.parameters(), lr=0.001)
fullGAN=CombinedModel(genModel,discModel).to(device)
fullGANOptimizer = torch.optim.Adam(fullGAN.parameters(), lr=0.001)
criterion = torch.nn.BCELoss()

num_epochs=100
batch_size = 32
latent_dim = 100

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
with open("cnnmodeloutput.txt", "a") as file:
    file.write(f"Simple model training started at {start_time}\n")
print("CNN model training started at ",start_time)
for epoch in range(num_epochs):
    for inputs, targets in train_loader:
        inputs = inputs.to(device)
        targets = targets.to(device)
        fullGAN.Discriminator.train()
        fullGAN.Generator.eval()
        #step 0: modify the inputs and targets
        #generate random vectors
        random_vectors = torch.randn(batch_size, latent_dim,device=device)
        #pass them through the Generator
        gen_images=genModel(random_vectors).detach().clone()
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

        #discModel.eval()
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
        with open("cnnmodeloutput.txt", "a") as file:
            file.write(f"Epoch [{epoch+1}/{num_epochs}], Discriminator Loss: {discLoss.item():.4f}\n")
            file.write(f"Epoch [{epoch+1}/{num_epochs}], Generator Loss: {genLoss.item():.4f}\n")
            file.write(f"Epoch [{epoch+1}/{num_epochs}], completed at {end_time}, total run time so far:{time_difference.total_seconds()}\n")
        print(f"Epoch [{epoch+1}/{num_epochs}], Discriminator Loss: {discLoss.item():.4f}")
        print(f"Epoch [{epoch+1}/{num_epochs}], Generator Loss: {genLoss.item():.4f}")
        print(f"Epoch [{epoch+1}/{num_epochs}], completed at ",end_time, " total run time so far:",time_difference.total_seconds()," seconds")
    if genLoss < .005 and discLoss < .005:
        break

with open("cnnmodeloutput.txt", "a") as file:
    file.write(f"Epoch [{epoch+1}/{num_epochs}], Discriminator Loss: {discLoss.item()}")
    file.write(f"Epoch [{epoch+1}/{num_epochs}], Generator Loss: {genLoss.item()}")
print(f"Epoch [{epoch+1}/{num_epochs}], CNNDiscriminator Loss: {discLoss.item()}")
print(f"Epoch [{epoch+1}/{num_epochs}], CNNGenerator Loss: {genLoss.item()}")