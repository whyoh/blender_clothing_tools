# blender_clothing_tools
helper scripts for creation of clothing from sewing patterns for the blender cloth physics engine.

note: the terminology between blender and sewing gets a bit collisiony.  when we say "seam" below, we're referring to sewing seams, not blender seams!


## usage
In blender, copy the shapes from a sewing pattern into planar meshes so they look like they've been cut out of flat material.  (I keep the pieces vertical so that they're ready to wrap round a dummy).
You need to make sure that any seams have the same number of vertices on each piece that will be sewn together.

TODO - I'd like to add a script to import SVG lines and turn them into a sensible mesh.

Add a dummy (I use a MB-Lab character) and set it as a collision target.
Position the pieces around the dummy where they should be (but keep them vertical for now - it shouldn't adversely affect the sewing process and it makes it easier to adjust things).

Now load the clothing_edge_finder.py script into the scripting window.

Go into edit mode and select one vertex from each side of a seam.
Run the script.
Repeat those two steps for each seam.

It will follow the boundaries of the pieces until it finds a corner, sewing the pieces together as it goes.  (It only joins the vertices together with edges - that's how the blender sewing system works.)

If you'd like a seam with gaps (e.g. for a button front) set the "buttons" and "runs" values at the top of the script before running it.
