# import modules
import pygame, sys
import os
import time
import threading
import socket
import random

# disclaimer the variables used in the hashing algorithm was originaly made to suit a custom hash that is 126 bits but was later modified to suit 64 bits

# turns password into binary and puts each charecter in a list
def binary_conversion(password):
    binary = []
    for x in password:  # itterates through each letter of the password
        binary.append(str(bin(ord(x))[2:].zfill(8)))  # converts the letter into asci and adds it to a list
    return (binary)

# extends the list to an appropriate length
# binary is a list with each item bieng charecters
def extending(binary):
    if len(binary) < 61:  # checks if the binary is less than 61 which is when so
        binary.append("1" * 8)
    while len(binary) < 61:  # 35 is what I have taken as my max charecter count I will change it later on
        binary.append("0" * 8)
    if len(binary) < 61:  # checks if the binary is less than 61 which is when so
        binary.append("1" * 8)
    return binary

# returns the size of the list in a list with each number in binary
# binary is a list with each item bieng charecters note not the extended function answer
def size(binary):
    result = []
    x = (str(len(binary) * 8))# gets the length / size of the password
    while len(x) != 0: # iterates till all charecter / number is covered
        result.append(str(bin(ord(x[0]))[2:].zfill(8))) # converts into binary and adds it to the result
        x = x[1:]
    while len(result) < 3: # loops till answer is at least 3 items
        result.append("0" * 8) # adds filler data
    return result


# binary is a single string in bianry
def rightrotation(binary, num):
    return binary[-num:] + binary[:-num]

# binary is a single string in bianry
def rightshift(binary, num):
    return "0" * num + binary[:-num]


# binary is a list with three items
def addition_mod_2(binary):
    ans = ""
    for x in range(0, len(binary[0])):  # iterates through the binary string
        modulo = 0  # the answer for this charetcer in binary
        for y in range(0, len(binary)):
            modulo += int(binary[y][x])  # adding up each binary charecter
        ans += str(modulo % 2)  # adding the answer to the main
    return (ans)

# Ch in the video
# binary is a list with 3 items
def choose(binary):
    ans = ""
    for x in range(0, len(binary[0])):  # iterates through item 1 of binary list
        # print(binary[0][x])
        if binary[0][x] == "0":
            ans += binary[2][x]  # adds from third item if charecter is 0
        else:
            ans += binary[1][x]  # adds from second item if charecter is 0
    return (ans)


# Maj in the video
# binary is a list with 3 items
# copied the code from the previously written addition mod2 function
# hence variables may not accurately reflect all parts of the code in this function
def majority(binary):
    ans = ""
    for x in range(0, len(binary[0])):  # iterates though one of the items
        modulo = ""
        for y in range(0, len(binary)):  # adds up all the
            modulo += (binary[y][x])  # adds the items in all the lists of the current index into a string
        if modulo.count("1") >= 2:  # checks which charecter is the most common in the string
            ans += "1"  # adds 1 if 1
        else:
            ans += "0"  # adds 0 if 0
    return (ans)

# binary is a string
def lower_sigma0(binary):
    return addition_mod_2([rightrotation(binary, 7), rightrotation(binary, 18), rightshift(binary, 3)])


# binary is a string
def lower_sigma1(binary):
    return addition_mod_2([rightrotation(binary, 17), rightrotation(binary, 19), rightshift(binary, 10)])


# binary is a string
def upper_sigma0(binary):
    return addition_mod_2([rightrotation(binary, 2), rightrotation(binary, 13), rightrotation(binary, 22)])


# binary is a string
def upper_sigma1(binary):
    return addition_mod_2([rightrotation(binary, 6), rightrotation(binary, 11), rightrotation(binary, 25)])


# binary is a list with 64 items each 8 bits long
def split32(binary):
    ans = []
    for x in range(0, 64, 4):  # iterates through the list skipping 4 at a time
        item = ""
        for y in range(0, 4):  # iterates through the numbers 0 to 3
            item += binary[x:x + 4][y]  # combines the strings placing it one after another
        ans.append(item)  # adds the longer answer
    return (ans)


# binary is a list with 8 items which are 16 bits each
def Wlist(binary):
    for x in range(17, 64 + 1):  # creates the rest of the message scheduling lists
        binary.append(
            addition([lower_sigma1(binary[x - 2]), binary[x - 5], lower_sigma0(binary[x - 7]), binary[x - 9]]))
    return (binary)


# this function adds up the binary numbers
# binary is a list with multiple items of binary
def addition(binary):
    total = 0
    for x in range(0, len(binary)):  # iterates through all sublists in the binary list
        total += (int(binary[x], 2))  # adds up the numbers by converting it into integers
    ans = str(bin(total % (2 ** 32)))[2:].zfill(32)  # converts the numbers back to binary
    return (ans)


