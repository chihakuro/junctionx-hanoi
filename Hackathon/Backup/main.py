import tkinter as tk
from tkinter import ttk
import tkinterdnd2 as tkd
import cv2
import numpy as np
from PIL import Image, ImageTk
import ekkk1
import path 

# create the main window
window = tkd.Tk()
window.title("Overlap Area Estimation")

# Initialize the first frame
frame_list = [] # create an empty list to keep track of all frames
frame = tk.Frame(window, width=400, height=300, bg="white")
frame.grid(row=0, column=0, padx=10, pady=10)
frame_list.append(frame) # append the frame to the list of frames

# Label "Drag and drop a video..." at the center of the frame
label = tk.Label(frame, text="Drag and drop a camera...", bg="white")
label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

video_list = []
total = []
first_frame = []
first  = True
# Drag and drop initialization
def drop(event):
    global frame_list
    global first_frame
    if frame in frame_list:
        # Remove the first frame if it is still there
        frame_list[0].destroy()
        frame_list.pop(0)
    else:
        pass
    # Create a new frame for the video
    video_frame = tk.Frame(window, width=400, height=300, bg="white")
    video_frame.grid(row=len(frame_list)//2, column=len(frame_list)%2, padx=10, pady=10)
    video_frame.pack_propagate(0)

    # Create a label for the video and pack it into the new frame
    video_label = tk.Label(video_frame, bg="white")
    video_label.pack(fill=tk.BOTH, expand=True)

    # Label "Camera 1, 2, 3, etc." at the top left of the frame
    label = tk.Label(video_frame, text="Camera {}".format(len(frame_list)+1), bg="white")
    label.place(relx=0, rely=0, anchor=tk.NW)

    # Load the video and display its first frame in the label
    video = event.data
    # print(video)
    cap = cv2.VideoCapture(video)
    ret, fram = cap.read()
    
    # cv2.imwrite("E:/help/frame_%d.jpg" % count, fram)
    # count += 1
    # Fit the video to the frame size
    fram = cv2.resize(fram, (400, 300))
    first_frame.append(fram)
    cv2image = cv2.cvtColor(fram, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    # print(type(video_label))
    video_label.configure(image=imgtk)

    # Pack the new frame next to the existing frames
    frame_list.append(video_frame) # append the new frame to the list of frames
    video_list.append([cap, video_label]) # append the cap object and the video_label to the list of videos
    #print(video_list)

# Bind the drop event to the frame
window.drop_target_register(tkd.DND_FILES)
window.dnd_bind('<<Drop>>', drop)
k = 0
# Function to remove last frame and play all the videos in the window at once
def play():
    global count
    global total
    global k
    global first
    frames = []

    if first == True:
        first = False
        hulls  = ekkk1.get_hulls(first_frame)
        total.append(hulls)
        prc_frames = ekkk1.get_lines(hulls,first_frame)
    
        for i in range(len(prc_frames)):

            cv2image = cv2.cvtColor(prc_frames[i], cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            # video_label.imgtk = imgtk
            
            video_list[i][1].imgtk = imgtk
            video_list[i][1].configure(image=imgtk)
            # except:
            #     pass
        
    for cap, video_label in video_list:
        
        ret, fram = cap.read()
        if ret:
            # Fit the video to the frame size
            fram = cv2.resize(fram, (400, 300))
            #print(fram)
            # export the frame to a file

            frames.append(fram)
            # cv2.imwrite("E:/help/frame_%d.jpg" % count, fram)
            # count += 1
            # cv2image = cv2.cvtColor(fram, cv2.COLOR_BGR2RGBA)
            # img = Image.fromarray(cv2image)
            # imgtk = ImageTk.PhotoImage(image=img)
            # video_label.imgtk = imgtk
        '''else:
            # Reached end of video, restart from beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, fram = cap.read()
            # Fit the video to the frame size
            fram = cv2.resize(fram, (400, 300))
            cv2image = cv2.cvtColor(fram, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)'''
        # try:
        #     video_label.imgtk = imgtk
        #     video_label.configure(image=imgtk)
        # except:
        #     pass
    if ret:
        
        hulls  = ekkk1.get_hulls(frames)
        total.append(hulls)
        prc_frames = ekkk1.get_lines(hulls,frames)
    
        for i in range(len(prc_frames)):

            cv2image = cv2.cvtColor(prc_frames[i], cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            # video_label.imgtk = imgtk
            
            video_list[i][1].imgtk = imgtk
            video_list[i][1].configure(image=imgtk)
            # except:
            #     pass
        window.after(33, play)
    else:
        print(len(total))
        scenes = 3
        export(total, scenes)
        # schedule the next iteration of the loop at 1/30th of a second
    

def overlap():
    # For each 4 videos, calculate the overlap area (frame folder:'E:/help/')
    le = len(frame_list)
    for i in range(1, count, 4):
        # Read the 4 frames
        frame1 = cv2.imread("E:/help/frame_{}.jpg".format(i))
        frame2 = cv2.imread("E:/help/frame_{}.jpg".format(i+1))
        frame3 = None
        frame4 = None
        if le > 2:
            frame3 = cv2.imread("E:/help/frame_{}.jpg".format(i+2))
            if le > 3:
                frame4 = cv2.imread("E:/help/frame_{}.jpg".format(i+3))

        ekkk.video(frame1, frame2, frame3, frame4)
        # Replace existing frames in the window with the new frames
        for frame in frame_list:
            frame.destroy()
            frame_list.pop(0)
        for i in range(4):
            video_frame = tk.Frame(window, width=400, height=300, bg="white")
            video_frame.grid(row=i//2, column=i%2, padx=10, pady=10)
            video_frame.pack_propagate(0)

            # Create a label for the video and pack it into the new frame
            video_label = tk.Label(video_frame, bg="white")
            video_label.pack(fill=tk.BOTH, expand=True)

            # Label "Camera 1, 2, 3, etc." at the top left of the frame
            label = tk.Label(video_frame, text="Camera {}".format(i+1), bg="white")
            label.place(relx=0, rely=0, anchor=tk.NW)

            # Load the video and display its first frame in the label
            if i == 0:
                fram = frame1
            elif i == 1:
                fram = frame2
            elif i == 2:
                fram = frame3
            elif i == 3:
                fram = frame4
            else:
                pass

            # Fit the video to the frame size
            fram = cv2.resize(fram, (400, 300))
            cv2image = cv2.cvtColor(fram, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            print(type(video_label))
            video_label.configure(image=imgtk)

            # Pack the new frame next to the existing frames
            frame_list.append(video_frame)
     
# Function to export txt file
def export(total, scenes):
    data = {}
    for i in range(len(total[0])):
        for frame in total:
            if i in data:
                data[i].append(frame[i])
            else:
                data[i] = [frame[i]]
    path.create_txt(data, scenes)
    

    # Export the txt file

    pass       



# Create buttons frame
buttons_frame = tk.Frame(window, bg="white")
buttons_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=2)

# Button "Play" to play all the videos in the window at once
play_button = tk.Button(window, text="Play", command=play)
play_button.grid(row=0, column=2, padx=10, pady=10)

# Button "Overlap" to calculate the overlap area
overlap_button = tk.Button(window, text="Overlap", command=overlap)
overlap_button.grid(row=1, column=2, padx=10, pady=10)

window.mainloop()

