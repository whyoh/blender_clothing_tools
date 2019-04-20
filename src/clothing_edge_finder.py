import bpy
import bmesh
from mathutils import Vector

# TODO UI for these settings (at least).
# if buttons is non zero then the script will only sew a set of 'run' edges every 'buttons' vertices.
# so with buttons=7, run=2 you get 2 sewn edges, 5 gaps, 2 sewn edges, 5 gaps etc.
# whether that pattern will start from one end of the seam or the other is random.
buttons = 0
run = 2
sharpness = 0.7  # 1 means "edges must be exactly straight lines", 0 means "keep going until you reach a right-angle".

###
# start script with pattern mesh in edit mode and one or more vertices, (TODO edges and polygons) selected on each edge to be sewn.
# script follows the edges and adds edges to sew them.
###

mesh = bpy.context.object.data
bm = bmesh.from_edit_mesh(mesh)

# for now you must select one vertex on each edge you want to sew .. and not on a corner!
vert_pair = [v for v in bm.verts if v.select]
outer_edges = [e for e in bm.edges if e.is_boundary]

# make sure we find our selected edges first.  otherwise oddness sometimes occurs!
a = [e for e in outer_edges if e.verts[0] == vert_pair[0] or e.verts[1] == vert_pair[0]]
i = outer_edges.index(a[0])
e = outer_edges.pop(i)
outer_edges.append(e)
a = [e for e in outer_edges if e.verts[0] == vert_pair[1] or e.verts[1] == vert_pair[1]]
i = outer_edges.index(a[0])
e = outer_edges.pop(i)
outer_edges.append(e)

lines = 0
current_line = []
head_finished = True
tail_finished = True
sewing_line = False
sewing_lines = []
while outer_edges:
    if head_finished and tail_finished:
        if current_line:
            lines += 1
            if sewing_line:
                sewing_lines.append([])
                for n, e in enumerate(current_line):
                    if not n:
                        if e.verts[0] == head or e.verts[0] == tail:
                            sewing_lines[-1].append(e.verts[0])
                            sewing_lines[-1].append(e.verts[1])
                        else:
                            sewing_lines[-1].append(e.verts[1])
                            sewing_lines[-1].append(e.verts[0])
                    else:
                        if e.verts[0] == sewing_lines[-1][-1]:
                            sewing_lines[-1].append(e.verts[1])
                        else:
                            sewing_lines[-1].append(e.verts[0])
                if len(sewing_lines) == 2:
                    break
        else:
            assert not lines
        current_line = [outer_edges.pop()]
        head_finished = False
        tail_finished = False
        sewing_line = False
        head = current_line[0].verts[0]
        tail = current_line[0].verts[1]

    if head.select or tail.select:
        sewing_line = True
    if not head_finished:
        end = head
        end_edge = current_line[0]
    else:
        end = tail
        end_edge = current_line[-1]
    next = [e for e in outer_edges if e.verts[0] == end or e.verts[1] == end]
    if next:
        a, b = [v.co for v in end_edge.verts]
        c, d = [v.co for v in next[0].verts]
        if end_edge.verts[0] != end:
            a, b = b, a
        if next[0].verts[0] != end:
            c, d = d, c
        i = (b - a).normalized()
        j = (d - c).normalized()
        p = i.dot(j)  # TODO try BMVert.calc_edge_angle()
        if p > -sharpness:  # sharp corner!
            if end == head:
                head_finished = True
            else:
                tail_finished = True
            continue
        if next[0].verts[0] == end:
            subs = next[0].verts[1]
        else:
            subs = next[0].verts[0]
        if end == head:
            head = subs
            current_line = [outer_edges.pop(outer_edges.index(next[0]))] + current_line
        else:
            tail = subs
            current_line.append(outer_edges.pop(outer_edges.index(next[0])))
    else:
        end_point = end.co
        if end == head:
            head_finished = True
        else:
            tail_finished = True
        continue

assert len(sewing_lines[0]) == len(sewing_lines[1])

# make sure we're not going to sew them up backwards!
a = sewing_lines[0][0].co
b = sewing_lines[1][0].co
c = sewing_lines[1][-1].co
if (b - a).length > (c - a).length:
    sewing_lines[1].reverse()

for n, (a, b) in enumerate(zip(*sewing_lines)):
    if buttons and n % buttons >= run:
        continue
    try:
        bm.edges.new((a, b))
    except ValueError:
        pass  # probably duplicate vert when doing darts.

bmesh.update_edit_mesh(mesh, destructive=True)  # TODO check we really need 'destructive' for adding edges.

###
# pattern left in edit mode so you can select more points and run again
###