# w is a list with 32 items
def alphabets(w):  # main hashing answer
    k = [  # constants derived from square rooting prime numbers - stops backdoors
        "01000010100010100010111110011000",
        "01110001001101110100010010010001",
        "10110101110000001111101111001111",
        "11101001101101011101101110100101",
        "00111001010101101100001001011011",
        "01011001111100010001000111110001",
        "10010010001111111000001010100100",
        "10101011000111000101111011010101",
        "11011000000001111010101010011000",
        "00010010100000110101101100000001",
        "00100100001100011000010110111110",
        "01010101000011000111110111000011",
        "01110010101111100101110101110100",
        "10000000110111101011000111111110",
        "10011011110111000000011010100111",
        "11000001100110111111000101110100",
        "11100100100110110110100111000001",
        "11101111101111100100011110000110",
        "00001111110000011001110111000110",
        "00100100000011001010000111001100",
        "00101101111010010010110001101111",
        "01001010011101001000010010101010",
        "01011100101100001010100111011100",
        "01110110111110011000100011011010",
        "10011000001111100101000101010010",
        "10101000001100011100011001101101",
        "10110000000000110010011111001000",
        "10111111010110010111111111000111",
        "11000110111000000000101111110011",
        "11010101101001111001000101000111",
        "00000110110010100110001101010001",
        "00010100001010010010100101100111",
        "10001100110001110000001000001000",
        "10010000101111101111111111111010",
        "10100100010100000110110011101011",
        "10111110111110011010001111110111",
        "11000110011100010111100011110010",
        "11001010001001110011111011001110",
        "11010001100001101011100011000111",
        "11101010110110100111110111010110",
        "11110101011111010100111101111111",
        "00000110111100000110011110101010",
        "00001010011000110111110111000101",
        "00010001001111111001100000000100",
        "00011011011100010000101100110101",
        "00101000110110110111011111110101",
        "00110010110010101010101101111011",
        "00111100100111101011111000001010",
        "01000011000111010110011111000100",
        "01001100110001011101010010111110",
        "01011001011111110010100110011100",
        "01011111110010110110111110101011",
        "01101100010001000001100110001100",
        "01110100100011111000001011101110",
        "01111000101001010110001101101111",
        "10000100110010000111100000010100",
        "10001111000110111111110011011110",
        "10011100011001101110010010101001",
        "10100010101111111110100010100001",
        "10101000000110100110011001001011",
        "11000011110100101110000101000010",
        "11000110101100111101101110100101",
        "11010101010111100011111110001001",
        "11101010110110100111110111010110"
    ]

    h = [  # constants derived from cube rooting prime numbers - stops backdoors
        "01101010000010011110011001100111",
        "10111011011001111010111010000101",
        "00111100011011101111001101110010",
        "10100101010011111111010100111010",
        "01010001000011100101001001111111",
        "10011011000001010110100010001100",
        "00011111100000111101100110101011",
        "01011011111000001100110100011001"
    ]

    for t in range(0, 64):  # iterates through the entire list which I know is going to have a total of 64 elements
        t1 = addition([h[7], upper_sigma1(h[4]), choose([h[4], h[5], h[6]]), k[t],
                       w[t]])  # creates a variable from the previous items + iteration number
        t2 = addition([upper_sigma0(h[0]),
                       majority([h[0], h[1], h[2]])])  # creates a variable from the previous items + iteration number
        h = rotate(h, t1, t2)
    return (h)


# h is a list with 8 items each item is a string of 32 bits
def rotate(h, t1, t2):
    hnew = []

    # appends original list in a different order than normal
    hnew.append(addition([t1, t2]))
    hnew.append(h[0])
    hnew.append(h[1])
    hnew.append(h[2])
    hnew.append(addition([h[3], t1]))
    hnew.append(h[4])
    hnew.append(h[5])
    hnew.append(h[6])

    return hnew


# processing
def process(password):
    binary_list = (binary_conversion(password))  # gets the binary version of password
    extended_list = extending(binary_list)  # extends the binary list tot he appropriate length
    for x in size(binary_conversion(password)):  # gets the size of binary function
        extended_list.append(x)  # adds it to the extended list

    extended_list = (split32(extended_list))  # formats the extended list in the right way
    w32list = Wlist(extended_list)  # does the message scheduling for final hash

    ans = ""
    for x in alphabets(w32list):  # final hash
        ans += x  # adds them up to get it in the correct format instead of a list
    return ans

# function to display an image
def display_image(screen, image, scale, x, y):
    signin = pygame.image.load(image)
    w = signin.get_width()
    h = signin.get_height()
    signin = pygame.transform.scale(signin, (round(w * scale), round(h * scale)))
    screen.blit(signin, (x, y))


# function to get width and height of the image
def getdimentions(image, scale):
    signin = pygame.image.load(image)
    w = signin.get_width()
    h = signin.get_height()
    return [int(w * scale), int(h * scale)]

# draws a rectange
def buttoncheck(x, y, width, height, screen, color):
    pygame.draw.rect(screen, color, (x, y, width, height))

# reads a text file
def textread(f):
    fileName = f
    fileOpen = open(fileName, "r")
    return fileOpen.read()

# checks if a word is in a list of words
def check_word(words, word):
    for x in words:
        if x.lower() in word.lower():
            return True
            break
    return False

