import classes.textbox_class as textbox

class CLIENT:

	def __init__(self, clientNumber, name, phone, email, address):
		self.clientNumber = clientNumber
		self.name = name
		self.phone = phone
		self.email = email
		self.address = address
		
		self.height = None

		# Textboxes
		self.clientNumberText = textbox.TEXT(self.clientNumber)
		self.nameText = textbox.TEXT(self.name)
		self.phoneText = textbox.TEXT(self.phone)
		self.emailText = textbox.TEXT(self.email)
		self.addressText = textbox.TEXT(self.address)
		self.texts = [self.clientNumberText, self.nameText, self.phoneText, self.emailText, self.addressText]

	def search_text(self, text):
		results = [t.get_text() for t in self.texts]
		for result in results:
			if text in result:
				return True
		return False

	def get_name(self):
		return self.name

	def get_address(self):
		return self.address

	def get_phone(self):
		return self.phone

	def set_height(self, height):
		self.height = height
		if self.height == 0:
			self.boldText = True

	def get_height(self):
		return self.height

	def initialise_text(self, columnsX, rowsY, columnsW, rowHeight, textColour, backColour):
		self.clientNumberText.initialise(columnsX[0], rowsY+self.height*rowHeight, columnsW[0], rowHeight, textColour, backColour)
		self.nameText.initialise(columnsX[1], rowsY+self.height*rowHeight, columnsW[1], rowHeight, textColour, backColour)
		self.phoneText.initialise(columnsX[2], rowsY+self.height*rowHeight, columnsW[2], rowHeight, textColour, backColour)
		self.emailText.initialise(columnsX[3], rowsY+self.height*rowHeight, columnsW[3], rowHeight, textColour, backColour)
		self.addressText.initialise(columnsX[4], rowsY+self.height*rowHeight, columnsW[4], rowHeight, textColour, backColour)

	def render_specific_text(self, index, x=None, columnsW=None):
		self.texts[index].render(x=x[index], maxW=columnsW[index])

	def render_texts(self):
		for text in self.texts:
			text.render()

	def draw(self, window, y):
		for text in self.texts:
			text.draw(window, y)