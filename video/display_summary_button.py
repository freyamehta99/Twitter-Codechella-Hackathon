
def display_summary_video():
    with open('data/summary.txt', 'r') as infile:
        summary = infile.read()
    print(summary)
    
display_summary_video()
