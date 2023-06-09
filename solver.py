import torch
import torch.optim as optim
import torch.nn as nn
import os
import time
from tqdm import tqdm
import sys
from models.mask_rcnn import Mask_RCNN
from utils.utils import  visualize_mask, show, visualize_bbox, predicted_bbox, predicted_mask
from torchvision.utils import draw_segmentation_masks, make_grid
import matplotlib.pyplot as plt
import torchvision
import cv2, random, numpy as np
from utils.pytorchtools import EarlyStopping
from torchmetrics.detection.mean_ap import MeanAveragePrecision
from torch.utils.tensorboard import SummaryWriter

class Solver(object):
    """Solver for training and testing."""

    def __init__(self, train_loader, valid_loader, test_loader, device, classes, args):
        """Initialize configurations."""
        self.args = args
        self.model_name = 'modanet_maskRCNN_{}.pth'.format(self.args.model_name)

        # Define the model
        self.classes = classes
        self.num_classes = len(self.classes)

        self.net = Mask_RCNN(self.num_classes, self.args).to(device)

        self.train_loader = train_loader
        self.valid_loader = valid_loader
        self.test_loader = test_loader

        self.device = device

        # load a pretrained model
        if self.args.resume_train or self.args.mode in ['test','evaluate']:
            self.load_model()
        
        if(self.args.mode == "train"):
            # Choose optimizer 
            if self.args.pretrained:
                params = [p for p in self.net.parameters() if p.requires_grad]
            else:
                for param in self.net.parameters():
                    param.requires_grad = True
                params = [p for p in self.net.parameters()]
            for n,p in self.net.named_parameters():
                print(n, p.requires_grad)
            if self.args.opt == "SGD":
                self.optimizer = optim.SGD(params, lr=self.args.lr)
            elif self.args.opt == "Adam":
                self.optimizer = optim.Adam(params, lr=self.args.lr)

            self.epochs = self.args.epochs
            self.writer = SummaryWriter(self.args.checkpoint_path + '/runs/' + self.args.run_name + self.args.opt)

    def save_model(self, epoch):
        # if you want to save the model
        checkpoint_name = "epoch" + str(epoch) + "_" + self.model_name
        check_path = os.path.join(self.args.checkpoint_path, checkpoint_name)
        torch.save(self.net.state_dict(), check_path)
        print("Model saved!")

    def load_model(self):
        # function to load the model
        check_path = os.path.join(self.args.checkpoint_path, self.model_name)
        self.net.load_state_dict(torch.load(check_path, map_location=torch.device(self.device)))
        print("Model loaded!", flush=True)
    
    def train(self):
        self.net.train()
        self.train_loss = []
        self.val_loss = []
        early_stopping = EarlyStopping(patience=2, verbose=True)
        for epoch in range(self.epochs):
            print(f"\nEPOCH {epoch+1} of {self.epochs}", flush=True)
            running_loss = 0.0
            # start timer and carry out training and validation
            start = time.time()
            print('Solver Training', flush=True)
            train_loss_list = []
            
            # initialize tqdm progress bar
            prog_bar = tqdm(self.train_loader, total=len(self.train_loader))
            loss_dict_tb = {
                "loss_classifier": 0,
                "loss_box_reg": 0,
                "loss_mask": 0,
                "loss_objectness": 0,
                "loss_rpn_box_reg": 0,
            }
            if self.args.cls_accessory:
                loss_dict_tb["loss_accessory"]=0

            for i, data in enumerate(prog_bar):
                self.optimizer.zero_grad()
                images, targets = data
                images =  list(image.to(self.device) for image in images)
                targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]

                loss_dict = self.net(images, targets) # when given images and targets as input it will return the loss
                losses = sum(loss for loss in loss_dict.values())
                loss_value = losses.item()
                train_loss_list.append(loss_value)
                losses.backward()
                self.optimizer.step()
                
                prog_bar.set_description(desc=f"Loss: {loss_value:.4f}")

                running_loss += loss_value
               
                for loss in loss_dict:
                    loss_dict_tb[loss] += loss_dict[loss].item()

                del losses, loss_dict, loss_value
                if i % self.args.print_every == self.args.print_every - 1:  
                    print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / self.args.print_every:.3f}')

                    self.writer.add_scalar('training loss',
                        running_loss / self.args.print_every,
                        epoch * len(self.train_loader) + i)
                    
                    for loss in loss_dict_tb:
                        self.writer.add_scalar(loss,
                        loss_dict_tb[loss]/ self.args.print_every,
                        epoch * len(self.train_loader) + i)

                    running_loss = 0.0
                    loss_dict_tb = {
                        "loss_classifier": 0,
                        "loss_box_reg": 0,
                        "loss_mask": 0,
                        "loss_objectness": 0,
                        "loss_rpn_box_reg": 0
                    }
                    if self.args.cls_accessory:
                        loss_dict_tb["loss_accessory"]=0
            val_loss_list = self.validate()
            self.evaluate(epoch)
            print(f"Epoch #{epoch+1} train loss: {sum(train_loss_list)/len(self.train_loader):.3f}", flush=True)   
            print(f"Epoch #{epoch+1} validation loss: {sum(val_loss_list)/len(self.valid_loader):.3f}", flush=True)  

            self.train_loss.append(sum(train_loss_list)/len(self.train_loader));
            self.val_loss.append(sum(val_loss_list)/len(self.valid_loader));

            self.writer.add_scalar('validation loss',
                        sum(val_loss_list)/len(self.valid_loader),epoch)
            end = time.time()
            print(f"Took {((end - start) / 60):.3f} minutes for epoch {epoch}", flush=True)
            #self.test(epoch)
            self.save_model(epoch)
            early_stopping(sum(val_loss_list)/len(self.valid_loader), self.net)
        
            if early_stopping.early_stop:
                print("Early stopping", flush=True)
                break
        
            
        self.writer.flush()
        self.writer.close()
        print('Finished Training', flush=True)  
        #self.test() 

    def validate(self):
        print('Validating')
        val_itr = 0
        val_loss_list = []
        # initialize tqdm progress bar
        prog_bar = tqdm(self.valid_loader, total=len(self.valid_loader))
        loss_value = 0
        for i, data in enumerate(prog_bar):
            images, targets = data
            images = list(image.to(self.device) for image in images)
            targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]
            with torch.no_grad():
                loss_dict = self.net(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            loss_value = losses.item()
            val_loss_list.append(loss_value)
            val_itr += 1
            # update the loss value beside the progress bar for each iteration
            prog_bar.set_description(desc=f"Loss: {loss_value:.4f}\n\n")
        self.net.train()
        return val_loss_list
    
    def test(self, img_count=1):
        print("Testing", flush=True)
        i = 0
        for data in self.test_loader:
            if(i==img_count):
                break
            images, targets = data
            self.net.eval()
            #test_img = images[0].to(self.device)
            #prediction = self.net(test_img)
            prediction = self.net([images[0]])
            test_img = images[0].to(self.device)
            prediction = self.net([test_img])
            #print(prediction[0])
            #print(targets[0], flush=True)
            results = predicted_bbox(images[0],prediction,self.classes)
            results += predicted_mask(images[0],prediction)
            concatenation = np.concatenate((results[0],results[1],results[2]), axis=1)
            # image_name = str(epoch) + "_" + str(i) + "_image"
            # self.writer.add_image(image_name, concatenation)
            #show(results)
            i+=1
            
    def evaluate(self, epoch):
        self.net.eval()
        metric_bbox = MeanAveragePrecision(iou_type="bbox")
        metric_mask = MeanAveragePrecision(iou_type="segm")
        with torch.no_grad():
          for data in tqdm(self.valid_loader):
              images, targets = data
              images = list(image.to(self.device) for image in images)
              targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]
              prediction = self.net(images)
              metric_bbox.update(prediction, targets)
              for pred in prediction:
                  pred['masks']=pred['masks'].squeeze()
                  pred['masks'] = pred['masks']>0.5
              metric_mask.update(prediction, targets)
          result_bbox = metric_bbox.compute()
          result_mask = metric_mask.compute()
        if self.args.mode == "train":
            self.writer.add_scalar('accuracy bbox',
                            result_bbox.map.item(),epoch)
            self.writer.add_scalar('accuracy mask',
                            result_mask.map.item(),epoch)
        file_path = self.args.checkpoint_path + self.model_name + '_evaluate.txt'  # Specify the path to your file
        file = open(file_path, 'a')

        # Write content to the file
        file.write('result_mask MAP: ',result_mask.map.item())
        file.write('result_bbox MAP: ',result_bbox.map.item())
        self.net.train()
    

    def debug(self):
        print("Debug")