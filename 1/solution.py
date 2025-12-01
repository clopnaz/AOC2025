#!/usr/bin/env python3

lines = [line.strip() for line in open('input.txt').readlines()]
# lines = [line.strip() for line in open('test.txt').readlines()]

direction = 50
password_1 = 0
password_2 = 0
# password_2_slop = 0
for line in lines:
    line_direction = line[0]
    if line_direction == 'L':
        line_amount = -int(line[1:])
    elif line_direction == 'R':
        line_amount = int(line[1:])
    old_password_2 = password_2
    old_direction = direction
    unmodded_direction = direction + line_amount
    direction = unmodded_direction % 100
    # password_2_slop += password_2_increment - int(password_2_increment)
    if direction == 0:
        password_1 += 1
    if unmodded_direction == 0:
        password_2 += 1
    elif unmodded_direction < 0:
        password_2 += -unmodded_direction // 100
        if old_direction > 0:
            password_2 += 1


    elif unmodded_direction > 0:
        password_2 += (unmodded_direction // 100)

    password_2_increment = password_2 - old_password_2
    print(f"{line_amount = } {old_direction = } {direction = } {unmodded_direction = } {password_2_increment = }")
    if password_2_increment:
        # print(f"{line_amount = } {old_direction = } {direction = } {unmodded_direction = } {password_2_increment = }")
        if line_amount < 0:
            # breakpoint()
            pass

    # if unmodded_direction < -99:
    #     breakpoint()
    # password_2 += password_2_increment

print(f"{password_1 = }")
print(f"{password_2 = }")
# wrong answers:
# 5450
# 6923
# 6861
# 6402
