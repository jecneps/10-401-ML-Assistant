

import pygame
import sys
import NeuralNets as nets
import Neurons
import DigitDrawerViewModel as ddvm
import DataViewModel as dvm
import TrainingViewModel as TTVM
import NNDrawer as NND
import jygame as jp
import Colors
import KNNViewModel as KNNView


class Controler(object):
	def __init__(self, views, classes):
		self.mainView = views
		self.classes = classes
		self.index = 0
		self.buttons = [jp.GenericRectButton(self.inc, "Change Algorithim", 10, 10)]

	def inc(self):
		self.index = (self.index + 1) % len(self.classes);
		self.mainView[1] = self.classes[self.index]

	def getDrawables(self):
		shapes = list()
		shapes.extend(self.buttons)
		return shapes

	def quit(self):
		pass

	def mouseEvent(self, x, y, eventType):
		if eventType == pygame.MOUSEBUTTONDOWN:
			for button in self.buttons:
				if button.inRange(x,y):
					button.onClick()
		pass


class MachineLearningGameLoop(object):

	def __init__(self):
		pygame.init()
		infoObj = pygame.display.Info()
		self.width = infoObj.current_w
		self.height = infoObj.current_h - 60
	
		self.screen = pygame.display.set_mode((self.width, self.height))
		
		print(self.width)
		print(self.height)

		self.specFrame = None
		self.frames = self.initFrames(); # might want to be in func init?

		self.viewModels = list()
		self.viewModels.append(dvm.DataView(self.frames[0])) # dumb hack
		self.viewModels.append(KNNView.KNNView(self.frames[1]))
		self.viewModels.append(ddvm.DigitDrawerVM(self.frames[2], self.viewModels[0].model))
		self.viewModels.append(TTVM.TestTrainView(self.getCurAlgo, self.viewModels[2].model, self.viewModels[0].model))
		self.viewModels.append(Controler(self.viewModels, (self.viewModels[1], NND.NNDrawer(self.frames[1]))))

	def getCurAlgo(self):
		return self.viewModels[1].model


	
	def initFrames(self):
		frames = list()		
		frame = jp.Frame((0, 0), 150, self.height // 2)
		frame.margin = 10
		frames.append(frame)

		frame = jp.Frame((150, 0), (self.width - 500 - 150), self.height)
		frame.margin = 10
		frames.append(frame)

		frame = jp.Frame((self.width - 500, 0), 500, self.height // 2)
		frame.margin = 10
		frames.append(frame)

		frame = jp.Frame((self.width - 500, self.height // 2), 500, self.height // 2)
		frame.margin = 10
		frames.append(frame)

		frame = jp.Frame((0, self.height // 2), 150, self.height // 2)
		frame.margin = 10
		frames.append(frame)
		return frames

	def global2Frame(self,x,y):  # dif scope/not in the class?
		for i,frame in enumerate(self.frames):
			if frame.containsCoord(x,y):
				return (i, frame.transform(x,y));


		print("oops, no frame held your coord\n")
		return (-1,(-1,-1))

		

	def init(self):
		pass

	def step(self):
		pass

	def handleEvents(self): #design decision: each thing can only be interacted with via buttons (mouse clicks) key presses are only for the global control
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				for viewModel in self.viewModels:
					viewModel.quit() #yeah, the data model will save it's data, the knn saves nothing, ann saves it's nn (maybe)
				pygame.quit()
				sys.exit()

			elif (event.type == pygame.MOUSEBUTTONDOWN or
				  event.type == pygame.MOUSEBUTTONUP or
				  event.type == pygame.MOUSEMOTION):
				(i, (x,y)) = self.global2Frame(*pygame.mouse.get_pos())
				if i >= 0:
					self.viewModels[i].mouseEvent(x, y, event.type)
				
			elif event.type == pygame.KEYDOWN:
				pass

	def redraw(self):
		self.screen.fill(Colors.RED)
		for frame in self.frames:
			#print(frame)
			pygame.draw.rect(frame.screen, Colors.DEEPSKYBLUE, (0,0,frame.width,frame.height), 0)

		for i in range(len(self.viewModels)):
			viewModel = self.viewModels[i]
			frame = self.frames[i]   #INTERSESTING, the frame you pass to the viewmodel does not have to be this same frame.
			for drawable in viewModel.getDrawables():
				drawable.draw(frame)


		for frame in self.frames:
			self.screen.blit(frame.screen, (frame.x, frame.y))

	
		pygame.display.update()

	


	def run(self):
		self.init()
		while True:
			self.handleEvents();
			self.step();
			self.redraw();
		return False

game = MachineLearningGameLoop()
game.run()
