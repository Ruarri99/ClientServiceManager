import pygame
import classes.textbox_class as textbox
import classes.scrollbar_class as scrollc
import classes.static_variables as sv

class DISPLAY:

	def __init__(self, x, y, width, height, window):
		self.x = x
		self.y = y
		self.displayWidth = width
		self.displayHeight = height
		self.children = []
		self.lastMousePos = None
		self.window = window

		# Row Specs
		self.rowHeight = 20
		self.rowsY = self.y
		self.excessHeight = None

		# Adjuster Specs
		self.adjusterWidth = 10
		self.adjusterHeight = self.rowHeight
		self.adjusterMinimumSpacing = 28
		self.adjusting = False
		self.adjustedColumn = None

		# Column Specs
		self.columnPadding = 2
		self.columnsPercent = [0, 0.03, 0.15, 0.3, 0.5]
		self.columnsPixel = None
		self.columnsWidth = None
		self.columnsAdjusters = None
		self.calculate_columns()

		# Scrollbar
		self.scrollbarPadding = 2
		self.scrollbarRect = pygame.Rect(self.x+self.displayWidth, self.y, 20, self.displayHeight)
		self.scrollbar = scrollc.SCROLLBAR(self.scrollbarRect.x, self.scrollbarRect.y, self.scrollbarRect.width, self.scrollbarRect.height, self.scrollbarPadding)


	def calculate_columns(self):
		self.columnsPixel = []
		self.columnsWidth = []
		self.columnsAdjusters = []

		# Column Positions
		for column in self.columnsPercent:
			self.columnsPixel.append(self.x + self.displayWidth*column)

		# Column Widths
		for i in range(len(self.columnsPixel)):
			try:
				self.columnsWidth.append(self.columnsPixel[i+1]-self.columnsPixel[i]-self.columnPadding)
			except IndexError:
				self.columnsWidth.append(self.x+self.displayWidth-self.columnsPixel[i]-self.columnPadding)

		# Columns Adjusters
		for column in self.columnsPercent:
			self.columnsAdjusters.append(pygame.Rect(self.x-self.columnPadding//2-self.adjusterWidth//2+self.displayWidth*column, self.y, self.adjusterWidth, self.adjusterHeight))

		del self.columnsAdjusters[0]


	def set_children(self, children):
		self.clear_children()
		for child in children:
			self.children.append(child)

		

		self.excessHeight = len(self.children)*self.rowHeight-self.displayHeight
		if self.excessHeight > 0:
			self.scrollbar.set_enabled(True)
			self.scrollbar.set_length(self.displayHeight-self.displayHeight*(self.excessHeight/(self.displayHeight+self.excessHeight)))


		self.set_children_height()
		self.initialise_children_text()
		self.render_children_text()


	def clear_children(self):
		self.children = []


	def get_scrollbar_size(self):
		return (self.scrollbarRect.size)


	def set_children_height(self):
		for i in range(len(self.children)):
			self.children[i].set_height(i)


	def initialise_children_text(self):
		self.children[0].initialise_text(self.columnsPixel, self.y, self.columnsWidth, self.rowHeight, sv.black, sv.grey)
		for i in range(1, len(self.children)):
			if i % 2 == 1:
				textColour = sv.black
				backColour = sv.lighterGrey
			else:
				textColour = sv.black
				backColour = sv.lightGrey
			self.children[i].initialise_text(self.columnsPixel, self.rowsY-self.scrollbar.get_pos()*self.excessHeight, self.columnsWidth, self.rowHeight, textColour, backColour)


	def render_children_text(self):
		windowInfo = pygame.display.Info()
		for i in range(len(self.children)):
			self.children[i].render_texts()
			pygame.draw.rect(self.window, sv.darkBeige, (windowInfo.current_w//4, round(windowInfo.current_h*(4/5)), round(windowInfo.current_w//2), 26))
			pygame.draw.rect(self.window, sv.orange, (windowInfo.current_w//4+3, round(windowInfo.current_h*(4/5))+3, round(i/len(self.children)*(windowInfo.current_w//2)), 20))
			pygame.display.update()
			

	def check_click(self, mousePos):
		if mousePos[0] > self.x+self.displayWidth:
			self.scrollbar.check_click(mousePos)
		else:
			self.lastMousePos = mousePos
			for column in self.columnsAdjusters:
				if column.collidepoint(mousePos):
					self.move_adjuster(column)


	def check_hover(self, mousePos):
		hovering = False
		for column in self.columnsAdjusters:
			if column.collidepoint(mousePos):
				hovering = True
		return hovering


	def move_adjuster(self, column):
		self.adjusting = True
		self.adjustedColumn = column


	def mouse_scroll(self, scroll):
		self.scrollbar.change_pos(scroll)


	def draw(self, window):
		# Display Background
		pygame.draw.rect(window, sv.white, (self.x, self.y, self.displayWidth, self.displayHeight))

		# Clients
		for i in range(1, len(self.children)):
			self.children[i].draw(window, self.rowsY+self.children[i].get_height()*self.rowHeight-self.scrollbar.get_pos()*self.excessHeight)

		self.children[0].draw(window, self.y)

		# Scrollbar
		self.scrollbar.draw(window)

		# Adjuster Boxes
		if self.adjusting and pygame.mouse.get_pressed()[0]:
			pygame.draw.line(window, sv.black, (self.adjustedColumn[0]+self.adjustedColumn[2]//2-1, self.adjustedColumn[1]), (self.adjustedColumn[0]+self.adjustedColumn[2]//2-1, self.adjustedColumn[1]+self.displayHeight), 2)
			mousePos = pygame.mouse.get_pos()

			newAdjustedPercent = round((mousePos[0]-self.x)/self.displayWidth, 3)

			if self.columnsAdjusters.index(self.adjustedColumn) != 0:
				if newAdjustedPercent-self.columnsPercent[self.columnsAdjusters.index(self.adjustedColumn)] < round(self.adjusterMinimumSpacing/self.displayWidth, 2): newAdjustedPercent = round(self.columnsPercent[self.columnsAdjusters.index(self.adjustedColumn)]+self.adjusterMinimumSpacing/self.displayWidth, 2)
			else:
				if newAdjustedPercent < round(self.adjusterMinimumSpacing/self.displayWidth, 2): newAdjustedPercent = round(self.adjusterMinimumSpacing/self.displayWidth, 2)
			
			if self.columnsAdjusters.index(self.adjustedColumn) != len(self.columnsAdjusters)-1:
				if self.columnsPercent[self.columnsAdjusters.index(self.adjustedColumn)+2]-newAdjustedPercent < round(self.adjusterMinimumSpacing/self.displayWidth, 2): newAdjustedPercent = round(self.columnsPercent[self.columnsAdjusters.index(self.adjustedColumn)+2]-self.adjusterMinimumSpacing/self.displayWidth, 2)
			else:
				if newAdjustedPercent > 1-round(self.adjusterMinimumSpacing/self.displayWidth, 2): newAdjustedPercent = 1-round(self.adjusterMinimumSpacing/self.displayWidth, 2)

			self.columnsPercent[self.columnsAdjusters.index(self.adjustedColumn)+1] = newAdjustedPercent
			self.calculate_columns()
			self.adjustedColumn = self.columnsAdjusters[self.columnsPercent.index(newAdjustedPercent)-1]
			for client in self.children:
				client.render_specific_text(self.columnsPercent.index(newAdjustedPercent), self.columnsPixel, self.columnsWidth)
				client.render_specific_text(self.columnsPercent.index(newAdjustedPercent)-1, self.columnsPixel, self.columnsWidth)
			self.lastMousePos = mousePos
		else:
			self.adjusting = False
			self.adjustedColumn = None
			for column in self.columnsAdjusters:
				pygame.draw.line(window, sv.white, (column[0]+column[2]//2-1, column[1]), (column[0]+column[2]//2-1, column[1]+self.displayHeight), 2)