from PyOpticL import layout, optomech
from datetime import datetime

name = "TA In Fiber Out Splitter"
date_time = datetime.now().strftime("%m/%d/%Y")
label = name + " " +  "2025"

base_dx = 5.75*layout.inch
base_dy = 11.75*layout.inch # Original 11.75
base_dz = 0.5*layout.inch
gap = 0

# x_offset = -9 - 25.4/2
# y_offset = 10 - 25.4/2 + 8
x_offset = 0
y_offset = 8-13.85

# mount_holes_temp = [(1,3),(3,4),(4,0),(9,0),(9,4),(10,2),(12,3)]
mount_holes=[]
mount_holes_temp = [(1,1), (1,7), (3,3)] # Original had (3,7) also
for x,y in mount_holes_temp:
    mount_holes.append((x+x_offset/25.4,y+y_offset/25.4))

# Note that for mirror_mount_c05g, an offset of 6mm is needed as the pos is 
# centered at the optical start, not the drill hole as in openscad. 

d_inch = 25.4

# Positioning for Mount Placement

hca3_width = 41

fiber_in_x = hca3_width/2
fiber_in_y = 4*d_inch

start_x = 75 + 8
start_y = 40 - 5

new_fibers = False

# Original mirror mount was the mirror_mount_m05


def fb_input_splitter(x=0, y=0, angle=0, mirror=optomech.mirror_mount_k05s1, x_split=False, thumbscrews=True):

    # Define Baseplate:
    baseplate = layout.baseplate(base_dx, base_dy, base_dz, x=x, y=y, angle=angle,
                                 gap=gap, mount_holes=mount_holes,
                                 name=name, label=label)

    # Define beam path:
    beam = baseplate.add_beam_path(x=base_dx-60, y=start_y+10, angle=layout.cardinal['left'], color = (0,0,255))


    # Optic Placement Definitions:
    # baseplate.place_element("evalminiTA", optomech.eval_miniTA, x=base_dx-start_x-5+3, y=start_y+10, angle=layout.cardinal['left'])

    # baseplate.place_element("fiber_in", optomech.fiberport_12mm, x=base_dx-15-60, y=start_y+10, angle=180, port=1)

    baseplate.place_element("evalminiTA", optomech.eval_miniTA, x=base_dx-start_x-5+3, y=start_y+10, angle=layout.cardinal['left'])

    baseplate.place_element_along_beam("mirror1_in", optomech.circular_mirror, beam,
                                       beam_index=0b1, distance=50-8-5-(-start_x-5+3)-60, angle=180-135,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    # baseplate.place_element_along_beam("isolator", optomech.isolator_895, beam, beam_index=0b1,
    #                                    distance=30-2, angle=layout.cardinal['down'])
    baseplate.place_element_along_beam("pinhole1", optomech.circular_lens, beam, 
                                       beam_index=0b1, distance=40-5-4+10+5+28-20-30-2-1-11, angle=-90, mount_type=optomech.mirror_mount_c05g)
    
    baseplate.place_element_along_beam("isolator", optomech.isolator_895_high_power, beam, beam_index=0b1, distance=60-2-1+11, angle=270, cage=True)
    
    baseplate.place_element_along_beam("mirror2_in", optomech.circular_mirror, beam,
                                       beam_index=0b1, distance=15-8+2+50-20-10+5+20+30+40-60-1, angle=180-225,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("waveplate1_in", optomech.waveplate, beam, 
                                       beam_index=0b1, distance=25+8, angle=0, 
                                       mount_type=optomech.chromatic_rotation_stage)

    baseplate.place_element_along_beam("pbs", optomech.cube_splitter, beam,
                                       beam_index=0b1, distance=20+15-10-6+23-15+8-15-8, angle=180-0, invert=False,
                                       mount_type=optomech.skate_mount)

    # Transmitted pbs parts:
    baseplate.place_element_along_beam("mirror1_out", optomech.circular_mirror, beam,
                                       beam_index=0b10, distance=15-8+2+5+10-8+5, angle=180+45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("pinhole2", optomech.circular_lens, beam,
                                       beam_index=0b10, distance=20+10+40-8-4-3-11, angle=90, mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("mirror2_out", optomech.circular_mirror, beam,
                                       beam_index=0b10, distance=30+5+5+(25.4/4)-30+11, angle=45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("waveplate1_out", optomech.waveplate, beam, 
                                       beam_index=0b10, distance=20+9-10+7-5-5, angle=180-0, 
                                       mount_type=optomech.chromatic_rotation_stage)

    # baseplate.place_element_along_beam("fiberport_out_1", optomech.fiberport_mount_hca3, beam,
    #                                    beam_index=0b10, distance=15-3+6, angle=180-0)
    fb_tx, fb_ty = base_dx, 113-(25.4/4)+8
    baseplate.place_element("mod_mountL", optomech.modular1, x=fb_tx, 
                            y=fb_ty, angle=0)
    baseplate.place_element("fiber_out_transmitted", optomech.fiberport_12mm, x=fb_tx-15,
                             y=fb_ty, angle=180, port=1)

    # Reflected pbs parts:
    baseplate.place_element_along_beam("pinhole3", optomech.circular_lens, beam,
                                       beam_index=0b11, distance=50-20+8+4+3-11, angle=270, mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("mirror3_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=65+5+10-50-20+11, angle=180-(-45),
                                       mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element_along_beam("mirror4_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=20+5+3+2-10-3-3+23-15+8, angle=180-135,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("mirror4_out", optomech.circular_mirror, beam,
                                       beam_index=0b11, distance=35+11.05-5-10-5, angle=-45,
                                       mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    
    baseplate.place_element_along_beam("waveplate1_out", optomech.waveplate, beam, 
                                       beam_index=0b11, distance=105-30-10+7-5, angle=180, 
                                       mount_type=optomech.chromatic_rotation_stage)

    # baseplate.place_element_along_beam("fiberport_out_1", optomech.fiberport_mount_hca3, beam,
    #                                    beam_index=0b11, distance=15-3, angle=180)
    fb_rx, fb_ry = base_dx, 259.05+8
    baseplate.place_element("mod_mountL", optomech.modular1, x=fb_rx, 
                            y=fb_ry, angle=0)
    baseplate.place_element("fiber_out_reflected", optomech.fiberport_12mm, x=fb_rx-15,
                             y=fb_ry, angle=180, port=1)



if __name__ == "__main__":
    fb_input_splitter()
    layout.redraw()