def login():

    # sending messages to the server
    def send(msg):
        message = msg.encode(FORMAT)

        # creating the header
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))

        # sending information to server
        client.send(send_length)
        client.send(message)

    # receiving messages from the server
    def recieve():
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            return (msg)

    # files
    # password related files
    file = "sorted passwords.txt"
    commonpasswords = textread(file).split()
    new = []
    for x in commonpasswords:
        new.append(x.lower())
    commonpasswords = new
    # username related files
    file1 = []
    with open("bad_words_cleaned.txt", 'r') as file:
        lines = file.readlines()
    for x in lines:
        file1.append(x.rstrip('\n'))

    # sets the size of the login
    scale = 1

    # variable holders for display
    background_colour = (26, 19, 47)  # a variable that holds the background color
    try:
        width = getdimentions("sign_up_cropped.png", scale)[0]  # width of the game window
        height = getdimentions("sign_up_cropped.png", scale)[1]  # height of the game window
    except:
        print("sign up UI image not found")
        sys.exit()
    # setting up screen
    pygame.init()
    screen = pygame.display.set_mode([width, height])  # setting the size of the window
    pygame.display.set_caption('sign in / sign up')  # assigning the window a name
    clock = pygame.time.Clock()  # shortens time syntax and is used for clock
    clock1 = pygame.time.Clock()  # shortens time syntax and is used for clock 1

    # variables for UI
    show_password = False
    running = True  # variable that controls game loop
    signbutton = True  # True = log in ; False = sign up
    password = False
    userid = False
    UID = ""
    Upassword = ""
    error = ""
    font = pygame.font.Font(pygame.font.match_font('timesnewroman'), 38)
    visible = True
    attempts = 0
    timer = 10  # in seconds

    # constants for an client server connection
    PORT = 5050
    SERVER = "192.168.0.8"  # needs to be changed depending on the server device
    ADDR = (SERVER, PORT)
    FORMAT = "utf-8"
    HEADER = 64
    DISCONNECT_MESSAGE = "!DISCONNECT"

    # setting up the online connection
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except:
        print("server not running")
        sys.exit()

    # defining main game loop
    while running:
        # getting events
        for event in pygame.event.get():  # looks for all inputs
            if event.type == pygame.QUIT:  # checking if cross button is pressed
                running = False  # stops the game
                send(DISCONNECT_MESSAGE)
                return "exit"
                pygame.quit()
                sys.exit()
            # mouse presses
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # log in switch
                if 175 < pos[0] < (470):
                    if 193 < pos[1] < (300):
                        # reseting variables
                        UID = ""
                        Upassword = ""
                        signbutton = True
                        error = ""
                # sign up switch
                if (465) < pos[0] < (470 + 465):
                    if 193 < pos[1] < (300):
                        # reseting variables
                        UID = ""
                        Upassword = ""
                        signbutton = False
                        error = ""
                # submit
                if 255 < pos[0] < (720):
                    if 680 < pos[1] < (840):
                        # submit for log in
                        error = ""
                        if attempts < 3: # checks if too many attempts
                            if signbutton == True:
                                # checking for errors
                                if len(UID) == 0 or len(Upassword) == 0: # checks for empty entries
                                    error = "username or password section has been left blank" # if there are empty entries error message displayed
                                else: # if no empty entries
                                    if len(UID) >= 3: # if username if logn enough
                                        if len(Upassword) >= 4: # if the password is long enough
                                            if Upassword.lower() in commonpasswords: # if password not unique enough
                                                error = "password is too common" # if the password is too common displays an error message
                                            else:
                                                if check_word(file1, UID): # checks if usename does not have profanities
                                                    error = "profanities in username that are not allowed" # displays an error message
                                                else: # the inputs have passed all validation on the client side - sends data to server for authentication
                                                    send("check" + " " + UID + " " + str(process(Upassword)))# sending data with trigger word
                                                    reply = recieve() # recieving a response
                                                    if reply == "incorrect password": # if password is wrong
                                                        error = "the password is incorrect" # error message is displayed
                                                        attempts += 1 # increases attempts
                                                    elif reply == "username not found": # username does not exist
                                                        error = "the username does not exist" # displays an error message
                                                    else:  # reply has to be correct
                                                        send(DISCONNECT_MESSAGE) # the authentication is done checked all the categories
                                                        homescreen(UID)

                                        else:
                                            error = "password is too short need a minimum of " + str(4 - len(Upassword)) + " more charecters" # displays error if password is too short
                                    else:
                                        error = "username is too short need a minimum of " + str(3 - len(UID)) + " more charecters" # displays error message if username too short
                        # submit for sign up
                        if signbutton == False:
                            # checking for errors
                            if len(UID) == 0 or len(Upassword) == 0: # checks for empty entries
                                error = "username or password section has been left blank"
                            else:
                                if len(UID) >= 3: # checks for minimum username length
                                    if len(Upassword) >= 4:# checks for minimum password length
                                        if Upassword in commonpasswords: # password is too common
                                            error = "password is too common" # displays an error message
                                        else:
                                            if check_word(file1, UID): # checks if username has profanities
                                                error = "profanities in username that are not allowed" # displays an error message
                                            else:
                                                send("save" + " " + UID + " " + str(process(Upassword))) # sends data to server because passed verification check
                                                reply = recieve()
                                                if reply == "username is taken by someone else": # username already taken
                                                    error = "username is taken by someone else" # displays the error on the screen
                                                else: # passed all authentification processes
                                                    # takes you to the log in page
                                                    UID = ""
                                                    Upassword = ""
                                                    signbutton = True

                                    else:
                                        error = "password is too short need a minimum of " + str(4 - len(Upassword)) + " more charecters" # password too short
                                else:
                                    error = "username is too short need a minimum of " + str(3 - len(UID)) + " more charecters" # username too short

                if 180 < pos[0] < (750): # if username box selected
                    if 410 < pos[1] < (490):
                        userid = True # activates username inputs
                        password = False
                if 180 < pos[0] < (750): # if password box selected
                    if 580 < pos[1] < (580 + 490 - 410):
                        password = True # activates password inputs
                        userid = False
                else: # nothing selected
                    userid = False # deactivates everything
                    password = False

            # getting key presses
            if event.type == pygame.KEYDOWN:
                # updating userid
                if userid: # getting keyboard inputs
                    if event.key == pygame.K_BACKSPACE: # deleting charecters
                        UID = UID[:-1]
                    else:
                        if len(UID) < 29: # adding new charecters if limit not reached
                            UID += event.unicode
                # updating password
                elif password: # getting keyboard inputs
                    if event.key == pygame.K_BACKSPACE:
                        Upassword = Upassword[:-1] # deleting charecters
                    else:
                        if len(Upassword) < 29: # adding new charecters if limit not reached
                            Upassword += event.unicode

                # shift key inputs
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    show_password = True # shift to revial password

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    show_password = False # stops password from being revealed

        # slider controls
        if signbutton == True:
            try:
                display_image(screen, "log_in_cropped.png", scale, 0, 0)
            except:
                print("log in UI image not found")
                sys.exit()
        else:
            try:
                display_image(screen, "sign_up_cropped.png", scale, 0, 0)
            except:
                print("sign up UI image not found")
                sys.exit()
        # incorrect log in attempts limiter
        if attempts == 3: # starting countdown
            timepassed += clock1.get_time()
            if timer - (timepassed / 1000) < 0: # checks if enough time has passed
                timer = timer * 2 # increases timer
                attempts = 0 # resets attempts
                error = "" # resets error
            else:
                error = "too many incorrect attempts cooldown: " + str(round(timer - (timepassed / 1000), 1))
        elif attempts != 3:
            timepassed = 0

        # visability toggleing for blinker
        if password == True or userid == True: # activating blinker
            cursor_time += clock.get_time()
            if cursor_time >= 530: # cursor time
                # inverses the visibility (on turns off vise versa)
                if visible == True:
                    visible = False
                elif visible == False:
                    visible = True
                cursor_time = 0
        else:
            cursor_time = 0 # reseting blinker

        # updating the display
        # when password must be shown
        if show_password:
            if password == False:
                # displaying when password is not active
                userpassworddisplay = font.render(Upassword, True, (255, 0, 255))
            else:
                # displaying when password is active
                # blinker
                if visible == True:
                    userpassworddisplay = font.render(Upassword + "|", True, (255, 0, 255)) # cursor shown
                elif visible == False:
                    userpassworddisplay = font.render(Upassword, True, (255, 0, 255)) # cursor not shown
        # when password must be hidden
        else:
            # displaying when password is not active
            if password == False:
                userpassworddisplay = font.render("*" * len(Upassword), True, (255, 0, 255))
            # displaying when password is active
            # blinker
            else:
                if visible == True:
                    userpassworddisplay = font.render("*" * len(Upassword) + "|", True, (255, 0, 255)) # cursor shown
                elif visible == False:
                    userpassworddisplay = font.render("*" * len(Upassword), True, (255, 0, 255)) # cursor not shown

        if userid == False:
            useriddisplay = font.render(UID, True, (255, 0, 255))
        else:
            if visible == True:
                useriddisplay = font.render(UID + "|", True, (255, 0, 255))
            elif visible == False:
                useriddisplay = font.render(UID, True, (255, 0, 255))

        usererror = font.render(error, True, (255, 0, 0))

        # displaying stuff on the screen
        screen.blit(usererror, (20, 880)) # errors if any
        screen.blit(userpassworddisplay, (190, 610)) # password
        screen.blit(useriddisplay, (190, 436)) # username

        # update screen
        pygame.display.flip()  # allows to make changes to the screen / display
        clock.tick(60)  # only updates at a refresh of 60 hertz
        clock1.tick(10)

