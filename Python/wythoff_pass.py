import numpy as np
from matplotlib import pyplot as plt

# move function of Wythoff variant
# When cs is True, a pass move at the terminal position is possible, and this corresponds to the disjunctive sum of Wythoff and an extra one stone.
# When cs is False, a pass move at the terminal position is not possible, and this corresponds to Wythoff with a pass.
def wythoff_with_p(position,cs=False):
    x = position[0]
    y = position[1]
    p = position[2]
    x_move = [(x-i, y, p) for i in range(1,x+1)]
    y_move = [(x, y-i, p) for i in range(1,y+1)]
    xy_move = [(x-i, y-i, p) for i in range(1,min([x,y])+1)]
    pass_move = [(x, y, i) for i in range(p)]*int(bool(x+y)|cs)
    all_move = x_move + y_move + xy_move + pass_move
    return all_move

# mex function
def mex(setx):
    setx = setx | {-1}
    ad_cset = set(range(max(setx)+2)) - setx
    return min(ad_cset)

#　Grundy number dictionarry
grundy_dict = {}
move=wythoff_with_p

# Function to compute the Grundy number of a given position
def get_grundynumber(position, cs=False):
    all_moves = move(position,cs)
    all_number = []
    for m in all_moves:
        try:
            number = grundy_dict[m]
        except KeyError:
            number = get_grundynumber(m)
        all_number.append(number)
    grundy_number = mex(set(all_number))
    grundy_dict[position] = grundy_number
    return grundy_number


# Computation range
xx = 8
yy = 8

# Grundy number of normal Wythoff 
nonpass_grundy_map = [[get_grundynumber((i,j,0)) for i in range(xx+1)] for j in range(yy+1)]
# Grundy number of Wythoff with a pass
pass_grundy_map = [[get_grundynumber((i,j,1)) for i in range(xx+1)] for j in range(yy+1)]

# Grundy number of Wythoff with an extra one stone
grundy_dict.clear()
onestone_grundy_map = [[get_grundynumber((i,j,1), cs=True) for i in range(xx+1)] for j in range(yy+1)]


# Preparing the table for Grundy numbers
axis1 = np.array(list(range(xx+1)))
axis2 = np.array(list(range(yy+1)))

data1 = np.array(nonpass_grundy_map)
data2 = np.array(pass_grundy_map)
data3 = np.array(onestone_grundy_map)

data1_with_labels = np.column_stack((axis2.reshape(-1, 1), data1))
data2_with_labels = np.column_stack((axis2.reshape(-1, 1), data2))
data3_with_labels = np.column_stack((axis2.reshape(-1, 1), data3))

header = [''] + list(axis1)
data1_with_labels = np.vstack((header, data1_with_labels))
data2_with_labels = np.vstack((header, data2_with_labels))
data3_with_labels = np.vstack((header, data3_with_labels))

plt.rcParams['font.family'] = 'Helvetica'


# Creating the table
fig1 = plt.figure()
fig1.suptitle('Grundy number of Wythoff Nim with no pass')# Set the table name
ax1 = fig1.add_subplot(111)
ax1.axis('off')

fig2 = plt.figure()
fig2.suptitle('Grundy number of Wythoff Nim with pass')# Set the table name
ax2 = fig2.add_subplot(111)
ax2.axis('off')

fig3 = plt.figure()
fig3.suptitle('Grundy number of Wythoff Nim with one stone in extra pile ')# Set the table name
ax3 = fig3.add_subplot(111)
ax3.axis('off')

table1 = ax1.table(cellText=data1_with_labels, loc="center", cellLoc='center')
table2 = ax2.table(cellText=data2_with_labels, loc="center", cellLoc='center')
table3 = ax3.table(cellText=data3_with_labels, loc="center", cellLoc='center')

def format_table_with_colors(table, data_with_labels):
    nrows, ncols = data_with_labels.shape

    for (row, col), cell in table.get_celld().items():
        text = data_with_labels[row][col]
        
        cell.set_text_props(ha='center', va='center', fontsize=18)
        
        cell.set_width(1 / ncols)
        cell.set_height(1 / nrows)

        if row == 0 or col == 0:
            cell.set_facecolor('#BFBFBF')

        else:
            try:
                if int(text) == 0:
                    cell.set_facecolor('#FF0000')
            except:
                pass

format_table_with_colors(table1, data1_with_labels)
format_table_with_colors(table2, data2_with_labels)
format_table_with_colors(table3, data3_with_labels)

# Save the image
fig1.savefig("wythoff_no_pass.png", bbox_inches='tight', dpi=400)
fig2.savefig("wythoff_with_pass.png", bbox_inches='tight', dpi=400)
fig3.savefig("wythoff_extra_pile.png", bbox_inches='tight', dpi=400)

# Display the image
plt.show()
plt.close()