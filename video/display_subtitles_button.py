#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def display_subtitles_for_video(lists_file='data/lists.txt'):
    """ Displays time-stamped subtitles. """
    from time import sleep
    import json
    
    # Import lists
    with open(lists_file) as json_file:
        dic = json.load(json_file)
    list_words = dic['list_words']
    list_start_times = dic['list_start_times']
    list_end_times = dic['list_end_times']
    
    # Align the word display with the word timetamp.
    sleep(list_start_times[0])
    for i in range(len(list_words)):
        if i < len(list_words)-1 :
            print(list_words[i],
                  sep=' ',
                  end=' ',
                  flush=True
                 ); sleep(list_start_times[i+1]-list_start_times[i])
        elif i == len(list_words)-1:
            print(list_words[i], sep=' ', end=' ', flush=True)
            
display_subtitles_for_video()

