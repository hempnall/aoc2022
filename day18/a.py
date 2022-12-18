f = open("input.txt","r")
lines=[ l.strip() for l in f.readlines( )]

sample=[
    (1,1,1),
    (2,1,1)
]

def read_line(l):
    return eval(f'({l})')

coords=[ read_line(l) for l in lines]

def oppside(box,vec):
    return (box[0]+vec[0],box[1]+vec[1],box[2]+vec[2])

x_faces=set()
y_faces=set()
z_faces=set()

def add_coords(arr):
    for box in arr:
        x_faces.add(box)
        x_faces.add(oppside(box,(1,0,0)))
        y_faces.add(box)
        y_faces.add(oppside(box,(0,1,0)))
        z_faces.add(box)
        z_faces.add(oppside(box,(0,0,1)))

def visble_faces(arr,axes):
    expected_faces = 2 * len(arr)
    distinct_faces = len(list(axes))
    diff = expected_faces - distinct_faces
    count = expected_faces - 2 * diff
    print(count)
    return count

def part1(arr):
    add_coords(arr)
    total_box_faces=len(arr)*6
    total_size=visble_faces(arr,x_faces) + visble_faces(arr,y_faces) + visble_faces(arr,z_faces)
    print(f'total_box_sides={total_box_faces} total_size={total_size}')

part1(coords)


