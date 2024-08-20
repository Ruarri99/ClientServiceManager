import pygame, math
import classes.static_variables as sv

class SCROLLBAR:

	def __init__(self, x, y, width, height, padding):
		self.x = x+padding//2
		self.y = y+padding//2
		self.width = width-padding
		self.height = height-padding
		self.enabled = False
		self.moving = False
		self.lastMousePos = None
		self.barY = self.y
		self.barLength = 100
		self.barPosition = 0
		self.barRect = None
		self.set_bar_rect(self.x, round(self.y+self.height*self.barPosition-self.barLength*self.barPosition), self.width, round(self.barLength))


	def set_enabled(self, status):
		self.enabled = status


	def get_enabled(self):
		return self.enabled


	def set_length(self, length):
		self.barLength = length


	def get_pos(self):
		return self.barPosition


	def change_pos(self, change):
		self.barPosition -= 0.1*change
		if self.barPosition > 1: self.barPosition = 1 
		if self.barPosition < 0: self.barPosition = 0 


	def set_bar_rect(self, x, y, width, height):
		self.barRect = pygame.Rect(x, y, width, height)


	def check_click(self, mousePos):
		if self.barRect.collidepoint(mousePos):
			self.moving = True
			self.lastMousePos = mousePos


	def draw(self, window):
		if self.enabled:
			if self.moving and pygame.mouse.get_pressed()[0]:
				mousePos = pygame.mouse.get_pos()
				if mousePos[1] < self.lastMousePos[1]:
					self.barY -= self.lastMousePos[1]-mousePos[1]
					if self.barY < self.y:
						self.barY = self.y
				elif mousePos[1] > self.lastMousePos[1]:
					self.barY += mousePos[1]-self.lastMousePos[1]
					if self.barY > self.y+self.height-self.barLength:
						self.barY = self.y+self.height-self.barLength

				self.lastMousePos = mousePos
				self.barPosition = (self.barY-self.y)/(self.height-self.barLength)
			else:
				self.moving = False


			# Update "bar" using new coordinates
			self.set_bar_rect(self.x, round(self.y+self.height*self.barPosition-self.barLength*self.barPosition), self.width, math.ceil(self.barLength))

			# Draw the middle of the "track"
			pygame.draw.line(window, sv.black, (self.x+self.width//2, self.y), (self.x+self.width//2, self.y+self.height))

			# Draw the "bar"
			pygame.draw.rect(window, sv.lightGrey, self.barRect)

			# Draw the ends of the "track"
			pygame.draw.line(window, sv.black, (self.x, self.y), (self.x+self.width-1, self.y))
			pygame.draw.line(window, sv.black, (self.x, self.y+self.height), (self.x+self.width-1, self.y+self.height))