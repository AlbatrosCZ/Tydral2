import pygame, string, os, sys
import time as t

pygame.init()
pygame.mixer.init()

def error(text = False):
    if not text:
        text = "unknow error"
    raise TypeError("ERROR: " + str(text))

class Window:
    """This is class of window. Via this class you can draw buttons, images, lines ... \n*fullscreen - True / False\n*width - integer up to your screen size\n*height - integer up to your screen size\n*start_bg - window color on start (red, green, blue)\n\nImportant: fullscreen, width, height"""
    def __init__(self, fullscreen: bool, width: int, height: int, start_bg = (255, 255, 255)):
    
        self.fullscreen = fullscreen
        

        self.clocks = pygame.time.Clock()

        if fullscreen:
            self.screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode([width, height])
        self.actions = actions_listener()

        self.width, self.height = self.screen.get_size()

        self.screen.fill(start_bg)
        self.abc = [" "]
        for i in list(string.printable):
            if i not in list(string.whitespace):
                self.abc.append(i)

        self.fps = 120

        self.images = {}
        self.fonts = {}
        self.entrys = {}
        self.radiobuttones = {}
        self.text_pozitions = {}
        self.switch = {}

        self.loop()

    def __generate_pozition_from_text(self, text, size):
        if "{},{}".format(text, size) in self.text_pozitions:
            return self.text_pozitions["{},{}".format(text, size)]
        for i in range(len(text)):
            if text[i] == "r":
                text = text[0:i] + str(self.width - size[0]) + text[i+1:]
            if text[i] == "c":
                text = text[0:i] + str((self.width - size[0]) // 2) + text[i+1:]
            if text[i] == "d": 
                text = text[0:i] + str(self.height - size[1]) + text[i+1:]
            if text[i] == "m":
                text = text[0:i] + str((self.height - size[1]) // 2) + text[i+1:]
        a = 0
        b = 0
        j = "+"
        do = text + "+"
        for i in do:
            if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                a *= 10
                a += int(i)
            else:
                if j == "+":
                    b += a
                    a = 0
                elif j == "-":
                    b -= a
                    a = 0
                elif j == "/":
                    b = b//a
                    a = 0
                elif j == "*":
                    b *= a
                    a = 0
                j = i
        self.text_pozitions["{},{}".format(text, size)] = b
        return b

    def draw_img(self, path: str, geometry: list, rotate = 0, alpha = 255):
        """*path = string(c:/.../name.imgtype or ./.../name.imgtype)\n*geometry = [x, y, width, height]\n*rotate = integer up to 360\n*alpha = integer up to 255"""
        if path not in self.images.keys():
            self.images[path] = pygame.image.load(path)
        image = self.images[path]
        image = pygame.transform.scale(image, (geometry[2], geometry[3]))
        if 360 > rotate%360 > 0:
            image = pygame.transform.rotate(image, rotate)
        if alpha < 255:
            image = image.convert()
            image.set_alpha(alpha)
        if type(geometry[0]) == str:
            geometry[0] = self.__generate_pozition_from_text(geometry[0], [geometry[2], geometry[3]]) 
        if type(geometry[1]) == str:
            geometry[1] = self.__generate_pozition_from_text(geometry[1], [geometry[2], geometry[3]]) 
        self.screen.blit(image, geometry) 
    def draw_text(self, pozition: list, text = "", size = 50, font = "PalatinoLinoType", color = (255, 255, 255), blit = True):
        """*pozition = (x, y)\n*text = string\n*size = integer\n*font = font name\n*color = (red, green, blue)\n*blit = True/False\n\nReturns: width, height"""
        if "{},{}".format(font, size) not in self.fonts.keys():
            self.fonts["{},{}".format(font, size)] = pygame.font.SysFont(font, size)
        font = self.fonts["{},{}".format(font, size)]
        text = font.render(text, True, color)
        text_width = text.get_width()
        text_height = text.get_height()
        if type(pozition[0]) == str:
            pozition[0] = self.__generate_pozition_from_text(pozition[0], [text_width, text_height])
        if type(pozition[1]) == str:
            pozition[1] = self.__generate_pozition_from_text(pozition[1], [text_width, text_height])
        if blit:
            self.screen.blit(text, (pozition[0], pozition[1]))
        return text_width, text_height
    def draw_shape(self, typ, geometry, color):
        """*typ = rect/poly/elip/line/point\n*geometry = rect[x, y, width, height] /\n            polygon[x1, y1, x2 y2 ...] /\n            elip[x, y, šířka, výška] /\n            line[[x1, y1], [y1, y2]] /\n            point[x, y]\n*color = (red, green, blue)"""
        if typ == "rect":
            pygame.draw.rect(self.screen, color, geometry)
        elif typ == "poly":
            pygame.draw.polygon(self.screen, color, geometry)
        elif typ == "elip":
            pygame.draw.ellipse(self.screen, color, geometry)
        elif typ == "line":
            pygame.draw.line(self.screen, color, geometry[0], geometry[1])
        elif typ == "point":
            pygame.draw.line(self.screen, color, geometry, geometry)
    def draw_image_button(self, geometry, path, path_click = "", buttons = [1, 2], alpha = 255):
        """*geometry = [x, y, width, height]\n*path = path to image\n*path_click = path to image that show when someone click on button\n*buttons = list of mouse button to activate\n*alpha = 0-255 (0 = 100% traspatent, 255 = non-transparent)\n\nReturns: mouse on button (True/False), button pressed (True/False)"""
        mouse = pygame.mouse.get_pos()

        if type(geometry[0]) == str:
            geometry[0] = self.__generate_pozition_from_text(geometry[0], [geometry[2], geometry[3]])
        if type(geometry[1]) == str:
            geometry[1] = self.__generate_pozition_from_text(geometry[1], [geometry[2], geometry[3]])

        clicked = False
        for i in self.actions.mouse_down:
            if i[0] in buttons:
                clicked = True
                break

        if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3] and clicked and path_click != "":
            self.draw_img(path_click, geometry, alpha = alpha)      
        else:
            self.draw_img(path, geometry, alpha = alpha)

        equal = False
        on = False
        if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3]:
            on = True
            for i in self.actions.mouse_up:
                if i in buttons:
                    equal = True
                    break
        return on, equal
    def draw_button(self, geometry, button_color = (255,255,255), text_color = (0,0,0), buttons = [1, 3], text = "", font = "PalatinoLinoType", size = 25):
        """*geometry = [x1, x2, minimal width, minimal height]\n*button_color = (red, green, blue)\n*text_color = (red, green, blue)\n*buttons = list of mouse button to activate\n*text = string\n*font = font name\n*size = integer\n\nReturns: mouse on button (True/False), button pressed (True/False)"""
        mouse = pygame.mouse.get_pos()

        width, height = self.draw_text([geometry[0], geometry[1]], text, size, font, text_color, False)

        if width + 4 > geometry[2]:
            geometry[2] = width + 4
        if height + 4 > geometry[3]:
            geometry[3] = height + 4
        
        if type(geometry[0]) == str:
            geometry[0] = self.__generate_pozition_from_text(geometry[0], [geometry[2], geometry[3]])
        if type(geometry[1]) == str:
            geometry[1] = self.__generate_pozition_from_text(geometry[1], [geometry[2], geometry[3]])

        clicked = False
        for i in self.actions.mouse_down:
            if i[0] in buttons:
                clicked = True
                break
        
        if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3] and clicked:        
            self.draw_shape("rect", geometry, button_color)
            self.draw_shape("rect", [geometry[0] + 1, geometry[1] + 1, geometry[2] - 2, geometry[3] - 2], text_color)
            self.draw_text((geometry[0] + 2, geometry[1]+2), text, size, font, button_color)
        else:
            self.draw_shape("rect", geometry, text_color)
            self.draw_shape("rect", [geometry[0] + 1, geometry[1] + 1, geometry[2] - 2, geometry[3] - 2], button_color)
            self.draw_text((geometry[0] + 2, geometry[1]+2), text, size, font, text_color)

        equal = False
        on = False
        if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3]:
            on = True
            for i in self.actions.mouse_up:
                if i in buttons:
                    equal = True
                    break
        return on, equal
    def draw_entry(self, geometry, entryId, button_color = (255,255,255), text_color = (0,0,0), font = "PalatinoLinoType", size = 25, text_type = "text", text_null = "", text_null_color = (150,150,150)):
        """*geometry = [x, y, width, min height]\n*entryId = string\n*button_color = (red, green, blue)\n*text_color = (red, green, blue)\n*font = font name\n*size = integer\n*text_type = %/number/password\n*text_null = text that sow if nothing write in\n*text_null_color = (red, green, blue)\n\nReturns: text in entry"""
        if entryId not in self.entrys.keys():
            self.entrys[entryId] = {"text": "", "using": False, "pozition": {"cursor": 0, "first_letter": 0}, "timer": 0}

        using = self.entrys[entryId]["using"]
        text  = self.entrys[entryId]["text"]
        cursor_poz   = self.entrys[entryId]["pozition"]["cursor"]
        first_letter = self.entrys[entryId]["pozition"]["first_letter"]
        if using:
            self.entrys[entryId]["timer"] += 1
            if self.entrys[entryId]["timer"] > self.fps:
                self.entrys[entryId]["timer"] = 0
            timer = self.entrys[entryId]["timer"]
        else:
            self.entrys[entryId]["timer"] = 0
            timer = self.fps
        text1 = text[:cursor_poz]
        text2 = text[cursor_poz:]
        if self.actions.key_down and using:
            for i in self.actions.key_down:
                time = (t.time() - i[1])*100
                if time > 150 and time%10 == 0 or time < 0.1:
                    if i[0] == 8:
                        text1 = text1[:-1]
                        if cursor_poz > 0:
                            cursor_poz -= 1
                        if cursor_poz < first_letter + 1 and first_letter != 0:
                            first_letter = cursor_poz - 1
                    elif i[0] == 127:
                        text2 = text2[1:]
                    elif i[2] != "" and text_type != "number":
                        if i[2] in ["\r", "\n", "\x1b"] :
                            pass
                        elif i[2] == "\t":
                            text1 += "    "
                            cursor_poz += 4
                        else:
                            text1 += i[2]
                            cursor_poz += 1
                    elif i[2] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] and text_type == "number":
                        text1 += i[2]
                        cursor_poz += 1
                    if i[0] == 276:
                        if cursor_poz > 0:
                            cursor_poz -= 1
                        if cursor_poz < first_letter + 1 and first_letter != 0:
                            first_letter = cursor_poz - 1
                    if i[0] == 275:
                        if len(text) > cursor_poz:
                            cursor_poz += 1
        text = text1 + text2
        self.entrys[entryId]["pozition"]["cursor"] = cursor_poz
        width, height = self.draw_text((geometry[0], geometry[1]), text, size, font, text_color, False)
        
        if height + 4 > geometry[3]:
            geometry[3] = height + 4
        
        if type(geometry[0]) == str:
            geometry[0] = self.__generate_pozition_from_text(geometry[0], [geometry[2], geometry[3]])
        if type(geometry[1]) == str:
            geometry[1] = self.__generate_pozition_from_text(geometry[1], [geometry[2], geometry[3]])

        mouse = pygame.mouse.get_pos()
        if 1 in self.actions.mouse_up:
            if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3]:
                using = True
            else:
                using = False
        self.entrys[entryId]["using"] = using

        self.entrys[entryId]["text"] = text

        if using:
            text = text[:cursor_poz] + " " + text[cursor_poz:]

        

        right = len(text)
        left  = first_letter
        center = 0
        while width + 4 > geometry[2]:
            width = self.draw_text((geometry[0], geometry[1]), text[left:right], size, font, text_color, False)[0]
            if not width + 4 > geometry[2]:
                break
            if right > cursor_poz + 1:
                right -=1
            else:
                left += 1
            
        cursor_x, cursor_y = self.draw_text((geometry[0], geometry[1]), text[left:cursor_poz], size, font, text_color, False)

        cursor_x += 3

        self.draw_shape("rect", geometry, button_color)
        if text:
            self.draw_text((geometry[0]+2, geometry[1]+2), text[left:right], size, font, text_color)
            if timer <= self.fps/2:
                self.draw_shape("line", [[cursor_x + geometry[0], geometry[1] + 5], [cursor_x + geometry[0], geometry[1] + cursor_y - 5]], text_color)
        else:
            self.draw_text((geometry[0]+2, geometry[1]+2), text_null, size, font, text_null_color)

        self.entrys[entryId]["pozition"]["first_letter"] = left
        return self.entrys[entryId]["text"]
        
    def draw_radiobutton(self, typ, geometry, radiobuttonID, buttons, horizontal = False, **args):
        """*typ = shape/image\n*geometry = [x, y, width/height]\n*radiobuttonID = String\n*buttons = ["text_on1"...]\n*horizontal = True/False\n*path = string(c:/.../name.imgtype or ./.../name.imgtype)\n*set_if_not = Integer(id button)\n*color = shape[outline+text(red, green, blue), field_in(red, green, blue)]\n         image(red, green, blue)\n*font = font name\n*size = integer\n\nImportant: typ, geometry, radiobuttonID, buttons, path(only if typ is image), color\n\nReturns: id button"""
        if radiobuttonID not in self.radiobuttones.keys():
            try:
                self.radiobuttones[radiobuttonID] = args["set_if_not"]
            except:
                self.radiobuttones[radiobuttonID] = None
        if typ == "shape":
            try:
                color_border, color_fill = args["color"]
            except:
                raise ValueError("color is not define")
        elif typ == "image":
            try:
                color_border = args["color"]
            except:
                raise ValueError("color is not define")
        try:
            font = args["font"]
        except:
            font = "PalatinoLinoType"
        try:
            path = args["path"]
        except:
            path = ""
        try:
            size = args["size"]
        except:
            size = 50

        lenghts = []
        for i in buttons:
            width, height = self.draw_text((0,0), i, blit = False)
            if horizontal:
                lenghts.append(height - 2)
            else:
                lenghts.append(width + 10)

        x, y, height = geometry

        mouse = pygame.mouse.get_pos()

        for i in range(len(buttons)):
            if x < mouse[0] < x + lenghts[i] + 8 and y < mouse[1] < y + 50:
                for i in self.actions.mouse_down:
                    if i[0] == 1:
                        self.radiobuttones[radiobuttonID] = buttons[i]
            if typ == "shape" and not horizontal:
                self.draw_shape("rect", (x, y, lenghts[i] + 10, height), color_border)
                self.draw_shape("rect", (x+1, y+1, lenghts[i] + 8, height - 2), color_fill)
                self.draw_text((x+5,y), buttons[i], size, font, color_border)
                if self.radiobuttones[radiobuttonID] == buttons[i]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], color_border)
                x += lenghts[i] + 8
            if typ == "image" and not horizontal:
                self.draw_img(path, (x, y, lenghts[i] + 10, height))
                self.draw_text((x+5,y), buttons[i], size, font, color_border)
                if self.radiobuttones[radiobuttonID] == buttons[i]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], color_border)
                x += lenghts[i] + 10
            if typ == "shape" and horizontal:
                self.draw_shape("rect", (x, y, height, lenghts[i]), color_border)
                self.draw_shape("rect", (x+1, y+1, height-2, lenghts[i]-2), color_fill)
                self.draw_text((x+5,y), buttons[i], size, font, color_border)
                if self.radiobuttones[radiobuttonID] == buttons[i]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], color_border)
                y += lenghts[i]
            if typ == "image" and horizontal:
                self.draw_img(path, (x, y, height, lenghts[i]))
                self.draw_text((x+5,y), buttons[i], size, font, color_border)
                if self.radiobuttones[radiobuttonID] == buttons[i]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], color_border)
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], color_border)
                y += lenghts[i]
            
        return self.radiobuttones[radiobuttonID]    

    def draw_switch(self, typ, geometry, switchID, **args):
        """*typ = shape/image\n*geometry = [x, y, width/height]\n*switchID = String\n*path = string(c:/.../name.imgtype or ./.../name.imgtype)\n*set_if_not = bool\n*color = shape[outline+text(red, green, blue), field_in(red, green, blue)]\n         image(red, green, blue)\n*font = font name\n*size = integer\n\nImportant: typ, geometry, switchID, path(only if typ is image), color(only if typ is shape)\n\nReturns: bool"""
        
    def loop(self):
        self.clocks.tick(self.fps)
        pygame.display.update()
        self.actions.loop()