def homescreen(username):
    # constants for an client server connection
    PORT = 5050
    SERVER = "192.168.0.8"  # needs to be changed becuase I am using codehs
    ADDR = (SERVER, PORT)
    FORMAT = "utf-8"
    HEADER = 64
    DISCONNECT_MESSAGE = "!DISCONNECT"

    # setting up the online connection
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except:
        print("server not running")
        sys.exit()

    # sending messages to the server
    def send(msg):
        message = msg.encode(FORMAT)

        # creating the header
        msg_length = len(message) # getting actual message length
        send_length = str(msg_length).encode(FORMAT) # encoding the message length
        send_length += b" " * (HEADER - len(send_length)) # calculating the final length

        # sending information to server
        client.send(send_length) # sending the length
        client.send(message)

    # receiving messages from the server
    def recieve():
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            return (msg)

    def loading(dtime, x_pos, time):
        width = 700 * (time - (dtime)) / time
        buttoncheck(x_pos, 350, 700, 50, screen, (255, 0, 0))
        buttoncheck(x_pos, 350, width, 50, screen, (0, 255, 0))

    send("log" + " " +str(username))
    reply = recieve()
    print(reply)
    send(DISCONNECT_MESSAGE)

    # sets the size of the login
    scale = 0.75
    charecter = 1

    # variable holders for display
    try:
        width = getdimentions("Homescreen.png.png", scale)[0] + 390  # width of the game window
        height = getdimentions("Homescreen.png.png", scale)[1]  # height of the game window
    except:
        print("homescreen UI image not found")
        sys.exit()# exiting of the game window

    # setting up screen
    pygame.init()
    screen = pygame.display.set_mode([width, height])  # setting the size of the window
    pygame.display.set_caption('sign in / sign up')  # assigning the window a name
    clock = pygame.time.Clock()  # shortens time syntax

    # variables for login
    running = True
    settings = False
    battlelog = False

    while running:
        # getting events
        for event in pygame.event.get():  # looks for keyboard inputs
            if event.type == pygame.QUIT:  # checking if cross button is pressed
                running = False  # stops the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # main screen button clicks
                if battlelog == False and settings == False: # decativates controls if subscreen is active
                    # fight
                    if 290 < pos[0] < 825:
                        if 115 < pos[1] < 310:
                            print("fight")
                            maingame(charecter,username) # calls main game
                    # settings
                    if 305 < pos[0] < 820:
                        if 350 < pos[1] < 470:
                            settings = True # activates settings sub screen
                    # battle log
                    if 305 < pos[0] < 820:
                        if 500 < pos[1] < 620:
                            battlelog = True # activates the battle log sub screen
                    # exit
                    if 305 < pos[0] < 820:
                        if 640 < pos[1] < 735:
                            running = False  # stops the game
                            pygame.quit()
                            sys.exit() # stops the homescreen
                    # log out
                    if 305 < pos[0] < 820:
                        if 770 < pos[1] < 860:
                            running = False  # stops the homescreen
                            login() # calls the login function

                if settings == True:
                    # controls of settings
                    if 980 < pos[0] < 1040:
                        if 70 < pos[1] < 142:
                            settings = False
                    if 190 < pos[0] < 315:
                        if 730 < pos[1] < 770:
                            charecter=1
                            print("sanji selected")
                    if 800 < pos[0] < 925:
                        if 730 < pos[1] < 760:
                            charecter=0
                            print("zoro selected")

                if battlelog == True:
                    # controls of battle log
                    if 980 < pos[0] < 1040:
                        if 70 < pos[1] < 142:
                            battlelog = False

        # screen
        try:
            display_image(screen, "background.jpg", 0.483, 0, 0)
        except:
            print("homescreen background image not found")
            sys.exit()
        try:
            display_image(screen, "Homescreen.png.png", scale, 180, 0)
        except:
            print("homescreen UI image not found")
            sys.exit()
        if settings == True:
            buttoncheck(100, 50, (width - 200), (height - 100), screen, (54, 127, 217))
            try:
                display_image(screen, "cross.png", 0.08, 970, 60)
            except:
                print("cross image not found")
                sys.exit()
            try:
                display_image(screen, "idle/1.png", 0.4, 750, 400)
            except:
                print("idle for zoro not found")
                sys.exit()
            try:
                display_image(screen, "1.png", 0.32, 200, 400)
            except:
                print("idle for sanji not found")
                sys.exit()
            font = pygame.font.SysFont(None, 50)
            text_surface = font.render("select", True, (0, 0, 0))
            screen.blit(text_surface, (200, 730))
            screen.blit(text_surface, (810, 730))

        if battlelog == True:
            buttoncheck(100, 50, (width - 200), (height - 100), screen, (54, 127, 217))
            try:
                display_image(screen, "cross.png", 0.08, 970, 60)
            except:
                print("cross image not found")
                sys.exit()
            font = pygame.font.SysFont(None, 50)
            battles = font.render(reply[0] + " number of wins", True, (0, 0, 0))
            wins = font.render(reply[2] + " number of battles played", True, (0, 0, 0))
            loading(int(reply[0]), 250, int(reply[2]))
            screen.blit(battles, (130, 730))
            screen.blit(wins, (600, 730))


        # update screen
        pygame.display.flip()  # allows to make changes to the screen / display
        clock.tick(60)  # only updates at a refresh of 60 hertz
    pygame.quit()

