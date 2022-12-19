import sys

f = open("input.txt","r")
lines=[ l.strip() for l in f.readlines( )]
print(sys.setrecursionlimit(20000))
sample=[
    (1,1,1),
    (2,1,1)
]

def read_line(l):
    return eval(f'({l})')

coords=[ read_line(l) for l in lines]

def oppside(box,vec):
    return (box[0]+vec[0],box[1]+vec[1],box[2]+vec[2])

def addvec(box,vec):
    return oppside(box,vec)

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
    return count

def part1(arr):
    add_coords(arr)
    total_box_faces=len(arr)*6
    total_size=visble_faces(arr,x_faces) + visble_faces(arr,y_faces) + visble_faces(arr,z_faces)
    print(f'total_box_sides={total_box_faces} total_size={total_size}')
    return total_size

def get_bounding_box(arr,axes):
    min_f=min( [ c[axes] for c in arr ])
    max_f=max( [ (c[axes]+1) for c in arr ] )
    return (min_f-1,max_f+1)


bounding_box_x=get_bounding_box(coords,0)
bounding_box_y=get_bounding_box(coords,1)
bounding_box_z=get_bounding_box(coords,2)

print(bounding_box_x)
print(bounding_box_y)
print(bounding_box_z)

def in_bounding_box( coord ):
    if coord[0] < bounding_box_x[0] or coord[0] >= bounding_box_x[1]:
        return False
    if coord[1] < bounding_box_y[0] or coord[1] >= bounding_box_y[1]:
        return False
    if coord[2] < bounding_box_z[0] or coord[2] >= bounding_box_z[1]:
        return False
    return True

def exterior_surface_bounding_box():
    x_len=bounding_box_x[1] - bounding_box_x[0]
    y_len=bounding_box_y[1] - bounding_box_y[0]
    z_len=bounding_box_z[1] - bounding_box_z[0]
    return 2 * (
            x_len * y_len +
            x_len * z_len +
            z_len * y_len
        )

exterior_boxes=set()
start_point=(bounding_box_x[0],bounding_box_y[0],bounding_box_z[0])
directions=[
    (1,0,0),
    (-1,0,0),
    (0,1,0),
    (0,-1,0),
    (0,0,1),
    (0,0,-1)
]

def flood_fill(arr,start_point):
    if not in_bounding_box(start_point):
        return
    if start_point in exterior_boxes:
        return
    if start_point in arr:
        return 
    exterior_boxes.add(start_point)
    for vec in directions:
        flood_fill(arr,addvec(start_point,vec))

flood_fill(coords,start_point)
print(exterior_boxes)
total_area=part1(list(exterior_boxes))
size_exterior=exterior_surface_bounding_box()
print(total_area-size_exterior)



    

