# blender_clothing_tools
helper scripts for creation of clothing from sewing patterns for the blender cloth physics engine.

![the sewing process](sewing.png)

*note: the terminology between blender and sewing gets a bit collisiony.  when we say "seam" below, we're referring to sewing seams, not blender seams!*


## usage
In blender, copy the shapes from a sewing pattern into planar meshes so they look like they've been cut out of flat material.  (I keep the pieces vertical so that they're ready to wrap round a dummy).
You need to make sure that any seams have the same number of vertices on each edge that will be sewn together.
Join (ctrl-J) all the mesh objects so that they become one object.

**TODO** - I'd like to add a script to import SVG lines and turn them into a sensible mesh, including matching up the numbers of vertices.

Add a dummy (I use a MB-Lab character) and set it as a collision target.
Position the pieces around the dummy where they should be (but keep them vertical for now - it shouldn't adversely affect the sewing process and it makes it easier to adjust things).

Now load the clothing_edge_finder.py script into the scripting window.
**TODO** make this an add-on so you can select it from a menu/shortcut rather than loading and running the script!

Now the actual sewing bit:

- Go into edit mode and select one vertex from each side of a seam.
- Run the script.
- Repeat those two steps for each seam.

It will follow the boundaries of the pieces until it finds a corner, sewing the pieces together as it goes.  (It only joins the vertices together with edges - that's how the blender sewing system works.)

If you'd like a seam with gaps (e.g. for a button front) set the "buttons" and "runs" values at the top of the script before running it.

Finally, to join up the sewn seams, enable "cloth" in the physics tab for the clothing object and press the animation play button.  The cloth should sew itself up onto the dummy.

**TODO** - turn this into a proper tutorial so you can see what all the above actually looks like and don't have to go googling how to do all that in blender!
