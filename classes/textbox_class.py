import pygame

class TEXT:

	def __init__(self, text, x=None, y=None, width=None, height=None, boldText=False):
		self.x = x
		self.y = y
		self.maxW = width
		self.maxH = height
		self.w = None
		self.h = None
		self.textColour = None
		self.backColour = None
		self.boldText = boldText
		self.originalText = text
		self.renderedText = None
		self.textRect = None

		if self.boldText:
			self.font = pygame.font.Font('fonts//UbuntuMono-Bold.ttf', 18)
		else:
			self.font = pygame.font.Font('fonts//NotoSansMono.ttf', 14)


	def initialise(self, x, y, w, h, textColour, backColour):
		self.x = x
		self.y = y
		self.maxW = w
		self.maxH = h
		self.textColour = textColour
		self.backColour = backColour

	def get_size(self):
		return (self.w, self.h)


	def get_pos(self):
		return (self.x, self.y)


	def get_text(self):
		return self.originalText


	def set_text(self, text):
		self.originalText = text
		self.render_text(text)


	def check_width(self, text):
		(self.w, self.h) = self.font.size(text)
		if self.w > self.maxW:
			while self.w > self.maxW:
				text = text[:-1]
				(self.w, self.h) = self.font.size(text+"...")
				if text == "":
					break
			text = text+"..."

		return text


	def render(self, text=None, x=None, maxW=None):
		if x: self.x = x
		if maxW: self.maxW = maxW
		if not text: text = self.originalText
		text = self.check_width(text)
		self.renderedText = self.font.render(text, True, self.textColour, self.backColour)
		self.textRect = self.renderedText.get_rect()
		self.textRect.topleft = (self.x, self.y)


	def draw(self, window, y):
		self.y = y
		self.textRect = (self.x, self.y)
		if self.renderedText != None:
			pygame.draw.rect(window, self.backColour, (self.x, self.y, self.maxW, self.maxH))
			window.blit(self.renderedText, self.textRect)