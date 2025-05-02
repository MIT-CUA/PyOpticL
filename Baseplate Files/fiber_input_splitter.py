from PyOpticL import layout, optomech
from datetime import datetime

name = "Fiber In/Out Splitter"
date_time = datetime.now().strftime("%m/%d/%Y")
label = name + " " +  "2025"

base_dx = 5.75*layout.inch
base_dy = 11.75*layout.inch
base_dz = 0.5*layout.inch
gap = 0

x_offset = -9 - 25.4/2
y_offset = 10 - 25.4/2

mount_holes = [(1,1), (1,7), (3,3), (3,7)]

d_inch = 25.4

# Positioning for Mount Placement
hca3_width = 41

fiber_in_x = hca3_width/2
fiber_in_y = 4*d_inch

start_x = 75 + 8
start_y = 40 - 5

new_fibers = False


def fb_input_splitter(x=0, y=0, angle=0, mirror=optomech.mirror_mount_m05, x_split=False, thumbscrews=False):

    baseplate = layout.baseplate(base_dx, base_dy, base_dz, x=x, y=y, angle=angle,
                                 gap=gap, mount_holes=mount_holes,
                                 name=name, label=label)

    beam = baseplate.add_beam_path(x=base_dx-60, y=start_y+10, angle=layout.cardinal['left'], color = (0,0,255))

    baseplate.place_element("fiber_in", optomech.fiberport_12mm, x=base_dx-15-60, y=start_y+10, angle=180, port=1)

    baseplate.place_element_along_beam("mirror1_in", optomech.circular_mirror, beam,
                                       beam_index=0b1, distance=50-8-5-(-start_x-5+3)-60, angle=180-135,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    
    baseplate.place_element_along_beam("pinhole1", optomech.circular_lens, beam, 
                                       beam_index=0b1, distance=40-5-4+10+5+28-20, angle=90, mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("waveplate1_in", optomech.waveplate, beam, 
                                       beam_index=0b1, distance=20, angle=270, 
                                       mount_type=optomech.rotation_stage_rsp05)
    baseplate.place_element_along_beam("mirror2_in", optomech.circular_mirror, beam,
                                       beam_index=0b1, distance=15-8+2+50-20-10+5, angle=180-225,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("pbs", optomech.cube_splitter, beam,
                                       beam_index=0b1, distance=20+15-10-6+23-15, angle=180-0, invert=False,
                                       mount_type=optomech.skate_mount)

    # Transmitted pbs parts:
    baseplate.place_element_along_beam("mirror1_out", optomech.circular_mirror, beam,
                                       beam_index=0b10, distance=15-8+2+5+10, angle=180+45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("pinhole2", optomech.circular_lens, beam,
                                       beam_index=0b10, distance=20+10, angle=270, mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("mirror2_out", optomech.circular_mirror, beam,
                                       beam_index=0b10, distance=30+5+5+(25.4/4)-30, angle=45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("waveplate1_out", optomech.waveplate, beam, 
                                       beam_index=0b10, distance=20+9, angle=180-0, 
                                       mount_type=optomech.rotation_stage_rsp05)
    
    fb_tx, fb_ty = base_dx, 113-(25.4/4)
    baseplate.place_element("mod_mountL", optomech.modular1, x=fb_tx, 
                            y=fb_ty, angle=0)
    baseplate.place_element("fiber_out_transmitted", optomech.fiberport_12mm, x=fb_tx-15,
                             y=fb_ty, angle=180, port=1)

    # Reflected pbs parts:
    baseplate.place_element_along_beam("pinhole3", optomech.circular_lens, beam,
                                       beam_index=0b11, distance=50, angle=90, mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("mirror3_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=65+5+10-50, angle=180-(-45),
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("mirror4_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=20+5+3+2-10-3-3+23-15, angle=180-135,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("mirror4_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=35+11.05-5-10-5, angle=-45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    
    baseplate.place_element_along_beam("waveplate1_out", optomech.waveplate, beam, 
                                       beam_index=0b11, distance=105-30, angle=180, 
                                       mount_type=optomech.rotation_stage_rsp05)
    
    fb_rx, fb_ry = base_dx, 259.05
    baseplate.place_element("mod_mountL", optomech.modular1, x=fb_rx, 
                            y=fb_ry, angle=0)
    baseplate.place_element("fiber_out_reflected", optomech.fiberport_12mm, x=fb_rx-15,
                             y=fb_ry, angle=180, port=1)


if __name__ == "__main__":
    fb_input_splitter()
    layout.redraw()