# button check
def buttoncheck(x, y, width, height, screen, color):
    pygame.draw.rect(screen, color, (x, y, width, height))

# creates a loading bar
def loadingnew():
    # variables for the laoding bar
    time = random.randint(10, 100)
    pygame.init()

    width = 800
    height = 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Loading screen")

    clock = pygame.time.Clock()
    dtime = 0

    # Main game loop
    running = True

    # makes the loading bar work
    while running:
        # allows users to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # adding a background color
        screen.fill((49, 18, 184))

        #  creating the loading the bar
        dtime += clock.tick()
        width = 700 * (time - (dtime / 100)) / time
        buttoncheck(50, 350, width, 100, screen, (0, 0, 0))

        pygame.display.flip()

        # calculating the time
        if (time - (dtime / 100)) / time <= 0:
            print("done")
            running = False
            pygame.quit()

# a function that sets up the win / lose screen
def endscreen(condition,username):
    # constants for an client server connection
    PORT = 5050
    SERVER = "192.168.0.8"  # needs to be changed becuase I am using codehs
    ADDR = (SERVER, PORT)
    FORMAT = "utf-8"
    HEADER = 64
    DISCONNECT_MESSAGE = "!DISCONNECT"

    # setting up the online connection
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except:
        print("server not running")
        sys.exit()

    # sending messages to the server
    def send(msg):
        message = msg.encode(FORMAT)

        # creating the header
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))

        # sending information to server
        client.send(send_length)
        client.send(message)

    send("update" + " " + username + " " + condition) # sends data to the server so they can update the users file
    send(DISCONNECT_MESSAGE)

    # function that displays a image
    def display_image(screen, image, scale, x, y):
        signin = pygame.image.load(image)
        w = signin.get_width()
        h = signin.get_height()
        signin = pygame.transform.scale(signin, (round(w * scale), round(h * scale)))
        return signin

    # function that gives you the dimentions of the image
    def getdimentions(image, scale):
        signin = pygame.image.load(image)
        w = signin.get_width()
        h = signin.get_height()
        return [w, h]

    # background variables
    scale = 1
    try:
        width = getdimentions("win.png", scale)[0]
        height = getdimentions("win.png", scale)[1]
    except:
        print("homescreen UI image not found")
        sys.exit()

    # setting up pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Loading screen")

    # Main game loop
    running = True

    while running:
        # displays win background if you won / lose background if you lost
        if condition == "win":
            screen.blit(display_image(screen, "win.png", scale, 0, 0), (0, 0))
        if condition == "lose":
            screen.blit(display_image(screen, "lose.png", scale, 0, 0), (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 240 < pos[0] < (790):
                    if 640 < pos[1] < (840):
                        running = False
                        print("homescreen")
                        pygame.quit()
                        homescreen(username) # takes you back to the homescreen
def maingame(charecter,username):
    # a class for the network
    class Network:
        # initial set up this is what happens when the Network is declared
        def __init__(self): # sets up server variables needed to make a connection
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server = "192.168.0.8"
            self.port = 5555
            self.addr = (self.server, self.port)
            self.pos = self.connect()

        # connects to the server initally
        def connect(self):
            try: # connects to the server
                self.client.connect(self.addr)
                initial_pos = self.client.recv(2048).decode()
                return initial_pos
            except: # if failed prints an error message
                print("server not running")
                sys.exit()


        # sends a message to the server and returns a response sent by the server
        def send(self, data):
            try:# sends messages to the server
                self.client.send(str.encode(data))
                return self.client.recv(2048).decode()
            except: # if failed prints an error message
                print("server not running")
                sys.exit()

        # functions that take in inputs from the network and decodes them in the right way
        def read_pos(self, str): # decodes the data recieved
            str = str.split(",")
            x = str[0]
            y = str[1]
            direction = str[2]
            cycle = str[3]
            animation = str[4]
            health = str[5]
            charecter = str[6]
            dammage = str[7]
            return [int(x), int(y), int(direction), int(cycle), int(animation), int(health), int(charecter),int(dammage)] # returns the data as a list

        # function that encodes the data to be sent the right way
        def make_pos(self, pos):
            return str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2]) + "," + str(pos[3]) + "," + str(pos[4]) + "," + str(pos[5]) + "," + str(pos[6]) + "," + str(pos[7])

    # class for bliting boxes onto the screen
    class box():
        # initial set up this is what happens when a box is declared
        def __init__(self, x, y, color, speed, yspeed, gravity, health, charecter):
            self.x = x
            self.y = y
            self.color = color
            self.speed = speed
            self.init_yspeed = -yspeed
            self.gravity = gravity
            self.jumping = False
            self.animation = 0
            self.cycle = 0
            self.direction = True
            self.locked = False
            self.dammage = 0
            self.health = health
            self.charecter = charecter
            print(charecter)

        # function for attacks
        def attack(self, size):
            # check try and accept in case cycle is out of sync
            try:
                # adjusting attacks based on direction
                if self.direction == True:
                    # creates a an attacking region
                    self.rect = pygame.Rect((int(self.x) + (self.spriteswidth[self.charecter][self.animation][self.cycle]) // 2 - 50 + 100, int(self.y), size, 200))
                    pygame.draw.rect(screen, (255, 0, 0), self.rect)
                    return self.rect
                else:
                    # creates a an attacking region
                    self.rect = pygame.Rect((int(self.x) + (self.spriteswidth[self.charecter][self.animation][self.cycle]) // 2 - 50 - size, int(self.y), size, 200))
                    pygame.draw.rect(screen, (255, 0, 0), self.rect)
                    return self.rect
            except:
                # resets the animation cycle becuse it reached its end and also changes and lock animations so that they are not locked anymore
                self.locked = False
                self.cycle = 0
                # creates a an attacking region based on direction
                if self.direction == True:
                    self.rect = pygame.Rect((int(self.x) + (self.spriteswidth[self.charecter][self.animation][self.cycle]) // 2 - 50 + 100, int(self.y), size, 200))
                    pygame.draw.rect(screen, (255, 0, 0), self.rect)
                    return self.rect
                # creates a an attacking region based on direction
                else:
                    self.rect = pygame.Rect((int(self.x) + (self.spriteswidth[self.charecter][self.animation][self.cycle]) // 2 - 50 - size, int(self.y), size, 200))
                    pygame.draw.rect(screen, (255, 0, 0), self.rect)
                    return self.rect

        # loads the sprites from they're folders and saves it in a list
        def spriteload(self):
            # defining the lists where updates occur
            self.spriteswidth = [[], []]
            self.sprites = [[], []]
            # updating main lists for idle
            # temporary lists
            sprites = []
            width = []

            # cycling through the sprites
            try:  # if images exists
                for x in range(1, 8):
                    # finding out which scale to use
                    scale = 200 / getdimentions('idle/' + str(x) + '.png', 1)[1]
                    # updating the width list coresponding with the scale
                    width.append(getdimentions('idle/' + str(x) + '.png', 1)[0] * scale)
                    # getting pygame loadable sprite images coresponding with the scale
                    sprites.append(display_image(" ", 'idle/' + str(x) + '.png', scale, 1, 1))
                # final updating of the main lists
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:  # if they dont print error message and quit
                print("idle images not found")
                sys.exit()
            # repreat same procedure for walking
            sprites = []
            width = []
            try:
                for x in range(1, 9):
                    scale = 200 / getdimentions('walk/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('walk/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'walk/' + str(x) + '.png', scale, 1, 1))
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:
                print("walk images not found")
                sys.exit()
            # repreat same procedure for jumping
            sprites = []
            width = []
            try:
                for x in range(1, 3):
                    scale = 200 / getdimentions('jump/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('jump/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'jump/' + str(x) + '.png', scale, 1, 1))
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:
                print("jump images not found")
                sys.exit()
            # repreat same procedure for dodgeing
            sprites = []
            width = []
            try:
                for x in range(1, 4):
                    scale = 200 / getdimentions('dodge/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('dodge/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'dodge/' + str(x) + '.png', scale, 1, 1))
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:
                print("dodge images not found")
                sys.exit()
            # repreat same procedure for running
            sprites = []
            width = []
            try:
                for x in range(1, 7):
                    scale = 200 / getdimentions('running/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('running/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'running/' + str(x) + '.png', scale, 1, 1))
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:
                print("running images not found")
                sys.exit()
            # repreat same procedure for attacks
            sprites = []
            width = []
            try:
                for x in range(1, 6):
                    scale = 200 / getdimentions('attack1/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('attack1/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'attack1/' + str(x) + '.png', scale, 1, 1))
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:
                print("attack1 images not found")
                sys.exit()
            # repreat same procedure for attacks
            sprites = []
            width = []
            try:
                for x in range(1, 6):
                    scale = 200 / getdimentions('attack2/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('attack2/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'attack2/' + str(x) + '.png', scale, 1, 1))
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:
                print("attack2 images not found")
                sys.exit()
            sprites = []
            width = []
            # repreat same procedure for blocking
            try:
                for x in range(1, 4):
                    scale = 200 / getdimentions('block/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('block/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'block/' + str(x) + '.png', scale, 1, 1))
                self.sprites[0].append(sprites)
                self.spriteswidth[0].append(width)
            except:
                print("block images not found")
                sys.exit()
            sprites = []
            width = []
            # cycling through the sprites
            try:
                for x in range(1, 5):
                    # finding out which scale to use
                    scale = 200 / getdimentions('idle1/' + str(x) + '.png', 1)[1]
                    # updating the width list coresponding with the scale
                    width.append(getdimentions('idle1/' + str(x) + '.png', 1)[0] * scale)
                    # getting pygame loadable sprite images coresponding with the scale
                    sprites.append(display_image(" ", 'idle1/' + str(x) + '.png', scale, 1, 1))
                # final updating of the main lists
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("idle1 images not found")
                sys.exit()
            # repreat same procedure for walking
            sprites = []
            width = []
            try:
                for x in range(1, 9):
                    scale = 200 / getdimentions('walking1/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('walking1/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'walking1/' + str(x) + '.png', scale, 1, 1))
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("walking1 images not found")
                sys.exit()
            # repreat same procedure for jumping
            sprites = []
            width = []
            try:
                for x in range(1, 2):
                    scale = 200 / getdimentions('jump1/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('jump1/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'jump1/' + str(x) + '.png', scale, 1, 1))
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("jump1 images not found")
                sys.exit()
            # repreat same procedure for dodgeing
            sprites = []
            width = []
            try:
                for x in range(1, 4):
                    scale = 200 / getdimentions('dodge1/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('dodge1/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'dodge1/' + str(x) + '.png', scale, 1, 1))
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("dodge1 images not found")
                sys.exit()
            # repreat same procedure for running
            sprites = []
            width = []
            try:
                for x in range(1, 7):
                    scale = 200 / getdimentions('running1/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('running1/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'running1/' + str(x) + '.png', scale, 1, 1))
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("running1 images not found")
                sys.exit()
            # repreat same procedure for attacks
            sprites = []
            width = []
            try:
                for x in range(1, 6):
                    scale = 200 / getdimentions('attack1/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('attack1/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'attack1/' + str(x) + '.png', scale, 1, 1))
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("attack1 images not found")
                sys.exit()
            # repreat same procedure for attacks
            sprites = []
            width = []
            try:
                for x in range(1, 6):
                    scale = 200 / getdimentions('attack2/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('attack2/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'attack2/' + str(x) + '.png', scale, 1, 1))
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("attack2 images not found")
                sys.exit()
            sprites = []
            width = []
            # repreat same procedure for blocking
            try:
                for x in range(1, 4):
                    scale = 200 / getdimentions('block1/' + str(x) + '.png', 1)[1]
                    width.append(getdimentions('block1/' + str(x) + '.png', 1)[0] * scale)
                    sprites.append(display_image(" ", 'block1/' + str(x) + '.png', scale, 1, 1))
                self.sprites[1].append(sprites)
                self.spriteswidth[1].append(width)
            except:
                print("block1 images not found")
                sys.exit()

        # displays player on the screen
        def draw(self, screen):
            # use try accept to cycle to reset if it does not work
            try:
                self.rect = pygame.Rect((int(self.x) + (self.spriteswidth[self.charecter][self.animation][self.cycle]) // 2 - 50, int(self.y), 100, 200))
                pygame.draw.rect(screen, self.color, self.rect)
            except:
                self.locked = False
                self.cycle = 0
                self.rect = pygame.Rect((int(self.x) + (self.spriteswidth[self.charecter][self.animation][self.cycle]) // 2, int(self.y), 100, 200))
                pygame.draw.rect(screen, self.color, self.rect)
            # actually displaying it it
            screen.blit(pygame.transform.flip(self.sprites[self.charecter][self.animation][self.cycle], self.direction, False),(self.x, self.y))

        # moves animations to the next sprite in the cycle
        def update(self):
            if self.jumping == True and self.animation != 3 and self.animation != 4:
                # keep animation and cycle fixed during jump
                self.animation = 2
                self.cycle = 0
            else:
                self.cycle += 1

        # direction = True = facing right
        # direction = False = facing left

        # changes the position of the code
        def move(self, keys):
            # sets up change in speed
            currentstate = self.animation
            dx = 0
            # button checks
            if self.locked == False:
                # running / dodgeing
                if keys[pygame.K_RIGHT] == True:
                    # identifies which animation to keep based on direction + updates speed
                    if self.direction == True:
                        currentstate = 4
                        dx = self.speed * 2
                    else:
                        currentstate = 3
                        dx = self.speed * 2
                # running / dodgeing
                elif keys[pygame.K_LEFT] == True:
                    # identifies which animation to keep based on direction + updates speed
                    if self.direction == True:
                        currentstate = 3
                        dx = -self.speed * 2
                    else:
                        currentstate = 4
                        dx = -self.speed * 2
                #  walking left
                elif keys[pygame.K_a] == True and self.jumping == False:
                    # updates speed
                    dx = -self.speed
                    if self.animation != 1:
                        currentstate = 1  # changes animation cycle
                    self.direction = False  # changes direction
                # walking right
                elif keys[pygame.K_d] == True and self.jumping == False:
                    # updates speed
                    dx = self.speed
                    if self.animation != 1:
                        currentstate = 1  # changes animation cycle
                    self.direction = True  # changes direction

                # reseting to idle if no other animation should be active
                elif self.jumping == False:
                    currentstate = 0  # changes aniamtion cycle

                # checks for jumping
                if keys[pygame.K_w] == True:
                    if self.jumping == False:
                        self.jumping = True
                        self.yspeed = self.init_yspeed
                # checks for blocking
                if keys[pygame.K_i] == True:
                    currentstate = 7
                    self.locked = True
                # checks for attacks
                elif keys[pygame.K_p] == True:
                    currentstate = 5
                    self.locked = True
                # checks for attacks
                elif keys[pygame.K_o] == True:
                    currentstate = 6
                    self.locked = True
                # actually updating animation if anything has changed
                if currentstate != self.animation:
                    self.animation = currentstate
                    self.cycle = 0

            # updates the position for x
            self.x += dx
            if self.x < 120:
                self.x = 120
            if self.x > 1165:
                self.x = 1165
            # updates the position for y
            if self.jumping == True:
                self.yspeed += self.gravity
                self.y += self.yspeed
            if self.y >= 575:
                self.y = 575
                self.jumping = False

    # draws a rectangle based on inputs
    def buttoncheck(x, y, width, height, screen, color):
        pygame.draw.rect(screen, color, (x, y, width, height))

    # time is the max health of the player dtime is the dammage that has been dealt
    # xpos is the xposition to display the health bar
    def loading(dtime, x_pos, time):
        # draws out the health bar
        width = 300 * (time - (dtime / 60)) / time
        buttoncheck(x_pos, 20, 300, 50, screen, (255, 0, 0)) # dammage delt
        buttoncheck(x_pos, 20, width, 50, screen, (0, 255, 0)) # health left

        if (time - (dtime)) / time <= 0:
            return "died"

    # function that displays a image
    def display_image(screen, image, scale, x, y):
        signin = pygame.image.load(image)
        # gets dimentions so scale can be changed later
        w = signin.get_width()
        h = signin.get_height()
        # updates the image based on the scale
        signin = pygame.transform.scale(signin, (round(w * scale), round(h * scale)))
        return signin

    # function that gives you the dimentions of the image
    def getdimentions(image, scale):
        signin = pygame.image.load(image)
        w = signin.get_width()
        h = signin.get_height()
        return [w, h]

    # setting up the game variables
    # setting up the players
    box1 = box(120, 575, (255, 255, 0), 10, 30, 2, 120, charecter)
    box2 = box(1165, 575, (255, 0, 255), 10, 30, 2, 120, 0)
    # loading up the sprites in a thread so it can run in parralel with the loading bar
    sprites1 = threading.Thread(target=box1.spriteload)
    sprites2 = threading.Thread(target=box2.spriteload)
    # starting the thread
    sprites1.start()
    sprites2.start()
    loadingnew()# creating the loading bar page
    running = True

    # background variables
    scale = 1
    try:
        width = getdimentions("ship 8.png", scale)[0]
        height = getdimentions("ship 8.png", scale)[1]
    except:
        print("ship background image not found")
        sys.exit()

    # setting up pygame
    pygame.init()
    cursor_time = 0
    screen = pygame.display.set_mode([width, height]) # setting up the screen
    pygame.display.set_caption('Main Game')
    clock = pygame.time.Clock() # adding a clock for the game

    # loading up the background image
    try:
        background = display_image(screen, "ship 8.png", scale, 0, 0)
    except:
        print("ship background image not found")
        sys.exit()

    # setting up the network class
    n = Network()
    initial = n.read_pos(n.pos) # recieving the first set of data from the server
    # only updating essential data dont need all for the set up
    box1.x = initial[0]
    box1.y = initial[1]
    if initial[2] == 1:
        box1.direction = False
    else:
        box1.direction = True
    box1.cycle = initial[3]
    box1.animation = initial[4]

    timecheck = [71, 56, 0, 67, 58, 100, 80, 120] # a list that adjusts the ammount of time to wait before switching to next frame

    # game loop
    while running:
        for event in pygame.event.get():
            # looking for quit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        # passing keys to box to update movement
        keys = pygame.key.get_pressed()
        box1.move(keys)

        # checking if the player has died
        if box2.dammage / 60 >= box2.health:
            running = False
            pygame.quit()
            endscreen("win",username)
        if box1.dammage / 60 >= box1.health:
            running = False
            pygame.quit()
            endscreen("lose",username)

        # displaying background and sprites on the screen
        screen.blit(background, (0, 0))
        box1.draw(screen)
        box2.draw(screen)

        # dammage updates
        if box2.animation == 5:
            hit = box2.attack(100) # gets the attacking region of the apponent
            if hit.colliderect(box1.rect): # looks for collision between other players attack and yourself to see if you are hit
                print("HIT!")
                if box1.animation != 7: # checks if you are blocking
                    box1.dammage += 15 # updates your dammage based on weather you are blocking
                else:
                    box1.dammage += 5 # updates your dammage based on weather you are blocking
        elif box2.animation == 6:
            hit = box2.attack(150) # gets the attacking region of the apponent
            if hit.colliderect(box1.rect): # looks for collision between other players attack and yourself to see if you are hit
                print("HIT!")
                if box1.animation != 7: # checks if you are blocking
                    box1.dammage += 30 # updates your dammage based on weather you are blocking
                else:
                    box1.dammage += 10 # updates your dammage based on weather you are blocking

        # displaying attacks for checking purposes
        if box1.animation == 5:
            hit = box1.attack(100)
        elif box1.animation == 6:
            hit = box1.attack(150)

        # drawing the health bars for both players
        loading(box1.dammage, 30, box1.health)
        loading(box2.dammage, 1070, box2.health)

        # updating box 2 position by getting it from the server
        # converting your direction into integers
        if box1.direction == False:
            intdirec = 1
        else:
            intdirec = 0
        pos_string = n.make_pos((box1.x, box1.y, intdirec, box1.cycle, box1.animation, box1.health, box1.charecter, box1.dammage)) # formating the data to send
        reply = n.send(pos_string) # sending your data to the server
        pos = n.read_pos(reply) # recieveing the opponenets data fromt he server
        # updating the opponents data
        box2.x = pos[0] # x position of opponent
        box2.y = pos[1] # y position of opponent
        if pos[2] == 1:
            box2.direction = False # converting direction back to floats so they are useable
        else:
            box2.direction = True # converting direction back to floats so they are useable
        box2.cycle = pos[3] # cycle
        box2.animation = pos[4] # animation
        box2.health = pos[5] # health
        box2.charecter = pos[6] # charecter
        box2.dammage = pos[7] # dammage

        # updating animation cycle
        cursor_time += clock.get_time() # calculating how mcuh time has passed
        if cursor_time >= timecheck[box1.animation]: # checking if it is time to change the frame based on animation
            box1.update()
            cursor_time = 0

        # pygame updates
        pygame.display.flip()
        clock.tick(60)
print(login())
