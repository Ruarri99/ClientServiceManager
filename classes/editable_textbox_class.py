import pygame
import classes.static_variables as sv

class TEXT:

	def __init__(self, x, y, w, h, padding, text=""):
		self.boxX = x
		self.boxY = y
		self.boxW = w
		self.boxH = h
		self.borderThickness = 2
		self.boxRect = pygame.Rect(self.boxX, self.boxY, self.boxW, self.boxH)
		self.borderRect = pygame.Rect(self.boxX-self.borderThickness, self.boxY-self.borderThickness, self.boxW+self.borderThickness*2, self.boxH+self.borderThickness*2)

		self.padding = padding
		self.textX = self.boxX + self.padding
		self.textY = self.boxY
		self.textW = None
		self.textH = None

		self.originalText = None
		self.alteredText = None
		self.renderedText = None
		self.displacement = 0
		self.textColour = sv.black
		self.backColour = sv.grey
		self.font = pygame.font.Font('fonts//NotoSansMono.ttf', 14)
		self.set_text(text)

		self.enteringText = False
		self.cursor_show = False
		self.cursor_position = 0
		self.BLINK_TEXTBOX_CURSOR = pygame.USEREVENT


	def get_entering_text(self):
		return self.enteringText


	def get_text(self):
		return self.originalText


	def get_user_event(self):
		return self.BLINK_TEXTBOX_CURSOR


	def get_text_width(self, start=0, length=None):
		if not length:
			length = self.cursor_position
		return self.font.size(self.alteredText[start:start+length])


	def get_click_pos(self, x):
		textList = list(self.alteredText)
		for i in range(len(textList)):
			# print(i, self.textX + self.get_text_width(length=textList.index(i)+1)[0] - self.font.size(i)[0]//2)
			if self.textX + self.get_text_width(length=i+1)[0] - self.font.size(textList[i])[0]//2 > x:
				# print(i, self.get_text_width(length=textList.index(i)+1)[0], self.font.size(i)[0]//2, textList.index(i), x)
				return i

		return len(self.alteredText)


	def check_click(self, mousePos):
		if self.boxRect.collidepoint(mousePos):
			if self.enteringText:
				self.cursor_position = self.get_click_pos(mousePos[0])
				self.blink_cursor(True)
			else:
				self.enteringText = True
				self.blink_cursor(True)
		else:
			self.enteringText = False


	def blink_cursor(self, blink=None):
		if self.enteringText:
			self.cursor_show = blink if blink else not self.cursor_show
			pygame.time.set_timer(self.BLINK_TEXTBOX_CURSOR, 500, 1)
		else:
			self.cursor_show = False


	def check_input(self, key, pyKey):
		if key == "\u001B" or key == "\r":
			self.enteringText = False

		elif key == "\b":
			if self.cursor_position == 0 and self.displacement > 0:
				self.set_text(self.originalText[:self.displacement-1]+self.alteredText)
			else:
				if self.displacement > 0:
					self.set_text(self.originalText[:self.displacement]+self.alteredText[:self.cursor_position-1]+self.alteredText[self.cursor_position:])
				else:
					self.set_text(self.originalText[:self.displacement]+self.alteredText[:self.cursor_position-1]+self.alteredText[self.cursor_position:])
					self.cursor_position = self.cursor_position-1 if self.cursor_position > 0 else 0


		elif pyKey == pygame.K_DELETE:
			self.set_text(self.originalText[:self.displacement]+self.alteredText[:self.cursor_position]+self.alteredText[self.cursor_position+1:])
			if self.displacement > 0:
				self.cursor_position = self.cursor_position+1 if self.cursor_position < len(self.alteredText) else len(self.alteredText)
		else:
			if not type(key) == pygame.event.Event and key != "":
				self.set_text(self.originalText[:self.displacement]+self.alteredText[:self.cursor_position]+key+self.alteredText[self.cursor_position:])
				if self.displacement == 0:
					self.cursor_position = self.cursor_position+1 if self.cursor_position < len(self.alteredText) else len(self.alteredText)

			elif pyKey == pygame.K_LEFT:
				self.cursor_position = self.cursor_position-1 if self.cursor_position > 0 else 0
				self.blink_cursor(True)

			elif pyKey == pygame.K_RIGHT:
				self.cursor_position = self.cursor_position+1 if self.cursor_position < len(self.alteredText) else len(self.alteredText)
				self.blink_cursor(True)


	def set_text(self, text, x=None):
		if x: self.textX = x
		self.originalText = text
		self.render()


	def check_width(self):
		self.displacement = 0
		self.alteredText = self.originalText
		while self.font.size(self.alteredText)[0] > self.boxRect.width-self.padding*2:
			self.displacement += 1
			self.alteredText = self.originalText[self.displacement:]


	def render(self):
		self.check_width()
		self.renderedText = self.font.render(self.alteredText, True, self.textColour, self.backColour)
		self.textRect = self.renderedText.get_rect()
		self.textRect.midleft = (self.textX, self.textY+self.boxH//2)


	def draw(self, window):
		pygame.draw.rect(window, sv.darkBeige, self.borderRect)
		pygame.draw.rect(window, sv.grey, self.boxRect)
		if self.renderedText:
			window.blit(self.renderedText, self.textRect)

		if self.cursor_show:
			pygame.draw.line(window, sv.black, (self.textX+self.get_text_width(length=self.cursor_position)[0], self.boxY+self.boxH//4), (self.textX+self.get_text_width(length=self.cursor_position)[0], self.boxY+self.boxH//4*3))