class actions_listener:
    def __init__(self):

        self.mouse_down = []            # [button, time]
        self.mouse_up = []              # button
        self.key_down = []              # [key, time, asci]
        self.key_up = []                # key
        self.exit_ = False              # True/False
        self.expose = False             # True/False
        self.mouse_in_screen = 1        # 1/0
        self.minimalize = 0             # 1/0

    def loop(self):
        
        self.expose = False
        self.mouse_up = []
        self.key_up = []

        for event in pygame.event.get(): 
            if event.type == 1:
                if event.state == 1:
                    self.mouse_in_screen = event.gain

                elif event.state == 6:
                    self.minimalize = event.gain

            if event.type == 2:
                self.key_down.append([event.key, t.time(), event.unicode])

            elif event.type == 3:
                for i in range(len(self.key_down)):
                    if self.key_down[i][0] == event.key:
                        del self.key_down[i]
                        self.key_up.append(event.key)
                        break

            elif event.type == 4:
                self.mouse_motion = [event.rel, event.pos]

            elif event.type == 5:
                self.mouse_down.append([event.button, t.time()])

            elif event.type == 6:
                for i in range(len(self.mouse_down)):
                    if self.mouse_down[i][0] == event.button:
                        del self.mouse_down[i]
                        self.mouse_up.append(event.button)
                        break

            elif event.type == 17:
                self.expose = True
            
            if event.type == 12:
                self.exit_ = True
            else:
                self.exit_ = False
