### Technical Soundness
The methods in your HMM file are very well defined; they work as they are supposed to. The logic seems impeccable, and your demonstrated results are the evidences.
### Technical Depth
You seem to have a good understanding of HMM modeling. As your documentation hints, you have very well applied the concept to our blind robot problem. And it is obvious that you know what affect matrix multiplication has on the distribution table.

A very minor suggestion I have for you is that you can get rid of some redundant lines of codes. For instance, I don't think it is necessary that you write the same lines of codes for each color, each movement of the robot, etc.

For instance,
```
def build_observation_matrices():
    O_red = np.zeros((num_freesquares, num_freesquares), dtype=np.float64)
    for i in range(0, num_freesquares):
        if (index_to_color_map[i] == 'r'):
            O_red[i][i] = .88
        else:
            O_red[i][i] = .04

    #print("O_r:\n" + str(O_red))

    #green

    O_green = np.zeros((num_freesquares, num_freesquares), dtype=np.float64)
    for i in range(0, num_freesquares):
        if (index_to_color_map[i] == 'g'):
            O_green[i][i] = .88
        else:
            O_green[i][i] = .04

    #print("O_g:\n" + str(O_g))

    #yellow

    O_yellow = np.zeros((num_freesquares, num_freesquares), dtype=np.float64)
    for i in range(0, num_freesquares):
        if (index_to_color_map[i] == 'y'):
            O_yellow[i][i] = .88
        else:
            O_yellow[i][i] = .04

    #print("O_y:\n" + str(O_y))

    #blue

    O_blue = np.zeros((num_freesquares, num_freesquares), dtype=np.float64)
    for i in range(0, num_freesquares):
        if (index_to_color_map[i] == 'b'):
            O_blue[i][i] = .88
        else:
            O_blue[i][i] = .04

    #print("O_b:\n" + str(O_b))

    return (O_red, O_green, O_yellow, O_blue)
```

The method above can be reduced to 1/4th its current size. You could either use a for loop (`for color in ['r','g','b','y']`), or have the function take in a char variable for color as a parameter.

Everything else looks super nice.

### Presentation
I was literally awed by your presentation. The illustrations are just simply perfect. Your documentation is very concise and on point. Not to mention the comments you've added to your _HMM.py_ file. It made things so much easier for the reader to read over your code.

A few very minor suggestions I have for you are as follows. I was expecting to see a little more explanation on your model mechanism. And it would be a bit easier for the readers to read through your documentation if you had the pdf version of your markdown as well.

What can I say; a phenomenal illustration along with a great report. Well done!
