
with open('BOT/old.html') as f:
    line_count = 0
    for line in f:
        line_count += 1
    if line_count == 1:
        print(line_count)
    else:
        print("line_count > 1")