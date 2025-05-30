from PyOpticL import layout, optomech
from datetime import datetime

name = "Fiber In/Out Splitter"
date_time = datetime.now().strftime("%m/%d/%Y")
label = name + " " +  "2025"

base_dx = 5*layout.inch
base_dy = 9.5*layout.inch
base_dz = 0.5*layout.inch
gap = 0

x_offset = -9 - 25.4/2
y_offset = 10 - 25.4/2

mount_holes = [(1, 0), (1, 1), (1, 3), (1, 7), (1, 8), (3, 0), (3, 1), (3, 6), (3, 7)]

d_inch = 25.4

# Positioning for Mount Placement
hca3_width = 41

fiber_in_x = hca3_width/2
fiber_in_y = 4*d_inch

start_x = 75 + 8
start_y = 10

fiber_out_dist = 6*d_inch
fiber_out_x_0 = 2*d_inch
fiber_out_x_1 = fiber_out_dist + fiber_out_x_0

new_fibers = False


def fb_input_splitter(x=0, y=0, angle=0, mirror=optomech.mirror_mount_m05, thumbscrews=True):

    baseplate = layout.baseplate(base_dx, base_dy, base_dz, x=x, y=y, angle=angle,
                                 gap=gap, mount_holes=mount_holes,
                                 name=name, label=label)

    beam = baseplate.add_beam_path(x=base_dx-50-26, y=start_y+10, angle=layout.cardinal['left'], color = (0,0,255))

    baseplate.place_element("fiber_in", optomech.fiberport_12mm, x=base_dx-50-26, y=start_y+10, angle=180, port=1)

    # baseplate.place_element_along_beam("waveplate1_in", optomech.waveplate, beam, 
    #                                    beam_index=0b1, distance=26, angle=180, 
    #                                    mount_type=optomech.rotation_stage_rsp05)
    baseplate.place_element_along_beam("mirror1_in", optomech.circular_mirror, beam,
                                       beam_index=0b1, distance=35, angle=180-135,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
                                       
    baseplate.place_element_along_beam("pinhole1", optomech.circular_lens, beam, 
                                       beam_index=0b1, distance=15, angle=-90, mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("waveplate1_in", optomech.waveplate, beam, 
                                       beam_index=0b1, distance=41, angle=90, 
                                       mount_type=optomech.rotation_stage_rsp05, mount_args={"invert": True})
    baseplate.place_element_along_beam("mirror2_in", optomech.circular_mirror, beam,
                                       beam_index=0b1, distance=34, angle=180-225,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("pbs", optomech.cube_splitter, beam,
                                       beam_index=0b1, distance=17, angle=180-0, invert=False,
                                       mount_type=optomech.skate_mount)

    dist_to_fiber = -((113 - (24.4/4) - 1.5*d_inch) - (start_y + 10) - (15+41+34) + 0.25)
    # Transmitted pbs parts:
    m1o = baseplate.place_element_along_beam("mirror1_out", optomech.circular_mirror, beam,
                                       beam_index=0b10, distance=20, angle=180+45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("mirror2_out", optomech.circular_mirror, beam,
                                       beam_index=0b10, distance=dist_to_fiber, angle=45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("waveplate1_out", optomech.waveplate, beam, 
                                       beam_index=0b10, distance=17, angle=180-0, 
                                       mount_type=optomech.rotation_stage_rsp05)
    baseplate.place_element_along_beam("pinhole2", optomech.circular_lens, beam,
                                       beam_index=0b10, distance=8, angle=180, mount_type=optomech.mirror_mount_c05g)
    
    fb_tx, fb_ty = base_dx, 113-(25.4/4)-1.5*d_inch
    # baseplate.place_element("mod_mountL", optomech.modular1, x=fb_tx, 
    #                         y=fb_ty, angle=0)
    baseplate.place_element("fiber_out_reflected", optomech.fiberport_12mm, x=fb_tx-15,
                             y=fb_ty, angle=180, port=1)
    # Reflected pbs parts:

    baseplate.place_element_along_beam("waveplate1_out", optomech.waveplate, beam, 
                                       beam_index=0b11, distance=30, angle=90, 
                                       mount_type=optomech.rotation_stage_rsp05)

    baseplate.place_element_along_beam("mirror3_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=30, angle=180-(-45),
                                       mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("mirror4_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=17, angle=180-135,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    
    dist_to_fiber = ((259.05 - 2.5*d_inch) - (start_y + 10) - 90 - 60 + 1)
    baseplate.place_element_along_beam("mirror4_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=dist_to_fiber, angle=-45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))

    baseplate.place_element_along_beam("pinhole3", optomech.circular_lens, beam,
                                       beam_index=0b11, distance=50, angle=180, mount_type=optomech.mirror_mount_c05g)
    
    fb_rx, fb_ry = base_dx, 259.05-2.5*d_inch
    # baseplate.place_element("mod_mountL", optomech.modular1, x=fb_rx, 
    #                         y=fb_ry, angle=0)
    baseplate.place_element("fiber_out_reflected", optomech.fiberport_12mm, x=fb_rx-15,
                             y=fb_ry, angle=180, port=1)
    
    # baseplate.place_element("fiber_out_reflected_2", optomech.fiberport_12mm, x=fb_rx-15,
    #                          y=fb_ry + 1*d_inch, angle=180, port=1)
    baseplate.place_element("mirror5_out", optomech.circular_mirror, x=16,
                             y=fb_ry + 1*d_inch, angle=-45, mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element("pinhold4", optomech.circular_lens, x=16+50,
                             y=fb_ry + 1*d_inch, angle=180, mount_type=optomech.mirror_mount_c05g)


if __name__ == "__main__":
    fb_input_splitter()
    layout.redraw()