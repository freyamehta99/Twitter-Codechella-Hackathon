#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# For voice tweet

def display_text_for_voice(text_file='data/text.txt'):
    """ Displays text extracted from voice tweet. """
    import json
    
    with open(text_file) as json_file:
        text = json.load(json_file)
    print(text)
    
display_text_for_voice()

