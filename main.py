import pygame, os
import classes.textbox_class as textc
import classes.client_class as clientc
import classes.info_display_class as displayc
import classes.static_variables as sv


# ~~~~ Variables ~~~~


# Pygame
clock = pygame.time.Clock()
fps = 60

# Misc
leftMouseClick = False


# ~~~~ SETUP ~~~~

pygame.init()
(width, height) = (pygame.display.Info().current_w, pygame.display.Info().current_h)
window = pygame.display.set_mode((width, height), pygame.NOFRAME)
os.environ["SDL_VIDEO_CENTERED"] = "1"

loading = pygame.image.load("images//loading.png")
csmIcon = pygame.image.load("images//icon.png")

pygame.display.set_caption("CSM")
pygame.display.set_icon(csmIcon)

loadingRect = loading.get_rect()
loadingRect.center = (width//2, height//2)
window.fill(sv.beige)
window.blit(loading, loadingRect)
pygame.display.update()


# ~~~~ LOAD CLIENTS ~~~~


clientFile = open("test_files//randomized_client_data_quoted.csv")
clients = []
line = clientFile.readline()
while line:
	splitting = True
	line = line.strip("\n")
	tempLine = ""
	clientInfo = []
	for char in line:
		if char == "," and splitting:
			clientInfo.append(tempLine)
			tempLine = ""
		else:
			if char == "\"":
				splitting = False if splitting else True
			else:
				tempLine += char
	if tempLine != "":
		clientInfo.append(tempLine)

	clients.append(clientc.CLIENT(clientInfo[0], clientInfo[1], clientInfo[2], clientInfo[3], clientInfo[4]))
	line = clientFile.readline()
clientFile.close()


# ~~~ INFO DISPLAY ~~~~

clientDisplayRect = pygame.Rect(20, 50, width-60, height-70)
clientDisplay = displayc.DISPLAY(clientDisplayRect.x, clientDisplayRect.y, clientDisplayRect.width, clientDisplayRect.height, window)
clientDisplay.set_children(clients)

clientDisplayFrameSize = 2
clientDisplayFrameRect = pygame.Rect(clientDisplayRect.x-clientDisplayFrameSize, clientDisplayRect.y-clientDisplayFrameSize, clientDisplayRect.width+clientDisplayFrameSize+clientDisplay.get_scrollbar_size()[0], clientDisplayRect.height+clientDisplayFrameSize)

# ~~~~ Main Loop ~~~~
run = True
while run:


	# ~~~ EVENTS ~~~


	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				clientDisplay.check_click(pygame.mouse.get_pos())

		elif event.type == pygame.MOUSEWHEEL:
			clientDisplay.mouse_scroll(event.y)

		mousePos = pygame.mouse.get_pos()
		if clientDisplay.check_hover(mousePos):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


	# ~~~ DISPLAY ~~~


	window.fill(sv.white)


	clientDisplay.draw(window)
	
	# Draw Frame
	pygame.draw.rect(window, sv.beige, (0, 0, width, 50))
	pygame.draw.rect(window, sv.beige, (0, 0, 20, height))
	pygame.draw.rect(window, sv.beige, (0, height-20, width, 20))
	pygame.draw.rect(window, sv.beige, (width-20, 0, 20, height))

	pygame.draw.line(window, sv.darkBeige, clientDisplayFrameRect.topleft, clientDisplayFrameRect.topright, 2)
	pygame.draw.line(window, sv.darkBeige, clientDisplayFrameRect.topright, clientDisplayFrameRect.bottomright, 2)
	pygame.draw.line(window, sv.darkBeige, clientDisplayFrameRect.bottomleft, clientDisplayFrameRect.bottomright, 2)
	pygame.draw.line(window, sv.darkBeige, clientDisplayFrameRect.topleft, clientDisplayFrameRect.bottomleft, 2)

	pygame.display.update()
	clock.tick(fps)

pygame.quit()
quit()