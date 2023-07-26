# Packing Shape Processing
This repo provides a set of tools for processing packing shapes that compatible with our [irregular packing solver]((https://github.com/alexfrom0815/IR-BPP)).
To perform robust collision detections and ray-casting tests in the simulation world, we stipulate that objects are
represented as closed manifold mesh surfaces. 

For each object: 
1. We first reconstruct  [(download the reconstruction code here)](https://github.com/autonomousvision/occupancy_networks/tree/master/external/mesh-fusion)
  the mesh into a watertight one. 
2. We then extract all the planar-stable poses of the object.
3. Some planar-stable poses are rotation-symmetric, and we remove redundant poses and retain only one representative from each rotation-symmetric group (see our [TOG paper](https://dl.acm.org/doi/pdf/10.1145/3603544) for more details).
4. Several rigid body simulators (like bullet) only accept convex shape primitives. We thus apply the convex decomposition algorithm for non-convex shapes. 


Note, this repo is still under development. I will add some demo shape for processing after I get my past data from my old computer.